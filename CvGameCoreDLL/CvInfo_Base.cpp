// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"

CvInfoBase::CvInfoBase() : m_bGraphicalOnly(false) {}

// advc.xmldefault:
CvInfoBase::CvInfoBase(CvInfoBase const& kOther)
{
	FErrorMsg("Copy-ctor not implemented");
}

#if ENABLE_XML_FILE_CACHE
void CvInfoBase::read(FDataStreamBase* pStream)
{
	reset();
	pStream->Read(&m_bGraphicalOnly);
	pStream->ReadString(m_szType);
	pStream->ReadString(m_szCivilopediaKey);
	pStream->ReadString(m_szHelpKey);
	pStream->ReadString(m_szStrategyKey);
	pStream->ReadString(m_szButton);
	pStream->ReadString(m_szTextKey);
}

void CvInfoBase::write(FDataStreamBase* pStream)
{
	pStream->Write(m_bGraphicalOnly);
	pStream->WriteString(m_szType);
	pStream->WriteString(m_szCivilopediaKey);
	pStream->WriteString(m_szHelpKey);
	pStream->WriteString(m_szStrategyKey);
	pStream->WriteString(m_szButton);
	pStream->WriteString(m_szTextKey);
}
#endif
void CvInfoBase::reset()
{
	//clear cache
	m_aCachedDescriptions.clear();
	m_szCachedText.clear();
	m_szCachedHelp.clear();
	m_szCachedStrategy.clear();
	m_szCachedCivilopedia.clear();
}

bool CvInfoBase::isGraphicalOnly() const
{
	return m_bGraphicalOnly;
}

TCHAR const* CvInfoBase::getType() const
{
	if (m_szType.empty())
		return NULL;
	return m_szType;
}

// advc.xmldefault:
bool CvInfoBase::isDefaultsType() const
{
	if (m_szType.empty())
		return false;
	CvString const szEnding = "_DEFAULTS";
	return (m_szType.length() > szEnding.length() &&
			m_szType.compare(
			m_szType.length() - szEnding.length(),
			szEnding.length(),
			szEnding) == 0);
}

TCHAR const* CvInfoBase::getButton() const
{
	if (m_szButton.empty())
		return NULL;

	return m_szButton;
}

wchar const* CvInfoBase::getTextKeyWide() const
{
	return m_szTextKey;
}

/*	<advc.137> Split the original code so that derived classes don't need to worry
	about the cache */
wchar const* CvInfoBase::getDescription(uint uiForm) const
{
	while(m_aCachedDescriptions.size() <= uiForm)
		m_aCachedDescriptions.push_back(getDescriptionInternal());
	return m_aCachedDescriptions[uiForm];
}

CvWString CvInfoBase::getDescriptionInternal() const
{
	return gDLL->getObjectText(m_szTextKey, m_aCachedDescriptions.size());
} // </advc.137>

wchar const* CvInfoBase::getText() const
{
	// used instead of getDescription for Info entries that are not objects
	// so they do not have gender/plurality/forms defined in the Translator system
	if(m_szCachedText.empty())
		m_szCachedText = gDLL->getText(m_szTextKey);
	return m_szCachedText;
}

wchar const* CvInfoBase::getCivilopedia() const
{
	if(m_szCachedCivilopedia.empty())
		m_szCachedCivilopedia = gDLL->getText(m_szCivilopediaKey);
	return m_szCachedCivilopedia;
}

wchar const* CvInfoBase::getHelp() const
{
	if (m_szCachedHelp.empty())
		m_szCachedHelp = gDLL->getText(m_szHelpKey);
	return m_szCachedHelp;
}

wchar const* CvInfoBase::getStrategy() const
{
	if (m_szCachedStrategy.empty())
		m_szCachedStrategy = gDLL->getText(m_szStrategyKey);
	return m_szCachedStrategy;
}

bool CvInfoBase::isMatchForLink(std::wstring szLink, bool bKeysOnly) const
{
	if (szLink == CvWString(getType()).GetCString())
		return true;

	if (!bKeysOnly)
	{
		uint iNumForms = gDLL->getNumForms(getTextKeyWide());
		for (uint i = 0; i < iNumForms; i++)
		{
			if (szLink == getDescription(i))
				return true;
		}
	}
	return false;
}

