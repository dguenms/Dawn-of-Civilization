// advc.003x: Cut from CvInfos.cpp

#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"


CvYieldInfo::CvYieldInfo() :
m_wcSymbol(0),
m_iHillsChange(0),
m_iPeakChange(0),
m_iLakeChange(0),
m_iCityChange(0),
m_iPopulationChangeOffset(0),
m_iPopulationChangeDivisor(0),
m_iMinCity(0),
m_iTradeModifier(0),
m_iGoldenAgeYield(0),
m_iGoldenAgeYieldThreshold(0),
m_iAIWeightPercent(0),
m_iColorType(NO_COLOR),
m_paszSymbolPath(NULL)
{}

CvYieldInfo::~CvYieldInfo()
{
	//SAFE_DELETE_ARRAY(m_paszSymbolPath); // advc.003j
}

wchar CvYieldInfo::getChar() const
{
	return m_wcSymbol;
}

void CvYieldInfo::setChar(wchar wc)
{
	m_wcSymbol = wc;
}

int CvYieldInfo::getColorType() const
{
	return m_iColorType;
}

const TCHAR* CvYieldInfo::getSymbolPath(int i) const
{
	/*FAssertMsg(i < GC.getDefineINT("MAX_YIELD_STACK"), "Index out of bounds");
	FAssertMsg(i > -1, "Index out of bounds");
	return m_paszSymbolPath ? m_paszSymbolPath[i] : -1;*/
	/*  <advc.003j> This function is never called. The paths were unused, so
		I'm no longer loading them. */
	FErrorMsg("CvYieldInfo::m_paszSymbolPath not loaded (disabled by AdvCiv)");
	return NULL; // </advc.003j>
}

bool CvYieldInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iHillsChange, "iHillsChange");
	pXML->GetChildXmlValByName(&m_iPeakChange, "iPeakChange");
	pXML->GetChildXmlValByName(&m_iLakeChange, "iLakeChange");
	pXML->GetChildXmlValByName(&m_iCityChange, "iCityChange");
	pXML->GetChildXmlValByName(&m_iPopulationChangeOffset, "iPopulationChangeOffset");
	pXML->GetChildXmlValByName(&m_iPopulationChangeDivisor, "iPopulationChangeDivisor");
	pXML->GetChildXmlValByName(&m_iMinCity, "iMinCity");
	pXML->GetChildXmlValByName(&m_iTradeModifier, "iTradeModifier");
	pXML->GetChildXmlValByName(&m_iGoldenAgeYield, "iGoldenAgeYield");
	pXML->GetChildXmlValByName(&m_iGoldenAgeYieldThreshold, "iGoldenAgeYieldThreshold");
	pXML->GetChildXmlValByName(&m_iAIWeightPercent, "iAIWeightPercent");

	pXML->SetInfoIDFromChildXmlVal(m_iColorType, "ColorType");
	// advc.003j: Disabled
	/*if (gDLL->getXMLIFace()->SetToChildByTagName(pXML->GetXML(), "SymbolPaths"))
	{
		if (pXML->SkipToNextVal())
		{
			int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(pXML->GetXML());
			FAssert(GC.getDefineINT("MAX_YIELD_STACK") > 0);
			m_paszSymbolPath = new CvString[GC.getDefineINT("MAX_YIELD_STACK")];
			if (iNumSibs > 0)
			{
				if (pXML->GetChildXmlVal(szTextVal))
				{
					FAssertMsg((iNumSibs <= GC.getDefineINT("MAX_YIELD_STACK")) ,"There are more siblings than memory allocated for them in SetGlobalYieldInfo");
					for (int j = 0; j < iNumSibs; j++)
					{
						m_paszSymbolPath[j] = szTextVal;
						if (!pXML->GetNextXmlVal(szTextVal))
							break;
					}

					gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
				}
			}
		}
		gDLL->getXMLIFace()->SetToParent(pXML->GetXML());
	}*/

	return true;
}

CvCommerceInfo::CvCommerceInfo() :
m_wcSymbol(0),
m_iInitialPercent(0),
m_iInitialHappiness(0),
m_iAIWeightPercent(0),
m_bFlexiblePercent(false)
{}

wchar CvCommerceInfo::getChar() const
{
	return m_wcSymbol;
}

void CvCommerceInfo::setChar(wchar wc)
{
	m_wcSymbol = wc;
}

int CvCommerceInfo::getInitialPercent() const
{
	return m_iInitialPercent;
}

int CvCommerceInfo::getInitialHappiness() const
{
	return m_iInitialHappiness;
}

bool CvCommerceInfo::isFlexiblePercent() const
{
	return m_bFlexiblePercent;
}

bool CvCommerceInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;

	pXML->GetChildXmlValByName(&m_iInitialPercent, "iInitialPercent");
	pXML->GetChildXmlValByName(&m_iInitialHappiness, "iInitialHappiness");
	pXML->GetChildXmlValByName(&m_iAIWeightPercent, "iAIWeightPercent");
	pXML->GetChildXmlValByName(&m_bFlexiblePercent, "bFlexiblePercent");

	return true;
}

const NiColorA& CvColorInfo::getColor() const
{
	return m_Color;
}

bool CvColorInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	float afColorVals[4];
	pXML->GetChildXmlValByName(&afColorVals[0], "fRed");
	pXML->GetChildXmlValByName(&afColorVals[1], "fGreen");
	pXML->GetChildXmlValByName(&afColorVals[2], "fBlue");
	pXML->GetChildXmlValByName(&afColorVals[3], "fAlpha");

	m_Color = NiColorA(afColorVals[0], afColorVals[1], afColorVals[2], afColorVals[3]);

	return true;
}

CvPlayerColorInfo::CvPlayerColorInfo() :
m_eColorTypePrimary(NO_COLOR),
m_eColorTypeSecondary(NO_COLOR),
m_eTextColorType(NO_COLOR)
{}

int CvPlayerColorInfo::getColorTypePrimaryExternal() const
{
	return getColorTypePrimary();
}

int CvPlayerColorInfo::getColorTypeSecondaryExternal() const
{
	return getColorTypeSecondary();
}

ColorTypes CvPlayerColorInfo::getColorTypePrimary() const
{
	return m_eColorTypePrimary;
}

ColorTypes CvPlayerColorInfo::getColorTypeSecondary() const
{
	return m_eColorTypeSecondary;
}

ColorTypes CvPlayerColorInfo::getTextColorType() const
{
	return m_eTextColorType;
}

bool CvPlayerColorInfo::read(CvXMLLoadUtility* pXML)
{
	if (!CvInfoBase::read(pXML))
		return false;

	pXML->SetInfoIDFromChildXmlVal(m_eColorTypePrimary, "ColorTypePrimary");
	pXML->SetInfoIDFromChildXmlVal(m_eColorTypeSecondary, "ColorTypeSecondary");
	pXML->SetInfoIDFromChildXmlVal(m_eTextColorType, "TextColorType");

	return true;
}
