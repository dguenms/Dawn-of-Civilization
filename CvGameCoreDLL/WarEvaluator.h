#pragma once

#ifndef WAR_EVALUATOR_H
#define WAR_EVALUATOR_H

class WarEvalParameters;
class WarUtilityAspect;
class UWAIReport;

/*	advc.104: New class. Computes the utility of a war between an
	"agent" team and a "target" team from the agent's point of view. */
class WarEvaluator
{
public:
	// The cache should only be used for UI purposes; see comments in implementation file.
	WarEvaluator(WarEvalParameters& kWarEvalParams, bool bUseCache = false);

	/*	Can be called repeatedly on the same instance for different
		war plan types. If eWarPlan=NO_WARPLAN, then the current war plan
		is evaluated, LIMITED_WAR if none.
		Preparation time -1 lets WarEvaluator choose a preparation time matching
		the war plan type, the war plan age and other factors.
		(The base values are defined in UWAIAI.h.)
		Use 0 prep time for wars that have to be declared immediately
		(e.g. sponsored wars).
		Returns the war utility value. 100 is very high, 0 is no gain and no pain,
		-100 very small, but values can be (several times) higher or smaller than that.
		Will store in the WarEvalParamters instance (passed to the constructor) which
		war plan type and preparation time are assumed and whether it'll be a naval war. */
	/*	The first evaluate function lets WarEvaluator decide whether naval war
		is preferable. */
	int evaluate(WarPlanTypes eWarPlan = NO_WARPLAN, int iPreparationTime = -1);
	int evaluate(WarPlanTypes eWarPlan, bool bNaval, int iPreparationTime);
	int defaultPreparationTime(WarPlanTypes eWarPlan = NO_WARPLAN);

private:
	void reportPreamble();
	/*	Utility from pov of an individual agent member. Will evaluate the aspects
		(which may modify the aspect instances). */
	void evaluate(PlayerTypes eAgentPlayer, std::vector<WarUtilityAspect*>& kAspects);
	/*  Creates the top-level war utility aspects: war gains and war costs;
		the aspect objects create their sub-aspects themselves. */
	void fillWithAspects(std::vector<WarUtilityAspect*>& kAspects);

	// Caveat: The order of the reference members is important for the ctor
	WarEvalParameters& m_kParams;
	CvTeamAI& m_kTarget;
	CvTeamAI& m_kAgent;
	UWAIReport& m_kReport;
	bool m_bPeaceScenario;
	bool m_bUseCache;

	bool atTotalWarWithTarget() const;
	void gatherCivsAndTeams();

	public:
		/*  If (or while) enabled, all WarEvaluator instances use the cache, not just
			those with useCache=true. */
		static void enableCache();
		static void disableCache();
		static void clearCache(); // Invalidates the cache (disableCache does not do so)
	private:
		static bool m_bCheckCache;
		static bool m_bCacheCleared;
};

#endif
