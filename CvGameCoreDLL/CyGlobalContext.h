#pragma once

#ifndef CyGlobalContext_h
#define CyGlobalContext_h

//
// Python wrapper class for global vars and fxns
// Passed to Python
//

#include "CvGlobals.h"
#include "CvArtFileMgr.h"
// doc: advciv does not need these includes so perhaps something is missing
#include "CvInfo_Building.h"
#include "CvInfo_Civics.h"
#include "CvInfo_City.h"

class CyGame;
class CyMap;
class CyPlayer;
class CvRandom;
class CyEngine;
class CyTeam;
class CyArtFileMgr;
class CyUserProfile;
class CyVariableSystem;

class CyGlobalContext
{
public:
	CyGlobalContext();
	virtual ~CyGlobalContext();

	static CyGlobalContext& getInstance();		// singleton accessor

	bool isDebugBuild() const;
	CyGame* getCyGame() const;
	CyMap* getCyMap() const;
	CyPlayer* getCyPlayer(int idx);
	CyPlayer* getCyActivePlayer();
	CvRandom& getCyASyncRand() const;
	CyTeam* getCyTeam(int i);
	CyArtFileMgr* getCyArtFileMgr() const;
	// <kekm.27>
	bool isLogging();
	bool isRandLogging();
	// </kekm.27>
	CvEffectInfo* getEffectInfo(int i) const;
	CvTerrainInfo* getTerrainInfo(int i) const;
	CvBonusClassInfo* getBonusClassInfo(int i) const;
	CvBonusInfo* getBonusInfo(int i) const;
	CvFeatureInfo* getFeatureInfo(int i) const;
	CvCivilizationInfo* getCivilizationInfo(int idx) const;
	CvLeaderHeadInfo* getLeaderHeadInfo(int i) const;
	CvTraitInfo* getTraitInfo(int i) const;
	CvUnitInfo* getUnitInfo(int i) const;
	CvSpecialUnitInfo* getSpecialUnitInfo(int i) const;
	CvYieldInfo* getYieldInfo(int i) const;
	CvCommerceInfo* getCommerceInfo(int i) const;
	CvRouteInfo* getRouteInfo(int i) const;
	CvImprovementInfo* getImprovementInfo(int i) const;
	CvGoodyInfo* getGoodyInfo(int i) const;
	CvBuildInfo* getBuildInfo(int i) const;
	CvHandicapInfo* getHandicapInfo(int i) const;
	CvGameSpeedInfo* getGameSpeedInfo(int i) const;
	CvTurnTimerInfo* getTurnTimerInfo(int i) const;
	CvBuildingClassInfo* getBuildingClassInfo(int i) const;
	CvMissionInfo* getMissionInfo(int i) const;
	CvCommandInfo* getCommandInfo(int i) const;
	CvAutomateInfo* getAutomateInfo(int i) const;
	CvActionInfo* getActionInfo(int i) const;
	CvUnitClassInfo* getUnitClassInfo(int i) const;
	CvInfoBase* getUnitCombatInfo(int i) const;
	CvInfoBase* getDomainInfo(int i) const;
	CvBuildingInfo* getBuildingInfo(int i) const;
	CvCivicOptionInfo* getCivicOptionInfo(int i) const;
	CvCivicInfo* getCivicInfo(int i) const;
	CvDiplomacyInfo* getDiplomacyInfo(int i) const;
	CvProjectInfo* getProjectInfo(int i) const;
	CvVoteInfo* getVoteInfo(int i) const;
	CvProcessInfo* getProcessInfo(int i) const;
	CvSpecialistInfo* getSpecialistInfo(int i) const;
	CvReligionInfo* getReligionInfo(int i) const;
	CvInfoBase* getPaganReligionInfo(int i) const; // doc
	CvCorporationInfo* getCorporationInfo(int i) const;
	CvControlInfo* getControlInfo(int i) const;
	CvTechInfo* getTechInfo(int i) const;
	CvSpecialBuildingInfo* getSpecialBuildingInfo(int i) const;
	CvPromotionInfo* getPromotionInfo(int i) const;
	CvAnimationPathInfo * getAnimationPathInfo(int i) const;
	CvEmphasizeInfo * getEmphasizeInfo(int i) const;
	CvUpkeepInfo * getUpkeepInfo(int i) const;
	CvCultureLevelInfo * getCultureLevelInfo(int i) const;
	CvEraInfo * getEraInfo(int i) const;
	CvVictoryInfo * getVictoryInfo(int i) const;
	CvWorldInfo * getWorldInfo(int i) const;
	CvClimateInfo * getClimateInfo(int i) const;
	CvSeaLevelInfo * getSeaLevelInfo(int i) const;
	CvInfoBase * getUnitAIInfo(int i) const;
	CvColorInfo* getColorInfo(int i) const;
	CvUnitArtStyleInfo* getUnitArtStyleTypeInfo(int i) const;

