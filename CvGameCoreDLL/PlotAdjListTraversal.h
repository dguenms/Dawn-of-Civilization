#pragma once

#ifndef PLOT_ADJ_LIST_TRAVERSAL_H
#define PLOT_ADJ_LIST_TRAVERSAL_H

// advc.003s: Macros for traversing the adjacency list of a CvPlot

// Helpers ...

#define iANON_ADJ_LIST_POS CONCATVARNAME(iAnonAdjListPos_, __LINE__)
/*	kCenterPlot in the macro below can be e.g. a conditional expression.
	Don't want to evaluate that more than once. */
#define kANON_CACHED_CENTER_PLOT CONCATVARNAME(kAnonCachedCenterPlot_, __LINE__)

#define FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlotType, iInitialPos, iStep) \
	CvPlot const& kANON_CACHED_CENTER_PLOT = (kCenterPlot); \
	int iANON_ADJ_LIST_POS = iInitialPos; \
	for (CvPlotType* pLoopPlot; \
		/* Need to do the loop step as part of the termination check */ \
		/* to avoid stepping out of bounds */ \
		iANON_ADJ_LIST_POS < kANON_CACHED_CENTER_PLOT.numAdjacentPlots() && \
		(pLoopPlot = kANON_CACHED_CENTER_PLOT.getAdjacentPlotUnchecked(iANON_ADJ_LIST_POS), true) && \
		(iANON_ADJ_LIST_POS += iStep, true); )

#define aiANON_ADJ_LIST_INDICES CONCATVARNAME(aiAnonAdjListIndices, __LINE__)

#define FOR_EACH_ADJ_PLOT_RAND_HELPER(kCenterPlot, pLoopPlot, CvPlotType, kRand) \
	std::vector<int> aiANON_ADJ_LIST_INDICES((kCenterPlot).numAdjacentPlots()); \
	(kRand).shuffle(aiANON_ADJ_LIST_INDICES); \
	int iANON_ADJ_LIST_POS = 0; \
	for (CvPlotType* pLoopPlot; \
		iANON_ADJ_LIST_POS < (kCenterPlot).numAdjacentPlots() && \
		(pLoopPlot = (kCenterPlot).getAdjacentPlotUnchecked( \
		aiANON_ADJ_LIST_INDICES[iANON_ADJ_LIST_POS]), true) && \
		(iANON_ADJ_LIST_POS++, true); )

typedef CvPlot const CvPlot_const_t; // Looks a bit ugly in IntelliSense :(

/*	16 combinations:
	const vs. variable,
	automatically named loop variable vs. manually named (2-argument macro),
	all adjacent plots vs. only cardinal directions vs. only intermediate directions.
	Plus 4 combinations with randomized order (only for all adjacent plots). */
#define FOR_EACH_ADJ_PLOT(kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pAdj, CvPlot_const_t, 0, 1)
#define FOR_EACH_ADJ_PLOT_VAR(kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pAdj, CvPlot, 0, 1)
#define FOR_EACH_ADJ_PLOT2(pLoopPlot, kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlot_const_t, 0, 1)
#define FOR_EACH_ADJ_PLOT_VAR2(pLoopPlot, kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlot, 0, 1)
#define FOR_EACH_ORTH_ADJ_PLOT(kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pAdj, CvPlot_const_t, 0, 2)
#define FOR_EACH_ORTH_ADJ_PLOT_VAR(kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pAdj, CvPlot, 0, 2)
#define FOR_EACH_ORTH_ADJ_PLOT2(pLoopPlot, kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlot_const_t, 0, 2)
#define FOR_EACH_ORTH_ADJ_PLOT_VAR2(pLoopPlot, kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlot, 0, 2)
#define FOR_EACH_DIAG_ADJ_PLOT(kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pAdj, CvPlot_const_t, 1, 2)
#define FOR_EACH_DIAG_ADJ_PLOT_VAR(kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pAdj, CvPlot, 1, 2)
#define FOR_EACH_DIAG_ADJ_PLOT2(pLoopPlot, kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlot_const_t, 1, 2)
#define FOR_EACH_DIAG_ADJ_PLOT_VAR2(pLoopPlot, kCenterPlot) \
	FOR_EACH_ADJ_PLOT_HELPER(kCenterPlot, pLoopPlot, CvPlot, 1, 2)

#define FOR_EACH_ADJ_PLOT_RAND(kCenterPlot, kRand) \
	FOR_EACH_ADJ_PLOT_RAND_HELPER(kCenterPlot, pAdj, CvPlot_const_t, kRand)
#define FOR_EACH_ADJ_PLOT_VAR_RAND(kCenterPlot, kRand) \
	FOR_EACH_ADJ_PLOT_RAND_HELPER(kCenterPlot, pAdj, CvPlot, kRand)
#define FOR_EACH_ADJ_PLOT_RAND2(pLoopPlot, kCenterPlot, kRand) \
	FOR_EACH_ADJ_PLOT_RAND_HELPER(kCenterPlot, pLoopPlot, CvPlot_const_t, kRand)
#define FOR_EACH_ADJ_PLOT_VAR_RAND2(pLoopPlot, kCenterPlot, kRand) \
	FOR_EACH_ADJ_PLOT_RAND_HELPER(kCenterPlot, pLoopPlot, CvPlot, kRand)

#endif
