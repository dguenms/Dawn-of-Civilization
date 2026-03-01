#pragma once

#ifndef INVASION_GRAPH_H
#define INVASION_GRAPH_H

#include "MilitaryBranch.h"
#include "UWAICache.h"
#include "UWAIReport.h"
#include "UWAISets.h"

class MilitaryAnalyst;
class SimulationStep;
class CvArea;

/*	advc.104: New class; part of the UWAI component, associated with an
	instance of MilitaryAnalyst.
	The invasion graph says who tries to invade whom, and can run a simulation
	of who might conquer which cities (cf. simulate(int)).
	This is analyzed from the perspective of an agent player (the owner of
	the MilitaryAnalyst).
	There's a node in the graph for each civ player that is presently at war or
	is soon going to be. Projected wars are based on the knowledge of the agent,
	i.e. its war plans in preparation and under consideration.
	NB: This class does not _decide_ who targets whom. That happens in CvPlayerAI.
	The invasion graph is a prediction on which the agent bases its decisions
	on war and peace.
	Tbd.: This class does too much and has too many LoC. If everything triggered
	by simulate(int) could be encapsulated in a new class (and file), that would
	be best. Else, at least the step function should be moved into SimulationStep,
	and SimulationStep into a new file. */
class InvasionGraph
{
public:
	friend class Node; // Nested class with full access to outer class

	/*	A Node in an invasion graph. Represents a single player.
		A single outgoing edge represents that player's (primary) target, and
		any incoming edges represent war opponents that the player is targeted by.
		I.e. each player is assumed to focus its attacks on one opponent at a time.
		"Targets" in this context are civ players assumed to be (soon/ in the
		medium term) attacked by invading units. The "target team" during
		war evaluation is a different concept.
		It's important to distinguish the player represented by a Node (m_ePlayer)
		from the player (agent) from whose perspective the graph is computed
		(InvasionGraph::m_eAgent). Only one node in the graph represents the agent. */
	class Node
	{
	public:
		Node(PlayerTypes ePlayer, InvasionGraph const& kOuter);
		~Node();
		void findAndLinkTarget(); // Selects primary target
		void addWarOpponents(PlyrSet const& kWarOpponents);
		// If they aren't war opponents: no effect
		void removeWarOpponents(PlyrSet const& kWarOpponents);
		PlayerTypes getPlayer() const { return m_ePlayer; }
		bool hasTarget() const { return (m_pPrimaryTarget != NULL); }
		bool isIsolated() const { return (!hasTarget() && m_targetedBy.empty()); }

		/*	The rest of the public functions are not to be called
			until the InvasionGraph has been created.
			Might be better to move them elsewhere, e.g. a wrapper. */
		void prepareForSimulation();
		void logTypicalUnits();
		void predictArmament(int iTurns, bool bNoUpgrading = false);
		/*	Follows primaryTarget links backwards recursively and resolves
			(simulated) city losses (by calling resolveLosses). Won't terminate
			when called on a Node that's part of a cycle. */
		void resolveLossesRec();
		/*	Follows primaryTarget links until encountering a cycle.
			The traversed path is stored in kPath. Returns the (path) index of
			the first Node encountered that is part of the cycle. A return value
			of kPath.size() indicates that there is no reachable cycle. */
		size_t findCycle(std::vector<Node*>& kPath);
		// Won't terminate when called on a Node that's part of a cycle
		Node& findSink();
		bool hasLost(PlotNumTypes eCityPlot) const
		{
			return (m_cityLosses.count(eCityPlot) > 0);
		}
		// Updates adjacency lists. NULL deletes an edge.
		void changePrimaryTarget(Node* pNewTarget);
		InvasionGraph::Node* getPrimaryTarget() const { return m_pPrimaryTarget; }
		PlyrSet const& getTargetedBy() const { return m_targetedBy; }
		/*	To be called on the attacker. Caller needs to delete the result.
			Last two parameters only for clash steps */
		SimulationStep* step(scaled rArmyPortionDefender = 0,
				scaled rArmyPortionAttacker = 1, bool bClashOnly = false,
				bool bUniformGarrisons = false) const;
		void applyStep(SimulationStep const& kStep); // To be called on the defender
		void setEliminated(bool b) { m_bEliminated = b; }
		bool isEliminated() const { return m_bEliminated; }
		void resolveLosses();
		/*	Simulates a clash of armies of two Nodes targeting each other.
			This node clashes with its target. The parameters says which
			portion of their respective armies the two nodes commits to the clash. */
		void clash(scaled rArmyPortion, scaled rTargetArmyPortion);
		// For iterating over connected components
		bool isComponentDone() const { return m_bComponentDone; }