	int getInfoTypeForString(const char* szInfoType) const;
	int getTypesEnum(const char* szType) const;

	int getNumPlayerColorInfos() const { return kGlobals.getNumPlayerColorInfos(); }
	CvPlayerColorInfo* getPlayerColorInfo(int i) const;

	CvInfoBase* getHints(int i) const;
	CvMainMenuInfo* getMainMenus(int i) const;
	CvInfoBase* getInvisibleInfo(int i) const;
	CvVoteSourceInfo* getVoteSourceInfo(int i) const;
	CvInfoBase* getAttitudeInfo(int i) const;
	CvInfoBase* getMemoryInfo(int i) const;
	CvInfoBase* getConceptInfo(int i) const;
	CvInfoBase* getNewConceptInfo(int i) const;
	CvInfoBase* getCityTabInfo(int i) const;
	CvInfoBase* getCalendarInfo(int i) const;
	CvInfoBase* getGameOptionInfo(int i) const;
	CvInfoBase* getMPOptionInfo(int i) const;
	CvInfoBase* getForceControlInfo(int i) const;
	CvInfoBase* getSeasonInfo(int i) const;
	CvInfoBase* getMonthInfo(int i) const;
	CvInfoBase* getDenialInfo(int i) const;
	//CvQuestInfo* getQuestInfo(int i) const; // advc.003j
	CvTutorialInfo* getTutorialInfo(int i) const;
	CvEventTriggerInfo* getEventTriggerInfo(int i) const;
	CvEventInfo* getEventInfo(int i) const;
	CvEspionageMissionInfo* getEspionageMissionInfo(int i) const;
	CvHurryInfo* getHurryInfo(int i) const;
	CvPlayerOptionInfo* getPlayerOptionInfo(int i) const;
	CvPlayerOptionInfo* getPlayerOptionsInfoByIndex(int i) const;

	bool IsGraphicsInitialized() const; // advc
	CvGraphicOptionInfo* getGraphicOptionInfo(int i) const;
	CvGraphicOptionInfo* getGraphicOptionsInfoByIndex(int i) const;

	// ArtInfos
	CvArtInfoInterface* getInterfaceArtInfo(int i) const;
	CvArtInfoMovie* getMovieArtInfo(int i) const;
	CvArtInfoMisc* getMiscArtInfo(int i) const;
	CvArtInfoUnit* getUnitArtInfo(int i) const;
	CvArtInfoBuilding* getBuildingArtInfo(int i) const;
	CvArtInfoCivilization* getCivilizationArtInfo(int i) const;
	CvArtInfoLeaderhead* getLeaderheadArtInfo(int i) const;
	CvArtInfoBonus* getBonusArtInfo(int i) const;
	CvArtInfoImprovement* getImprovementArtInfo(int i) const;
	CvArtInfoTerrain* getTerrainArtInfo(int i) const;
	CvArtInfoFeature* getFeatureArtInfo(int i) const;


	// Structs

