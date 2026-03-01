#pragma once

#ifndef AI_STRATEGIES_H // advc: Renamed this file from AI_Defines.h
#define AI_STRATEGIES_H

// BETTER_BTS_AI_MOD, 03/08/10, jdog5000: START
// Could increase this value now that player closeness is fixed
#define DEFAULT_PLAYER_CLOSENESS 7

#define AI_DAGGER_THRESHOLD			100  //higher is a lower chance

enum AIStrategy // advc.enum: To avoid mixup with victory strategies (was #define)
{
	NO_AI_STRATEGY					=	0, // advc.enum
// Military strategies based on power, war status
	AI_DEFAULT_STRATEGY				=	(1 << 0),
	AI_STRATEGY_DAGGER              =	(1 << 1),   // Aggressive early game
	AI_STRATEGY_CRUSH				=	(1 << 2),   // Convert units to City Attack
	AI_STRATEGY_ALERT1				=	(1 << 3),   // Likely attack from neighbor
	AI_STRATEGY_ALERT2				=	(1 << 4),   // Seemingly imminent attack from enemy
	AI_STRATEGY_TURTLE              =	(1 << 5),   // Defensive shell
	AI_STRATEGY_LAST_STAND			=	(1 << 6),
	AI_STRATEGY_FINAL_WAR			=	(1 << 7),
// Military strategies based on analysis of trainable units
	AI_STRATEGY_GET_BETTER_UNITS	=	(1 << 8),
	AI_STRATEGY_FASTMOVERS          =	(1 << 9),
	AI_STRATEGY_LAND_BLITZ			=	(1 << 10),
	AI_STRATEGY_AIR_BLITZ			=	(1 << 11),
	AI_STRATEGY_OWABWNW				=	(1 << 12),	// "Our words are backed with nuclear weapons"
// Domestic strategies
	AI_STRATEGY_PRODUCTION          =	(1 << 13),
	AI_STRATEGY_MISSIONARY          =	(1 << 14),
	AI_STRATEGY_BIG_ESPIONAGE		=	(1 << 15),
	// K-Mod - catch up in tech, at the expense of military
	AI_STRATEGY_ECONOMY_FOCUS       =	(1 << 16),
	// K-Mod - run high espionage slider to steal techs at a discount.
	AI_STRATEGY_ESPIONAGE_ECONOMY   =	(1 << 17),
};

// AI victory stages
enum AIVictoryStage // advc: replacing preprocessor defines
{
	NO_AI_VICTORY_STAGE				=	0, // advc.enum
	AI_DEFAULT_VICTORY_STAGE		=	(1 << 0),
	AI_VICTORY_SPACE1				=	(1 << 1),
	AI_VICTORY_SPACE2				=	(1 << 2),
	AI_VICTORY_SPACE3				=	(1 << 3),
	AI_VICTORY_SPACE4				=	(1 << 4),
	AI_VICTORY_CONQUEST1			=	(1 << 5),
	AI_VICTORY_CONQUEST2			=	(1 << 6),
	AI_VICTORY_CONQUEST3			=	(1 << 7),
	AI_VICTORY_CONQUEST4			=	(1 << 8),
	AI_VICTORY_CULTURE1				=	(1 << 9),   //religions and wonders
	AI_VICTORY_CULTURE2				=	(1 << 10),  //mass culture buildings
	AI_VICTORY_CULTURE3				=	(1 << 11),  //culture slider
	AI_VICTORY_CULTURE4				=	(1 << 12),
	AI_VICTORY_DOMINATION1			=	(1 << 13),
	AI_VICTORY_DOMINATION2			=	(1 << 14),
	AI_VICTORY_DOMINATION3			=	(1 << 15),
	AI_VICTORY_DOMINATION4			=	(1 << 16),
	AI_VICTORY_DIPLOMACY1			=	(1 << 17),
	AI_VICTORY_DIPLOMACY2			=	(1 << 18),
	AI_VICTORY_DIPLOMACY3			=	(1 << 19),
	AI_VICTORY_DIPLOMACY4			=	(1 << 20),
	AI_VICTORY_MILITARY1			=	AI_VICTORY_DOMINATION1 | AI_VICTORY_CONQUEST1,
	AI_VICTORY_MILITARY2			=	AI_VICTORY_DOMINATION2 | AI_VICTORY_CONQUEST2,
	AI_VICTORY_MILITARY3			=	AI_VICTORY_DOMINATION3 | AI_VICTORY_CONQUEST3,
	AI_VICTORY_MILITARY4			=	AI_VICTORY_DOMINATION4 | AI_VICTORY_CONQUEST4,
};
// BETTER_BTS_AI_MOD: END
// advc: Added by the BtS expansion; has (sadly perhaps) remained unused.
/*enum AICityRole
{
	AI_CITY_ROLE_VALID              =	(1 <<  1),	//zero is bad
	AI_CITY_ROLE_BIG_CULTURE        =	(1 <<  2),	//culture victory, probably
	AI_CITY_ROLE_BIG_PRODUCTION     =	(1 <<  3),	//don't build girly NW's
	AI_CITY_ROLE_BIG_MILITARY       =	(1 <<  4),	//stick with military stuff
	AI_CITY_ROLE_SCIENCE            =	(1 <<  5),	//
	AI_CITY_ROLE_GOLD               =	(1 <<  6),	//
	AI_CITY_ROLE_PRODUCTION         =	(1 <<  7),	//
	AI_CITY_ROLE_SPECIALIST         =	(1 <<  8),	//
	AI_CITY_ROLE_FISHING            =	(1 <<  9),	//
	AI_CITY_ROLE_STAGING            =	(1 << 10),	//send troops here
	AI_CITY_ROLE_LINCHPIN            =	(1 << 11),	//this city must not fall
};
// <advc.enum>
OVERLOAD_BITWISE_OPERATORS(AICityRole)*/
OVERLOAD_BITWISE_OPERATORS(AIStrategy)
OVERLOAD_BITWISE_OPERATORS(AIVictoryStage)
// </advc.enum>

#endif // AI_DEFINES_H
