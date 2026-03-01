#pragma once

#ifndef CV_PYTHON_CALLER_H
#define CV_PYTHON_CALLER_H

class CyArgsList;
enum CallbackDefines;
class CvPopup;
class CvArea;

/*  advc.003y: New class. Wrapper for all calls to CvDLLPythonIFaceBase - except:
	- onEvent calls are still handled by CvDllPythonEvents.
	- Memory tracking is still handled by CvGameCoreDLL.cpp.
	- BUG options are still handled by CvBugOptions. */
class CvPythonCaller
{
public:
	CvPythonCaller();
	~CvPythonCaller();
	bool isUseFinishTextCallback() const; // Needed for a DllExport in CvGlobals
	void call(char const* szFunctionName, char const* szModuleName = PYGameModule,
			bool bAssertSuccess = true, bool bCheckExists = false) const;

	// Screens ...
	void showPythonScreen(char const* szScreenName) const;
	void launchPythonScreenPopup(CvPopupInfo const& kPopupInfo, CvPopup* pPopup) const;
	void callScreenFunction(char const* szFunctionName) const;
	void showForeignAdvisorScreen(int iTab = -1) const;
	void showInfoScreen(int iTab = 0, bool bEndGame = false) const;
	void showHallOfFameScreen(bool bAllowReplay) const;
	CvPlot* WBGetHighlightPlot() const;
	void onOKClicked(CvPopupInfo const& kInfo, int iButtonClicked) const;
	bool onFocus(CvPopupInfo const& kInfo) const;
	void refreshMilitaryAdvisor(int iMode, int iData) const;
	void jumpToPediaMain(int iCategory) const;
	void jumpToPedia(int iData, char const* szDataType) const;
	void jumpToPediaDescription(int iEntryData1, int iEntryData2) const;
	bool updateColoredPlots() const;
	bool isSkipResearchPopup(PlayerTypes ePlayer) const;
	bool isShowTechChooserButton(PlayerTypes ePlayer) const;
	TechTypes recommendedTech(PlayerTypes ePlayer, bool bFirst, TechTypes eBest = NO_TECH) const;
	bool isSkipProductionPopup(CvCity const& kCity) const;
	bool isShowExamineButton(CvCity const& kCity) const;
	UnitTypes recommendedUnit(CvCity const& kCity) const;
	BuildingTypes recommendedBuilding(CvCity const& kCity) const;

	// Misc. UI ...
	bool canPickRevealedPlot(CvPlot const& kPlot) const;
	bool cannotSelectionListMoveOverride(CvPlot const& kPlot,
			bool bAlt, bool bShift, bool bCtrl) const;
	bool cannotSelectionListNetOverride(GameMessageTypes eMessage, int aiData[3],
			int iFlags, bool bAlt, bool bShift) const;
	bool cannotHandleActionOverride(CvPlot* pPlot, int iAction, bool bTestVisible) const;
	bool cannotDoControlOverride(ControlTypes eControl) const;
	void sendEmailReminder(CvString szEmailAddress) const;

	// Random events ...
	bool canTriggerEvent(CvCity const& kCity, EventTriggerTypes eTrigger) const;
	bool canTriggerEvent(CvUnit const& kUnit, EventTriggerTypes eTrigger) const;
	CvWString eventHelp(EventTypes eEvent, EventTriggeredData const* pTriggered) const;
	bool doEventTrigger(PlayerTypes ePlayer, EventTriggeredData const& kTriggered,
			CvCity*& pCity, CvPlot*& pPlot, CvUnit*& pUnit, PlayerTypes& eOtherPlayer,
			CvCity*& pOtherPlayerCity, ReligionTypes& eReligion,
			CorporationTypes& eCorporation, BuildingTypes& eBuilding) const;
	void afterEventTriggered(EventTriggeredData const& kTriggered) const;
	bool canDoEvent(EventTypes eEvent, EventTriggeredData const& kTriggered) const;
	void applyEvent(EventTypes eEvent, EventTriggeredData const& kTriggered) const;
	bool checkExpireEvent(EventTypes eEvent, EventTriggeredData const& kTriggered) const;

