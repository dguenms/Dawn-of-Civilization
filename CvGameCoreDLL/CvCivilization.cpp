// advc.003w: New class; see header file.

#include "CvGameCoreDLL.h"
#include "CvCivilization.h"
#include "CvInfo_Building.h"


CvCivilization::CvCivilization(CvCivilizationInfo const& kInfo) : m_kInfo(kInfo)
{
	m_buildings.reserve(GC.getNumBuildingClassInfos());
	for (int i = 0; i < GC.getNumBuildingClassInfos(); i++)
	{
		BuildingClassTypes eBuildingClass = (BuildingClassTypes)i;
		BuildingTypes eBuilding = getBuilding(eBuildingClass);
		if (eBuilding != NO_BUILDING)
		{
			m_buildings.push_back(eBuilding);
			if (eBuilding != GC.getInfo(eBuildingClass).getDefaultBuilding())
				m_uniqueBuildings.push_back(eBuilding);
		}
	}
	m_units.reserve(GC.getNumUnitClassInfos());
	for (int i = 0; i < GC.getNumUnitClassInfos(); i++)
	{
		UnitClassTypes eUnitClass = (UnitClassTypes)i;
		UnitTypes eUnit = getUnit(eUnitClass);
		if (eUnit != NO_UNIT)
		{
			m_units.push_back(eUnit);
			if (eUnit != GC.getInfo(eUnitClass).getDefaultUnit())
				m_uniqueUnits.push_back(eUnit);
		}
	}
}

BuildingTypes CvCivilization::getBuilding(BuildingClassTypes eBuildingClass) const
{
	if (eBuildingClass == NO_BUILDINGCLASS)
		return NO_BUILDING;
	return m_kInfo.getCivilizationBuildings(eBuildingClass);
}

UnitTypes CvCivilization::getUnit(UnitClassTypes eUnitClass) const
{
	if (eUnitClass == NO_UNITCLASS)
		return NO_UNIT;
	return m_kInfo.getCivilizationUnits(eUnitClass);
}

bool CvCivilization::isUnique(BuildingTypes eBuilding) const
{
	return (std::find(m_uniqueBuildings.begin(), m_uniqueBuildings.end(),
			eBuilding) != m_uniqueBuildings.end());
}

bool CvCivilization::isUnique(UnitTypes eUnit) const
{
	return (std::find(m_uniqueUnits.begin(), m_uniqueUnits.end(),
			eUnit) != m_uniqueUnits.end());
}

bool CvCivilization::isFreeBuilding(BuildingClassTypes eBuildingClass) const
{
	return m_kInfo.isCivilizationFreeBuildingClass(eBuildingClass);
}

int CvCivilization::getNumFreeUnits(UnitClassTypes eUnitClass) const
{
	return m_kInfo.getCivilizationFreeUnitsClass(eUnitClass);
}

CivicTypes CvCivilization::getInitialCivic(CivicOptionTypes eCivicOption) const
{
	return (CivicTypes)m_kInfo.getCivilizationInitialCivics(eCivicOption);
}

BuildingClassTypes CvCivilization::buildingClass(BuildingTypes eBuilding)
{
	if (eBuilding == NO_BUILDING)
		return NO_BUILDINGCLASS;
	return GC.getInfo(eBuilding).getBuildingClassType();
}

UnitClassTypes CvCivilization::unitClass(UnitTypes eUnit)
{
	if (eUnit == NO_UNIT)
		return NO_UNITCLASS;
	return GC.getInfo(eUnit).getUnitClassType();
}
