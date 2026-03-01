#pragma once

#ifndef ARMAMENT_FORECAST_H
#define ARMAMENT_FORECAST_H

#include "UWAI.h"
#include "UWAICache.h"

class MilitaryAnalyst;
class UWAIReport;
class CvArea;


/*	advc.104: New class. Part of the UWAI military analysis.
	Predicts the military build-up of a given player.
	(I.e. it predicts, in broad strokes, the decisions made by
	CvCityAI::AI_chooseProduction.)
	The computation happens in the constructor.
	NB: The aim is not to predict how many units the player will _own_ on
	a future turn - but how many units will be _trained_, i.e. ignoring losses.
	Losses are predicted when resolving the InvasionGraph.
	Disregards financial trouble since unit cost is rarely a limiting factor
	for AI armament. */
class ArmamentForecast
{
public:
	/*	kMA is making a forecast about ePlayer. The predicted power increase
		is written to kMilitary.
		bPeaceScenario: Assume peace between the agent and target of kMA.
		bPartyAddedRecently: Indicates that this is the first forecast after adding
		any war parties to kMA. Need to figure out if a DoW on ePlayer is recent
		(recently attacked players train more military).
		The pTargetCity from ePlayer's UWAICache is used for figuring out whether
		ePlayer is in a naval war. */
	ArmamentForecast(PlayerTypes ePlayer,
			MilitaryAnalyst const& kMA,
			std::vector<MilitaryBranch*>& kMilitary, int iTimeHorizon,
			bool bPeaceScenario, bool bNoUpgrading,
			bool bPartyAddedRecently, bool bAllPartiesKnown,
			UWAICache::City const* pTargetCity = NULL,
			scaled rProductionPortion = 1); // Remaining after assumed losses of cities
	scaled getProductionInvested() const { return m_rProductionInvested; }

private:
	PlayerTypes m_ePlayer;
	MilitaryAnalyst const& m_kMA;
	PlayerTypes m_eAnalyst;
	UWAIReport& m_kReport;
	std::vector<MilitaryBranch*>& m_kMilitary;
	int m_iTimeHorizon;
	scaled m_rProductionInvested;

	enum Intensity
	{
		DECREASED = -1,
		NORMAL = 0,
		INCREASED,
		FULL,
	};
	static char const* strIntensity(Intensity eIntensity); // for report
	/*	Can eFirst reach eSecond or vice versa. Based on the two teams'
		UWAICache, i.e. a cheat. */
	bool canReachEither(TeamTypes eFirst, TeamTypes eSecond) const;
	// Both directly increase the power values in m_kMilitary
	void predictArmament(int iTurnsBuildUp, scaled rPerTurnProduction,
			/* rAdditionalProduction: Currently, that's unit upgrades converted
			   into production. */
			scaled rAdditionalProduction, Intensity eIntensity, bool bDefensive,
			bool bNavalArmament);
	scaled productionFromUpgrades();
	/*	The Area AI differentiates between continents, the forecast doesn't
		(perhaps it should ...). Only considers the Area AI for the home area --
		which is what this function returns. */
	AreaAITypes getAreaAI(PlayerTypes ePlayer) const;
};

#endif