	// City ...
	bool isCitiesDestroyFeatures(int iX, int iY) const;
	bool canTrainOverride(CvCity const& kCity, UnitTypes eUnit, bool bContinue,
			bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const;
	bool cannotTrainOverride(CvCity const& kCity, UnitTypes eUnit, bool bContinue,
			bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const;
	bool canConstructOverride(CvCity const& kCity, BuildingTypes eBuilding, bool bContinue,
			bool bTestVisible, bool bIgnoreCost) const;
	bool cannotConstructOverride(CvCity const& kCity, BuildingTypes eBuilding, bool bContinue,
			bool bTestVisible, bool bIgnoreCost) const;
	bool canCreateOverride(CvCity const& kCity, ProjectTypes eProject, bool bContinue,
			bool bTestVisible) const;
	bool cannotCreateOverride(CvCity const& kCity, ProjectTypes eProject, bool bContinue,
			bool bTestVisible) const;
	bool canMaintainOverride(CvCity const& kCity, ProcessTypes eProcess, bool bContinue) const;
	bool cannotMaintainOverride(CvCity const& kCity, ProcessTypes eProcess, bool bContinue) const;
	int buildingCostMod(CvCity const& kCity, BuildingTypes eBuilding) const;
	UnitTypes conscriptUnitOverride(PlayerTypes ePlayer) const;
	bool doGrowth(CvCity const& kCity) const;
	bool doCulture(CvCity const& kCity) const;
	bool doPlotCultureTimes100(CvCity const& kCity, PlayerTypes ePlayer,
			bool bUpdate, int iCultureRateTimes100) const;
	bool doProduction(CvCity const& kCity) const;
	bool doReligion(CvCity const& kCity) const;
	bool doGreatPeople(CvCity const& kCity) const;
	bool doMeltdown(CvCity const& kCity) const;
	bool AI_chooseProduction(CvCity const& kCity) const;
	bool captureGold(CvCity const& kOldCity, int& iCaptureGold) const;
	bool canRaze(CvCity const& kCity, PlayerTypes eNewOwner) const;

	// Plot/ player ...
	bool canBuild(CvPlot const& kPlot, BuildTypes eBuild, PlayerTypes ePlayer, bool& bOverride) const;
	bool doGoody(CvPlot const& kPlot, CvUnit const* pUnit, PlayerTypes ePlayer) const;
	bool cannotFoundCityOverride(CvPlot const& kPlot, PlayerTypes ePlayer) const;
	bool canFoundWaterCity(CvPlot const& kWaterPlot) const;

	// Player ...
	int unitCostMod(PlayerTypes ePlayer, UnitTypes eUnit) const;
	int extraExpenses(PlayerTypes ePlayer) const;
	bool canDoResearch(PlayerTypes ePlayer) const;
	bool cannotResearchOverride(PlayerTypes ePlayer, TechTypes eTech, bool bTrade) const;
	bool canResearchOverride(PlayerTypes ePlayer, TechTypes eTech, bool bTrade) const;
	bool cannotDoCivicOverride(PlayerTypes ePlayer, CivicTypes eCivic) const;
	bool canDoCivicOverride(PlayerTypes ePlayer, CivicTypes eCivic) const;
	bool doGold(PlayerTypes ePlayer) const;
	bool doResearch(PlayerTypes ePlayer) const;
	short AI_foundValue(PlayerTypes ePlayer, CvPlot const& kPlot) const;
	TechTypes AI_chooseTech(PlayerTypes ePlayer, bool bFree) const;
	bool AI_doDiplo(PlayerTypes ePlayer) const;

	// Team ...
	bool AI_doWar(TeamTypes eTeam) const;
	bool doOrganizationTech(TeamTypes eTechTeam, PlayerTypes eTechPlayer, TechTypes eTech) const;
	bool canDeclareWar(TeamTypes eTeam, TeamTypes eTargetTeam) const;

	// Unit/ group ...
	bool doCombat(CvSelectionGroup const& kGroup, CvPlot const& kPlot) const;
	bool isActionRecommended(CvUnit const& kUnit, int iAction) const;
	bool cannotMoveIntoOverride(CvUnit const& kUnit, CvPlot const& kPlot) const;
	bool cannotSpreadOverride(CvUnit const& kUnit, CvPlot const& kPlot, ReligionTypes eReligion) const;
	bool doPillageGold(CvUnit const& kUnit, CvPlot const& kPlot, int& iPillageGold) const;
	int upgradePrice(CvUnit const& kUnit, UnitTypes eToUnit) const;
	int experienceNeeded(CvUnit const& kUnit) const;
	bool AI_update(CvUnit const& kUnit) const;

	// Map ...
	bool callMapFunction(char const* szFunctionName) const;
	int numCustomMapOptions(char const* szMapScriptName, bool bHidden) const;
	CustomMapOptionTypes customMapOptionDefault(char const* szMapScriptName, int iOption) const;
	// <advc.004>
	CvWString customMapOptionDescription(char const* szMapScriptName, int iOption,
			CustomMapOptionTypes eOptionValue) const; // </advc.004>
	bool mapGridDimensions(WorldSizeTypes eWorldSize, int& iWidth, int& iHeight) const;
	bool mapPlotsPercent(WorldSizeTypes eWorldSize, int& iModifier) const; // advc.165
	void mapLatitudeExtremes(int& iTop, int& iBottom) const;
	void mapWraps(bool& bWrapX, bool& bWrapY) const;
	bool generateRandomMap() const;
	// Caller needs to initialize the array
	bool generatePlotTypes(int* aiPlotTypes, size_t uiSize) const;
	bool generateTerrainTypes(std::vector<int>& r, size_t uiTargetSize) const;
	bool canPlaceBonusAt(CvPlot const& kPlot, bool& bOverride) const;
	bool canPlaceGoodyAt(CvPlot const& kPlot, bool& bOverride) const;
	int riverValue(CvPlot const& kPlot, bool& bOverride) const;
	bool addBonusType(BonusTypes eBonus) const;
	bool addBonuses() const;
	bool addGoodies() const;
	bool addFeatures() const;
	bool addLakes() const;
	bool addRivers() const;
	void riverStartCardinalDirection(CvPlot const& kPlot, CardinalDirectionTypes& r) const;
	bool isHumanExplorerPlacementRandomized() const;
	int minStartingDistanceMod() const;
	CvArea* findStartingArea(PlayerTypes eStartingPlayer) const;
	CvPlot* findStartingPlot(PlayerTypes eStartingPlayer) const;
	bool isBonusIgnoreLatitude() const;

	// Game ...
	void doPlayerScore(PlayerTypes ePlayer, bool bFinal, bool bVictory, int& iScore) const;
	bool doReviveActivePlayer() const;
	bool doHolyCity() const;
	bool createBarbarianCities() const;
	bool createBarbarianUnits() const;
	bool isVictory(VictoryTypes eVictory) const;
	bool isVictoryPossible() const;

private:
	CvDLLPythonIFaceBase& m_python;
	bool* m_abUseCallback; // Replacing all the USE_..._CALLBACK variables and getters
	mutable bool m_bLastCallSuccessful;

	void call(char const* szFunctionName, CyArgsList& kArgsList, long& lResult,
			char const* szModuleName = PYGameModule, bool bAssertSuccess = true,
			bool bCheckExists = false) const;
	void call(char const* szFunctionName, long& lResult,
			char const* szModuleName = PYGameModule, bool bAssertSuccess = true,
			bool bCheckExists = false) const;
	void call(char const* szFunctionName, CyArgsList& kArgsList,
			char const* szModuleName = PYGameModule, bool bAssertSuccess = true,
			bool bCheckExists = false) const;
	bool isOverride() const;
	bool canPlaceItemAt(char const* szItemName, CvPlot const& kPlot, bool& bOverride) const;
	bool isUse(CallbackDefines eCallback) const
	{
		return m_abUseCallback[eCallback];
	}
	static int toInt(long l)
	{
		return static_cast<int>(l); // They're the same in MSVC03 x086
	}
	static bool toBool(long l)
	{
		FAssert(l >= 0);
		return (l == TRUE);
	}
};

#endif
