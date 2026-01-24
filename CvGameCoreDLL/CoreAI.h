#pragma once

#ifndef COREAI_H
#define COREAI_H // Caveat: This guard gets referenced in other headers too

// advc.make: Wrapper header to reduce the number of include directives

#include "CvGamePlay.h" // The AI headers aren't much good w/o the core gameplay headers
#include "CvGameAI.h"
#include "CvTeamAI.h"
#include "CvPlayerAI.h"

// <advc.003u> Overwrite the definitions in CvGamePlay.h and CvTeamAI.h
#undef GET_TEAM
#define GET_TEAM(x) CoreAI::getTeam(x)

namespace CoreAI
{
	__forceinline CvTeamAI& getTeam(TeamTypes eTeam)
	{
		return CvTeamAI::AI_getTeam(eTeam);
	}
	__forceinline CvTeamAI& getTeam(PlayerTypes ePlayer)
	{
		return CvTeamAI::AI_getTeam(TEAMID(ePlayer));
	}
} // </advc.003u>

#endif
