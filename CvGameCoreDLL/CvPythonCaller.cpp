#include "CvGameCoreDLL.h"
#include "CvPythonCaller.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvCity.h"
#include "CvUnit.h"
#include "CvGame.h"
#include "CvMap.h"
#include "CvPopupInfo.h"
#include "CySelectionGroup.h"
#include "CvGameTextMgr.h" // for sendEmailReminder

// advc.003y: New file; see CvPythonCaller.h.

#define DO_FOR_EACH_CALLBACK_DEFINE(DO) \
	DO(FINISH_TEXT) \
	DO(CANNOT_FOUND_CITY) \
	DO(CAN_FOUND_CITIES_ON_WATER) \
	DO(IS_PLAYER_RESEARCH) \
	DO(CAN_RESEARCH) \
	DO(CANNOT_DO_CIVIC) \
	DO(CAN_DO_CIVIC) \
	DO(CANNOT_CONSTRUCT) \
	DO(CAN_CONSTRUCT) \
	DO(CAN_DECLARE_WAR) \
	DO(CANNOT_RESEARCH) \
	DO(GET_UNIT_COST_MOD) \
	DO(GET_BUILDING_COST_MOD) \
	DO(GET_CITY_FOUND_VALUE) \
	DO(CANNOT_HANDLE_ACTION) \
	DO(CAN_BUILD) \
	DO(CANNOT_TRAIN) \
	DO(CAN_TRAIN) \
	DO(UNIT_CANNOT_MOVE_INTO) \
	DO(CANNOT_SPREAD_RELIGION) \
	/* K-Mod */ \
	DO(AI_UNIT_UPDATE) \
	DO(AI_DO_DIPLO) \
	DO(AI_CHOOSE_PRODUCTION) \
	DO(AI_DO_WAR) \
	DO(AI_CHOOSE_TECH) \
	DO(DO_GROWTH) \
	DO(DO_CULTURE) \
	DO(DO_PLOT_CULTURE) \
	DO(DO_PRODUCTION) \
	DO(DO_RELIGION) \
	DO(DO_GREAT_PEOPLE) \
	DO(DO_MELTDOWN) \
	DO(DO_PILLAGE_GOLD) \
	DO(GET_EXPERIENCE_NEEDED) \
	DO(UNIT_UPGRADE_PRICE) \
	DO(DO_COMBAT) \
	/* <advc.003y> These are easy enough to add now */ \
	DO(CITIES_DESTROY_FEATURES) \
	DO(CANNOT_CREATE) \
	DO(CAN_CREATE) \
	DO(CANNOT_MAINTAIN) \
	DO(CAN_MAINTAIN) \
	DO(CONSCRIPT_UNIT_TYPE) \
	DO(IS_VICTORY) \
	DO(IS_VICTORY_TEST) \
	DO(IS_CITY_CAPTURE_GOLD) \
	DO(CAN_RAZE) \
	DO(CALCULATE_SCORE) \
	DO(DO_HOLY_CITY) \
	DO(DO_GOODY) \
	DO(EXTRA_COST) \
	DO(DO_GOLD) \
	DO(DO_RESEARCH) \
	DO(DO_HOLY_CITY_TECH) \
	DO(IS_ACTION_RECOMMENDED) \
	/* </advc.003y> */
enum CallbackDefines
{
	DO_FOR_EACH_CALLBACK_DEFINE(MAKE_ENUMERATOR)
	NUM_CALLBACK_DEFINES
};
#define MAKE_STRING(VAR) "USE_"#VAR"_CALLBACK",

CvPythonCaller::CvPythonCaller() : m_python(*gDLL->getPythonIFace()), m_bLastCallSuccessful(false)
{
	// Load global defines - see CvGlobals::cacheGlobalInts for comments.
	const char* const aszGlobalCallbackTagNames[] = {
		DO_FOR_EACH_CALLBACK_DEFINE(MAKE_STRING)
	};
	FAssert(ARRAYSIZE(aszGlobalCallbackTagNames) == NUM_CALLBACK_DEFINES);
	m_abUseCallback = new bool[NUM_CALLBACK_DEFINES];
	for (int i = 0; i < NUM_CALLBACK_DEFINES; i++)
		m_abUseCallback[i] = GC.getDefineBOOL(aszGlobalCallbackTagNames[i]);
}

CvPythonCaller::~CvPythonCaller()
{
	SAFE_DELETE_ARRAY(m_abUseCallback);
}

bool CvPythonCaller::isUseFinishTextCallback() const
{
	return isUse(FINISH_TEXT);
}

#define ARGSLIST(iDefaultResult) CyArgsList argsList; long lResult = (iDefaultResult); (void)0

void CvPythonCaller::showPythonScreen(char const* szScreenName) const
{
	CvString szFunctionName("show");
	szFunctionName.append(szScreenName);
	callScreenFunction(szFunctionName.c_str());
}

// Moved from CvDLLButtonPopup; the comment is from there too.
void CvPythonCaller::launchPythonScreenPopup(CvPopupInfo const& kPopupInfo, CvPopup* pPopup) const
{
	/*  this is not really a popup, but a Python screen
		we trick the app into thinking that it's a popup so that we can
		take advantage of the popup queuing system */
	ARGSLIST(0);
	argsList.add(kPopupInfo.getData1());
	argsList.add(kPopupInfo.getData2());
	argsList.add(kPopupInfo.getData3());
	argsList.add(kPopupInfo.getOption1());
	argsList.add(kPopupInfo.getOption2());
	call(CvString(kPopupInfo.getText()).c_str(), argsList, lResult, PYScreensModule);
	if (lResult != 0)
		gDLL->UI().popupSetAsCancelled(pPopup);
}

void CvPythonCaller::callScreenFunction(char const* szFunctionName) const
{
	call(szFunctionName, PYScreensModule);
}

void CvPythonCaller::showForeignAdvisorScreen(int iTab) const
{
	CyArgsList argsList;
	argsList.add(iTab);
	call("showForeignAdvisorScreen", argsList, PYScreensModule);
}

void CvPythonCaller::showInfoScreen(int iTab, bool bEndGame) const
{
	CyArgsList argsList;
	argsList.add(iTab);
	argsList.add(bEndGame);
	call("showInfoScreen", argsList, PYScreensModule);
}

void CvPythonCaller::showHallOfFameScreen(bool bAllowReplay) const
{
	CyArgsList argsList;
	argsList.add(bAllowReplay);
	call("showHallOfFame", argsList, PYScreensModule);
}

