#pragma once

#ifndef UWAI_H
#define UWAI_H

class FDataStreamBase;

/*  advc.104: AI functionality for decisions on war and peace.
	Main class of the Utility-Based War AI component (UWAI).
	Instead of making lots of additions to CvTeamAI and CvPlayerAI, I've put the
	new functions in classes UWAI::Team and UWAI::Player, which are
	defined in UWAIAgent.h. The outer class UWAI shared by Team and Player is
	for overarching stuff that would otherwise fit into CvGameAI or
	CvGameCoreUtils. An instance is accessible through the macro "getUWAI".

	The main function for war planning is UWAI::Team::doWar. */

// The parentheses are unnecessary, but I think it's more intuitive this way.
#define getUWAI() GC.AI_getGame().uwai()


/*	Setting this to 1 should remove almost all runtime overhead from logging in
	optimized release builds. The overhead should be pretty small in any case,
	so I'd rather keep logging available (via an XML switch) in releases. */
#define DISABLE_UWAI_REPORT 0

class UWAI : private boost::noncopyable
{
public:
	// Nested classes; defined in UWAIAgent.h.
	class Player;
	class Team;

	UWAI();
	void invalidateUICache();
	// When a colonial vassal is created
	void initNewPlayerInGame(PlayerTypes eNewPlayer);
	// When the colonial vassal has received a capital and tech
	void processNewPlayerInGame(PlayerTypes eNewPlayer);
	/*  true if UWAI fully enabled, making all decisions, otherwise false.
		If bInBackground is set, then true if UWAI is running only in the background
		(through an XML switch), but false if UWAI fully enabled or fully disabled. */
	bool isEnabled(bool bInBackground = false) const; // Exposed to Python via CyGame::useKModAI
	void setUseLegacyAI(bool b);
	void setInBackground(bool b);
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream) const;
	int maxLandDist() const { return maxSeaDist() - 1; }
	int maxSeaDist() const;
	bool isReady() const;

	int preparationTimeLimited() const { return 8; }
	int preparationTimeLimitedNaval() const { return 10; }
	int preparationTimeTotal() const { return 15; }
	int preparationTimeTotalNaval() const { return 20; }

	void doXML();
	#define DO_FOR_EACH_WAR_UTILITY_ASPECT(DO)\
		DO(GREED_FOR_ASSETS) \
		DO(GREED_FOR_VASSALS) \
		DO(GREED_FOR_SPACE) \
		DO(GREED_FOR_CASH) \
		DO(LOATHING) \
		DO(MILITARY_VICTORY) \
		DO(PRESERVATION_OF_PARTNERS) \
		DO(RECONQUISTA) \
		DO(REBUKE) \
		DO(FIDELITY) \
		DO(HIRED_HAND) \
		DO(BORDER_DISPUTES) \
		DO(SUCKING_UP) \
		DO(PREEMPTIVE_WAR) \
		DO(KING_MAKING) \
		DO(EFFORT) \
		DO(RISK) \
		DO(ILL_WILL) \
		DO(AFFECTION) \
		DO(DISTRACTION) \
		DO(PUBLIC_OPPOSITION) \
		DO(REVOLTS) \
		DO(ULTERIOR_MOTIVES) \
		DO(FAIR_PLAY) \
		DO(BELLICOSITY) \
		DO(TACTICAL_SITUATION) \
		DO(LOVE_OF_PEACE) \
		DO(THIRD_PARTY_INTERVENTION) \
		DO(DRAMATIC_ARC)
	enum AspectTypes
	{
		DO_FOR_EACH_WAR_UTILITY_ASPECT(MAKE_ENUMERATOR)
		NUM_ASPECTS
	};
	scaled aspectWeight(AspectTypes eAspect) const
	{
		FAssertBounds(0, NUM_ASPECTS, eAspect);
		return per100(m_aiXmlWeights[eAspect]);
	}
	char const* aspectName(AspectTypes eAspect) const
	{
		FAssertBounds(0, NUM_ASPECTS, eAspect);
		return m_aszAspectNames[eAspect];
	}

private:
	std::vector<int> m_aiXmlWeights;
	std::vector<char const*> m_aszAspectNames;
	bool m_bEnabled; // false iff Legacy AI enabled through game option
	bool m_bInBackground; // status of background switch in XML

	void applyPersonalityWeight();
};

#endif
