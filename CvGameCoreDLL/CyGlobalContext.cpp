//
// Python wrapper class for global vars and fxns
// Author - Mustafa Thamer
//

#include "CvGameCoreDLL.h"
#include "CvInfo_GameOption.h"
#include "CvInfo_Misc.h"
#include "CvGamePlay.h"
#include "CyGame.h"
#include "CyPlayer.h"
#include "CyMap.h"
#include "CyTeam.h"
#include "CyArtFileMgr.h"

CyGlobalContext::CyGlobalContext() :
	kGlobals(CvGlobals::getInstance()) // advc.003t
{}

CyGlobalContext::~CyGlobalContext()
{}

CyGlobalContext& CyGlobalContext::getInstance()
{
	static CyGlobalContext globalContext;
	return globalContext;
}

bool CyGlobalContext::isDebugBuild() const
{
#ifdef _DEBUG
	return true;
#else
	return false;
#endif
}

CyGame* CyGlobalContext::getCyGame() const
{
	static CyGame cyGame(GC.getGame());
	return &cyGame;
}


CyMap* CyGlobalContext::getCyMap() const
{
	static CyMap cyMap(GC.getMap());
	return &cyMap;
}


CyPlayer* CyGlobalContext::getCyPlayer(int idx)
{
	static CyPlayer cyPlayers[MAX_PLAYERS];
	static bool bInit=false;

	if (!bInit)
	{
		int i;
		for(i=0;i<MAX_PLAYERS;i++)
			cyPlayers[i]=CyPlayer(&GET_PLAYER((PlayerTypes)i));
		bInit=true;
	}

	FAssert(idx>=0);
	FAssert(idx<MAX_PLAYERS);

	return idx < MAX_PLAYERS && idx != NO_PLAYER ? &cyPlayers[idx] : NULL;
}


CyPlayer* CyGlobalContext::getCyActivePlayer()
{
	PlayerTypes ePlayer = GC.getGame().getActivePlayer();
	return ePlayer != NO_PLAYER ? getCyPlayer(ePlayer) : NULL;
}


CvRandom& CyGlobalContext::getCyASyncRand() const
{
	return GC.getASyncRand();
}

CyTeam* CyGlobalContext::getCyTeam(int i)
{
	static CyTeam cyTeams[MAX_TEAMS];
	static bool bInit=false;

	if (!bInit)
	{
		int j;
		for(j=0;j<MAX_TEAMS;j++)
		{
			cyTeams[j]=CyTeam(&GET_TEAM((TeamTypes)j));
		}
		bInit = true;
	}

	return i<MAX_TEAMS ? &cyTeams[i] : NULL;
}
// <kekm.27> (advc)
bool CyGlobalContext::isLogging() {

	return GC.isLogging();
}

bool CyGlobalContext::isRandLogging() {

	return GC.isRandLogging();
} // </kekm.27>

CvEffectInfo* CyGlobalContext::getEffectInfo(int /*EffectTypes*/ i) const
{
	return (i>=0 && i<GC.getNumEffectInfos()) ? &GC.getInfo((EffectTypes)i) : NULL;
}

CvTerrainInfo* CyGlobalContext::getTerrainInfo(int /*TerrainTypes*/ i) const
{
	return (i>=0 && i<GC.getNumTerrainInfos()) ? &GC.getInfo((TerrainTypes)i) : NULL;
}

CvBonusClassInfo* CyGlobalContext::getBonusClassInfo(int /*BonusClassTypes*/ i) const
{
	return (i > 0 && i < GC.getNumBonusClassInfos() ? &GC.getInfo((BonusClassTypes)i) : NULL);
}


CvBonusInfo* CyGlobalContext::getBonusInfo(int /*(BonusTypes)*/ i) const
{
	return (i>=0 && i<GC.getNumBonusInfos()) ? &GC.getInfo((BonusTypes)i) : NULL;
}

CvFeatureInfo* CyGlobalContext::getFeatureInfo(int i) const
{
	return (i>=0 && i<GC.getNumFeatureInfos()) ? &GC.getInfo((FeatureTypes)i) : NULL;
}

CvCivilizationInfo* CyGlobalContext::getCivilizationInfo(int i) const
{
	return (i>=0 && i<GC.getNumCivilizationInfos()) ? &GC.getInfo((CivilizationTypes)i) : NULL;
}


