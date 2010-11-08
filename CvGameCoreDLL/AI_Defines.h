#pragma once

#ifndef AI_DEFINES_H
#define AI_DEFINES_H

#define DEFAULT_PLAYER_CLOSENESS 6
#define AI_DAGGER_THRESHOLD			100  //higher is a lower chance

#define AI_DEFAULT_STRATEGY             (1 << 0)
#define AI_STRATEGY_DAGGER              (1 << 1)
#define AI_STRATEGY_SLEDGEHAMMER        (1 << 2)
#define AI_STRATEGY_CASTLE              (1 << 3)
#define AI_STRATEGY_FASTMOVERS          (1 << 4)
#define AI_STRATEGY_SLOWMOVERS          (1 << 5)
#define AI_STRATEGY_CULTURE1            (1 << 6)  //religions and wonders
#define AI_STRATEGY_CULTURE2            (1 << 7)  //mass culture buildings
#define AI_STRATEGY_CULTURE3            (1 << 8)  //culture slider
#define AI_STRATEGY_CULTURE4			(1 << 9)
#define AI_STRATEGY_MISSIONARY          (1 << 10)
#define AI_STRATEGY_CRUSH				(1 << 11)  //convert units to City Attack
#define AI_STRATEGY_PRODUCTION          (1 << 12)
#define AI_STRATEGY_PEACE				(1 << 13)  //lucky... neglect defenses.
#define AI_STRATEGY_GET_BETTER_UNITS	(1 << 14)
#define AI_STRATEGY_LAND_BLITZ			(1 << 15)
#define AI_STRATEGY_AIR_BLITZ			(1 << 16)
#define AI_STRATEGY_LAST_STAND			(1 << 17)
#define AI_STRATEGY_FINAL_WAR			(1 << 18)
#define AI_STRATEGY_OWABWNW				(1 << 19)
#define AI_STRATEGY_BIG_ESPIONAGE		(1 << 20)


#define AI_CITY_ROLE_VALID              (1 <<  1)    //zero is bad
#define AI_CITY_ROLE_BIG_CULTURE        (1 <<  2)    //culture victory, probably
#define AI_CITY_ROLE_BIG_PRODUCTION     (1 <<  3)    //don't build girly NW's
#define AI_CITY_ROLE_BIG_MILITARY       (1 <<  4)    //stick with military stuff
#define AI_CITY_ROLE_SCIENCE            (1 <<  5)    //
#define AI_CITY_ROLE_GOLD               (1 <<  6)    //
#define AI_CITY_ROLE_PRODUCTION         (1 <<  7)    //
#define AI_CITY_ROLE_SPECIALIST         (1 <<  8)    //
#define AI_CITY_ROLE_FISHING            (1 <<  9)   //
#define AI_CITY_ROLE_STAGING            (1 << 10)    //send troops here
#define AI_CITY_ROLE_LICHPIN            (1 << 11)    //this city must not fall

#endif // AI_DEFINES_H