// read from XML: TYPE, DESC, BUTTON
bool CvInfoBase::read(CvXMLLoadUtility* pXML)
{
	// Skip any comments and stop at the next value we might want
	if (!pXML->SkipToNextVal())
		return false;

	pXML->MapChildren(); // try to hash children for fast lookup by name

	pXML->GetChildXmlValByName(&m_bGraphicalOnly, "bGraphicalOnly", /* advc.006b: */ false);
	pXML->GetChildXmlValByName(m_szType, "Type", /* advc.006b: */ "");
	pXML->GetChildXmlValByName(m_szTextKey, "Description", /* advc.006b: */ L"");
	pXML->GetChildXmlValByName(m_szCivilopediaKey, "Civilopedia", /* advc.006b: */ L"");
	pXML->GetChildXmlValByName(m_szHelpKey, "Help", /* advc.006b: */ L"");
	pXML->GetChildXmlValByName(m_szStrategyKey, "Strategy", /* advc.006b: */ L"");
	pXML->GetChildXmlValByName(m_szButton, "Button", /* advc.006b: */ "");

	return true;
}


bool CvScalableInfo::read(CvXMLLoadUtility* pXML)
{
	pXML->GetChildXmlValByName(&m_fScale, "fScale");
	pXML->GetChildXmlValByName(&m_fInterfaceScale, "fInterfaceScale", 1.0f);
	return true;
}

float CvScalableInfo::getScale() const
{
	return m_fScale;
}

float CvScalableInfo::getInterfaceScale() const
{
	return m_fInterfaceScale;
}

CvHotkeyInfo::CvHotkeyInfo() :
m_iActionInfoIndex(-1),
m_iHotKeyVal(-1),
m_iHotKeyPriority(-1),
m_iHotKeyValAlt(-1),
m_iHotKeyPriorityAlt(-1),
m_iOrderPriority(-1),
m_bAltDown(false),
m_bShiftDown(false),
m_bCtrlDown(false),
m_bAltDownAlt(false),
m_bShiftDownAlt(false),
m_bCtrlDownAlt(false)
{}

bool CvHotkeyInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML)) // advc.tag
		return false;

	// advc.006b: Default arguments added to GetChildXmlValByName calls

	pXML->GetChildXmlValByName(m_szHotKey, "HotKey", "");
	m_iHotKeyVal = pXML->GetHotKeyInt(m_szHotKey);
	pXML->GetChildXmlValByName(&m_iHotKeyPriority, "iHotKeyPriority",  -1);
	{
		CvString szTextVal;
		if (pXML->GetChildXmlValByName(szTextVal, "HotKeyAlt", ""))
			m_iHotKeyValAlt =  pXML->GetHotKeyInt(szTextVal);
	}
	pXML->GetChildXmlValByName(&m_iHotKeyPriorityAlt, "iHotKeyPriorityAlt", -1);
	pXML->GetChildXmlValByName(&m_bAltDown, "bAltDown", false);
	pXML->GetChildXmlValByName(&m_bShiftDown, "bShiftDown", false);
	pXML->GetChildXmlValByName(&m_bCtrlDown, "bCtrlDown", false);
	pXML->GetChildXmlValByName(&m_bAltDownAlt, "bAltDownAlt", false);
	pXML->GetChildXmlValByName(&m_bShiftDownAlt, "bShiftDownAlt", false);
	pXML->GetChildXmlValByName(&m_bCtrlDownAlt, "bCtrlDownAlt", false);
	pXML->GetChildXmlValByName(&m_iOrderPriority, "iOrderPriority", 5);

	setHotKeyDescription(getTextKeyWide(), NULL,
			hotkeyDescr::hotKeyFromDescription(
			getHotKey(), m_bShiftDown, m_bAltDown, m_bCtrlDown));

	return true;
}
#if ENABLE_XML_FILE_CACHE
void CvHotkeyInfo::read(FDataStreamBase* pStream)
{
	base_t::read(pStream); // advc.tag
	uint uiFlag=0;
	pStream->Read(&uiFlag);

	pStream->Read(&m_iHotKeyVal);
	pStream->Read(&m_iHotKeyPriority);
	pStream->Read(&m_iHotKeyValAlt);
	pStream->Read(&m_iHotKeyPriorityAlt);
	pStream->Read(&m_iOrderPriority);
	pStream->Read(&m_bAltDown);
	pStream->Read(&m_bShiftDown);
	pStream->Read(&m_bCtrlDown);
	pStream->Read(&m_bAltDownAlt);
	pStream->Read(&m_bShiftDownAlt);
	pStream->Read(&m_bCtrlDownAlt);
	pStream->ReadString(m_szHotKey);
	pStream->ReadString(m_szHotKeyDescriptionKey);
	pStream->ReadString(m_szHotKeyAltDescriptionKey);
	pStream->ReadString(m_szHotKeyString);
}