		/*	The rest of the public functions are not to be used
			until the simulation has finished ... */
		// Lost power minus shifted power
		scaled getLostPower(MilitaryBranchTypes eBranch) const
		{
			return m_arLostPower[eBranch] - m_arShiftedPower[eBranch];
		}
		// Power after simulation minus initial power
		scaled getGainedPower(MilitaryBranchTypes eBranch) const
		{
			return m_military[eBranch]->power() - m_arCurrentPow[eBranch];
		}
		// Invested during the build-up phases
		scaled getProductionInvested() const { return m_rProductionInvested; }
		/*	City plots included in the conquest and loss sets are guaranteed to exist
			(at the time of the call) in the UWAICache of m_eAgent */
		void getConquests(CitySet& kResult) const;
		void getCityLosses(CitySet& kResult) const;
		bool anyConquests() const { return !m_conquests.empty(); }
		bool anyCityLosses() const { return !m_cityLosses.empty(); }
		/*	Not ideal to store this team-level info at (player) nodes.
			Implemented such that all members of a master team (callees) write
			the same vassal team ids into kResult. */
		void getCapitulationsAccepted(TeamSet& kResult) const;
		// Only true if capitulated during the simulation.
		bool hasCapitulated() const { return m_bCapitulated; }

	private:
		InvasionGraph const& m_kOuter;
		UWAIReport& m_kReport;
		PlayerTypes m_ePlayer;
		PlayerTypes m_eAgent;
		PlyrSet m_warOpponents;
		std::vector<bool> m_abWarOpponent;
		std::vector<MilitaryBranch*> m_military;
		std::vector<scaled> m_arCurrentPow;
		scaled m_rProductionInvested;
		bool m_bEliminated;
		bool m_bCapitulated;
		bool m_bHasClashed;
		Node* m_pPrimaryTarget; // outgoing edge
		PlyrSet m_targetedBy; // Adjacency list (incoming edges)

		void initMilitary();
		int countUnitsWithAI(std::vector<UnitAITypes> aeAITypes) const;
		void logPower(char const* szMsg) const;
		/*	eExtra: Team (and its vassals) to be considered as the target
			(in addition to m_warOpponents). */
		PlayerTypes findTarget(TeamTypes eExtra = NO_TEAM) const;
		PlayerTypes findBestTarget(TeamTypes eExtra) const;
		bool isValidTarget(UWAICache::City const& kCacheCity, TeamTypes eExtra = NO_TEAM) const;
		bool isValidTarget(PlayerTypes eTarget, TeamTypes eExtra) const;

		/*	The rest of the private members are for simulations;
			call prepareForSimulation before using them. */
		std::vector<UWAICache::City const*> m_conquests;
		CitySet m_cityLosses;
		TeamSet m_capitulationsAccepted;
		UWAICache& m_kCache;
		UWAICache const& m_kAgentCache;
		int m_iCacheIndex;
		scaled m_arLostPower[NUM_BRANCHES];
		/*	Units shifted from e.g. army to guard are counted as losses.
			For war utility, may want to count them differently. To allow this,
			shifts are also tracked separately. Only records the branch that
			power is shifted away from. */
		scaled m_arShiftedPower[NUM_BRANCHES];
		scaled m_rEmergencyDefPow;
		bool m_bComponentDone;
		int m_iWarTurnsSimulated; // (For resolveLosses; currently not used.)
		scaled m_rTempArmyLosses;
		/*	Measure of (temporary) distraction: defense less effective while
			trying to conquer cities of a third player, and conquest less effective
			while trying to fend off a third player. */
		scaled m_rDistractionByConquest;
		scaled m_rDistractionByDefense;

		scaled productionPortion() const; // Remaining production capacity after losses
		UWAICache::City const* targetCity(
				// Default: based on m_pPrimaryTarget
				PlayerTypes eTargetOwner = NO_PLAYER) const;
		void addConquest(UWAICache::City const& kConqCity);
		void addCityLoss(UWAICache::City const& kLostCity)
		{
			m_cityLosses.insert(kLostCity.getID());
		}
		// (Vassals that break free are not modeled)
		void setCapitulated(TeamTypes eMaster);
		scaled clashDistance(Node const& kOther) const;
		bool isSneakAttack(Node const& kOther, bool bClash) const;
		bool isContinuedWar(Node const& kOther) const;
		bool canReachByLand(PlotNumTypes eCityPlot, bool bFromCapital) const;
		CvArea const* clashArea(PlayerTypes eEnemy) const;

