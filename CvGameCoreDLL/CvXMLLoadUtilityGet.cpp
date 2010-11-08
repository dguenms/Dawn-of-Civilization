//
// XML Get functions
//

#include "CvGameCoreDLL.h"
#include "CvDLLXMLIFaceBase.h"
#include "CvXMLLoadUtility.h"
#include "CvGlobals.h"
#include "CvArtFileMgr.h"
#include "FInputDevice.h"
#include "FProfiler.h"

//
// STATIC
// for progress bar display
// returns the number of steps we use
//
int CvXMLLoadUtility::GetNumProgressSteps()
{
	return 20;	// the function UpdateProgressCB() is called 20 times by CvXMLLoadUtilitySet
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(char* pszVal, char* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(char* pszVal, char* pszDefault)
{
	if (pszDefault)
	{
		strcpy(pszVal, pszDefault);
	}
	else
	{
		strcpy(pszVal, "");
	}

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(wchar* pszVal, wchar* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(wchar* pszVal, wchar* pszDefault)
{
	if (pszDefault)
	{
		wcscpy(pszVal, pszDefault);
	}
	else
	{
		wcscpy(pszVal, L"");
	}

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(std::string& pszVal, char* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(std::string& pszVal, char* pszDefault)
{
	if (pszDefault)
	{
		pszVal = pszDefault;
	}
	else
	{
		pszVal.clear();
	}

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(std::wstring& pszVal, wchar* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(std::wstring& pszVal, wchar* pszDefault)
{
	if (pszDefault)
	{
		pszVal = pszDefault;
	}
	else
	{
		pszVal.clear();
	}

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(int* piVal, int iDefault = 0)
//
//  PURPOSE :   Get the int value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(int* piVal, int iDefault)
{
	// set the value to the default
	*piVal = iDefault;

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,piVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(float* pfVal, float fDefault = 0.0f)
//
//  PURPOSE :   Get the float value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(float* pfVal, float fDefault)
{
	// set the value to the default
	*pfVal = fDefault;

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pfVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetXmlVal(bool* pbVal, bool bDefault = false)
//
//  PURPOSE :   Get the boolean value of the current xml node or the next non-comment xml node if the
//				current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetXmlVal(bool* pbVal, bool bDefault)
{
	// set the boolean value to it's default value
	*pbVal = bDefault;

	// skip to the next non-comment node
	if (SkipToNextVal())
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pbVal);
		return true;
	}
	// otherwise we can't find a non-comment node on this level so we will FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
		return false;
	}
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(std::string& pszVal, char* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the next sibling of the current xml node or the next 
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(std::string& pszVal, char* pszDefault)
{
	if (pszDefault)
	{
		pszVal = pszDefault;
	}
	else
	{
		pszVal.clear();
	}

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(std::wstring& pszVal, wchar* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the next sibling of the current xml node or the next 
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(std::wstring& pszVal, wchar* pszDefault)
{
	if (pszDefault)
	{
		pszVal = pszDefault;
	}
	else
	{
		pszVal.clear();
	}

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(char* pszVal, char* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the next sibling of the current xml node or the next 
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(char* pszVal, char* pszDefault)
{
	if (pszDefault)
	{
		strcpy(pszVal, pszDefault);
	}
	else
	{
		strcpy(pszVal, "");
	}

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(wchar* pszVal, wchar* pszDefault = NULL)
//
//  PURPOSE :   Get the string value of the next sibling of the current xml node or the next 
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(wchar* pszVal, wchar* pszDefault)
{
	if (pszDefault)
	{
		wcscpy(pszVal, pszDefault);
	}
	else
	{
		wcscpy(pszVal, L"");
	}

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(int* piVal, int iDefault = 0)
//
//  PURPOSE :   Get the int value of the next sibling of the current xml node or the next
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(int* piVal, int iDefault)
{
	// set the value to the default
	*piVal = iDefault;

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,piVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(float* pfVal, float fDefault = 0.0f)
//
//  PURPOSE :   Get the float value of the next sibling of the current xml node or the next
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(float* pfVal, float fDefault)
{
	// set the value to the default
	*pfVal = fDefault;

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pfVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetNextXmlVal(bool* pbVal, bool bDefault = false)
//
//  PURPOSE :   Get the boolean value of the next sibling of the current xml node or the next
//				non-comment xml node if the current node is a comment node
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetNextXmlVal(bool* pbVal, bool bDefault)
{
	// set the boolean value to it's default value
	*pbVal = bDefault;

	// if we can set the current xml node to it's next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pbVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no more sibling nodes but we were expecting them so FAssert and return false
	else
	{
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(std::string& pszVal, char* pszDefault = NULL)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's string value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(std::string& pszVal, char* pszDefault)
{
	if (pszDefault)
	{
		pszVal = pszDefault;
	}
	else
	{
		pszVal.clear();
	}

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(std::wstring& pszVal, wchar* pszDefault = NULL)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's string value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(std::wstring& pszVal, wchar* pszDefault)
{
	if (pszDefault)
	{
		pszVal = pszDefault;
	}
	else
	{
		pszVal.clear();
	}

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(char* pszVal, char* pszDefault = NULL)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's string value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(char* pszVal, char* pszDefault)
{
	if (pszDefault)
	{
		strcpy(pszVal, pszDefault);
	}
	else
	{
		strcpy(pszVal, "");
	}

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(wchar* pszVal, wchar* pszDefault = NULL)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's string value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(wchar* pszVal, wchar* pszDefault)
{
	if (pszDefault)
	{
		wcscpy(pszVal, pszDefault);
	}
	else
	{
		wcscpy(pszVal, L"");
	}

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(int* piVal, int iDefault = 0)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's integer value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(int* piVal, int iDefault)
{
	// set the value to the default
	*piVal = iDefault;

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,piVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(float* pfVal, float fDefault = 0.0f)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's float value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(float* pfVal, float fDefault)
{
	// set the value to the default
	*pfVal = fDefault;

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pfVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false, "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false, "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlVal(bool* pbVal, bool bDefault = false)
//
//  PURPOSE :   overloaded function that sets the current xml node to it's first non-comment child node 
//				and then that node's boolean value
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlVal(bool* pbVal, bool bDefault)
{
	// set the boolean value to it's default value
	*pbVal = bDefault;

	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		// skip to the next non-comment node
		if (SkipToNextVal())
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pbVal);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FAssertMsg(false, "Error in GetChildXmlVal function, unable to find the next non-comment node");
			return false;
		}
	}
	// otherwise there are no child nodes but we were expecting them so FAssert and return false
	else
	{
		FAssertMsg(false, "Error in GetChildXmlVal function, unable to find a child node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlValByName(wchar* pszVal, const TCHAR* szName, TCHAR* pszDefault = NULL)
//
//  PURPOSE :   Overloaded function that gets the child value of the tag with szName if there is only one child
// 				value of that name

//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(wchar* pszVal, const TCHAR* szName, wchar* pszDefault)
{
	int iNumChildrenByTagName=1;

	if (pszDefault)
	{
		wcscpy(pszVal, pszDefault);
	}
	else
	{
		wcscpy(pszVal, L"");
	}

#if 0
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
#endif
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		// FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlValByName(char* pszVal, const TCHAR* szName, TCHAR* pszDefault = NULL)
//
//  PURPOSE :   Overloaded function that gets the child value of the tag with szName if there is only one child
// 				value of that name

//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(char* pszVal, const TCHAR* szName, char* pszDefault)
{
	int iNumChildrenByTagName=1;

	if (pszDefault)
	{
		strcpy(pszVal, pszDefault);
	}
	else
	{
		strcpy(pszVal, "");
	}

#if 0
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
#endif
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		// FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlValByName(std::string& pszVal, const TCHAR* szName, TCHAR* pszDefault = NULL)
//
//  PURPOSE :   Overloaded function that gets the child value of the tag with szName if there is only one child
// 				value of that name

//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(std::string& pszVal, const TCHAR* szName, char* pszDefault)
{
	int iNumChildrenByTagName=1;

	if (pszDefault)
	{
		pszVal=pszDefault;
	}
	else
	{
		pszVal.clear();
	}

#if 0
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
#endif
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		//FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}

//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(std::wstring& pszVal, const TCHAR* szName, wchar* pszDefault)
{
	int iNumChildrenByTagName=1;

	if (pszDefault)
	{
		pszVal=pszDefault;
	}
	else
	{
		pszVal.clear();
	}

#if 0
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
#endif
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pszVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		//FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlValByName(int* piVal, const TCHAR* szName, int iDefault = 0)
//
//  PURPOSE :   Overloaded function that gets the child value of the tag with szName if there is only one child
// 				value of that name
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(int* piVal, const TCHAR* szName, int iDefault)
{
	int iNumChildrenByTagName=1;

	// set the value to the default
	*piVal = iDefault;

#if 0	// def _DEBUG
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
#endif
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,piVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		//FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlValByName(float* pfVal, const TCHAR* szName, float fDefault = 0.0f)
//
//  PURPOSE :   Overloaded function that gets the child value of the tag with szName if there is only one child
// 				value of that name

//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(float* pfVal, const TCHAR* szName, float fDefault)
{
	int iNumChildrenByTagName=1;

	// set the value to the default
	*pfVal = fDefault;
#if 0
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag5 name than expected, should only be 1.");
#endif
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pfVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		//FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetChildXmlValByName(bool* pbVal, const TCHAR* szName, bool bDefault = false)
//
//  PURPOSE :   Overloaded function that gets the child value of the tag with szName if there is only one child
// 				value of that name

//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::GetChildXmlValByName(bool* pbVal, const TCHAR* szName, bool bDefault)
{
	int iNumChildrenByTagName=1;

	// set the boolean value to it's default value
	*pbVal = bDefault;

#if 0
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml,szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
#endif
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szName))
		{
			// skip to the next non-comment node
			if (SkipToNextVal())
			{
				// get the string value of the current xml node
				gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml,pbVal);
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return true;
			}
			// otherwise we can't find a non-comment node on this level so we will FAssert and return false
			else
			{
				FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find the next non-comment node");
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				return false;
			}
		}
		// otherwise there are no child nodes but we were expecting them so FAssert and return false
		else
		{
//			FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
			return false;
		}
	}
	else
	{
		//FAssertMsg(false, "Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   GetHotKeyInt(TCHAR* pszHotKeyVal)
//
//  PURPOSE :   returns either the integer value of the keyboard mapping for the hot key or -1 if it
//				doesn't exist.
//
//------------------------------------------------------------------------------------------------------
int CvXMLLoadUtility::GetHotKeyInt(const TCHAR* pszHotKeyVal)
{
	// SPEEDUP
	PROFILE("GetHotKeyInt");
	int i;

	struct CvKeyBoardMapping
	{
		TCHAR szDefineString[25];
		int iIntVal;
	};


	const int iNumKeyBoardMappings=108;
	const CvKeyBoardMapping asCvKeyBoardMapping[iNumKeyBoardMappings] =
	{
		{"KB_ESCAPE",FInputDevice::KB_ESCAPE},
		{"KB_0",FInputDevice::KB_0},
		{"KB_1",FInputDevice::KB_1},
		{"KB_2",FInputDevice::KB_2},
		{"KB_3",FInputDevice::KB_3},
		{"KB_4",FInputDevice::KB_4},
		{"KB_5",FInputDevice::KB_5},
		{"KB_6",FInputDevice::KB_6},
		{"KB_7",FInputDevice::KB_7},
		{"KB_8",FInputDevice::KB_8},
		{"KB_9",FInputDevice::KB_9},
		{"KB_MINUS",FInputDevice::KB_MINUS},	    /* - on main keyboard */	
		{"KB_A",FInputDevice::KB_A},
		{"KB_B",FInputDevice::KB_B},
		{"KB_C",FInputDevice::KB_C},
		{"KB_D",FInputDevice::KB_D},
		{"KB_E",FInputDevice::KB_E},
		{"KB_F",FInputDevice::KB_F},
		{"KB_G",FInputDevice::KB_G},
		{"KB_H",FInputDevice::KB_H},
		{"KB_I",FInputDevice::KB_I},
		{"KB_J",FInputDevice::KB_J},
		{"KB_K",FInputDevice::KB_K},
		{"KB_L",FInputDevice::KB_L},
		{"KB_M",FInputDevice::KB_M},
		{"KB_N",FInputDevice::KB_N},
		{"KB_O",FInputDevice::KB_O},
		{"KB_P",FInputDevice::KB_P},
		{"KB_Q",FInputDevice::KB_Q},
		{"KB_R",FInputDevice::KB_R},
		{"KB_S",FInputDevice::KB_S},
		{"KB_T",FInputDevice::KB_T},
		{"KB_U",FInputDevice::KB_U},
		{"KB_V",FInputDevice::KB_V},
		{"KB_W",FInputDevice::KB_W},
		{"KB_X",FInputDevice::KB_X},
		{"KB_Y",FInputDevice::KB_Y},
		{"KB_Z",FInputDevice::KB_Z},
		{"KB_EQUALS",FInputDevice::KB_EQUALS},
		{"KB_BACKSPACE",FInputDevice::KB_BACKSPACE},
		{"KB_TAB",FInputDevice::KB_TAB},
		{"KB_LBRACKET",FInputDevice::KB_LBRACKET},
		{"KB_RBRACKET",FInputDevice::KB_RBRACKET},
		{"KB_RETURN",FInputDevice::KB_RETURN},		/* Enter on main keyboard */
		{"KB_LCONTROL",FInputDevice::KB_LCONTROL},
		{"KB_SEMICOLON",FInputDevice::KB_SEMICOLON},
		{"KB_APOSTROPHE",FInputDevice::KB_APOSTROPHE},
		{"KB_GRAVE",FInputDevice::KB_GRAVE},		/* accent grave */
		{"KB_LSHIFT",FInputDevice::KB_LSHIFT},
		{"KB_BACKSLASH",FInputDevice::KB_BACKSLASH},
		{"KB_COMMA",FInputDevice::KB_COMMA},
		{"KB_PERIOD",FInputDevice::KB_PERIOD},
		{"KB_SLASH",FInputDevice::KB_SLASH},
		{"KB_RSHIFT",FInputDevice::KB_RSHIFT},
		{"KB_NUMPADSTAR",FInputDevice::KB_NUMPADSTAR},
		{"KB_LALT",FInputDevice::KB_LALT},
		{"KB_SPACE",FInputDevice::KB_SPACE},
		{"KB_CAPSLOCK",FInputDevice::KB_CAPSLOCK},
		{"KB_F1",FInputDevice::KB_F1},
		{"KB_F2",FInputDevice::KB_F2},
		{"KB_F3",FInputDevice::KB_F3},
		{"KB_F4",FInputDevice::KB_F4},
		{"KB_F5",FInputDevice::KB_F5},
		{"KB_F6",FInputDevice::KB_F6},
		{"KB_F7",FInputDevice::KB_F7},
		{"KB_F8",FInputDevice::KB_F8},
		{"KB_F9",FInputDevice::KB_F9},
		{"KB_F10",FInputDevice::KB_F10},
		{"KB_NUMLOCK",FInputDevice::KB_NUMLOCK},
		{"KB_SCROLL",FInputDevice::KB_SCROLL},
		{"KB_NUMPAD7",FInputDevice::KB_NUMPAD7},
		{"KB_NUMPAD8",FInputDevice::KB_NUMPAD8},
		{"KB_NUMPAD9",FInputDevice::KB_NUMPAD9},
		{"KB_NUMPADMINUS",FInputDevice::KB_NUMPADMINUS},
		{"KB_NUMPAD4",FInputDevice::KB_NUMPAD4},
		{"KB_NUMPAD5",FInputDevice::KB_NUMPAD5},
		{"KB_NUMPAD6",FInputDevice::KB_NUMPAD6},
		{"KB_NUMPADPLUS",FInputDevice::KB_NUMPADPLUS},
		{"KB_NUMPAD1",FInputDevice::KB_NUMPAD1},
		{"KB_NUMPAD2",FInputDevice::KB_NUMPAD2},
		{"KB_NUMPAD3",FInputDevice::KB_NUMPAD3},
		{"KB_NUMPAD0",FInputDevice::KB_NUMPAD0},
		{"KB_NUMPADPERIOD",FInputDevice::KB_NUMPADPERIOD}, 
		{"KB_F11",FInputDevice::KB_F11},
		{"KB_F12",FInputDevice::KB_F12},
		{"KB_NUMPADEQUALS",FInputDevice::KB_NUMPADEQUALS},
		{"KB_AT",FInputDevice::KB_AT},
		{"KB_UNDERLINE",FInputDevice::KB_UNDERLINE},
		{"KB_COLON",FInputDevice::KB_COLON},
		{"KB_NUMPADENTER",FInputDevice::KB_NUMPADENTER},
		{"KB_RCONTROL",FInputDevice::KB_RCONTROL},
		{"KB_VOLUMEDOWN",FInputDevice::KB_VOLUMEDOWN},
		{"KB_VOLUMEUP",FInputDevice::KB_VOLUMEUP},
		{"KB_NUMPADCOMMA",FInputDevice::KB_NUMPADCOMMA},
		{"KB_NUMPADSLASH",FInputDevice::KB_NUMPADSLASH},
		{"KB_SYSRQ",FInputDevice::KB_SYSRQ},
		{"KB_RALT",FInputDevice::KB_RALT},
		{"KB_PAUSE",FInputDevice::KB_PAUSE},
		{"KB_HOME",FInputDevice::KB_HOME},
		{"KB_UP",FInputDevice::KB_UP},
		{"KB_PGUP",FInputDevice::KB_PGUP},
		{"KB_LEFT",FInputDevice::KB_LEFT},
		{"KB_RIGHT",FInputDevice::KB_RIGHT},
		{"KB_END",FInputDevice::KB_END},
		{"KB_DOWN",FInputDevice::KB_DOWN},
		{"KB_PGDN",FInputDevice::KB_PGDN},
		{"KB_INSERT",FInputDevice::KB_INSERT},
		{"KB_DELETE",FInputDevice::KB_DELETE},
	};

	for (i=0;i<iNumKeyBoardMappings;i++)
	{
		if (strcmp(asCvKeyBoardMapping [i].szDefineString, pszHotKeyVal) == 0)
		{
			return asCvKeyBoardMapping[i].iIntVal;
		}
	}

	return -1;
}

