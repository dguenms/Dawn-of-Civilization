#pragma once

#ifndef RISE_FALL_H
#define RISE_FALL_H

#include "RFChapter.h"
#include "RFTotalScore.h"

class CvPopup;
class CvDiplomacyResponse;
class CvWString;

/*	advc.700: Main class for the Rise & Fall mod component.
	(The coding style of the R&F classes is inconsistent with the rest
	of the codebase. The R&F code isn't really subject to change, so I'm
	not going to overhaul it.) */
class RiseFall {

public:
	RiseFall();
	~RiseFall();
	void reset();
	void init();
	void setPlayerHandicap(PlayerTypes civId, bool bHuman, bool bIncrease);
	void write(FDataStreamBase* pStream);
	void read(FDataStreamBase* pStream);
	void atGameTurnStart();
	void atActiveTurnStart();
	void atTurnEnd(PlayerTypes civId);
	void retire();
	int getRetireTurns() const;
	bool hasRetired() const;
	int getAutoPlayCountdown() const;
	std::pair<int,int> getChapterCountdown() const;
	int getInterludeCountdown() const;
	void reportElimination(PlayerTypes civId);
	void prepareForExtendedGame();
	int getFinalRiseScore() const;
	int getNormalizedFinalScore() const;
	static int victoryStage(PlayerTypes civId);
	// Callbacks for CvDLLButtonPopup
	  bool launchDefeatPopup(CvPopup* popup, CvPopupInfo& info);
	  void handleDefeatPopup(int buttonClicked, int pos);
	  bool launchCivSelectionPopup(CvPopup* popup, CvPopupInfo& info);
	  void handleCivSelection(PlayerTypes selectedCiv);
	  void afterCivSelection(int buttonClicked);
	  void assignCivSelectionHelp(CvWStringBuffer& szBuffer,
			PlayerTypes selectedCiv);
	  CvWString retireConfirmMsg() const;
	  bool launchRetirePopup(CvPopup* popup, CvPopupInfo& info);
	  void handleRetirePopup(int buttonClicked);
	  bool isSelectingCiv() const; // Waiting for callback
	bool isDeliverMessages(PlayerTypes civId) const;
	bool isCooperationRestricted(PlayerTypes aiCiv) const;
	// Some deals are non-collusive regardless of trade value
	bool isSquareDeal(CLinkList<TradeData> const& humanReceives,
			CLinkList<TradeData> const& aiReceives, PlayerTypes aiCiv) const;
	bool isNeededWarTrade(CLinkList<TradeData> const& humanReceives) const;
	/*  Deal value assuming that certain items like civics changes are of low
		value to the human side. */
	int pessimisticDealVal(PlayerTypes aiCivId, int dealVal,
			CLinkList<TradeData> const& humanReceives) const;
	double dealThresh(bool annual) const;
	// A hack to get the AI to refuse gifts:
	  void substituteDiploText(bool gift);
	  void restoreDiploText();
	// For aligning score breakdowns
	static wchar const* fillWS(int n, bool addPlus = false);
	RFChapter& getChapter(int i) const; // Helps with exposal to Python
	// Exposed to Python through CvGame:
	  std::wstring* chapterScoreBreakdown();
	  std::wstring* riseScoreBreakdown();
	  /*  Named "MaxChapters" in order to make clear that the game may well end
		  before all chapters are through */
	  int getMaxChapters() const;
	  int getCurrentChapter() const;
	  bool isBlockPopups() const;

private:
	RFChapter* mostRecentlyFinished() const;
	void computeEligibleCivs(std::vector<PlayerTypes>& r, bool allowRepeat) const;
	bool isEligible(PlayerTypes civId, bool allowRepeat) const;
	void updateOffLimits();
	CvWString knownName(PlayerTypes civId, bool nameNumber) const;
	int getCivChapter(PlayerTypes civId) const; // -1 if none
	void eligibleByRecommendation(std::vector<PlayerTypes>& r) const;
	static bool byRecommendation(PlayerTypes one, PlayerTypes two);
	void haltForCivSelection(PlayerTypes haltCiv);
	PlayerTypes nextCivAlive(PlayerTypes startExcluded) const;
	void setPlayerControl(PlayerTypes civId, bool b);
	void welcomeToNextChapter(int pos);
	void resetProductionDecay(PlayerTypes civId);
	void centerCamera(PlayerTypes civId);
	void showDoW();
	void showQuests();
	void abandonPlans(PlayerTypes civId);
	void setUIHidden(bool b);
	void setPlayerName();
	bool allSquare(CLinkList<TradeData> const& list, PlayerTypes from,
			PlayerTypes to) const;
	void shutOff(CvWString errorMsg);
	void showError(CvWString errorMsg);
	CvDiplomacyResponse* findThanks();
	void clearDiploStrings();

	int interludeLength;
	std::vector<RFChapter*> chapters;
	std::vector<CvString*> originalThanks;
	std::set<TeamTypes> offLimits;
	RFTotalScore riseScore;
	int interludeCountdown;
	bool selectingCiv;
	bool retryingCivSelection;
	CvWString* originalName;
};

#endif
