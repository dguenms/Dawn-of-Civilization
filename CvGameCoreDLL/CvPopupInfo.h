#pragma once
#ifndef CVPOPUPINFO_H
#define CVPOPUPINFO_H

//#include "CvEnums.h"

struct CvPopupButtonPython
{
	CvWString szText;
	CvString szArt;
};


class CvPopupInfo
{
public:
	DllExport CvPopupInfo(ButtonPopupTypes eButtonPopupType = BUTTONPOPUP_TEXT, int iData1 = -1, int iData2 = -1, int iData3 = -1, int iFlags = 0, bool bOption1 = false, bool bOption2 = false);
	DllExport virtual ~CvPopupInfo();

	DllExport void read(FDataStreamBase& stream);
	DllExport void write(FDataStreamBase& stream) const;

	DllExport const CvPopupInfo& operator=(const CvPopupInfo& other);

	// Accessors
	DllExport int getData1() const;
	DllExport int getData2() const;
	DllExport int getData3() const;
	DllExport int getFlags() const;
	DllExport bool getOption1() const;
	DllExport bool getOption2() const;
	DllExport ButtonPopupTypes getButtonPopupType() const;
	DllExport const CvWString& getText() const;
	DllExport bool getPendingDelete() const;
	DllExport const CvString& getOnFocusPythonCallback() const;
	DllExport const CvString& getOnClickedPythonCallback() const;
	DllExport const CvString& getPythonModule() const;
	DllExport const CvWString& getPythonButtonText(int i) const;
	DllExport const CvString& getPythonButtonArt(int i) const;
	DllExport int getNumPythonButtons() const;

	DllExport void setData1(int iValue);
	DllExport void setData2(int iValue);
	DllExport void setData3(int iValue);
	DllExport void setFlags(int iValue);
	DllExport void setOption1(bool bValue);
	DllExport void setOption2(bool bValue);
	DllExport void setButtonPopupType(ButtonPopupTypes eValue);
	DllExport void setText(const wchar* pszText);
	DllExport void setPendingDelete(bool bDelete);
	DllExport void setOnFocusPythonCallback(const char* szOnFocus);
	DllExport void setOnClickedPythonCallback(const char* szOnClicked);
	DllExport void setPythonModule(const char* szModule);
	DllExport void addPythonButton(const wchar* szText, const char* szArt);

protected:
	int m_iData1;
	int m_iData2;
	int m_iData3;
	int m_iFlags;
	bool m_bOption1;
	bool m_bOption2;
	ButtonPopupTypes m_eButtonPopupType;
	CvWString m_szText;

	std::vector<CvPopupButtonPython> m_aPythonButtons;
	CvString m_szOnFocusPythonCallback;
	CvString m_szOnClickedPythonCallback;
	CvString m_szPythonModule;

	bool m_bPendingDelete;
};


#endif