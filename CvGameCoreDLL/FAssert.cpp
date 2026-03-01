#include "CvGameCoreDll.h"

#if defined(FASSERT_ENABLE) && defined(WIN32)

#include "FDialogTemplate.h"
#include "CvGame.h" // advc.006l

#include <tchar.h>
#include <stdio.h>

namespace
{
	// These are the return values from the modal Assert Dialog
	enum
	{
		ASSERT_DLG_DEBUG,
		ASSERT_DLG_IGNORE,
		ASSERT_DLG_IGNOREALWAYS,
		ASSERT_DLG_STOP, // advc.006l (based on code by Erik in the WtP mod)
		ASSERT_DLG_EXIT,
	};

	// This global structure is filled out by the original call to our FAssert
	// and is used by the dialog proc to display appropriate debug info
	struct AssertInfo
	{
		const char* szExpression;
		const char* szMessage;
		const char* szFileName;
		const char* szFunctionName; // advc.006f
		unsigned int line;

		// EIP / EBP / ESP
		CONTEXT context;
	} g_AssertInfo;

	// Use a static array since often times asserts are fired in response to problems
	// caused by being low on resources, so dynamically creating strings here might not
	// be such a hot idea
	const unsigned int MAX_ASSERT_TEXT=65536;
	char g_AssertText[MAX_ASSERT_TEXT];

	// Some Resource IDs for our dialog template
#define IDC_IGNORE_ALWAYS               1001
#define IDC_IGNORE_ONCE                 1002
#define IDC_DEBUG                       1003
#define IDC_ABORT                       1004
#define IDC_ASSERTION_TEXT              1005
#define IDC_COPY_TO_CLIPBOARD           1006
#define IDC_STOP                        1007 // advc.006l

	INT_PTR CALLBACK AssertDlgProc(HWND hDlg, UINT msg,WPARAM wParam, LPARAM lParam)
	{
		switch(msg)
		{
		case WM_INITDIALOG:
			{
				char modulePath[MAX_PATH];
				GetModuleFileName(NULL, modulePath, MAX_PATH);

				const char* moduleName = strrchr(modulePath, '\\');
				moduleName = moduleName ? moduleName+1 : modulePath;

				char title[MAX_PATH + 20];
				sprintf(title, "Assert Failed: %s", moduleName);
				SetWindowText(hDlg, title);

				sprintf( g_AssertText, "Assert Failed\r\n\r\n"
					"File:  %s\r\n"
					"Line:  %u\r\n"
					"Func:  %s\r\n" // advc.006f
					"Expression:  %s\r\n"
					"Message:  %s\r\n"
					"\r\n"
					"----------------------------------------------------------\r\n",
					g_AssertInfo.szFileName,
					g_AssertInfo.line,
					g_AssertInfo.szFunctionName, // advc.006f
					g_AssertInfo.szExpression,
					g_AssertInfo.szMessage ? g_AssertInfo.szMessage : "" );

				::SetWindowText( ::GetDlgItem(hDlg, IDC_ASSERTION_TEXT), g_AssertText );
				::SetFocus( ::GetDlgItem(hDlg, IDC_DEBUG) );

				break;
			}
		case WM_COMMAND:
			{
				switch(LOWORD(wParam))
				{
				case IDC_DEBUG:
					EndDialog(hDlg, ASSERT_DLG_DEBUG);
					return TRUE;

				case IDC_IGNORE_ONCE:
					EndDialog(hDlg, ASSERT_DLG_IGNORE);
					return TRUE;

				case IDC_IGNORE_ALWAYS:
					EndDialog(hDlg, ASSERT_DLG_IGNOREALWAYS);
					return TRUE;

				case IDC_ABORT:
					EndDialog(hDlg, ASSERT_DLG_EXIT);
					return TRUE;
				// <advc.006l>
				case IDC_STOP:
					EndDialog(hDlg, ASSERT_DLG_STOP);
					return TRUE; // </advc.006l>
				}
			}
			break;
		}

		return FALSE;
	}