		/*	Tbd.: Should create a small class for this stuff. Related:
			Losses from city attack. */
		static scaled const m_rClashPortion;
		static std::pair<scaled,scaled> clashLossesWinnerLoser(
				scaled rPowAtt, scaled rPowDef,
				bool bNearCity = true, bool bNaval = false);
		static scaled clashLossesTemporary(scaled rPowAtt, scaled rPowDef)
		{
			return m_rClashPortion * std::min(rPowAtt, rPowDef) / 3;
		}
		static scaled stake(scaled rPowAtt, scaled rPowDef)
		{
			return m_rClashPortion * scaled::min(1, fixp(1.6) *
					powRatio(rPowAtt, rPowDef));
		}
		static scaled powRatio(scaled rFirstPow, scaled rSecondPow)
		{
			return std::min(rFirstPow, rSecondPow) /
					std::max(std::max(rFirstPow, rSecondPow), scaled::epsilon());
		}
	};

public:
	InvasionGraph(MilitaryAnalyst& kMilitaryAnalyst, PlyrSet const& kWarParties,
			bool bPeaceScenario = false);
	~InvasionGraph();
	Node* getNode(PlayerTypes ePlayer) const
	{
		FAssertBounds(0, MAX_PLAYERS, ePlayer);
		return m_nodeMap[ePlayer];
	}
	/*	No military build-up is estimated by simulate(int) until
		this function is called. Intended to be called exactly once.
		"Our side" being the agent (military analyst). */
	void addFutureWarParties(PlyrSet const& kOurSide, PlyrSet const& kOurFutureOpponents);
	// Call this before a simulation that assumes a peace treaty with the target
	void removeWar(PlyrSet const& kOurSide, PlyrSet const& kTheirSide);
	// (No need to call this after addFutureWarParties or removeWar; done internally.)
	void updateTargets();
	/*	Makes sure that these (possibly uninvolved) parties have nodes in the graph
		(and ArmamentForecasts). */
	void addUninvolvedParties(PlyrSet const& KParties);
	/*	Duration: Time horizon of the simulation. Affects the estimated military
		armament (if addFutureWarParties is called beforehand). Not suitable
		for long-term predictions (e.g. > 50 turns).
		No military build-up is assumed for the first phase.
		Simulates conquests and unit losses (expressed as a loss of power).
		These results are stored in the affected Node instances. */
	void simulate(int iTurns);

private:
	// Caveat: The order of the reference members is important for the constructor
	PlyrSet const& m_kWarParties;
	std::vector<Node*> m_nodeMap;
	MilitaryAnalyst& m_kMA;
	PlayerTypes m_eAgent;
	UWAIReport& m_kReport;
	bool m_bAllWarPartiesKnown;
	int m_iTimeLimit; // for simulateLosses
	bool m_bPeaceScenario;
	bool m_bLossesDone; // for deciding on recentlyAttacked
	bool m_bFirstSimulateCall;

	void simulateArmament(int iTurns, bool bNoUpgrading = false);
	void simulateLosses();
	/*	Simulation of the connected component containing kStart. This function
		will mark all encountered nodes as bComponentDone so that the caller
		can avoid simulating the same component twice. */
	void simulateComponent(Node& kStart);
	// (kCycle isn't modified, but the contained Nodes are.)
	void breakCycle(std::vector<Node*> const& kCycle);
	scaled willingness(PlayerTypes eAggressor, PlayerTypes eTarget) const;
};

/*	The results of a simulation step. A simulation step is either a clash step
	or a city attack step. The former is about two armies meeting in the field,
	the latter about an attacking army trying to conquer a city (which may also
	involve an open battle).
	The calculation happens in InvasionGraph::Node (with access to
	private members). The results are stored in instances of this class.
	Not handled by this class:
	If a city is contested between more than two war parties, then there are
	several SimulationStep objects, and only one of them is going to be applied
	(by changing the two respective Nodes). */
class SimulationStep
{
public:
	SimulationStep(PlayerTypes eAttacker, UWAICache::City const* pContestedCity = NULL);
	void setDuration(int iTurns) { m_iDuration = iTurns; }
	/*	ePlayer should be attacker or the defender (attacker's target). (Other player ids
		are treated as the defender.) */
	void reducePower(PlayerTypes ePlayer, MilitaryBranchTypes eBranch, scaled rSubtrahend);
	void setSuccess(bool b) { m_bSuccess = b; }
	void setThreat(scaled rThreat) { m_rThreat = rThreat; }
	/*	The defending army is assumed to be split to meet simultaneous attacks
		based on the attacks' threat values */
	scaled getThreat() const { return m_rThreat; }
	int getDuration() const { return m_iDuration; }
	// See reducePower
	scaled getLostPower(PlayerTypes ePlayer, MilitaryBranchTypes eBranch) const;
	// Temporary losses of attacking army
	scaled getTempLosses() const { return m_rTempLosses; }
	void setTempLosses(scaled rTempLosses) { m_rTempLosses = rTempLosses; }
	bool isAttackerSuccessful() const { return m_bSuccess; }
	bool isClashOnly() const { return (m_pContestedCity == NULL); }
	PlayerTypes getAttacker() const { return m_eAttacker; }
	UWAICache::City const* getCity() const { return m_pContestedCity; }

private:
	int m_iDuration;
	scaled m_rThreat;
	scaled m_arLostPowerAttacker[NUM_BRANCHES];
	scaled m_arLostPowerDefender[NUM_BRANCHES];
	PlayerTypes m_eAttacker; // (Defender is the attacker's primary target)
	UWAICache::City const* m_pContestedCity;
	bool m_bSuccess;
	scaled m_rTempLosses;
};

#endif
