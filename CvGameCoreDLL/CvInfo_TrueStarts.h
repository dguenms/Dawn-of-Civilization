#pragma once

#ifndef CV_INFO_TRUE_STARTS_H
#define CV_INFO_TRUE_STARTS_H

/*	advc.tsl: Storage classes for XML data used by the True Starts option.
	Not exposed to Python. */


class CvTruCivInfo : public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addMandatoryInt(LatitudeTimes10, "LatitudeTimes10");
		kElements.addMandatoryInt(LongitudeTimes10, "LongitudeTimes10");
		kElements.addInt(Precipitation, "Precipitation", -1);
		kElements.addInt(ClimateVariation, "ClimateVariation", -1);
		kElements.addInt(Oceanity, "Oceanity", -1);
		kElements.addInt(MajorRiverWeight, "MajorRiverWeight", -25);
		kElements.addInt(MaxElevation, "MaxElevation", MIN_INT);
		kElements.addInt(MountainousArea, "MountainousArea", -1);
		kElements.addInt(TotalArea, "TotalArea", -1);
		kElements.addInt(HStretch, "HStretch", -1);
		kElements.addInt(Bias, "Bias");
	}
public:
	enum IntElementTypes
	{
		LatitudeTimes10 = base_t::NUM_INT_ELEMENT_TYPES,
		LongitudeTimes10,
		Precipitation,
		ClimateVariation,
		Oceanity,
		MajorRiverWeight,
		MaxElevation,
		MountainousArea,
		TotalArea,
		HStretch,
		Bias,
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	}
	CvTruCivInfo() : m_eCiv(NO_CIVILIZATION), m_eGeoRegion(NO_ARTSTYLE) {}
	CivilizationTypes getCiv() const { return m_eCiv; }
	ArtStyleTypes getGeoRegion() const { return m_eGeoRegion; }
	bool read(CvXMLLoadUtility* pXML);

	static int minLatitude() { return -900; }
	static int maxLatitude() { return 900; }
	static int minLongitude() { return -1800; }
	static int maxLongitude() { return 1800; }

protected:
	CivilizationTypes m_eCiv;
	ArtStyleTypes m_eGeoRegion;
};


class CvTruLeaderInfo : public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addInt(StartOfReign, "StartOfReign", MIN_INT);
		kElements.addInt(Bias, "Bias");
	}
public:
	enum IntElementTypes
	{
		StartOfReign = base_t::NUM_INT_ELEMENT_TYPES,
		Bias,
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	}
	CvTruLeaderInfo() : m_eLeader(NO_LEADER) {}
	LeaderHeadTypes getLeader() const { return m_eLeader; }
	bool read(CvXMLLoadUtility* pXML);

protected:
	LeaderHeadTypes m_eLeader;
};


class CvTruBonusInfo : public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addBool(LandOnly, "LandOnly", false);
	}
public:
	enum BoolElementTypes
	{
		LandOnly = base_t::NUM_BOOL_ELEMENT_TYPES,
		NUM_BOOL_ELEMENT_TYPES
	};
	int get(BoolElementTypes e) const
	{
		return base_t::get(static_cast<base_t::BoolElementTypes>(e));
	}
	CvTruBonusInfo() : m_eBonus(NO_BONUS) {}
	BonusTypes getBonus() const { return m_eBonus; }
	DEF_INFO_ENUM2ENUM_MAP_DEFAULT(RegionDiscouragedUntil, ArtStyle, Era, ArrayEnumMap, (EraTypes)0);
	DEF_INFO_ENUM2ENUM_MAP_DEFAULT(CivDiscouragedUntil, Civilization, Era, ArrayEnumMap, (EraTypes)0);
	DEF_INFO_ENUM2ENUM_MAP_DEFAULT(CivEncouragedUntil, Civilization, Era, ArrayEnumMap, (EraTypes)0);
	bool read(CvXMLLoadUtility* pXML);

protected:
	BonusTypes m_eBonus;
};

#endif