CvLeaderHeadInfo* CyGlobalContext::getLeaderHeadInfo(int i) const
{
	return (i>=0 && i<GC.getNumLeaderHeadInfos()) ? &GC.getInfo((LeaderHeadTypes)i) : NULL;
}


CvTraitInfo* CyGlobalContext::getTraitInfo(int i) const
{
	return (i>=0 && i<GC.getNumTraitInfos()) ? &GC.getInfo((TraitTypes)i) : NULL;
}


CvUnitInfo* CyGlobalContext::getUnitInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitInfos()) ? &GC.getInfo((UnitTypes)i) : NULL;
}

CvSpecialUnitInfo* CyGlobalContext::getSpecialUnitInfo(int i) const
{
	return (i>=0 && i<GC.getNumSpecialUnitInfos()) ? &GC.getInfo((SpecialUnitTypes)i) : NULL;
}

CvYieldInfo* CyGlobalContext::getYieldInfo(int i) const
{
	return (i>=0 && i<NUM_YIELD_TYPES) ? &GC.getInfo((YieldTypes)i) : NULL;
}


CvCommerceInfo* CyGlobalContext::getCommerceInfo(int i) const
{
	return (i>=0 && i<NUM_COMMERCE_TYPES) ? &GC.getInfo((CommerceTypes)i) : NULL;
}


CvRouteInfo* CyGlobalContext::getRouteInfo(int i) const
{
	return (i>=0 && i<GC.getNumRouteInfos()) ? &GC.getInfo((RouteTypes)i) : NULL;
}


CvImprovementInfo* CyGlobalContext::getImprovementInfo(int i) const
{
	return (i>=0 && i<GC.getNumImprovementInfos()) ? &GC.getInfo((ImprovementTypes)i) : NULL;
}


CvGoodyInfo* CyGlobalContext::getGoodyInfo(int i) const
{
	return (i>=0 && i<GC.getNumGoodyInfos()) ? &GC.getInfo((GoodyTypes)i) : NULL;
}


CvBuildInfo* CyGlobalContext::getBuildInfo(int i) const
{
	return (i>=0 && i<GC.getNumBuildInfos()) ? &GC.getInfo((BuildTypes)i) : NULL;
}


CvHandicapInfo* CyGlobalContext::getHandicapInfo(int i) const
{
	return (i>=0 && i<GC.getNumHandicapInfos()) ? &GC.getInfo((HandicapTypes)i) : NULL;
}


CvBuildingClassInfo* CyGlobalContext::getBuildingClassInfo(int i) const
{
	return (i>=0 && i<GC.getNumBuildingClassInfos()) ? &GC.getInfo((BuildingClassTypes)i) : NULL;
}


CvBuildingInfo* CyGlobalContext::getBuildingInfo(int i) const
{
	return (i>=0 && i<GC.getNumBuildingInfos()) ? &GC.getInfo((BuildingTypes)i) : NULL;
}