	DWORD DisplayAssertDialog()
	{
		int const iTotalW = 379; // (advc.006l - as in BtS)
		CDialogTemplate dialogTemplate(_T("Assert Failed!"),
				DS_SETFONT | DS_CENTER | DS_MODALFRAME | DS_FIXEDSYS | WS_POPUP |
				WS_CAPTION | WS_SYSMENU,
				0, 0, iTotalW, 166, _T("MS Shell Dlg"), 8);
		// <advc>
		int const iBtnY = 145, iBtnH = 14, iLMargin = 7,
				iBtnW = /*64*/63, iSpacing = /*11*/10; // advc.006l
		int iIncrX = iBtnW + iSpacing;
		//int iBtnX = iLMargin + iIncrX; // </advc>
		// <advc.006l> Center-align instead
		int iTotalBtnW = 4 * iIncrX;
		bool const bShowStopBtn = (GC.getGame().getAIAutoPlay() > 0);
		if (bShowStopBtn)
			iTotalBtnW += iIncrX;
		int iBtnX = (iTotalW - iTotalBtnW) / 2; // </advc.006l>
		dialogTemplate.AddButton( _T("&Ignore Once"), WS_VISIBLE, 0,
				iBtnX, iBtnY, iBtnW, iBtnH, IDC_IGNORE_ONCE );
		iBtnX += iIncrX;
		dialogTemplate.AddButton( _T("Ignore Always"), WS_VISIBLE, 0,
				iBtnX, iBtnY, iBtnW, iBtnH, IDC_IGNORE_ALWAYS );
		// <advc.006l>
		if (bShowStopBtn)
		{
			iBtnX += iIncrX;
			dialogTemplate.AddButton(_T("&Stop Auto Play"), WS_VISIBLE, 0,
					iBtnX, iBtnY, iBtnW, iBtnH, IDC_STOP);
		} // </advc.006l>
		iBtnX += iIncrX;
		dialogTemplate.AddButton( _T("&Abort"), WS_VISIBLE, 0,
				iBtnX, iBtnY, iBtnW, iBtnH, IDC_ABORT );
		iBtnX += iIncrX;
		dialogTemplate.AddButton( _T("&Debug"), WS_VISIBLE, 0,
				iBtnX, iBtnY, iBtnW, iBtnH, IDC_DEBUG );
		dialogTemplate.AddEditBox( _T(""),
				ES_MULTILINE | ES_AUTOVSCROLL | ES_AUTOHSCROLL | ES_READONLY |
				WS_VSCROLL | WS_HSCROLL | WS_VISIBLE, WS_EX_STATICEDGE,
				iLMargin, iLMargin, 365, 130, IDC_ASSERTION_TEXT );
		int iRes = DialogBoxIndirect(GetModuleHandle(0),
				dialogTemplate.GetDialogTemplate(), NULL, (DLGPROC)AssertDlgProc);
		return iRes;
	}

} // end anonymous namespace

bool FAssertDlg( const char* szExpr, const char* szMsg, const char* szFile, unsigned int line,
	/* <advc.006f> */ const char* szFunction, /* </advc006f> */ bool& bIgnoreAlways )
{
	g_AssertInfo.szExpression = szExpr;
	g_AssertInfo.szMessage = szMsg;
	g_AssertInfo.szFileName = szFile;
	g_AssertInfo.szFunctionName = szFunction; // advc.006f
	g_AssertInfo.line = line;

	DWORD dwResult = DisplayAssertDialog();

	switch( dwResult )
	{
	case ASSERT_DLG_DEBUG:
		return true;

	case ASSERT_DLG_IGNORE:
		return false;

	case ASSERT_DLG_IGNOREALWAYS:
		bIgnoreAlways = true;
		return false;
	// <advc.006l>
	case ASSERT_DLG_STOP:
		GC.getGame().setAIAutoPlay(0);
		return false; // </advc.006l>

	case ASSERT_DLG_EXIT:
		exit(0);
		break;
	/*	<advc.wine> DisplayAssertDialog goes through DialogBoxIndirect (WinUser.h).
		I had assumed that Wine won't display that - but it does, so nvm.  */
	/*default:	
		printf("FAssertDlg: {%s} %s in %s, %s, line %d",
				szExpr, szMsg, szFile, szFunction, line);*/ // </advc.wine>
	}

	return true;
}

#endif // FASSERT_ENABLE && WIN32