	const char* getEntityEventTypes(int i) const { return kGlobals.getEntityEventTypes((EntityEventTypes) i); }
	const char* getAnimationOperatorTypes(int i) const { return kGlobals.getAnimationOperatorTypes((AnimationOperatorTypes) i); }
	const char* getFunctionTypes(int i) const { return kGlobals.getFunctionTypes((FunctionTypes) i); }
	const char* getFlavorTypes(int i) const { return kGlobals.getFlavorTypes((FlavorTypes) i); }
	const char* getArtStyleTypes(int i) const { return kGlobals.getArtStyleTypes((ArtStyleTypes) i); }
	const char* getCitySizeTypes(int i) const { return kGlobals.getCitySizeTypes((CitySizeTypes) i); }
	const char* getContactTypes(int i) const { return kGlobals.getContactTypes((ContactTypes) i); }
	const char* getDiplomacyPowerTypes(int i) const { return kGlobals.getDiplomacyPowerTypes((DiplomacyPowerTypes) i); }
	const char *getFootstepAudioTypes(int i) { return kGlobals.getFootstepAudioTypes(i); }
	const char *getFootstepAudioTags(int i) { return kGlobals.getFootstepAudioTags(i); }

	int getNumEffectInfos() const { return kGlobals.getNumEffectInfos(); }
	int getNumTerrainInfos() const { return kGlobals.getNumTerrainInfos(); }
	int getNumSpecialBuildingInfos() const { return kGlobals.getNumSpecialBuildingInfos(); }
	int getNumBonusInfos() const { return kGlobals.getNumBonusInfos(); };
	int getNumPlayableCivilizationInfos() const { return kGlobals.getNumPlayableCivilizationInfos(); }
	int getNumCivilizatonInfos() const { return kGlobals.getNumCivilizationInfos(); }
	int getNumLeaderHeadInfos() const { return kGlobals.getNumLeaderHeadInfos(); }
	int getNumTraitInfos() const { return kGlobals.getNumTraitInfos(); }
	int getNumUnitInfos() const { return kGlobals.getNumUnitInfos(); }
	int getNumSpecialUnitInfos() const { return kGlobals.getNumSpecialUnitInfos(); }
	int getNumRouteInfos() const { return kGlobals.getNumRouteInfos(); }
	int getNumFeatureInfos() const { return kGlobals.getNumFeatureInfos(); }
	int getNumImprovementInfos() const { return kGlobals.getNumImprovementInfos(); }
	int getNumGoodyInfos() const { return kGlobals.getNumGoodyInfos(); }
	int getNumBuildInfos() const { return kGlobals.getNumBuildInfos(); }
	int getNumHandicapInfos() const { return kGlobals.getNumHandicapInfos(); }
	int getNumGameSpeedInfos() const { return kGlobals.getNumGameSpeedInfos(); }
	int getNumTurnTimerInfos() const { return kGlobals.getNumTurnTimerInfos(); }
	int getNumBuildingClassInfos() const { return kGlobals.getNumBuildingClassInfos(); }
	int getNumBuildingInfos() const { return kGlobals.getNumBuildingInfos(); }
	int getNumUnitClassInfos() const { return kGlobals.getNumUnitClassInfos(); }
	int getNumUnitCombatInfos() const { return kGlobals.getNumUnitCombatInfos(); }
	// <advc.enum>
	int getNumAutomateInfos() const { return NUM_AUTOMATE_TYPES; }
	int getNumCommandInfos() const { return NUM_COMMAND_TYPES; }
	int getNumControlInfos() const { return NUM_CONTROL_TYPES; }
	int getNumMissionInfos() const { return NUM_MISSION_TYPES; } // </advc.enum>
	int getNumActionInfos() const { return kGlobals.getNumActionInfos(); }
	int getNumPromotionInfos() const { return kGlobals.getNumPromotionInfos(); }
	int getNumTechInfos() const { return kGlobals.getNumTechInfos(); }
	int getNumReligionInfos() const { return kGlobals.getNumReligionInfos(); }
	int getNumPaganReligionInfos() const { return GC.getNumPaganReligionInfos(); } // doc
	int getNumCorporationInfos() const { return kGlobals.getNumCorporationInfos(); }
	int getNumSpecialistInfos() const { return kGlobals.getNumSpecialistInfos(); }
	int getNumCivicInfos() const { return kGlobals.getNumCivicInfos(); }
	int getNumDiplomacyInfos() const { return kGlobals.getNumDiplomacyInfos(); }
	int getNumCivicOptionInfos() const { return kGlobals.getNumCivicOptionInfos(); }
	int getNumProjectInfos() const { return kGlobals.getNumProjectInfos(); }
	int getNumVoteInfos() const { return kGlobals.getNumVoteInfos(); }
	int getNumProcessInfos() const { return kGlobals.getNumProcessInfos(); }
	int getNumEmphasizeInfos() const { return kGlobals.getNumEmphasizeInfos(); }
	int getNumHurryInfos() const { return kGlobals.getNumHurryInfos(); }
	int getNumUpkeepInfos() const { return kGlobals.getNumUpkeepInfos(); }
	int getNumCultureLevelInfos() const { return kGlobals.getNumCultureLevelInfos(); }
	int getNumEraInfos() const { return kGlobals.getNumEraInfos(); }
	int getNumVictoryInfos() const { return kGlobals.getNumVictoryInfos(); }
	int getNumWorldInfos() const { return kGlobals.getNumWorldInfos(); }
	int getNumSeaLevelInfos() const { return kGlobals.getNumSeaLevelInfos(); }
	int getNumClimateInfos() const { return kGlobals.getNumClimateInfos(); }
	int getNumConceptInfos() const { return kGlobals.getNumConceptInfos(); }
	int getNumNewConceptInfos() const { return kGlobals.getNumNewConceptInfos(); }
	// <advc.enum> Return hardcoded values instead of GC.getNum...
	int getNumCityTabInfos() const { return NUM_CITYTAB_TYPES; }
	int getNumCalendarInfos() const { return NUM_CALENDAR_TYPES; }
	int getNumPlayerOptionInfos() const { return NUM_PLAYEROPTION_TYPES; }
	int getNumGameOptionInfos() const { return NUM_GAMEOPTION_TYPES; }
	int getNumMPOptionInfos() const { return NUM_MPOPTION_TYPES; }
	// </advc.enum>
	int getNumForceControlInfos() const { return NUM_FORCECONTROL_TYPES; }
	int getNumSeasonInfos() const { return kGlobals.getNumSeasonInfos(); }
	int getNumMonthInfos() const { return kGlobals.getNumMonthInfos(); }
	int getNumDenialInfos() const { return NUM_DENIAL_TYPES; } // advc.enum
	//int getNumQuestInfos() const { return kGlobals.getNumQuestInfos(); } // advc.003j
	int getNumTutorialInfos() const { return kGlobals.getNumTutorialInfos(); }
	int getNumEventTriggerInfos() const { return kGlobals.getNumEventTriggerInfos(); }
	int getNumEventInfos() const { return kGlobals.getNumEventInfos(); }
	int getNumEspionageMissionInfos() const { return kGlobals.getNumEspionageMissionInfos(); }
	int getNumHints() const { return kGlobals.getNumHints(); }
	int getNumMainMenus() const { return kGlobals.getNumMainMenuInfos(); }
	int getNumInvisibleInfos() const { return kGlobals.getNumInvisibleInfos(); }
	int getNumVoteSourceInfos() const { return kGlobals.getNumVoteSourceInfos(); }

