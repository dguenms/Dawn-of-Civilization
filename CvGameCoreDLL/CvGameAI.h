#pragma once

#ifndef CIV4_GAME_AI_H
#define CIV4_GAME_AI_H

#include "CvGame.h"
#include "UWAI.h" // advc.104


class CvGameAI : public CvGame
{
public:

	CvGameAI();
	~CvGameAI();

	void AI_init();
	void AI_initScenario(); // advc.104u
	void AI_uninit();
	void AI_reset(bool bConstructor = false);

	void AI_makeAssignWorkDirty();
	void AI_updateAssignWork();

	int AI_combatValue(UnitTypes eUnit) const;

	int AI_turnsPercent(int iTurns, int iPercent) const;
	// <advc.erai>
	scaled AI_getCurrEraFactor() const;
	int AI_getCurrEra() const { return AI_getCurrEraFactor().uround(); }
	EraTypes AI_getVoteSourceEra(VoteSourceTypes eVS = NO_VOTESOURCE) const;
	// </advc.erai>
	scaled AI_exclusiveRadiusWeight(int iDist = -1) const; // advc.099b
	void AI_updateVictoryWeights(); // advc.115f
	int AI_getMaxCultureLevelPercent() const { return m_iMaxCultureLevelPercent; } // advc.251

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

	UWAI& uwai() { return m_uwai; } // advc.104

protected:

	//int m_iPad; // advc: unused
	int m_iMaxCultureLevelPercent; // advc.251
	// <advc.104>
	UWAI m_uwai;
	void AI_sortOutUWAIOptions(bool bFromSaveGame);
	// </advc.104>
	ArrayEnumMap<VoteSourceTypes,EraTypes> m_aeVoteSourceEras; // advc.erai
	std::vector<scaled> m_arExclusiveRadiusWeight; // advc.099b

	void AI_updateExclusiveRadiusWeight(); // advc.009b
	void AI_updateVoteSourceEras(); // advc.erai
	void AI_updateMaxCultureLevelPercent(); // advc.251
};

#endif
