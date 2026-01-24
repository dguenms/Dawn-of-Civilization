#pragma once

#ifndef FREE_LIST_TRAVERSAL_H
#define FREE_LIST_TRAVERSAL_H

// advc.003s: Macros for traversing FFreeListTrashArray
// advc.003u: Added variants that provide a pointer to an AI object (e.g. FOR_EACH_UNITAI).

/*  All FOR_EACH macros need to be listed in cpp.hint so that Visual Studio can
	parse them properly! Otherwise, the navigation bar will show "Global Scope"
	for any functions that use the macros. (At least in VS2010; perhaps not an issue
	with more recent versions.) */

#define iANON_FREELIST_POS CONCATVARNAME(iAnonFreeListPos_, __LINE__)

/*  pointerType argument to allow the caller to choose AI or non-AI type and
	const or non-const. -- Not intuitive enough; create a separate macro for every
	combination instead. */
/*#define FOR_EACH_UNIT(pointerType, pUnit, kOwner) \
	int iANON_FREELIST_POS; \
	for(pointerType* pUnit = (kOwner).AI_firstUnit(&iANON_FREELIST_POS); pCity != NULL; pCity = (kOwner).AI_nextUnit(&iANON_FREELIST_POS))*/

// Make const the default (shortest macro name)
#define FOR_EACH_UNIT(pUnit, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvUnit const* pUnit = (kOwner).firstUnit(&iANON_FREELIST_POS); pUnit != NULL; pUnit = (kOwner).nextUnit(&iANON_FREELIST_POS))
#define FOR_EACH_UNIT_VAR(pUnit, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvUnit* pUnit = (kOwner).firstUnit(&iANON_FREELIST_POS); pUnit != NULL; pUnit = (kOwner).nextUnit(&iANON_FREELIST_POS))
#define FOR_EACH_UNITAI(pUnit, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvUnitAI const* pUnit = (kOwner).AI_firstUnit(&iANON_FREELIST_POS); pUnit != NULL; pUnit = (kOwner).AI_nextUnit(&iANON_FREELIST_POS))
#define FOR_EACH_UNITAI_VAR(pUnit, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvUnitAI* pUnit = (kOwner).AI_firstUnit(&iANON_FREELIST_POS); pUnit != NULL; pUnit = (kOwner).AI_nextUnit(&iANON_FREELIST_POS))

#define FOR_EACH_CITY(pCity, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvCity const* pCity = (kOwner).firstCity(&iANON_FREELIST_POS); pCity != NULL; pCity = (kOwner).nextCity(&iANON_FREELIST_POS))
#define FOR_EACH_CITY_VAR(pCity, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvCity* pCity = (kOwner).firstCity(&iANON_FREELIST_POS); pCity != NULL; pCity = (kOwner).nextCity(&iANON_FREELIST_POS))
#define FOR_EACH_CITYAI_VAR(pCity, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvCityAI* pCity = (kOwner).AI_firstCity(&iANON_FREELIST_POS); pCity != NULL; pCity = (kOwner).AI_nextCity(&iANON_FREELIST_POS))
#define FOR_EACH_CITYAI(pCity, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvCityAI const* pCity = (kOwner).AI_firstCity(&iANON_FREELIST_POS); pCity != NULL; pCity = (kOwner).AI_nextCity(&iANON_FREELIST_POS))

#define FOR_EACH_GROUP(pGroup, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvSelectionGroup const* pGroup = (kOwner).firstSelectionGroup(&iANON_FREELIST_POS); pGroup != NULL; pGroup = (kOwner).nextSelectionGroup(&iANON_FREELIST_POS))
#define FOR_EACH_GROUP_VAR(pGroup, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvSelectionGroup* pGroup = (kOwner).firstSelectionGroup(&iANON_FREELIST_POS); pGroup != NULL; pGroup = (kOwner).nextSelectionGroup(&iANON_FREELIST_POS))
#define FOR_EACH_GROUPAI(pGroup, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvSelectionGroupAI const* pGroup = (kOwner).AI_firstSelectionGroup(&iANON_FREELIST_POS); pGroup != NULL; pGroup = (kOwner).AI_nextSelectionGroup(&iANON_FREELIST_POS))
#define FOR_EACH_GROUPAI_VAR(pGroup, kOwner) \
	int iANON_FREELIST_POS; \
	for(CvSelectionGroupAI* pGroup = (kOwner).AI_firstSelectionGroup(&iANON_FREELIST_POS); pGroup != NULL; pGroup = (kOwner).AI_nextSelectionGroup(&iANON_FREELIST_POS))

/*  To avoid calling GC.getMap() in every iteration; probably makes no difference,
	but don't want to rely on inlining too much. */
#define MAPVARNAME CONCATVARNAME(kMap_, __LINE__)

#define FOR_EACH_AREA(pArea) \
	int iANON_FREELIST_POS; CvMap const& MAPVARNAME = GC.getMap(); \
	for(CvArea const* pArea = MAPVARNAME.firstArea(&iANON_FREELIST_POS); pArea != NULL; pArea = MAPVARNAME.nextArea(&iANON_FREELIST_POS))
#define FOR_EACH_AREA_VAR(pArea) \
	int iANON_FREELIST_POS; CvMap const& MAPVARNAME = GC.getMap(); \
	for(CvArea* pArea = MAPVARNAME.firstArea(&iANON_FREELIST_POS); pArea != NULL; pArea = MAPVARNAME.nextArea(&iANON_FREELIST_POS))

#define GAMEVARNAME CONCATVARNAME(kGame_, __LINE__)

#define FOR_EACH_DEAL(pDeal) \
	int iANON_FREELIST_POS; CvGame const& GAMEVARNAME = GC.getGame(); \
	for(CvDeal const* pDeal = GAMEVARNAME.firstDeal(&iANON_FREELIST_POS); pDeal != NULL; pDeal = GAMEVARNAME.nextDeal(&iANON_FREELIST_POS))
#define FOR_EACH_DEAL_VAR(pDeal) \
	int iANON_FREELIST_POS; CvGame const& GAMEVARNAME = GC.getGame(); \
	for(CvDeal* pDeal = GAMEVARNAME.firstDeal(&iANON_FREELIST_POS); pDeal != NULL; pDeal = GAMEVARNAME.nextDeal(&iANON_FREELIST_POS))

#endif