	// ArtInfos
	int getNumInterfaceArtInfos() const { return ARTFILEMGR.getNumInterfaceArtInfos(); }
	int getNumMovieArtInfos() const { return ARTFILEMGR.getNumMovieArtInfos(); }
	int getNumMiscArtInfos() const { return ARTFILEMGR.getNumMiscArtInfos(); }
	int getNumUnitArtInfos() const { return ARTFILEMGR.getNumUnitArtInfos(); }
	int getNumBuildingArtInfos() const { return ARTFILEMGR.getNumBuildingArtInfos(); }
	int getNumCivilizationArtInfos() const { return ARTFILEMGR.getNumCivilizationArtInfos(); }
	int getNumLeaderheadArtInfos() const { return ARTFILEMGR.getNumLeaderheadArtInfos(); }
	int getNumImprovementArtInfos() const { return ARTFILEMGR.getNumImprovementArtInfos(); }
	int getNumBonusArtInfos() const { return ARTFILEMGR.getNumBonusArtInfos(); }
	int getNumTerrainArtInfos() const { return ARTFILEMGR.getNumTerrainArtInfos(); }
	int getNumFeatureArtInfos() const { return ARTFILEMGR.getNumFeatureArtInfos(); }
	int getNumAnimationPathInfos() const { return NUM_ANIMATIONPATH_TYPES; } // advc.enum
	int getNumAnimationCategoryInfos() const { return kGlobals.getNumAnimationCategoryInfos(); }
	int getNumUnitArtStyleTypeInfos() const { return kGlobals.getNumUnitArtStyleInfos(); }