CvPlot* CvPythonCaller::WBGetHighlightPlot() const
{
	std::vector<int> iiReturn;
	CyArgsList argsList;
	argsList.add(0); // Unused on the Python side - but expected.
	m_bLastCallSuccessful = m_python.callFunction(PYScreensModule, "WorldBuilderGetHighlightPlot",
			argsList.makeFunctionArgs(), &iiReturn);
	if (!m_bLastCallSuccessful)
		return NULL;
	if (iiReturn.size() < (size_t)2)
	{
		FAssert(iiReturn.empty());
		return NULL;
	}
	return GC.getMap().plot(iiReturn[0], iiReturn[1]);
}

void CvPythonCaller::onOKClicked(CvPopupInfo const& kInfo, int iButtonClicked) const
{
	char const* szFunctionName = kInfo.getOnClickedPythonCallback().c_str();
	if (std::strlen(szFunctionName) <= 0)
		return;
	FAssertMsg(!GC.getGame().isNetworkMultiPlayer(), "Danger: Out of Sync");
	CyArgsList argsList;
	argsList.add(iButtonClicked);
	argsList.add(kInfo.getData1());
	argsList.add(kInfo.getData2());
	argsList.add(kInfo.getData3());
	argsList.add(kInfo.getFlags());
	argsList.add(kInfo.getText());
	argsList.add(kInfo.getOption1());
	argsList.add(kInfo.getOption2());
	call(szFunctionName, argsList, kInfo.getPythonModule().IsEmpty() ?
			PYScreensModule : kInfo.getPythonModule());
}

bool CvPythonCaller::onFocus(CvPopupInfo const& kInfo) const
{
	if (kInfo.getOnFocusPythonCallback().IsEmpty())
		return false;
	ARGSLIST(false);
	argsList.add(kInfo.getData1());
	argsList.add(kInfo.getData2());
	argsList.add(kInfo.getData3());
	argsList.add(kInfo.getFlags());
	argsList.add(kInfo.getText());
	argsList.add(kInfo.getOption1());
	argsList.add(kInfo.getOption2());
	call(kInfo.getOnFocusPythonCallback(), argsList, lResult, PYScreensModule);
	return (lResult != 0);
}

// Cut from the deleted CvDLLWidgetData::doRefreshMilitaryAdvisor
void CvPythonCaller::refreshMilitaryAdvisor(int iMode, int iData) const
{
	CyArgsList argsList;
	argsList.add(iMode);
	argsList.add(iData);
	call("refreshMilitaryAdvisor", argsList, PYScreensModule);
}

/*  Replacing the doPedia...Jump functions of CvDLLWidgetData. No type safety, but
	I don't want to (re-)write all those functions. */
void CvPythonCaller::jumpToPedia(int iData, char const* szDataType) const
{
	CyArgsList argsList;
	argsList.add(iData);
	CvString szFunctionName("pediaJumpTo");
	szFunctionName.append(szDataType);
	call(szFunctionName.c_str(), argsList, PYScreensModule);
}

void CvPythonCaller::jumpToPediaMain(int iCategory) const
{
	CyArgsList argsList;
	argsList.add(std::max(0, iCategory));
	call("pediaMain", argsList, PYScreensModule);
}

void CvPythonCaller::jumpToPediaDescription(int iEntryData1, int iEntryData2) const
{
	CyArgsList argsList;
	argsList.add(iEntryData1);
	argsList.add(iEntryData2);
	call("pediaShowHistorical", argsList, PYScreensModule);
}

bool CvPythonCaller::updateColoredPlots() const
{
	long lResult;
	call("updateColoredPlots", lResult);
	return toBool(lResult);
}

void CvPythonCaller::call(char const* szFunctionName, CyArgsList& kArgsList,
	long& lResult, char const* szModuleName, bool bAssertSuccess,
	bool bCheckExists) const
{
	/*	Not sure how expensive this check is; otherwise, I'd just always perform it.
		bLoadIfNecessary: Generally won't help I think, except after having run
		into some error while reloading Python scripts. I doubt that
		bLoadIfNecessary=true will take extra time when the module is found,
		and, normally, it should always be found. So let's go with true. */
	if (bCheckExists && !m_python.moduleExists(szModuleName, true))
		m_bLastCallSuccessful = false;
	else
	{
		m_bLastCallSuccessful = m_python.callFunction(szModuleName,
				szFunctionName, kArgsList.makeFunctionArgs(), &lResult);
	}
	FAssert(!bAssertSuccess || m_bLastCallSuccessful);
}

void CvPythonCaller::call(char const* szFunctionName, long& lResult,
	char const* szModuleName, bool bAssertSuccess, bool bCheckExists) const
{
	if (bCheckExists && !m_python.moduleExists(szModuleName, true))
		m_bLastCallSuccessful = false;
	else
	{
		m_bLastCallSuccessful = m_python.callFunction(szModuleName, szFunctionName,
				NULL, &lResult);
	}
	FAssert(!bAssertSuccess || m_bLastCallSuccessful);
}

void CvPythonCaller::call(char const* szFunctionName, CyArgsList& kArgsList,
	char const* szModuleName, bool bAssertSuccess, bool bCheckExists) const
{
	if (bCheckExists && !m_python.moduleExists(szModuleName, true))
		m_bLastCallSuccessful = false;
	else
	{
		m_bLastCallSuccessful = m_python.callFunction(szModuleName, szFunctionName,
				kArgsList.makeFunctionArgs());
	}
	FAssert(!bAssertSuccess || m_bLastCallSuccessful);
}

void CvPythonCaller::call(char const* szFunctionName,
	char const* szModuleName, bool bAssertSuccess, bool bCheckExists) const
{
	if (bCheckExists && !m_python.moduleExists(szModuleName, true))
		m_bLastCallSuccessful = false;
	else
	{
		m_bLastCallSuccessful = m_python.callFunction(szModuleName, szFunctionName);
	}
	FAssert(!bAssertSuccess || m_bLastCallSuccessful);
}