void CvHotkeyInfo::write(FDataStreamBase* pStream)
{
	base_t::write(pStream); // advc.tag
	uint uiFlag = 0;
	pStream->Write(uiFlag);

	pStream->Write(m_iHotKeyVal);
	pStream->Write(m_iHotKeyPriority);
	pStream->Write(m_iHotKeyValAlt);
	pStream->Write(m_iHotKeyPriorityAlt);
	pStream->Write(m_iOrderPriority);
	pStream->Write(m_bAltDown);
	pStream->Write(m_bShiftDown);
	pStream->Write(m_bCtrlDown);
	pStream->Write(m_bAltDownAlt);
	pStream->Write(m_bShiftDownAlt);
	pStream->Write(m_bCtrlDownAlt);
	pStream->WriteString(m_szHotKey);
	pStream->WriteString(m_szHotKeyDescriptionKey);
	pStream->WriteString(m_szHotKeyAltDescriptionKey);
	pStream->WriteString(m_szHotKeyString);
}
#endif

int CvHotkeyInfo::getActionInfoIndex() const
{
	return m_iActionInfoIndex;
}

void CvHotkeyInfo::setActionInfoIndex(int i)
{
	m_iActionInfoIndex = i;
}

int CvHotkeyInfo::getHotKeyVal() const
{
	return m_iHotKeyVal;
}

int CvHotkeyInfo::getHotKeyPriority() const
{
	return m_iHotKeyPriority;
}

int CvHotkeyInfo::getHotKeyValAlt() const
{
	return m_iHotKeyValAlt;
}

int CvHotkeyInfo::getHotKeyPriorityAlt() const
{
	return m_iHotKeyPriorityAlt;
}

int CvHotkeyInfo::getOrderPriority() const
{
	return m_iOrderPriority;
}

bool CvHotkeyInfo::isAltDown() const
{
	return m_bAltDown;
}

bool CvHotkeyInfo::isShiftDown() const
{
	return m_bShiftDown;
}

bool CvHotkeyInfo::isCtrlDown() const
{
	return m_bCtrlDown;
}

bool CvHotkeyInfo::isAltDownAlt() const
{
	return m_bAltDownAlt;
}

bool CvHotkeyInfo::isShiftDownAlt() const
{
	return m_bShiftDownAlt;
}

bool CvHotkeyInfo::isCtrlDownAlt() const
{
	return m_bCtrlDownAlt;
}

const TCHAR* CvHotkeyInfo::getHotKey() const
{
	return m_szHotKey;
}

std::wstring CvHotkeyInfo::getHotKeyDescription() const
{
	CvWString szTemptext;
	if (!m_szHotKeyAltDescriptionKey.empty())
	{
		szTemptext.Format(L"%s (%s)", gDLL->getObjectText(m_szHotKeyAltDescriptionKey, 0).GetCString(),
			gDLL->getObjectText(m_szHotKeyDescriptionKey, 0).GetCString());
	}
	else szTemptext = gDLL->getObjectText(m_szHotKeyDescriptionKey, 0);

	if (!m_szHotKeyString.empty())
		szTemptext += m_szHotKeyString;

	return szTemptext;
}

void CvHotkeyInfo::setHotKeyDescription(const wchar* szHotKeyDescKey,
	const wchar* szHotKeyAltDescKey, const wchar* szHotKeyString)
{
	m_szHotKeyDescriptionKey = szHotKeyDescKey;
	m_szHotKeyAltDescriptionKey = szHotKeyAltDescKey;
	m_szHotKeyString = szHotKeyString;
}

