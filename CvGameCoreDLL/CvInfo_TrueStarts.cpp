// advc.tsl: New implementation file; see comments in header.

#include "CvGameCoreDLL.h"
#include "CvInfo_TrueStarts.h"
#include "CvXMLLoadUtility.h"
#include "CvInfo_Terrain.h"

bool CvTruCivInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;
	FAssertBounds(minLatitude(), maxLatitude() + 1, get(CvTruCivInfo::LatitudeTimes10));
	FAssertBounds(minLongitude(), maxLongitude() + 1 , get(CvTruCivInfo::LongitudeTimes10));
	FAssertBounds(-1, 20000, get(CvTruCivInfo::Precipitation));
	FAssertBounds(-1, 101, get(CvTruCivInfo::ClimateVariation));
	FAssertBounds(-1, 101, get(CvTruCivInfo::Oceanity));
	FAssertBounds(-100, 101, get(CvTruCivInfo::MajorRiverWeight));
	// (Can't really catch issues with values in feet here)
	FAssert(get(CvTruCivInfo::MaxElevation) < 25000 &&
			(get(CvTruCivInfo::MaxElevation) == MIN_INT ||
			get(CvTruCivInfo::MaxElevation) > -500));
	FAssertBounds(-1, 101, get(CvTruCivInfo::MountainousArea));
	FAssertBounds(-1, 50000, get(CvTruCivInfo::TotalArea));
	FAssertBounds(-1, 1000, get(CvTruCivInfo::HStretch));
	{
		CvString szTextVal;
		pXML->GetChildXmlValByName(szTextVal, "CivilizationType");
		m_eCiv = (CivilizationTypes)GC.getInfoTypeForString(szTextVal);
		pXML->GetChildXmlValByName(szTextVal, "GeoRegion", "");
		m_eGeoRegion = (ArtStyleTypes)GC.getTypesEnum(szTextVal);
	}
	return true;
}


bool CvTruLeaderInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;
	CvString szTextVal;
	pXML->GetChildXmlValByName(szTextVal, "LeaderType");
	m_eLeader = (LeaderHeadTypes)GC.getInfoTypeForString(szTextVal);
	return true;
}


bool CvTruBonusInfo::read(CvXMLLoadUtility* pXML)
{
	if (!base_t::read(pXML))
		return false;
	{
		CvString szTextVal;
		pXML->GetChildXmlValByName(szTextVal, "BonusType");
		m_eBonus = (BonusTypes)GC.getInfoTypeForString(szTextVal);
	}
	#ifdef FASSERT_ENABLE
	if (get(CvTruBonusInfo::LandOnly))
	{	// Only makes sense when the bonus resource can appear on water and land
		bool bWaterFound = false;
		bool bLandFound = false;
		FOR_EACH_ENUM(Terrain)
		{
			if (!GC.getInfo(eLoopTerrain).isGraphicalOnly() &&
				GC.getInfo(getBonus()).isTerrain(eLoopTerrain))
			{
				if (!bWaterFound)
					bWaterFound = GC.getInfo(eLoopTerrain).isWater();
				if (!bLandFound)
					bLandFound = !GC.getInfo(eLoopTerrain).isWater();
			}
		}
		FAssert(bWaterFound && bLandFound);
	}
	#endif
	pXML->SetVariableListTagPair(RegionDiscouragedUntil(), "DiscouragedRegions");
	pXML->SetVariableListTagPair(CivDiscouragedUntil(), "DiscouragedCivs");
	pXML->SetVariableListTagPair(CivEncouragedUntil(), "EncouragedCivs");
	return true;
}