bool CvPythonCaller::isSkipResearchPopup(PlayerTypes ePlayer) const
{
	ARGSLIST(false);
	argsList.add(ePlayer);
	call("skipResearchPopup", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::isShowTechChooserButton(PlayerTypes ePlayer) const
{
	ARGSLIST(true);
	argsList.add(ePlayer);
	call("showTechChooserButton", argsList, lResult);
	return toBool(lResult);
}

TechTypes CvPythonCaller::recommendedTech(PlayerTypes ePlayer, bool bFirst, TechTypes eBest) const
{
	ARGSLIST(NO_TECH);
	argsList.add(ePlayer);
	if (!bFirst)
		argsList.add(eBest);
	call(bFirst ? "getFirstRecommendedTech" : "getSecondRecommendedTech", argsList, lResult);
	return (TechTypes)toInt(lResult);
}

bool CvPythonCaller::isSkipProductionPopup(CvCity const& kCity) const
{
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("skipProductionPopup", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::isShowExamineButton(CvCity const& kCity) const
{
	ARGSLIST(true);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("showExamineCityButton", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

UnitTypes CvPythonCaller::recommendedUnit(CvCity const& kCity) const
{
	ARGSLIST(NO_UNIT);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("getRecommendedUnit", argsList, lResult);
	delete pyCity;
	return (UnitTypes)toInt(lResult);
}

BuildingTypes CvPythonCaller::recommendedBuilding(CvCity const& kCity) const
{
	ARGSLIST(NO_BUILDING);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("getRecommendedBuilding", argsList, lResult);
	delete pyCity;
	return (BuildingTypes)toInt(lResult);
}

bool CvPythonCaller::canPickRevealedPlot(CvPlot const& kPlot) const
{
	ARGSLIST(true);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	call("canPickPlot", argsList, lResult);
	delete pyPlot;
	return toBool(lResult);
}

bool CvPythonCaller::cannotSelectionListMoveOverride(CvPlot const& kPlot,
	bool bAlt, bool bShift, bool bCtrl) const
{
	ARGSLIST(false);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	argsList.add(bAlt);
	argsList.add(bShift);
	argsList.add(bCtrl);
	call("cannotSelectionListMove", argsList, lResult);
	delete pyPlot;
	return toBool(lResult);
}

bool CvPythonCaller::cannotSelectionListNetOverride(GameMessageTypes eMessage,
	int aiData[3], int iFlags, bool bAlt, bool bShift) const
{
	ARGSLIST(false);
	argsList.add(eMessage);
	for (int i = 0; i < 3; i++)
		argsList.add(aiData[i]);
	argsList.add(iFlags);
	argsList.add(bAlt);
	argsList.add(bShift);
	call("cannotSelectionListGameNetMessage", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::cannotHandleActionOverride(CvPlot* pPlot, int iAction,
	bool bTestVisible) const
{
	if (!isUse(CANNOT_HANDLE_ACTION))
		return false;
	ARGSLIST(false);
	CyPlot* pyPlot = new CyPlot(pPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	argsList.add(iAction);
	argsList.add(bTestVisible);
	call("cannotHandleAction", argsList, lResult);
	delete pyPlot;
	return toBool(lResult);
}

bool CvPythonCaller::cannotDoControlOverride(ControlTypes eControl) const
{
	ARGSLIST(false);
	argsList.add(eControl);
	call("cannotDoControl", argsList, lResult);
	return toBool(lResult);
}
// Replacing the deleted CvPlayer::sendReminder. Copied the comment from there.
void CvPythonCaller::sendEmailReminder(CvString szEmailAddress) const
{
	/*  Only perform this step if we have a valid email address on record,
		and we have provided information about how to send emails. */
	if (szEmailAddress.empty() || gDLL->GetPitbossSmtpHost().empty())
		return;
	CvWString szYearStr;
	GAMETEXT.setTimeStr(szYearStr, GC.getGame().getGameTurn(), true);
	ARGSLIST(0);
	argsList.add(szEmailAddress);
	argsList.add(gDLL->GetPitbossSmtpHost());
	argsList.add(gDLL->GetPitbossSmtpLogin());
	argsList.add(gDLL->GetPitbossSmtpPassword());
	argsList.add(GC.getGame().getName());
	argsList.add(GC.getGame().isMPOption(MPOPTION_TURN_TIMER));
	argsList.add(GC.getGame().getPitbossTurnTime());
	argsList.add(gDLL->GetPitbossEmail());
	argsList.add(szYearStr);
	call("sendEmail", argsList, lResult, PYPitBossModule);
	FAssertMsg(lResult == 0, "Pitboss Python fn onSendEmail encountered an error");
}

bool CvPythonCaller::canTriggerEvent(CvCity const& kCity, EventTriggerTypes eTrigger) const
{
	CvEventTriggerInfo& kTrigger = GC.getInfo(eTrigger);
	char const* szFunctionName = kTrigger.getPythonCanDoCity();
	if (std::strlen(szFunctionName) <= 0)
		return true;
	ARGSLIST(false);
	argsList.add(eTrigger);
	argsList.add(kCity.getOwner());
	argsList.add(kCity.getID());
	call(szFunctionName, argsList, lResult, PYRandomEventModule);
	return (lResult != 0); // Not sure if the usual ==1 would also be OK here
}

bool CvPythonCaller::canTriggerEvent(CvUnit const& kUnit, EventTriggerTypes eTrigger) const
{
	char const* szFunctionName = GC.getInfo(eTrigger).getPythonCanDoUnit();
	if (std::strlen(szFunctionName) <= 0)
		return true;
	ARGSLIST(false);
	argsList.add(eTrigger);
	argsList.add(kUnit.getOwner());
	argsList.add(kUnit.getID());
	call(szFunctionName, argsList, lResult, PYRandomEventModule);
	return (lResult != 0); // Not sure if the usual ==1 would also be OK here
}

CvWString CvPythonCaller::eventHelp(EventTypes eEvent, EventTriggeredData const* pTriggered) const
{
	char const* szHelp = GC.getInfo(eEvent).getPythonHelp();
	if (std::strlen(szHelp) <= 0)
		return L"";
	CvWString szResult;
	CyArgsList argsList;
	argsList.add(eEvent);
	argsList.add(m_python.makePythonObject(pTriggered));
	m_bLastCallSuccessful = m_python.callFunction(PYRandomEventModule, szHelp,
			argsList.makeFunctionArgs(), &szResult);
	FAssert(m_bLastCallSuccessful);
	if (std::wcslen(szResult) == 0)
		return L"";
	szResult.insert(0, NEWLINE);
	return szResult;
}

bool CvPythonCaller::doEventTrigger(PlayerTypes ePlayer, EventTriggeredData const& kTriggered,
	CvCity*& pCity, CvPlot*& pPlot, CvUnit*& pUnit, PlayerTypes& eOtherPlayer,
	CvCity*& pOtherPlayerCity, ReligionTypes& eReligion,
	CorporationTypes& eCorporation, BuildingTypes& eBuilding) const
{
	char const* szFunctionName = GC.getInfo(kTriggered.m_eTrigger).
			getPythonCanDo();
	if (std::strlen(szFunctionName) <= 0)
		return true; // Allow the event to trigger
	ARGSLIST(false);
	argsList.add(m_python.makePythonObject(&kTriggered));
	call(szFunctionName, argsList, lResult, PYRandomEventModule);
	if (lResult == 0)
		return false;
	// Python may have changed kTriggered  // advc: Need some extra checks here now
	pCity = (kTriggered.m_iCityId == FFreeList::INVALID_INDEX ? NULL :
			CvCity::fromIDInfo(IDInfo(ePlayer, kTriggered.m_iCityId)));
	pPlot = GC.getMap().plot(kTriggered.m_iPlotX, kTriggered.m_iPlotY);
	pUnit = (kTriggered.m_iUnitId == FFreeList::INVALID_INDEX ? NULL:
			CvUnit::fromIDInfo(IDInfo(ePlayer, kTriggered.m_iUnitId)));
	eOtherPlayer = kTriggered.m_eOtherPlayer;
	if (eOtherPlayer != NO_PLAYER && kTriggered.m_iOtherPlayerCityId != FFreeList::INVALID_INDEX)
		pOtherPlayerCity = CvCity::fromIDInfo(IDInfo(eOtherPlayer, kTriggered.m_iOtherPlayerCityId));
	eReligion = kTriggered.m_eReligion;
	eCorporation = kTriggered.m_eCorporation;
	eBuilding = kTriggered.m_eBuilding;
	return true;
}

void CvPythonCaller::afterEventTriggered(EventTriggeredData const& kTriggered) const
{
	char const* szFunctionName = GC.getInfo(kTriggered.m_eTrigger).
			getPythonCallback();
	if (std::strlen(szFunctionName) <= 0)
		return; // Note: None of the BtS event triggers have a callback function
	ARGSLIST(0);
	argsList.add(m_python.makePythonObject(&kTriggered));
	// lResult is unused, but I guess it's expected on the Python side(?).
	call(szFunctionName, argsList, lResult, PYRandomEventModule);
}

bool CvPythonCaller::canDoEvent(EventTypes eEvent, EventTriggeredData const& kTriggered) const
{
	char const* szFunctionName = GC.getInfo(eEvent).getPythonCanDo();
	if (std::strlen(szFunctionName) <= 0)
		return true;
	ARGSLIST(false);
	argsList.add(eEvent);
	argsList.add(m_python.makePythonObject(&kTriggered));
	call(szFunctionName, argsList, lResult, PYRandomEventModule);
	return (lResult != 0); // Not sure if the usual ==1 would also be OK here
}

void CvPythonCaller::applyEvent(EventTypes eEvent, EventTriggeredData const& kTriggered) const
{
	char const* szFunctionName = GC.getInfo(eEvent).getPythonCallback();
	if (std::strlen(szFunctionName) <= 0)
		return;
	ARGSLIST(0);
	argsList.add(eEvent);
	argsList.add(m_python.makePythonObject(&kTriggered));
	// lResult is unused, but I guess it's expected on the Python side(?).
	call(szFunctionName, argsList, lResult, PYRandomEventModule,
			false); // Many of the apply functions named in XML don't exist
}

bool CvPythonCaller::checkExpireEvent(EventTypes eEvent, EventTriggeredData const& kTriggered) const
{
	char const* szFunctionName = GC.getInfo(eEvent).getPythonExpireCheck();
	if (std::strlen(szFunctionName) <= 0)
		return false;
	ARGSLIST(false);
	argsList.add(eEvent);
	argsList.add(m_python.makePythonObject(&kTriggered));
	call(szFunctionName, argsList, lResult, PYRandomEventModule);
	return (lResult != 0); // Not sure if the usual ==1 would also be OK here
}

bool CvPythonCaller::isCitiesDestroyFeatures(int iX, int iY) const
{
	if (!isUse(CITIES_DESTROY_FEATURES))
		return true;
	ARGSLIST(true);
	argsList.add(iX);
	argsList.add(iY);
	call("citiesDestroyFeatures", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::canTrainOverride(CvCity const& kCity, UnitTypes eUnit,
	bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const
{
	if (!isUse(CAN_TRAIN))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eUnit);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	argsList.add(bIgnoreCost);
	argsList.add(bIgnoreUpgrades);
	call("canTrain", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}
/*  Could easily combine the "can" and "cannot" functions into a single function
	with a bool& parameter, but then a Python modder who just needs either function
	would have to "pay" for two DLL-to-Python calls instead of one. */
bool CvPythonCaller::cannotTrainOverride(CvCity const& kCity, UnitTypes eUnit,
	bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const
{
	if (!isUse(CANNOT_TRAIN))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eUnit);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	argsList.add(bIgnoreCost);
	argsList.add(bIgnoreUpgrades);
	call("cannotTrain", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::canConstructOverride(CvCity const& kCity, BuildingTypes eBuilding,
	bool bContinue, bool bTestVisible, bool bIgnoreCost) const
{
	if (!isUse(CAN_CONSTRUCT))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eBuilding);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	argsList.add(bIgnoreCost);
	call("canConstruct", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::cannotConstructOverride(CvCity const& kCity, BuildingTypes eBuilding,
	bool bContinue, bool bTestVisible, bool bIgnoreCost) const
{
	if (!isUse(CANNOT_CONSTRUCT))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eBuilding);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	argsList.add(bIgnoreCost);
	call("cannotConstruct", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::canCreateOverride(CvCity const& kCity, ProjectTypes eProject,
	bool bContinue, bool bTestVisible) const
{
	if (!isUse(CAN_CREATE))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eProject);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	call("canCreate", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::cannotCreateOverride(CvCity const& kCity, ProjectTypes eProject,
	bool bContinue, bool bTestVisible) const
{
	if (!isUse(CANNOT_CREATE))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eProject);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	call("cannotCreate", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::canMaintainOverride(CvCity const& kCity, ProcessTypes eProcess,
	bool bContinue) const
{
	if (!isUse(CAN_MAINTAIN))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eProcess);
	argsList.add(bContinue);
	call("canMaintain", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::cannotMaintainOverride(CvCity const& kCity, ProcessTypes eProcess,
	bool bContinue) const
{
	if (!isUse(CANNOT_MAINTAIN))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(eProcess);
	argsList.add(bContinue);
	call("cannotMaintain", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

int CvPythonCaller::buildingCostMod(CvCity const& kCity, BuildingTypes eBuilding) const
{
	if (!isUse(GET_BUILDING_COST_MOD))
		return 0;
	ARGSLIST(0);
	argsList.add(kCity.getOwner());
	argsList.add(kCity.getID());
	argsList.add(eBuilding);
	call("getBuildingCostMod", argsList, lResult);
	return toInt(lResult);
}

UnitTypes CvPythonCaller::conscriptUnitOverride(PlayerTypes ePlayer) const
{
	if (!isUse(CONSCRIPT_UNIT_TYPE))
		return NO_UNIT;
	ARGSLIST(NO_UNIT);
	argsList.add(ePlayer);
	call("getConscriptUnitType", argsList, lResult);
	return (UnitTypes)toInt(lResult);
}

bool CvPythonCaller::doGrowth(CvCity const& kCity) const
{
	if (!isUse(DO_GROWTH))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doGrowth", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::doCulture(CvCity const& kCity) const
{
	if (!isUse(DO_CULTURE))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doCulture", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::doPlotCultureTimes100(CvCity const& kCity, PlayerTypes ePlayer,
	bool bUpdate,int iCultureRateTimes100) const
{
	if (!isUse(DO_PLOT_CULTURE))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	argsList.add(bUpdate);
	FAssert(ePlayer != NO_PLAYER);
	argsList.add(ePlayer);
	//argsList.add(iCultureRate);
	argsList.add(iCultureRateTimes100 / 100); // K-Mod
	call("doPlotCulture", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::doProduction(CvCity const& kCity) const
{
	if (!isUse(DO_PRODUCTION))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doProduction", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::doReligion(CvCity const& kCity) const
{
	if (!isUse(DO_RELIGION))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doReligion", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::doGreatPeople(CvCity const& kCity) const
{
	if (!isUse(DO_GREAT_PEOPLE))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doGreatPeople", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::doMeltdown(CvCity const& kCity) const
{
	if (!isUse(DO_MELTDOWN))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doMeltdown", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::AI_chooseProduction(CvCity const& kCity) const
{
	if (!isUse(AI_CHOOSE_PRODUCTION))
		return false;
	ARGSLIST(false);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("AI_chooseProduction", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::captureGold(CvCity const& kOldCity, int& iCaptureGold) const
{
	if (!isUse(IS_CITY_CAPTURE_GOLD))
		return false;
	int const iError = MIN_INT;
	ARGSLIST(iError);
	CyCity* pyCity = new CyCity(kOldCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("doCityCaptureGold", argsList, lResult);
	delete pyCity;
	if (lResult != iError)
	{
		iCaptureGold = toInt(lResult);
		return true;
	}
	else FAssert(lResult != iError);
	return false;
}

bool CvPythonCaller::canRaze(CvCity const& kCity, PlayerTypes eNewOwner) const
{
	if (!isUse(CAN_RAZE))
		return true;
	ARGSLIST(true);
	argsList.add(eNewOwner);
	CyCity* pyCity = new CyCity(kCity);
	argsList.add(m_python.makePythonObject(pyCity));
	call("canRazeCity", argsList, lResult);
	delete pyCity;
	return toBool(lResult);
}

bool CvPythonCaller::canBuild(CvPlot const& kPlot, BuildTypes eBuild, PlayerTypes ePlayer,
	bool& bOverride) const
{
	bOverride = false;
	if (!isUse(CAN_BUILD))
		return false;
	ARGSLIST(-1);
	argsList.add(kPlot.getX());
	argsList.add(kPlot.getY());
	argsList.add(eBuild);
	argsList.add(ePlayer);
	call("canBuild", argsList, lResult);
	// Comment in CvGameUtils.py: "Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can"
	if (lResult == -1)
		return false;
	bOverride = true;
	FAssertBounds(-1, 2, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doGoody(CvPlot const& kPlot, CvUnit const* pUnit, PlayerTypes ePlayer) const
{
	if (!isUse(DO_GOODY))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	// Note: pUnit can be NULL, but pyUnit can still be initialized (and is expected by Python).
	CyUnit* pyUnit = new CyUnit(*pUnit);
	argsList.add(m_python.makePythonObject(pyUnit));
	call("doGoody", argsList, lResult);
	delete pyPlot;
	delete pyUnit;
	return toBool(lResult);
}

bool CvPythonCaller::cannotFoundCityOverride(CvPlot const& kPlot, PlayerTypes ePlayer) const
{
	if (!isUse(CANNOT_FOUND_CITY))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	argsList.add(kPlot.getX());
	argsList.add(kPlot.getY());
	call("cannotFoundCity", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::canFoundWaterCity(CvPlot const& kWaterPlot) const
{
	if (!isUse(CAN_FOUND_CITIES_ON_WATER))
		return false;
	FAssert(kWaterPlot.isWater());
	ARGSLIST(false);
	argsList.add(kWaterPlot.getX());
	argsList.add(kWaterPlot.getY());
	call("canFoundCitiesOnWater", argsList, lResult);
	return toBool(lResult);
}

int CvPythonCaller::unitCostMod(PlayerTypes ePlayer, UnitTypes eUnit) const
{
	if (!isUse(GET_UNIT_COST_MOD))
		return 0;
	ARGSLIST(0);
	argsList.add(ePlayer);
	argsList.add(eUnit);
	call("getUnitCostMod", argsList, lResult);
	return toInt(lResult);
}

int CvPythonCaller::extraExpenses(PlayerTypes ePlayer) const
{
	if (!isUse(EXTRA_COST))
		return 0;
	ARGSLIST(0);
	argsList.add(ePlayer);
	call("getExtraCost", argsList, lResult);
	return toInt(lResult);
}

bool CvPythonCaller::canDoResearch(PlayerTypes ePlayer) const
{
	if (!isUse(IS_PLAYER_RESEARCH))
		return true;
	ARGSLIST(true);
	argsList.add(ePlayer);
	call("isPlayerResearch", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::cannotResearchOverride(PlayerTypes ePlayer, TechTypes eTech, bool bTrade) const
{
	if (!isUse(CANNOT_RESEARCH))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	argsList.add(eTech);
	argsList.add(bTrade);
	call("cannotResearch", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::canResearchOverride(PlayerTypes ePlayer, TechTypes eTech, bool bTrade) const
{
	if (!isUse(CAN_RESEARCH))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	argsList.add(eTech);
	argsList.add(bTrade);
	call("canResearch", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::cannotDoCivicOverride(PlayerTypes ePlayer, CivicTypes eCivic) const
{
	if (!isUse(CANNOT_DO_CIVIC))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	argsList.add(eCivic);
	call("cannotDoCivic", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::canDoCivicOverride(PlayerTypes ePlayer, CivicTypes eCivic) const
{
	if (!isUse(CAN_DO_CIVIC))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	argsList.add(eCivic);
	call("canDoCivic", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doGold(PlayerTypes ePlayer) const
{
	if (!isUse(DO_GOLD))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	call("doGold", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doResearch(PlayerTypes ePlayer) const
{
	if (!isUse(DO_RESEARCH))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	call("doResearch", argsList, lResult);
	return toBool(lResult);
}

short CvPythonCaller::AI_foundValue(PlayerTypes ePlayer, CvPlot const& kPlot) const
{
	if (!isUse(GET_CITY_FOUND_VALUE))
		return -1;
	ARGSLIST(-1);
	argsList.add(ePlayer);
	argsList.add(kPlot.getX());
	argsList.add(kPlot.getY());
	call("getCityFoundValue", argsList, lResult);
	FAssert(lResult <= MAX_SHORT); // K-Mod
	return safeIntCast<short>(lResult);
}

TechTypes CvPythonCaller::AI_chooseTech(PlayerTypes ePlayer, bool bFree) const
{
	if (!isUse(AI_CHOOSE_TECH))
		return NO_TECH;
	ARGSLIST(NO_TECH);
	argsList.add(ePlayer);
	argsList.add(bFree);
	call("AI_chooseTech", argsList, lResult);
	return (TechTypes)toInt(lResult);
}

bool CvPythonCaller::AI_doDiplo(PlayerTypes ePlayer) const
{
	if (!isUse(AI_DO_DIPLO))
		return false;
	ARGSLIST(false);
	argsList.add(ePlayer);
	call("AI_doDiplo", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::AI_doWar(TeamTypes eTeam) const
{
	if (!isUse(AI_DO_WAR))
		return false;
	ARGSLIST(false);
	argsList.add(eTeam);
	call("AI_doWar", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doOrganizationTech(TeamTypes eTechTeam, PlayerTypes eTechPlayer,
	TechTypes eTech) const
{
	if (!isUse(DO_HOLY_CITY_TECH))
		return false;
	ARGSLIST(false);
	argsList.add(eTechTeam);
	argsList.add(eTechPlayer);
	argsList.add(eTech);
	argsList.add(true); // bFirst - true at the single DLL call location
	call("doHolyCityTech", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::canDeclareWar(TeamTypes eTeam, TeamTypes eTargetTeam) const
{
	if (!isUse(CAN_DECLARE_WAR))
		return true;
	ARGSLIST(true);
	argsList.add(eTeam);
	argsList.add(eTargetTeam);
	call("canDeclareWar", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doCombat(CvSelectionGroup const& kGroup, CvPlot const& kPlot) const
{
	if (!isUse(DO_COMBAT))
		return false;
	ARGSLIST(false);
	CySelectionGroup* pyGroup = new CySelectionGroup(kGroup);
	argsList.add(m_python.makePythonObject(pyGroup));
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	call("doCombat", argsList, lResult);
	delete pyGroup;
	delete pyPlot;
	return toBool(lResult);
}

bool CvPythonCaller::isActionRecommended(CvUnit const& kUnit, int iAction) const
{
	if (!isUse(IS_ACTION_RECOMMENDED))
		return false;
	ARGSLIST(false);
	CyUnit* pyUnit = new CyUnit(kUnit);
	argsList.add(m_python.makePythonObject(pyUnit));
	argsList.add(iAction);
	call("isActionRecommended", argsList, lResult);
	delete pyUnit;
	return toBool(lResult);
}

bool CvPythonCaller::cannotMoveIntoOverride(CvUnit const& kUnit, CvPlot const& kPlot) const
{
	if (!isUse(UNIT_CANNOT_MOVE_INTO))
		return false;
	ARGSLIST(false);
	argsList.add(kUnit.getOwner());
	argsList.add(kUnit.getID());
	argsList.add(kPlot.getX());
	argsList.add(kPlot.getY());
	call("unitCannotMoveInto", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::cannotSpreadOverride(CvUnit const& kUnit, CvPlot const& kPlot, ReligionTypes eReligion) const
{
	if (!isUse(CANNOT_SPREAD_RELIGION))
		return false;
	ARGSLIST(false);
	argsList.add(kUnit.getOwner());
	argsList.add(kUnit.getID());
	argsList.add(eReligion);
	argsList.add(kPlot.getX());
	argsList.add(kPlot.getY());
	call("cannotSpreadReligion", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doPillageGold(CvUnit const& kUnit, CvPlot const& kPlot, int& iPillageGold) const
{
	if (!isUse(DO_PILLAGE_GOLD))
		return false;
	int const iError = MIN_INT;
	ARGSLIST(iError);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	CyUnit* pyUnit = new CyUnit(kUnit);
	argsList.add(m_python.makePythonObject(pyUnit));
	call("doPillageGold", argsList, lResult);
	delete pyPlot;
	delete pyUnit;
	if (lResult != iError)
		iPillageGold = toInt(lResult);
	else FAssert(lResult != iError);
	return true;
}

int CvPythonCaller::upgradePrice(CvUnit const& kUnit, UnitTypes eToUnit) const
{
	if (!isUse(UNIT_UPGRADE_PRICE))
		return -1;
	ARGSLIST(-1);
	argsList.add(kUnit.getOwner());
	argsList.add(kUnit.getID());
	argsList.add(eToUnit);
	call("getUpgradePriceOverride", argsList, lResult);
	return toInt(lResult);
}

int CvPythonCaller::experienceNeeded(CvUnit const& kUnit) const
{
	if (!isUse(GET_EXPERIENCE_NEEDED))
		return -1;
	ARGSLIST(-1);
	argsList.add(kUnit.getLevel());
	argsList.add(kUnit.getOwner());
	call("getExperienceNeeded", argsList, lResult);
	return toInt(lResult);
}

bool CvPythonCaller::AI_update(CvUnit const& kUnit) const
{
	if (!isUse(AI_UNIT_UPDATE))
		return false;
	ARGSLIST(false);
	CyUnit* pyUnit = new CyUnit(kUnit);
	argsList.add(m_python.makePythonObject(pyUnit));
	call("AI_unitUpdate", argsList, lResult);
	delete pyUnit;
	return toBool(lResult);
}

bool CvPythonCaller::callMapFunction(char const* szFunctionName) const
{
	call(szFunctionName, m_python.getMapScriptModule(), false);
	return isOverride();
}

int CvPythonCaller::numCustomMapOptions(char const* szMapScriptName, bool bHidden) const
{
	long lResult = 0;
	call(bHidden ? "getNumHiddenCustomMapOptions" : "getNumCustomMapOptions",
			// Earth2 has no getNumCustomMapOptions
			lResult, szMapScriptName, /*!bHidden*/ false, true);
	return toInt(lResult);
}

CustomMapOptionTypes CvPythonCaller::customMapOptionDefault(char const* szMapScriptName, int iOption) const
{
	ARGSLIST(NO_CUSTOM_MAPOPTION);
	argsList.add(iOption);
	call("getCustomMapOptionDefault", argsList, lResult, szMapScriptName,
			!GC.getInitCore().getSavedGame(), true);
	return (CustomMapOptionTypes)toInt(lResult);
}
// advc.004:
CvWString CvPythonCaller::customMapOptionDescription(char const* szMapScriptName,
	int iOption, CustomMapOptionTypes eOptionValue) const
{
	CvWString szResult;
	CyArgsList argsList;
	argsList.add(iOption);
	argsList.add(eOptionValue);
	if (!m_python.moduleExists(szMapScriptName, true))
		m_bLastCallSuccessful = false;
	else
	{
		m_bLastCallSuccessful = m_python.callFunction(szMapScriptName,
				"getCustomMapOptionDescAt", argsList.makeFunctionArgs(), &szResult);
	}
	/*  If the game was started from a savegame, then the map script may have been
		uninstalled; that's OK. */
	FAssert(m_bLastCallSuccessful || GC.getInitCore().getSavedGame());
	return szResult;
}

bool CvPythonCaller::mapGridDimensions(WorldSizeTypes eWorldSize, int& iWidth, int& iHeight) const
{
	std::vector<int> iiReturn;
	CyArgsList argsList;
	argsList.add(eWorldSize);
	m_bLastCallSuccessful = m_python.callFunction(m_python.getMapScriptModule(), "getGridSize",
			argsList.makeFunctionArgs(), &iiReturn);
	if (!isOverride() || iiReturn.size() < (size_t)2)
		return false;
	FAssertMsg(iiReturn[0] > 0 && iiReturn[1] > 0, "the width and height returned by python getGridSize() must be positive");
	iWidth = iiReturn[0];
	iHeight = iiReturn[1];
	return true;
}

// advc.165:
bool CvPythonCaller::mapPlotsPercent(WorldSizeTypes eWorldSize, int& iModifier) const
{
	long lResult = 100;
	CyArgsList argsList;
	argsList.add(eWorldSize);
	m_bLastCallSuccessful = m_python.callFunction(m_python.getMapScriptModule(),
			"getNumPlotsPercent", argsList.makeFunctionArgs(), &lResult);
	iModifier = toInt(lResult);
	return isOverride();
}

void CvPythonCaller::mapLatitudeExtremes(int& iTop, int& iBottom) const
{
	int const iNone = MIN_INT;
	long lResult = iNone;
	call("getTopLatitude", lResult, m_python.getMapScriptModule(), false);
	if (lResult != iNone && isOverride())
		iTop = toInt(lResult);
	lResult = iNone;
	call("getBottomLatitude", lResult, m_python.getMapScriptModule(), false);
	if (lResult != iNone && isOverride())
		iBottom = toInt(lResult);
}

void CvPythonCaller::mapWraps(bool& bWrapX, bool& bWrapY) const
{
	int const iError = -1;
	bool bWrapXTmp = false;
	{
		long lResult = iError;
		call("getWrapX", lResult, m_python.getMapScriptModule(), false);
		if (lResult == iError || !isOverride())
			return;
		bWrapXTmp = (lResult != 0); // As it was in CvMap::reset; perhaps the usual ==1 would also work.
	}
	long lResult = iError;
	call("getWrapY", lResult, m_python.getMapScriptModule(), false);
	if (lResult == iError || !isOverride())
		return;
	bWrapX = bWrapXTmp; // Don't set bWrapX until we know that bWrapY can also be set
	bWrapY = (lResult != 0);
}

bool CvPythonCaller::generateRandomMap() const
{
	call("generateRandomMap", m_python.getMapScriptModule(), false);
	return isOverride();
}
// CvMapGenerator needs this in an array; would otherwise prefer a vector& paramter.
bool CvPythonCaller::generatePlotTypes(int* aiPlotTypes, size_t uiSize) const
{
	std::vector<int> result;
	m_bLastCallSuccessful = m_python.callFunction(m_python.getMapScriptModule(),
			"generatePlotTypes", NULL, &result);
	if (!isOverride())
	{
		FErrorMsg("Map script has to override generatePlotTypes and mustn't call usingDefaultImpl");
		return false;
	}
	if (result.size() != uiSize)
	{
		FErrorMsg("Need to set a plot type for every plot");
		return false;
	}
	for (size_t i = 0; i < uiSize; i++)
		aiPlotTypes[i] = result[i];
	return true;
}

bool CvPythonCaller::generateTerrainTypes(std::vector<int>& r, size_t uiTargetSize) const
{
	r.reserve(uiTargetSize);
	m_bLastCallSuccessful = m_python.callFunction(m_python.getMapScriptModule(),
			"generateTerrainTypes", NULL, &r);
	if (!isOverride())
	{	// PlantGenerator seems to generate terrain in addFeatures, but that's highly irregular.
		FErrorMsg("Map script has to override generateTerrainTypes and mustn't call usingDefaultImpl");
		return false;
	}
	if (r.size() != uiTargetSize)
	{
		FErrorMsg("No terrain generated for some plots");
		return false;
	}
	return true;
}

bool CvPythonCaller::addBonusType(BonusTypes eBonus) const
{
	CyArgsList argsList;
	argsList.add(eBonus);
	call("addBonusType", argsList, m_python.getMapScriptModule(), false);
	return isOverride();
}

bool CvPythonCaller::canPlaceBonusAt(CvPlot const& kPlot, bool& bOverride) const
{
	return canPlaceItemAt("Bonus", kPlot, bOverride);
}

bool CvPythonCaller::canPlaceGoodyAt(CvPlot const& kPlot, bool& bOverride) const
{
	return canPlaceItemAt("Goody", kPlot, bOverride);
}

bool CvPythonCaller::canPlaceItemAt(char const* szItemName, CvPlot const& kPlot, bool& bOverride) const
{
	ARGSLIST(false);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	CvString szFunctionName("canPlace");
	szFunctionName.append(szItemName);
	szFunctionName.append("At");
	call(szFunctionName.c_str(), argsList, lResult, m_python.getMapScriptModule(), false);
	delete pyPlot;
	bOverride = isOverride();
	if (!bOverride)
		return false;
	if (lResult < 0)
	{
		FAssert(lResult >= 0);
		bOverride = false;
		return false;
	}
	return toBool(lResult);
}

int CvPythonCaller::riverValue(CvPlot const& kPlot, bool& bOverride) const
{
	ARGSLIST(-1);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	call("getRiverAltitude", argsList, lResult, m_python.getMapScriptModule(), false);
	delete pyPlot;
	bOverride = isOverride();
	if (!bOverride)
		return 0;
	if (lResult < 0)
	{
		FAssert(lResult >= 0);
		bOverride = false;
		return 0;
	}
	return toInt(lResult);
}

bool CvPythonCaller::addBonuses() const
{
	call("addBonuses", m_python.getMapScriptModule(), false);
	return isOverride();
}

bool CvPythonCaller::addGoodies() const
{
	call("addGoodies", m_python.getMapScriptModule(), false);
	return isOverride();
}

bool CvPythonCaller::addFeatures() const
{
	call("addFeatures", m_python.getMapScriptModule());
	return isOverride();
}

bool CvPythonCaller::addLakes() const
{
	call("addLakes", m_python.getMapScriptModule(), false);
	return isOverride();
}

bool CvPythonCaller::addRivers() const
{
	call("addRivers", m_python.getMapScriptModule(), false);
	return isOverride();
}

void CvPythonCaller::riverStartCardinalDirection(CvPlot const& kPlot,
	CardinalDirectionTypes& r) const
{
	ARGSLIST(NO_CARDINALDIRECTION);
	CyPlot* pyPlot = new CyPlot(kPlot);
	argsList.add(m_python.makePythonObject(pyPlot));
	call("getRiverStartCardinalDirection", argsList, lResult,
			m_python.getMapScriptModule(), false);
	delete pyPlot;
	if (!isOverride())
		return;
	if (lResult < 0)
	{
		FAssert(lResult >= 0);
		return;
	}
	r = (CardinalDirectionTypes)toInt(lResult);
}

bool CvPythonCaller::isHumanExplorerPlacementRandomized() const
{
	long lResult = false;
	call("startHumansOnSameTile", lResult, m_python.getMapScriptModule(), false);
	// If they don't start on the same tile, then placement is randomized.
	return !toBool(lResult);
}

int CvPythonCaller::minStartingDistanceMod() const
{
	long lResult = 0;
	call("minStartingDistanceModifier", lResult, m_python.getMapScriptModule(), false);
	return std::max(0, toInt(lResult));
}

CvArea* CvPythonCaller::findStartingArea(PlayerTypes eStartingPlayer) const
{
	ARGSLIST(-1);
	argsList.add(eStartingPlayer);
	call("findStartingArea", argsList, lResult, m_python.getMapScriptModule(), false);
	if (!isOverride())
		return NULL;
	CvArea* r = GC.getMap().getArea(toInt(lResult));
	FAssert(lResult == -1 || r != NULL); // Same condition as originally in CvPlayer::findStartingAreas
	return r;
}

CvPlot* CvPythonCaller::findStartingPlot(PlayerTypes eStartingPlayer) const
{
	ARGSLIST(-1);
	argsList.add(eStartingPlayer);
	call("findStartingPlot", argsList, lResult, m_python.getMapScriptModule(), false);
	if (!isOverride())
		return NULL;
	CvPlot* r = GC.getMap().plotByIndex(toInt(lResult));
	/*  advc.021a: Tectonics apparently assigns all starting plots at once on its own
		and then returns "None". Or something; doesn't seem to be a problem anyway.
		Now I'm having it return -10 to indicate that it's a known (or non-) issue. */
	FAssert(lResult == -10 || r != NULL);
	return r;
}

/*  Replacing CvGame::pythonIsBonusIgnoreLatitudes. The peculiar treatment of
	lResult has been copied from there. */
bool CvPythonCaller::isBonusIgnoreLatitude() const
{
	long lResult = -1;
	call("isBonusIgnoreLatitude", lResult, m_python.getMapScriptModule(), false);
	return (isOverride() && lResult != -1 && lResult != 0);
}

void CvPythonCaller::doPlayerScore(PlayerTypes ePlayer, bool bFinal, bool bVictory, int& iScore) const
{
	if (!isUse(CALCULATE_SCORE))
		return;
	int const iError = MIN_INT;
	ARGSLIST(iError);
	argsList.add(ePlayer);
	argsList.add(bFinal);
	argsList.add(bVictory);
	call("calculateScore", argsList, lResult);
	if (lResult != iError)
		iScore = toInt(lResult);
	else FAssert(lResult != iError);
}

bool CvPythonCaller::doReviveActivePlayer() const
{
	ARGSLIST(false);
	argsList.add(GC.getGame().getActivePlayer());
	call("doReviveActivePlayer", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::doHolyCity() const
{
	if (!isUse(DO_HOLY_CITY))
		return false;
	long lResult = false;
	call("doHolyCity", lResult);
	return toBool(lResult);
}

bool CvPythonCaller::createBarbarianCities() const
{
	long lResult = false;
	call("createBarbarianCities", lResult);
	return toBool(lResult);
}

bool CvPythonCaller::createBarbarianUnits() const
{
	long lResult = false;
	call("createBarbarianUnits", lResult);
	return toBool(lResult);
}

bool CvPythonCaller::isVictory(VictoryTypes eVictory) const
{
	if (!isUse(IS_VICTORY))
		return true;
	ARGSLIST(true);
	argsList.add(eVictory);
	call("isVictory", argsList, lResult);
	return toBool(lResult);
}

bool CvPythonCaller::isVictoryPossible() const
{
	if (!isUse(IS_VICTORY_TEST))
		return true;
	long lResult = true;
	call("isVictoryTest", lResult);
	return toBool(lResult);
}

bool CvPythonCaller::isOverride() const
{
	return (m_bLastCallSuccessful && !m_python.pythonUsingDefaultImpl());
}