// advc.154:
std::wstring CvHotkeyInfo::getHotKeyShortDesc() const
{
	return hotkeyDescr::hotKeyFromDescription(
			getHotKey(), isShiftDown(), isAltDown(), isCtrlDown());
}

// <advc.tag>
bool CvXMLInfo::read(CvXMLLoadUtility* pXML)
{
	CvInfoBase::read(pXML);

	ElementList elements;
	addElements(elements);
	#ifdef FASSERT_ENABLE
	// Check for accidental duplicates among element IDs and names ...
	/*	Hack to avoid checking more than one instance per derived class
		(to save time): */
	static std::set<std::string> aTypePrefixesChecked;
	std::string sTypePrefix = (getType() == NULL ? "" : getType());
	size_t uiSepPos = sTypePrefix.find("_");
	if (uiSepPos != std::string::npos)
	{
		sTypePrefix = sTypePrefix.substr(0, uiSepPos);
		if (aTypePrefixesChecked.count(sTypePrefix) <= 0)
		{
			aTypePrefixesChecked.insert(sTypePrefix);
			{
				std::set<int> aElementIDs;
				std::set<std::string> aElementNames;
				for (int i = 0; i < elements.numIntElements(); i++)
				{
					int iID = elements.intElementAt(i).getID();
					std::string sName = elements.intElementAt(i).getName();
					FAssert(aElementIDs.count(iID) == 0);
					aElementIDs.insert(iID);
					FAssert(aElementNames.count(sName) == 0);
					aElementNames.insert(sName);
				}
			}
			{
				std::set<int> aElementIDs;
				std::set<std::string> aElementNames;
				for (int i = 0; i < elements.numBoolElements(); i++)
				{
					int iID = elements.boolElementAt(i).getID();
					std::string sName = elements.boolElementAt(i).getName();
					FAssert(aElementIDs.count(iID) == 0);
					aElementIDs.insert(iID);
					FAssert(aElementNames.count(sName) == 0);
					aElementNames.insert(sName);
				}
			}
		}
	}
	#endif
	m_aiData.resize(elements.numIntElements());
	for (int i = 0; i < elements.numIntElements(); i++)
	{
		IntElement const& kElement = elements.intElementAt(i);
		CvString szName = kElement.getName();
		szName.insert(0, "i");
		int iTmp;
		if (kElement.isMandatory())
			pXML->GetChildXmlValByName(&iTmp, szName.GetCString());
		else
		{
			pXML->GetChildXmlValByName(&iTmp, szName.GetCString(),
					kElement.getDefaultValue());
		}
		set((IntElementTypes)kElement.getID(), iTmp);
	}
	m_abData.resize(elements.numBoolElements());
	for (int i = 0; i < elements.numBoolElements(); i++)
	{
		BoolElement const& kElement = elements.boolElementAt(i);
		CvString szName = kElement.getName();
		szName.insert(0, "b");
		bool bTmp;
		if (kElement.isMandatory())
			pXML->GetChildXmlValByName(&bTmp, szName.GetCString());
		else
		{
			pXML->GetChildXmlValByName(&bTmp, szName.GetCString(),
					kElement.getDefaultValue());
		}
		set((BoolElementTypes)kElement.getID(), bTmp);
	}
	return true;
}

#if ENABLE_XML_FILE_CACHE
/*	Will probably never be needed. Cache version flag not implemented.
	(Not sure how I'd go about that.) */
void CvXMLInfo::read(FDataStreamBase* pStream)
{
	CvInfoBase::read(pStream);
	for (size_t i = 0; i < m_aiData.size(); i++)
	{
		short iVal;
		pStream->Read(&iVal);
		m_aiData[i] = iVal;
	}
	for (size_t i = 0; i < m_abData.size(); i++)
	{
		bool bVal;
		pStream->Read(&bVal);
		m_abData[i] = bVal;
	}
}

void CvXMLInfo::write(FDataStreamBase* pStream)
{
	CvInfoBase::write(pStream);
	for (size_t i = 0; i < m_aiData.size(); i++)
	{
		pStream->Write(m_aiData[i]);
	}
	for (size_t i = 0; i < m_abData.size(); i++)
	{
		pStream->Write(m_abData[i]);
	}
}
#endif // </advc.tag>
