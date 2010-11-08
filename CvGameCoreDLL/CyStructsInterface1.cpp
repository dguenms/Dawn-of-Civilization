#include "CvGameCoreDLL.h"
#include "CvUnit.h"
//#include "CvStructs.h"
#include "CvInfos.h"

//
// Python interface for structs
// Exposed directly - no wrapper
// Author - Mustafa Thamer
//

void CyStructsPythonInterface1()
{
	OutputDebugString("Python Extension Module - CyStructsPythonInterface1\n");

	python::class_<NiPoint3>("NiPoint3")
		.def(python::init<float, float, float>())	// ctor which takes 3 floats
		.def_readwrite("x", &NiPoint3::x)
		.def_readwrite("y", &NiPoint3::y)
		.def_readwrite("z", &NiPoint3::z)
		;

	python::class_<NiPoint2>("NiPoint2")
		.def(python::init<float, float>())	// ctor which takes 2 floats
		.def_readwrite("x", &NiPoint2::x)
		.def_readwrite("y", &NiPoint2::y)
		;

	python::class_<NiColorA>("NiColorA")
		.def(python::init<float, float, float, float>())	// ctor which takes 4 floats
		.def_readwrite("r", &NiColorA::r)
		.def_readwrite("g", &NiColorA::g)
		.def_readwrite("b", &NiColorA::b)
		.def_readwrite("a", &NiColorA::a)
		;

	python::class_<POINT>("POINT")
		.def_readwrite("x", &POINT::x)
		.def_readwrite("y", &POINT::y)
		;

	python::class_<XYCoords>("XYCoords")
		.def(python::init<int, int>())	// ctor which takes 2 ints
		.def_readwrite("iX", &XYCoords::iX)
		.def_readwrite("iY", &XYCoords::iY)
		;

	python::class_<IDInfo>("IDInfo")
		.def_readwrite("eOwner", &IDInfo::eOwner)
		.def_readwrite("iID", &IDInfo::iID)
		;

	python::class_<GameTurnInfo>("GameTurnInfo")
		.def_readwrite("iMonthIncrement", &GameTurnInfo::iMonthIncrement)
		.def_readwrite("iNumGameTurnsPerIncrement", &GameTurnInfo::iNumGameTurnsPerIncrement)
		;

	python::class_<OrderData>("OrderData")
		.def_readwrite("eOrderType", &OrderData::eOrderType)
		.def_readwrite("iData1", &OrderData::iData1)
		.def_readwrite("iData2", &OrderData::iData2)
		.def_readwrite("bSave", &OrderData::bSave)
		;

	python::class_<MissionData>("MissionData")
		.def_readwrite("eMissionType", &MissionData::eMissionType)
		.def_readwrite("iData1", &MissionData::iData1)
		.def_readwrite("iData2", &MissionData::iData2)
		.def_readwrite("iFlags", &MissionData::iFlags)
		.def_readwrite("iPushTurn", &MissionData::iPushTurn)
		;

	python::class_<TradeData>("TradeData")
		.def_readwrite("ItemType", &TradeData::m_eItemType)
		.def_readwrite("iData", &TradeData::m_iData)
		.def_readwrite("bOffering", &TradeData::m_bOffering)
		.def_readwrite("bHidden", &TradeData::m_bHidden)
		;

	python::class_<EventTriggeredData>("EventTriggeredData")
		.def_readwrite("iId", &EventTriggeredData::m_iId)
		.def_readwrite("eTrigger", &EventTriggeredData::m_eTrigger)
		.def_readwrite("iTurn", &EventTriggeredData::m_iTurn)
		.def_readwrite("ePlayer", &EventTriggeredData::m_ePlayer)
		.def_readwrite("iCityId", &EventTriggeredData::m_iCityId)
		.def_readwrite("iPlotX", &EventTriggeredData::m_iPlotX)
		.def_readwrite("iPlotY", &EventTriggeredData::m_iPlotY)
		.def_readwrite("iUnitId", &EventTriggeredData::m_iUnitId)
		.def_readwrite("eOtherPlayer", &EventTriggeredData::m_eOtherPlayer)
		.def_readwrite("iOtherPlayerCityId", &EventTriggeredData::m_iOtherPlayerCityId)
		.def_readwrite("eReligion", &EventTriggeredData::m_eReligion)
		.def_readwrite("eCorporation", &EventTriggeredData::m_eCorporation)
		.def_readwrite("eBuilding", &EventTriggeredData::m_eBuilding)
		;

	python::class_<EventMessage>("EventMessage")
		.def_readwrite("iExpirationTurn", &EventMessage::iExpirationTurn)
		.def("getDescription", &EventMessage::getDescription)
		;

	python::class_<FOWVis>("FOWVis")
		.def_readwrite("uiCount", &FOWVis::uiCount)
		.def("getOffsets", &FOWVis::getOffsets)  // array of "Offset" points
		;

	python::class_<PBGameSetupData>("PBGameSetupData")
		.def_readwrite("iSize", &PBGameSetupData::iSize)
		.def_readwrite("iClimate", &PBGameSetupData::iClimate)
		.def_readwrite("iSeaLevel", &PBGameSetupData::iSeaLevel)
		.def_readwrite("iSpeed", &PBGameSetupData::iSpeed)
		.def_readwrite("iEra", &PBGameSetupData::iEra)
		.def_readwrite("iNumCustomMapOptions", &PBGameSetupData::iNumCustomMapOptions)
		.def("getCustomMapOption", &PBGameSetupData::getCustomMapOption)
		.def_readwrite("iNumVictories", &PBGameSetupData::iNumVictories)
		.def("getVictory", &PBGameSetupData::getVictory)
		.def("getMapName", &PBGameSetupData::getMapName)
		.def_readwrite("iMaxTurns", &PBGameSetupData::iMaxTurns)
		.def_readwrite("iCityElimination", &PBGameSetupData::iCityElimination)
		.def_readwrite("iAdvancedStartPoints", &PBGameSetupData::iAdvancedStartPoints)
		.def_readwrite("iTurnTime", &PBGameSetupData::iTurnTime)
		.def("getOptionAt", &PBGameSetupData::getOptionAt)
		.def("getMPOptionAt", &PBGameSetupData::getMPOptionAt)
		;
		
	python::class_<PBPlayerSetupData>("PBPlayerSetupData")
		.def_readwrite("iWho", &PBPlayerSetupData::iWho)
		.def_readwrite("iCiv", &PBPlayerSetupData::iCiv)
		.def_readwrite("iLeader", &PBPlayerSetupData::iLeader)
		.def_readwrite("iTeam", &PBPlayerSetupData::iTeam)
		.def_readwrite("iDifficulty", &PBPlayerSetupData::iDifficulty)
		.def("getStatusText", &PBPlayerSetupData::getStatusText)
		;

	python::class_<PBPlayerAdminData>("PBPlayerAdminData")
		.def("getName", &PBPlayerAdminData::getName)
		.def("getPing", &PBPlayerAdminData::getPing)
		.def("getScore", &PBPlayerAdminData::getScore)
		.def_readwrite("bHuman", &PBPlayerAdminData::bHuman)
		.def_readwrite("bClaimed", &PBPlayerAdminData::bClaimed)
		.def_readwrite("bTurnActive", &PBPlayerAdminData::bTurnActive)
		;
	//Added ST
	python::class_<CombatDetails>("CombatDetails")
		.def_readwrite("iExtraCombatPercent", &CombatDetails::iExtraCombatPercent)
		.def_readwrite("iAnimalCombatModifierTA", &CombatDetails::iAnimalCombatModifierTA)
		.def_readwrite("iAIAnimalCombatModifierTA", &CombatDetails::iAIAnimalCombatModifierTA)
		.def_readwrite("iAnimalCombatModifierAA", &CombatDetails::iAnimalCombatModifierAA)
		.def_readwrite("iAIAnimalCombatModifierAA", &CombatDetails::iAIAnimalCombatModifierAA)
		.def_readwrite("iBarbarianCombatModifierTB", &CombatDetails::iBarbarianCombatModifierTB)
		.def_readwrite("iAIBarbarianCombatModifierTB", &CombatDetails::iAIBarbarianCombatModifierTB)
		.def_readwrite("iBarbarianCombatModifierAB", &CombatDetails::iBarbarianCombatModifierAB)
		.def_readwrite("iAIBarbarianCombatModifierAB", &CombatDetails::iAIBarbarianCombatModifierAB)
		.def_readwrite("iPlotDefenseModifier", &CombatDetails::iPlotDefenseModifier)
		.def_readwrite("iFortifyModifier", &CombatDetails::iFortifyModifier)
		.def_readwrite("iCityDefenseModifier", &CombatDetails::iCityDefenseModifier)
		.def_readwrite("iHillsAttackModifier", &CombatDetails::iHillsAttackModifier)
		.def_readwrite("iHillsDefenseModifier", &CombatDetails::iHillsDefenseModifier)
		.def_readwrite("iFeatureAttackModifier", &CombatDetails::iFeatureAttackModifier)
		.def_readwrite("iFeatureDefenseModifier", &CombatDetails::iFeatureDefenseModifier)
		.def_readwrite("iTerrainAttackModifier", &CombatDetails::iTerrainAttackModifier)
		.def_readwrite("iTerrainDefenseModifier", &CombatDetails::iTerrainDefenseModifier)
		.def_readwrite("iCityAttackModifier", &CombatDetails::iCityAttackModifier)
		.def_readwrite("iDomainDefenseModifier", &CombatDetails::iDomainDefenseModifier)
		.def_readwrite("iCityBarbarianDefenseModifier", &CombatDetails::iCityBarbarianDefenseModifier)
		.def_readwrite("iClassDefenseModifier", &CombatDetails::iClassDefenseModifier)
		.def_readwrite("iClassAttackModifier", &CombatDetails::iClassAttackModifier)
		.def_readwrite("iCombatModifierT", &CombatDetails::iCombatModifierT)
		.def_readwrite("iCombatModifierA", &CombatDetails::iCombatModifierA)
		.def_readwrite("iDomainModifierA", &CombatDetails::iDomainModifierA)
		.def_readwrite("iDomainModifierT", &CombatDetails::iDomainModifierT)
		.def_readwrite("iAnimalCombatModifierA", &CombatDetails::iAnimalCombatModifierA)
		.def_readwrite("iAnimalCombatModifierT", &CombatDetails::iAnimalCombatModifierT)
		.def_readwrite("iRiverAttackModifier", &CombatDetails::iRiverAttackModifier)
		.def_readwrite("iAmphibAttackModifier", &CombatDetails::iAmphibAttackModifier)
		.def_readwrite("iKamikazeModifier", &CombatDetails::iKamikazeModifier)
		.def_readwrite("iModifierTotal", &CombatDetails::iModifierTotal)
		.def_readwrite("iBaseCombatStr", &CombatDetails::iBaseCombatStr)
		.def_readwrite("iCombat", &CombatDetails::iCombat)
		.def_readwrite("iMaxCombatStr", &CombatDetails::iMaxCombatStr)
		.def_readwrite("iCurrHitPoints", &CombatDetails::iCurrHitPoints)
		.def_readwrite("iMaxHitPoints", &CombatDetails::iMaxHitPoints)
		.def_readwrite("iCurrCombatStr", &CombatDetails::iCurrCombatStr)
		.def_readwrite("eOwner", &CombatDetails::eOwner)
		.def_readwrite("eVisualOwner", &CombatDetails::eVisualOwner)
		.def_readwrite("sUnitName", &CombatDetails::sUnitName)
		;
}
