//
// XML Get functions
//

#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"
#include "FInputDevice.h"


// For progress bar display. Returns the number of steps we use.
// advc.003k: Commented out; was unused.
/*int CvXMLLoadUtility::GetNumProgressSteps() {
	return 20; // the function UpdateProgressCB() is called 20 times by CvXMLLoadUtilitySet
	//^advc: That's not true btw
}
void CvXMLLoadUtility::RegisterProgressCB(ProgressCB cbFxn) {
	m_pCBFxn = cbFxn;
}*/

// <advc>
namespace
{
void assignDefault(std::wstring& val, wchar const* szDefault = NULL)
{
	if (szDefault != NULL)
		val = szDefault;
	else val.clear();
}

void assignDefault(std::string& val, char const* szDefault = NULL)
{
	if (szDefault != NULL)
		val = szDefault;
	else val.clear();
}

void assignDefault(wchar* val, wchar const* szDefault = NULL)
{
	if (szDefault != NULL)
		wcscpy(val, szDefault);
	else wcscpy(val, L"");
}

void assignDefault(char* val, char const* szDefault = NULL)
{
	if (szDefault != NULL)
		strcpy(val, szDefault);
	else strcpy(val, "");
}

template<class T>
void assignDefault(T& val, T tDefault = 0)
{
	val = tDefault;
}
// </advc>
/*  <advc.006d> Wrappers for FXml::GetLastNodeValue. From the MNAI mod.
	Comment copied from there:
	Get the value from the last located node. Returns true if successful.
	Otherwise, get default value, show assert and return false.
	These functions specifically check if the node is empty for non-string values. */
bool SafeGetLastNodeValue(FXml* pXml, std::string& r, char const* szDefault = NULL)
{
	bool bSuccess = gDLL->getXMLIFace()->GetLastNodeValue(pXml, r);
	if (bSuccess)
		return true;
	FAssertMsg(bSuccess, "Error getting value, probably not a string");
	assignDefault(r, szDefault);
	return false;
}

bool SafeGetLastNodeValue(FXml* pXml, std::wstring& r, wchar const* szDefault = NULL)
{
	bool bSuccess = gDLL->getXMLIFace()->GetLastNodeValue(pXml, r);
	if (bSuccess)
		return true;
	FAssertMsg(bSuccess, "Error getting value, probably not a wstring");
	assignDefault(r, szDefault);
	return false;
}

// Missing: SafeGetLastNodeValue(FXml* pXml, {w}char*...). Rarely used I suppose.

template<class T> // advc: template
bool SafeGetLastNodeValue(FXml* pXml, T& r, T tDefault = false)
{
	bool bSuccess = true;
	if (gDLL->getXMLIFace()->GetLastNodeTextSize(pXml) == 0)
	{
		FErrorMsg("Empty element");
		bSuccess = false;
	}
	if (bSuccess)
	{
		bSuccess = gDLL->getXMLIFace()->GetLastNodeValue(pXml, &r);
		FAssertMsg(bSuccess, "Error getting value (wrong data type?)");
	}
	if (bSuccess)
		return true;
	assignDefault(r, tDefault);
	return false;
}
} // (end of unnamed namespace) </advc.006d>

/*  Set r to the value of the current XML node or, if the current node is
	a comment node, the next non-comment XML node. */
bool CvXMLLoadUtility::GetXmlVal(char* r, char const* szDefault)
{
	assignDefault(r, szDefault);
	if (SkipToNextVal()) // skip to the next non-comment node
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
		return true;
	}
	// otherwise we can't find a non-comment node on this level
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

