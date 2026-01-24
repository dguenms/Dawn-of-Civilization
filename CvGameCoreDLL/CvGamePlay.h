#pragma once

#ifndef CIV4_GAME_PLAY_H
#define CIV4_GAME_PLAY_H // Caveat: This guard gets referenced in other headers too

/*  advc.make: Wrapper header to reduce the number of include statements and
	a place for the team accessor macros. (However, the one that returns a CvTeamAI
	reference is defined in CoreAI.h.) For inline definitions, both CvPlayer.h
	and CvTeam.h are needed. */

#include "CvGame.h"
#include "CvTeam.h"
#include "CvPlayer.h"
#include "AgentIterator.h" // advc.agent
#include "CvCivilization.h" // advc.003w

// <advc.003u>
#ifndef COREAI_H // Overwrite CvTeam(AI).h, but yield to CoreAI.h.
#undef GET_TEAM
#define GET_TEAM(x) CvGamePlay::getTeam(x)
#endif
#define TEAMID(x) GET_PLAYER(x).getTeam()

namespace CvGamePlay
{
	__forceinline CvTeam& getTeam(TeamTypes eTeam)
	{
		return CvTeam::getTeam(eTeam);
	}
	__forceinline CvTeam& getTeam(PlayerTypes ePlayer)
	{
		return CvTeam::getTeam(TEAMID(ePlayer));
	}
} // </advc.003u>

#endif