	int getNumEntityEventTypes() const { return kGlobals.getNumEntityEventTypes(); }
	int getNumAnimationOperatorTypes() const { return kGlobals.getNumAnimationOperatorTypes(); }
	int getNumArtStyleTypes() const { return kGlobals.getNumArtStyleTypes(); }
	int getNumFlavorTypes() const { return kGlobals.getNumFlavorTypes(); }
	int getNumCitySizeTypes() const { return NUM_CITYSIZE_TYPES; } // advc.enum
	int getNumFootstepAudioTypes() const { return kGlobals.getNumFootstepAudioTypes(); }

	//////////////////////
	// Globals Defines
	//////////////////////

	CyVariableSystem* getCyDefinesVarSystem();
	int getDefineINT(const char * szName) const { return kGlobals.getDefineINT(szName); }
	float getDefineFLOAT(const char * szName) const { return kGlobals.getDefineFLOAT(szName); }
	const char * getDefineSTRING(const char * szName) const { return kGlobals.getDefineSTRING(szName); }
	void setDefineINT(const char * szName, int iValue) { return kGlobals.setDefineINT(szName, iValue); }
	void setDefineFLOAT(const char * szName, float fValue) { return kGlobals.setDefineFLOAT(szName, fValue); }
	void setDefineSTRING(const char * szName, const char * szValue) { return kGlobals.setDefineSTRING(szName, szValue); }

	int getMOVE_DENOMINATOR() const { return kGlobals.getMOVE_DENOMINATOR(); }
	int getFOOD_CONSUMPTION_PER_POPULATION() const { return kGlobals.getFOOD_CONSUMPTION_PER_POPULATION(); }
	int getMAX_HIT_POINTS() const { return kGlobals.getMAX_HIT_POINTS(); }
	int getMAX_PLOT_LIST_ROWS() const { return kGlobals.getMAX_PLOT_LIST_ROWS(); }
	int getUNIT_MULTISELECT_MAX() const { return kGlobals.getUNIT_MULTISELECT_MAX(); }
	int getEVENT_MESSAGE_TIME() const { return kGlobals.getEVENT_MESSAGE_TIME(); }
	int getPERCENT_ANGER_DIVISOR() const { return kGlobals.getPERCENT_ANGER_DIVISOR(); }
	int getMIN_WATER_SIZE_FOR_OCEAN() const { return kGlobals.getDefineINT(CvGlobals::MIN_WATER_SIZE_FOR_OCEAN); }
	int getMAX_CITY_DEFENSE_DAMAGE() const { return kGlobals.getMAX_CITY_DEFENSE_DAMAGE(); }

