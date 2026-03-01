#pragma once

#ifndef CV_INFO_SYMBOL_H
#define CV_INFO_SYMBOL_H

/*  advc.003x: Cut from CvInfos.h. A few nuts-and-bolts classes to be precompiled:
	CvYieldInfo, CvCommerceInfo, CvColorInfo, CvPlayerColorInfo */
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvYieldInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvYieldInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python
	CvYieldInfo();
	~CvYieldInfo();

	wchar getChar() const; // advc: return wchar (not int)
	void setChar(/* advc: */ wchar wc);
	int getHillsChange() const { return m_iHillsChange; }
	int getPeakChange() const { return m_iPeakChange; }
	int getLakeChange() const { return m_iLakeChange; }
	int getCityChange() const { return m_iCityChange; }
	// advc: These two are unused in XML
	int getPopulationChangeOffset() const { return m_iPopulationChangeOffset; }
	int getPopulationChangeDivisor() const { return m_iPopulationChangeDivisor; }
	int getMinCity() const { return m_iMinCity; }
	int getTradeModifier() const { return m_iTradeModifier; }
	int getGoldenAgeYield() const { return m_iGoldenAgeYield; }
	int getGoldenAgeYieldThreshold() const { return m_iGoldenAgeYieldThreshold; }
	int getAIWeightPercent() const { return m_iAIWeightPercent; }
	int getColorType() const;

	const TCHAR* getSymbolPath(int i) const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	wchar m_wcSymbol;
	int m_iHillsChange;
	int m_iPeakChange;
	int m_iLakeChange;
	int m_iCityChange;
	int m_iPopulationChangeOffset;
	int m_iPopulationChangeDivisor;
	int m_iMinCity;
	int m_iTradeModifier;
	int m_iGoldenAgeYield;
	int m_iGoldenAgeYieldThreshold;
	int m_iAIWeightPercent;
	int m_iColorType;

	CvString* m_paszSymbolPath;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCommerceInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCommerceInfo : public CvInfoBase
{
	typedef CvInfoBase base_t;
public: // All the const functions are exposed to Python

	CvCommerceInfo();

	wchar getChar() const; // advc: return wchar (not int)
	void setChar(/* advc: */ wchar wc);
	int getInitialPercent() const;
	int getInitialHappiness() const;
	int getAIWeightPercent() const { return m_iAIWeightPercent; }

	bool isFlexiblePercent() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	wchar m_wcSymbol; // advc
	int m_iInitialPercent;
	int m_iInitialHappiness;
	int m_iAIWeightPercent;

	bool m_bFlexiblePercent;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvColorInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvColorInfo : public CvInfoBase
{
public:
	DllExport const NiColorA& getColor() const; // Exposed to Python
	bool read(CvXMLLoadUtility* pXML);

protected:
	NiColorA m_Color;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvPlayerColorInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlayerColorInfo : public CvInfoBase
{
public: // The const functions are exposed to Python
	CvPlayerColorInfo();

	// Types changed from int to ColorTypes
	int getColorTypePrimaryExternal() const; // (exported through .def file)
	int getColorTypeSecondaryExternal() const; // (exported through .def file)
	ColorTypes getColorTypePrimary() const;
	ColorTypes getColorTypeSecondary() const;
	ColorTypes getTextColorType() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	ColorTypes m_eColorTypePrimary;
	ColorTypes m_eColorTypeSecondary;
	ColorTypes m_eTextColorType;
};

#endif