CvUnitClassInfo* CyGlobalContext::getUnitClassInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitClassInfos()) ? &GC.getInfo((UnitClassTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getUnitCombatInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitCombatInfos()) ? &GC.getInfo((UnitCombatTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getDomainInfo(int i) const
{
	return (i>=0 && i<NUM_DOMAIN_TYPES) ? &GC.getInfo((DomainTypes)i) : NULL;
}


CvActionInfo* CyGlobalContext::getActionInfo(int i) const
{
	return (i>=0 && i<GC.getNumActionInfos()) ? &GC.getActionInfo(i) : NULL;
}

CvAutomateInfo* CyGlobalContext::getAutomateInfo(int i) const
{
	return (i>=0 && i<NUM_AUTOMATE_TYPES) ? &GC.getInfo((AutomateTypes)i) : NULL;
}

CvCommandInfo* CyGlobalContext::getCommandInfo(int i) const
{
	return (i>=0 && i<NUM_COMMAND_TYPES) ? &GC.getInfo((CommandTypes)i) : NULL;
}

CvControlInfo* CyGlobalContext::getControlInfo(int i) const
{
	return (i>=0 && i<NUM_CONTROL_TYPES) ? &GC.getInfo((ControlTypes)i) : NULL;
}

CvMissionInfo* CyGlobalContext::getMissionInfo(int i) const
{
	return (i>=0 && i<NUM_MISSION_TYPES) ? &GC.getInfo((MissionTypes)i) : NULL;
}

CvPromotionInfo* CyGlobalContext::getPromotionInfo(int i) const
{
	return (i>=0 && i<GC.getNumPromotionInfos()) ? &GC.getInfo((PromotionTypes)i) : NULL;
}


CvTechInfo* CyGlobalContext::getTechInfo(int i) const
{
	return (i>=0 && i<GC.getNumTechInfos()) ? &GC.getInfo((TechTypes)i) : NULL;
}


CvSpecialBuildingInfo* CyGlobalContext::getSpecialBuildingInfo(int i) const
{
	return (i>=0 && i<GC.getNumSpecialBuildingInfos()) ? &GC.getInfo((SpecialBuildingTypes) i) : NULL;
}


CvReligionInfo* CyGlobalContext::getReligionInfo(int i) const
{
	return (i>=0 && i<GC.getNumReligionInfos()) ? &GC.getInfo((ReligionTypes) i) : NULL;
}


CvInfoBase* CyGlobalContext::getPaganReligionInfo(int i) const
{
	return (i >= 0 && i < GC.getNumPaganReligionInfos()) ? &GC.getPaganReligionInfo((PaganReligionTypes)i) : NULL;
}


CvCorporationInfo* CyGlobalContext::getCorporationInfo(int i) const
{
	return (i>=0 && i<GC.getNumCorporationInfos()) ? &GC.getInfo((CorporationTypes) i) : NULL;
}


CvSpecialistInfo* CyGlobalContext::getSpecialistInfo(int i) const
{
	return (i>=0 && i<GC.getNumSpecialistInfos()) ? &GC.getInfo((SpecialistTypes) i) : NULL;
}


CvCivicOptionInfo* CyGlobalContext::getCivicOptionInfo(int i) const
{
	return &GC.getInfo((CivicOptionTypes)i);
}


CvCivicInfo* CyGlobalContext::getCivicInfo(int i) const
{
	return &GC.getInfo((CivicTypes)i);
}

CvDiplomacyInfo* CyGlobalContext::getDiplomacyInfo(int i) const
{
	return &GC.getDiplomacyInfo(i);
}

CvHurryInfo* CyGlobalContext::getHurryInfo(int i) const
{
	return (i>=0 && i<GC.getNumHurryInfos()) ? &GC.getInfo((HurryTypes)i) : NULL;
}


CvProjectInfo* CyGlobalContext::getProjectInfo(int i) const
{
	return (i>=0 && i<GC.getNumProjectInfos()) ? &GC.getInfo((ProjectTypes)i) : NULL;
}


CvVoteInfo* CyGlobalContext::getVoteInfo(int i) const
{
	return (i>=0 && i<GC.getNumVoteInfos()) ? &GC.getInfo((VoteTypes)i) : NULL;
}


CvProcessInfo* CyGlobalContext::getProcessInfo(int i) const
{
	return (i>=0 && i<GC.getNumProcessInfos()) ? &GC.getInfo((ProcessTypes)i) : NULL;
}

CvAnimationPathInfo* CyGlobalContext::getAnimationPathInfo(int i) const
{
	return (i>=0 && i<NUM_ANIMATIONPATH_TYPES) ? &GC.getInfo((AnimationPathTypes)i) : NULL;
}


CvEmphasizeInfo* CyGlobalContext::getEmphasizeInfo(int i) const
{
	return (i>=0 && i<GC.getNumEmphasizeInfos()) ? &GC.getInfo((EmphasizeTypes)i) : NULL;
}


CvCultureLevelInfo* CyGlobalContext::getCultureLevelInfo(int i) const
{
	return (i>=0 && i<GC.getNumCultureLevelInfos()) ? &GC.getInfo((CultureLevelTypes)i) : NULL;
}


CvUpkeepInfo* CyGlobalContext::getUpkeepInfo(int i) const
{
	return (i>=0 && i<GC.getNumUpkeepInfos()) ? &GC.getInfo((UpkeepTypes)i) : NULL;
}


CvVictoryInfo* CyGlobalContext::getVictoryInfo(int i) const
{
	return (i>=0 && i<GC.getNumVictoryInfos()) ? &GC.getInfo((VictoryTypes)i) : NULL;
}


CvEraInfo* CyGlobalContext::getEraInfo(int i) const
{
	return (i>=0 && i<GC.getNumEraInfos()) ? &GC.getInfo((EraTypes)i) : NULL;
}


CvWorldInfo* CyGlobalContext::getWorldInfo(int i) const
{
	return (i>=0 && i<GC.getNumWorldInfos()) ? &GC.getInfo((WorldSizeTypes)i) : NULL;
}


CvClimateInfo* CyGlobalContext::getClimateInfo(int i) const
{
	return (i>=0 && i<GC.getNumClimateInfos()) ? &GC.getInfo((ClimateTypes)i) : NULL;
}


CvSeaLevelInfo* CyGlobalContext::getSeaLevelInfo(int i) const
{
	return (i>=0 && i<GC.getNumSeaLevelInfos()) ? &GC.getInfo((SeaLevelTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getUnitAIInfo(int i) const
{
	return (i>=0 && i<NUM_UNITAI_TYPES) ? &GC.getInfo((UnitAITypes)i) : NULL;
}


CvColorInfo* CyGlobalContext::getColorInfo(int i) const
{
	return (i>=0 && i<GC.getNumColorInfos()) ? &GC.getInfo((ColorTypes)i) : NULL;
}


int CyGlobalContext::getInfoTypeForString(const char* szInfoType) const
{
	return GC.getInfoTypeForString(szInfoType, /* advc.006: */ false, true);
}


int CyGlobalContext::getTypesEnum(const char* szType) const
{
	return GC.getTypesEnum(szType, /* advc.006: */ false, true);
}


CvPlayerColorInfo* CyGlobalContext::getPlayerColorInfo(int i) const
{
	return (i>=0 && i<GC.getNumPlayerColorInfos()) ? &GC.getInfo((PlayerColorTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getHints(int i) const
{
	return ((i >= 0 && i < GC.getNumHintInfos()) ? &GC.getHintInfo(i) : NULL);
}


CvMainMenuInfo* CyGlobalContext::getMainMenus(int i) const
{
	return ((i >= 0 && i < GC.getNumMainMenuInfos()) ? &GC.getMainMenuInfo(i) : NULL);
}


CvVoteSourceInfo* CyGlobalContext::getVoteSourceInfo(int i) const
{
	return ((i >= 0 && i < GC.getNumVoteSourceInfos()) ? &GC.getInfo((VoteSourceTypes)i) : NULL);
}


CvInfoBase* CyGlobalContext::getInvisibleInfo(int i) const
{
	return ((i >= 0 && i < GC.getNumInvisibleInfos()) ? &GC.getInfo((InvisibleTypes)i) : NULL);
}


CvInfoBase* CyGlobalContext::getAttitudeInfo(int i) const
{
	return (i>=0 && i<NUM_ATTITUDE_TYPES) ? &GC.getAttitudeInfo((AttitudeTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getMemoryInfo(int i) const
{
	return (i>=0 && i<NUM_MEMORY_TYPES) ? &GC.getMemoryInfo((MemoryTypes)i) : NULL;
}


CvPlayerOptionInfo* CyGlobalContext::getPlayerOptionsInfoByIndex(int i) const
{
	return &GC.getInfo((PlayerOptionTypes)i);
}

// <advc>
bool CyGlobalContext::IsGraphicsInitialized() const {

	return GC.IsGraphicsInitialized();
} // </advc>


CvGraphicOptionInfo* CyGlobalContext::getGraphicOptionsInfoByIndex(int i) const
{
	return &GC.getInfo((GraphicOptionTypes) i);
}


CvInfoBase* CyGlobalContext::getConceptInfo(int i) const
{
	return (i>=0 && i<GC.getNumConceptInfos()) ? &GC.getInfo((ConceptTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getNewConceptInfo(int i) const
{
	return (i>=0 && i<GC.getNumNewConceptInfos()) ? &GC.getInfo((NewConceptTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getCityTabInfo(int i) const
{
	return (i>=0 && i<NUM_CITYTAB_TYPES) ? &GC.getInfo((CityTabTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getCalendarInfo(int i) const
{
	return (i>=0 && i<NUM_CALENDAR_TYPES) ? &GC.getInfo((CalendarTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getGameOptionInfo(int i) const
{
	return (i>=0 && i<NUM_GAMEOPTION_TYPES) ? &GC.getInfo((GameOptionTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getMPOptionInfo(int i) const
{
	return (i>=0 && i<NUM_MPOPTION_TYPES) ? &GC.getInfo((MultiplayerOptionTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getForceControlInfo(int i) const
{
	return (i>=0 && i<NUM_FORCECONTROL_TYPES) ? &GC.getInfo((ForceControlTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getSeasonInfo(int i) const
{
	return (i>=0 && i<GC.getNumSeasonInfos()) ? &GC.getInfo((SeasonTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getMonthInfo(int i) const
{
	return (i>=0 && i<GC.getNumMonthInfos()) ? &GC.getInfo((MonthTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getDenialInfo(int i) const
{
	return (i>=0 && i<NUM_DENIAL_TYPES) ? &GC.getInfo((DenialTypes)i) : NULL;
}

// advc.003j:
/*CvQuestInfo* CyGlobalContext::getQuestInfo(int i) const
{
	return (i>=0 && i<GC.getNumQuestInfos()) ? &GC.getQuestInfo(i) : NULL;
}*/


CvTutorialInfo* CyGlobalContext::getTutorialInfo(int i) const
{
	return (i>=0 && i<GC.getNumTutorialInfos()) ? &GC.getTutorialInfo(i) : NULL;
}


CvEventTriggerInfo* CyGlobalContext::getEventTriggerInfo(int i) const
{
	return (i>=0 && i<GC.getNumEventTriggerInfos()) ? &GC.getInfo((EventTriggerTypes)i) : NULL;
}


CvEventInfo* CyGlobalContext::getEventInfo(int i) const
{
	return (i>=0 && i<GC.getNumEventInfos()) ? &GC.getInfo((EventTypes)i) : NULL;
}


CvEspionageMissionInfo* CyGlobalContext::getEspionageMissionInfo(int i) const
{
	return (i>=0 && i<GC.getNumEspionageMissionInfos()) ? &GC.getInfo((EspionageMissionTypes)i) : NULL;
}


CvUnitArtStyleInfo* CyGlobalContext::getUnitArtStyleTypeInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitArtStyleInfos()) ? &GC.getInfo((UnitArtStyleTypes)i) : NULL;
}


CvArtInfoInterface* CyGlobalContext::getInterfaceArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumInterfaceArtInfos()) ? &ARTFILEMGR.getInterfaceArtInfo(i) : NULL;
}


CvArtInfoMovie* CyGlobalContext::getMovieArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumMovieArtInfos()) ? &ARTFILEMGR.getMovieArtInfo(i) : NULL;
}


CvArtInfoMisc* CyGlobalContext::getMiscArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumMiscArtInfos()) ? &ARTFILEMGR.getMiscArtInfo(i) : NULL;
}


CvArtInfoUnit* CyGlobalContext::getUnitArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumUnitArtInfos()) ? &ARTFILEMGR.getUnitArtInfo(i) : NULL;
}


CvArtInfoBuilding* CyGlobalContext::getBuildingArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumBuildingArtInfos()) ? &ARTFILEMGR.getBuildingArtInfo(i) : NULL;
}


CvArtInfoCivilization* CyGlobalContext::getCivilizationArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumCivilizationArtInfos()) ? &ARTFILEMGR.getCivilizationArtInfo(i) : NULL;
}


CvArtInfoLeaderhead* CyGlobalContext::getLeaderheadArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumLeaderheadArtInfos()) ? &ARTFILEMGR.getLeaderheadArtInfo(i) : NULL;
}


CvArtInfoBonus* CyGlobalContext::getBonusArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumBonusArtInfos()) ? &ARTFILEMGR.getBonusArtInfo(i) : NULL;
}


CvArtInfoImprovement* CyGlobalContext::getImprovementArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumImprovementArtInfos()) ? &ARTFILEMGR.getImprovementArtInfo(i) : NULL;
}


CvArtInfoTerrain* CyGlobalContext::getTerrainArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumTerrainArtInfos()) ? &ARTFILEMGR.getTerrainArtInfo(i) : NULL;
}


CvArtInfoFeature* CyGlobalContext::getFeatureArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumFeatureArtInfos()) ? &ARTFILEMGR.getFeatureArtInfo(i) : NULL;
}


CvGameSpeedInfo* CyGlobalContext::getGameSpeedInfo(int i) const
{
	return &(GC.getInfo((GameSpeedTypes)i));
}

CvTurnTimerInfo* CyGlobalContext::getTurnTimerInfo(int i) const
{
	return &(GC.getInfo((TurnTimerTypes)i));
}