	int getNUM_UNIT_AND_TECH_PREREQS() const { return kGlobals.getDefineINT(CvGlobals::NUM_UNIT_AND_TECH_PREREQS); }
	int getNUM_UNIT_PREREQ_OR_BONUSES() const { return kGlobals.getDefineINT(CvGlobals::NUM_UNIT_PREREQ_OR_BONUSES); }
	int getNUM_BUILDING_AND_TECH_PREREQS() const { return kGlobals.getDefineINT(CvGlobals::NUM_BUILDING_AND_TECH_PREREQS); }
	int getNUM_BUILDING_PREREQ_OR_BONUSES() const { return kGlobals.getDefineINT(CvGlobals::NUM_BUILDING_PREREQ_OR_BONUSES); }
	int getNUM_AND_TECH_PREREQS() const { return kGlobals.getDefineINT(CvGlobals::NUM_AND_TECH_PREREQS); }
	int getNUM_OR_TECH_PREREQS() const { return kGlobals.getDefineINT(CvGlobals::NUM_OR_TECH_PREREQS); }
	int getNUM_ROUTE_PREREQ_OR_BONUSES() const { return kGlobals.getDefineINT(CvGlobals::NUM_ROUTE_PREREQ_OR_BONUSES); }
	int getNUM_CORPORATION_PREREQ_BONUSES() const { return kGlobals.getDefineINT(CvGlobals::NUM_CORPORATION_PREREQ_BONUSES); }
	// advc.003t: Removed the other (unused) accessors for cached GlobalDefines

	float getCAMERA_MIN_YAW() const { return kGlobals.getCAMERA_MIN_YAW(); }
	float getCAMERA_MAX_YAW() const { return kGlobals.getCAMERA_MAX_YAW(); }
	float getCAMERA_FAR_CLIP_Z_HEIGHT() const { return kGlobals.getCAMERA_FAR_CLIP_Z_HEIGHT(); }
	float getCAMERA_MAX_TRAVEL_DISTANCE() const { return kGlobals.getCAMERA_MAX_TRAVEL_DISTANCE(); }
	float getCAMERA_START_DISTANCE() const { return kGlobals.getCAMERA_START_DISTANCE(); }
	float getAIR_BOMB_HEIGHT() const { return kGlobals.getAIR_BOMB_HEIGHT(); }
	float getPLOT_SIZE() const { return kGlobals.getPLOT_SIZE(); }
	float getCAMERA_SPECIAL_PITCH() const { return kGlobals.getCAMERA_SPECIAL_PITCH(); }
	float getCAMERA_MAX_TURN_OFFSET() const { return kGlobals.getCAMERA_MAX_TURN_OFFSET(); }
	float getCAMERA_MIN_DISTANCE() const { return kGlobals.getCAMERA_MIN_DISTANCE(); }
	float getCAMERA_UPPER_PITCH() const { return kGlobals.getCAMERA_UPPER_PITCH(); }
	float getCAMERA_LOWER_PITCH() const { return kGlobals.getCAMERA_LOWER_PITCH(); }
	float getFIELD_OF_VIEW() const { return kGlobals.getFIELD_OF_VIEW(); }
	float getSHADOW_SCALE() const { return kGlobals.getSHADOW_SCALE(); }
	float getUNIT_MULTISELECT_DISTANCE() const { return kGlobals.getUNIT_MULTISELECT_DISTANCE(); }
	// advc.004m:
	void updateCameraStartDistance(bool bReset) { kGlobals.updateCameraStartDistance(bReset); }

	int getMAX_CIV_PLAYERS() const { return MAX_CIV_PLAYERS; }
	int getMAX_PLAYERS() const { return MAX_PLAYERS; }
	int getMAX_CIV_TEAMS() const { return MAX_CIV_TEAMS; }
	int getMAX_TEAMS() const { return MAX_TEAMS; }
	int getBARBARIAN_PLAYER() const { return BARBARIAN_PLAYER; }
	int getBARBARIAN_TEAM() const { return BARBARIAN_TEAM; }
	int getINVALID_PLOT_COORD() const { return INVALID_PLOT_COORD; }
	int getNUM_CITY_PLOTS() const { return NUM_CITY_PLOTS; }
	int getCITY_HOME_PLOT() const { return CITY_HOME_PLOT; }
// <advc.003t> Non-const global context (previously the member functions had used GC)
private:
	CvGlobals& kGlobals; // </advc.003t>
};

#endif	// CyGlobalContext_h