// see CvXMLLoadUtility::GetXmlVal(char*...
bool CvXMLLoadUtility::GetXmlVal(wchar* r, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	if (SkipToNextVal()) // skip to the next non-comment node
	{
		// get the string value of the current xml node
		gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
		return true;
	}
	// otherwise we can't find a non-comment node on this level
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

// see CvXMLLoadUtility::GetXmlVal(char*...
bool CvXMLLoadUtility::GetXmlVal(std::string& r, char const* szDefault)
{
	assignDefault(r, szDefault);
	if (SkipToNextVal())
		return SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

// see CvXMLLoadUtility::GetXmlVal(char*...
bool CvXMLLoadUtility::GetXmlVal(std::wstring& r, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	if (SkipToNextVal())
		return SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

// see CvXMLLoadUtility::GetXmlVal(char*...
bool CvXMLLoadUtility::GetXmlVal(int& r, int iDefault)
{
	assignDefault(r, iDefault);
	if (SkipToNextVal())
		return SafeGetLastNodeValue(m_pFXml, r, iDefault); // advc.006d
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

// see CvXMLLoadUtility::GetXmlVal(char*...
bool CvXMLLoadUtility::GetXmlVal(float& r, float fDefault)
{
	assignDefault(r, fDefault);
	if (SkipToNextVal())
		return SafeGetLastNodeValue(m_pFXml, r, fDefault); // advc.006d
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

// see CvXMLLoadUtility::GetXmlVal(char*...
bool CvXMLLoadUtility::GetXmlVal(bool& r, bool bDefault)
{
	assignDefault(r, bDefault);
	if (SkipToNextVal())
		return SafeGetLastNodeValue(m_pFXml, r, bDefault); // advc.006d
	FAssertMsg(false , "Error in GetXmlVal function, unable to find the next non-comment node");
	return false;
}

/*  Get the value of the next sibling of the current XML node --
	or the next non-comment xml node if the current node is a comment node. */
bool CvXMLLoadUtility::GetNextXmlVal(std::string& r, char const* szDefault)
{
	assignDefault(r, szDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			return SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
		}
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// see CvXMLLoadUtility::GetNextXmlVal(std::string&...
bool CvXMLLoadUtility::GetNextXmlVal(std::wstring& r, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			return SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
		}
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// see CvXMLLoadUtility::GetNextXmlVal(std::string&...
bool CvXMLLoadUtility::GetNextXmlVal(char* r, char const* szDefault)
{
	assignDefault(r, szDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
			return true;
		}
		// otherwise we can't find a non-comment node on this level
		FAssertMsg(false , "Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// see CvXMLLoadUtility::GetNextXmlVal(std::string&...
bool CvXMLLoadUtility::GetNextXmlVal(wchar* r, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
			return true;
		}
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// see CvXMLLoadUtility::GetNextXmlVal(std::string&...
bool CvXMLLoadUtility::GetNextXmlVal(int& r, int iDefault)
{
	assignDefault(r, iDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, iDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// <advc.003t>
bool CvXMLLoadUtility::GetNextXmlVal(short& r, short iDefault)
{
	assignDefault(r, iDefault);
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal())
		{
			int i;
			bool b = SafeGetLastNodeValue(m_pFXml, i, (int)iDefault); // advc.006d
			r = safeIntCast<short>(i);
			return b;
		}
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false;
}

bool CvXMLLoadUtility::GetNextXmlVal(char& r, char iDefault)
{
	assignDefault(r, iDefault);
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal())
		{
			int i;
			bool b = SafeGetLastNodeValue(m_pFXml, i, (int)iDefault); // advc.006d
			r = safeIntCast<char>(i);
			return b;
		}
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false;
} // </advc.003t>

// see CvXMLLoadUtility::GetNextXmlVal(std::string&...
bool CvXMLLoadUtility::GetNextXmlVal(float& r, float fDefault)
{
	assignDefault(r, fDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, fDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// see CvXMLLoadUtility::GetNextXmlVal(std::string&...
bool CvXMLLoadUtility::GetNextXmlVal(bool& r, bool bDefault)
{
	assignDefault(r, bDefault);
	// if we can set the current xml node to its next sibling
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, bDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetNextXmlVal function, unable to find the next non-comment node");
		return false;
	}
	return false; // no more sibling nodes
}

// <advc.enum>
template<typename T>
bool CvXMLLoadUtility::GetNextXmlVal(T& r, T tDefault)
{
	assignDefault(r, tDefault);
	if (gDLL->getXMLIFace()->NextSibling(m_pFXml))
	{
		if (SkipToNextVal())
		{
			int iTmp = r;
			bool bResult = SafeGetLastNodeValue(m_pFXml,
					iTmp, static_cast<int>(tDefault));
			r = static_cast<T>(iTmp);
			return bResult;
		}
		FErrorMsg("Unable to find the next non-comment node");
		return false;
	}
	return false;
}
#define INSTANTIATE_GET_NEXT_XML_VAL(EnumPrefix, Dummy) \
	template bool CvXMLLoadUtility::GetNextXmlVal<EnumPrefix##Types>(EnumPrefix##Types&, EnumPrefix##Types);
DO_FOR_EACH_DYN_INFO_TYPE(INSTANTIATE_GET_NEXT_XML_VAL);
DO_FOR_EACH_STATIC_INFO_TYPE(INSTANTIATE_GET_NEXT_XML_VAL);
#undef INSTANTIATE_GET_NEXT_XML_VAL
// </advc.enum>

/*  Overloaded function that sets the current XML node to its
	first non-comment child node and then sets r to that node's value. */
bool CvXMLLoadUtility::GetChildXmlVal(std::string& r, char const* szDefault)
{
	assignDefault(r, szDefault);
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them.
	FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

// see GetChildXmlVal(std::string&...)
bool CvXMLLoadUtility::GetChildXmlVal(std::wstring& r, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them.
	FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

// see GetChildXmlVal(std::string&...)
bool CvXMLLoadUtility::GetChildXmlVal(char* r, char const* szDefault)
{
	assignDefault(r, szDefault);
	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
			return true;
		}
		// otherwise we can't find a non-comment node on this level
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them.
	FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

// see GetChildXmlVal(std::string&...)
bool CvXMLLoadUtility::GetChildXmlVal(wchar* r, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
			return true;
		}
		// otherwise we can't find a non-comment node on this level
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them.
	FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

// see GetChildXmlVal(std::string&...)
bool CvXMLLoadUtility::GetChildXmlVal(int& r, int iDefault)
{
	assignDefault(r, iDefault);
	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, iDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FAssertMsg(false , "Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them.
	FAssertMsg(false , "Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

// see GetChildXmlVal(std::string&...)
bool CvXMLLoadUtility::GetChildXmlVal(float& r, float fDefault)
{
	assignDefault(r, fDefault);
	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, fDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them so.
	FErrorMsg("Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

// see GetChildXmlVal(std::string&...)
bool CvXMLLoadUtility::GetChildXmlVal(bool& r, bool bDefault)
{
	assignDefault(r, bDefault);
	// if we successfully set the current xml node to it's first child node
	if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
			return SafeGetLastNodeValue(m_pFXml, r, bDefault); // advc.006d
		// otherwise we can't find a non-comment node on this level
		FErrorMsg("Error in GetChildXmlVal function, unable to find the next non-comment node");
		return false;
	}
	// otherwise there are no child nodes, but we were expecting them.
	FErrorMsg("Error in GetChildXmlVal function, unable to find a child node");
	return false;
}

CvString CvXMLLoadUtility::szAssertMsg = "Unable to find node "; // advc.006b

/*  Overloaded function that gets the child value of the tag with szName
	if there is only one child value of that name */
bool CvXMLLoadUtility::GetChildXmlValByName(wchar* r, TCHAR const* szName, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	/*  advc.006b: The iNumChildrenByTagName check had already been disabled.
		Keep it that way b/c NumOfChildrenByTagName can't handle comments in XML.
		As comments don't seem to lead to overcounting, one could still do this: */
	//FAssertMsg(gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName) < 2,"More children with tag name than expected, should only be 1.");
	// ... However, I think FXML already detects duplicate tags when enforcing the XML schema.

	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b> Replacing the asserts above (which were already commented out)
	/*  If pszDefault was set by the caller, we assume that it's OK to fall back
		on pszDefault. Otherwise warn. */
	FAssertMsg(szDefault != NULL || !m->bAssertMandatory, (szAssertMsg + szName).c_str());
	return false; // </advc.006b>
}

// see GetChildXmlValByName(wchar*...)
bool CvXMLLoadUtility::GetChildXmlValByName(char* r, TCHAR const* szName, char const* szDefault)
{
	assignDefault(r, szDefault);
	// advc.006b: See GetChildXmlValByName(wchar*...)
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			// get the string value of the current xml node
			gDLL->getXMLIFace()->GetLastNodeValue(m_pFXml, r);
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return true;
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b>
	FAssertMsg(szDefault != NULL || !m->bAssertMandatory, (szAssertMsg + szName).c_str());
	return false; // </advc.006>
}

// see GetChildXmlValByName(wchar*...)
bool CvXMLLoadUtility::GetChildXmlValByName(std::string& r, TCHAR const* szName, char const* szDefault)
{
	assignDefault(r, szDefault);
	// advc.006b: See GetChildXmlValByName(wchar*...)
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			bool bSuccess = SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return bSuccess; // advc.006d
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b>
	FAssertMsg(szDefault != NULL || !m->bAssertMandatory, (szAssertMsg + szName).c_str());
	return false; // </advc.006>
}

// see GetChildXmlValByName(wchar*...)
bool CvXMLLoadUtility::GetChildXmlValByName(std::wstring& r, TCHAR const* szName, wchar const* szDefault)
{
	assignDefault(r, szDefault);
	// advc.006b: See GetChildXmlValByName(wchar*...)
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			bool bSuccess = SafeGetLastNodeValue(m_pFXml, r, szDefault); // advc.006d
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return bSuccess; // advc.006d
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b>
	FAssertMsg(szDefault != NULL || !m->bAssertMandatory, (szAssertMsg + szName).c_str());
	return false; // </advc.006>
}

// see GetChildXmlValByName(wchar*...)
bool CvXMLLoadUtility::GetChildXmlValByName(int* r, TCHAR const* szName, int iDefault)
{
	assignDefault(*r, iDefault);
	// advc.006b: See GetChildXmlValByName(wchar*...)
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			bool bSuccess = SafeGetLastNodeValue(m_pFXml, *r, iDefault); // advc.006d
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return bSuccess; // advc.006d
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b>
	if (*r == MIN_INT && m->bAssertMandatory)
	{
		FErrorMsg((szAssertMsg + szName).c_str());
		/*  Try to allow the caller to ignore the error by setting a
			more sensible default than MIN_INT: */
		*r = 0; // (0 is also the "default default" that was set in this function's declaration in BtS)
	}
	return false; // </advc.006b>
}

// see GetChildXmlValByName(wchar*...)
bool CvXMLLoadUtility::GetChildXmlValByName(float* r, TCHAR const* szName, float fDefault)
{
	assignDefault(*r, fDefault);
	// advc.006b: See GetChildXmlValByName(wchar*...)
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag5 name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			bool bSuccess = SafeGetLastNodeValue(m_pFXml, *r, fDefault); // advc.006d
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return bSuccess; // advc.006d
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b>
	if (*r == FLT_MIN && m->bAssertMandatory)
	{
		FErrorMsg((szAssertMsg + szName).c_str());
		*r = 0; // See See GetChildXmlValByName(int*...)
	}
	return false; // </advc.006b>
}

// see GetChildXmlValByName(wchar*...)
bool CvXMLLoadUtility::GetChildXmlValByName(bool* r, TCHAR const* szName,
	/* <advc.006b> */ bool bMandatory /* </advc.006b> */, bool bDefault)
{
	assignDefault(*r, bDefault);
	// advc.006b: See GetChildXmlValByName(wchar*...)
	/*int iNumChildrenByTagName=1;
	iNumChildrenByTagName = gDLL->getXMLIFace()->NumOfChildrenByTagName(m_pFXml, szName);
	FAssertMsg((iNumChildrenByTagName < 2),"More children with tag name than expected, should only be 1.");
	// we only continue if there are one and only one children with this tag name
	if (iNumChildrenByTagName == 1)
	{*/
	if (SkipToNextVal() && // advc.001
		gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szName))
	{
		if (SkipToNextVal()) // skip to the next non-comment node
		{
			bool bSuccess = SafeGetLastNodeValue(m_pFXml, *r, bDefault); // advc.006d
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return bSuccess; // advc.006d
		}
		// otherwise we can't find a non-comment node on this level so we will FAssert and return false
		else
		{
			FErrorMsg("Error in GetChildXmlValByName function, unable to find the next non-comment node");
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
			return false;
		}
	}
	/*else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	} }
	else {
		//FErrorMsg("Error in GetChildXmlValByName function, unable to find a specified node");
		return false;
	}*/ // <advc.006b>
	FAssertMsg(!bMandatory || !m->bAssertMandatory, (szAssertMsg + szName).c_str());
	return false; // </advc.006b>
}

// <advc.xmldefault>
void CvXMLLoadUtility::SetGlobalTypeFromChildXmlVal(int& iR, TCHAR const* szName,
	bool bInfoType)
{
	CvString szTextVal;
	GetChildXmlValByName(szTextVal, szName, iR == 0 ? NULL : "");
	if (!szTextVal.IsEmpty())
	{
		iR = (bInfoType ? FindInInfoClass(szTextVal) :
				getGlobalEnumFromString(szTextVal));
	}
}

// (based on code by rheinig)
int CvXMLLoadUtility::GetChildTypeIndex()
{
	CvString szType;
	if (GetChildXmlValByName(szType, "Type") && !szType.empty())
		return GC.getInfoTypeForString(szType, true);
	return -1;
} // </advc.xmldefault>

// advc.006b:
void CvXMLLoadUtility::setAssertMandatoryEnabled(bool b)
{
	m->bAssertMandatory = b;
}

/*	Returns either the integer value of the keyboard mapping for the hot key --
	or -1 if it doesn't exist. */
int CvXMLLoadUtility::GetHotKeyInt(const TCHAR* pszHotKeyVal)
{
	PROFILE("GetHotKeyInt");

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

	for (int i = 0; i < iNumKeyBoardMappings; i++)
	{
		if (strcmp(asCvKeyBoardMapping [i].szDefineString, pszHotKeyVal) == 0)
		{
			return asCvKeyBoardMapping[i].iIntVal;
		}
	}

	return -1;
}
