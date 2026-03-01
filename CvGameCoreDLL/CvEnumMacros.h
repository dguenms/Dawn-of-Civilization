#pragma once
#ifndef CV_ENUM_MACROS_H
#define CV_ENUM_MACROS_H

/*  advc.enum: Helper macros for defining global (i.e. precompiled)
	enum types, their traits and global accessors for instances
	of the associated CvInfo classes. */

/*  Number of instances not known at compile time, but it's safe to say, even in
	mod-mods, that it's not going to be greater than MAX_CHAR.
	(CvXMLLoadUtility will verify this too.) */
#define DO_FOR_EACH_SMALL_DYN_INFO_TYPE(DO) \
	/* getNumInfos function exported */ \
	DO(Route, ROUTE) \
	/* getInfo function and getNumInfos function exported */ \
	DO(Climate, CLIMATE) \
	DO(SeaLevel, SEALEVEL) \
	DO(Terrain, TERRAIN) \
	DO(Feature, FEATURE) \
	DO(Improvement, IMPROVEMENT) \
	DO(TurnTimer, TURNTIMER) \
	DO(Handicap, HANDICAP) \
	DO(GameSpeed, GAMESPEED) \
	DO(Era, ERA) \
	DO(Victory, VICTORY) \
	/* internal only */ \
	/*DO(Camera, CAMERAANIMATION)*/ /* advc.003j: unused */ \
	DO(Advisor, ADVISOR) \
	DO(Emphasize, EMPHASIZE) \
	DO(BonusClass, BONUSCLASS) \
	/*DO(River, RIVER)*/ /* advc.003j: unused */ \
	DO(Goody, GOODY) \
	DO(Trait, TRAIT) \
	DO(Process, PROCESS) \
	DO(Season, SEASON) \
	DO(Month, MONTH) \
	DO(UnitCombat, UNITCOMBAT) \
	DO(Invisible, INVISIBLE) \
	DO(VoteSource, VOTESOURCE) \
	DO(Specialist, SPECIALIST) \
	DO(Religion, RELIGION) \
	DO(Corporation, CORPORATION) \
	DO(Hurry, HURRY) \
	DO(Upkeep, UPKEEP) \
	DO(CultureLevel, CULTURELEVEL) \
	DO(CivicOption, CIVICOPTION)

// Number of instances not known at compile time; can be greater than MAX_CHAR.
#define DO_FOR_EACH_BIG_DYN_INFO_TYPE(DO) \
	/* getInfo function exported */ \
	DO(Color, COLOR) \
	DO(AnimationCategory, ANIMCAT) \
	DO(EntityEvent, ENTITYEVENT) \
	DO(Effect, EFFECT) \
	DO(Attachable, ATTACHABLE) \
	DO(Build, BUILD) \
	/* getInfo function and getNumInfos function exported */ \
	DO(PlayerColor, PLAYERCOLOR) \
	DO(Bonus, BONUS) \
	DO(LeaderHead, LEADER) \
	DO(Civilization, CIVILIZATION) \
	DO(Cursor, CURSOR) \
	/* internal only */ \
	DO(BuildingClass, BUILDINGCLASS) \
	DO(Building, BUILDING) \
	DO(SpecialBuilding, SPECIALBUILDING) \
	DO(Project, PROJECT) \
	DO(Vote, VOTE) \
	DO(Concept, CONCEPT) \
	DO(NewConcept, NEW_CONCEPT) \
	DO(UnitClass, UNITCLASS) \
	DO(Unit, UNIT) \
	DO(SpecialUnit, SPECIALUNIT) \
	DO(Promotion, PROMOTION) \
	DO(Tech, TECH) \
	DO(Civic, CIVIC) \
	DO(Event, EVENT) \
	DO(EventTrigger, EVENTTRIGGER) \
	DO(EspionageMission, ESPIONAGEMISSION) \
	DO(UnitArtStyle, UNIT_ARTSTYLE) \
	/* <advc.tsl> (not exposed to Python) */ \
	DO(TruCiv, TRUCIV) \
	DO(TruLeader, TRULEADER) \
	DO(TruBonus, TRUBONUS) /* </advc.tsl> */

// Number of instances not known at compile time
#define DO_FOR_EACH_DYN_INFO_TYPE(DO) \
	DO_FOR_EACH_SMALL_DYN_INFO_TYPE(DO) \
	DO_FOR_EACH_BIG_DYN_INFO_TYPE(DO)

/*  Number of instances not known at compile time; no associated enum type.
	(I've entered upper-case prefixes though in case that enums are desired at a
	later time.) */
#define DO_FOR_EACH_INT_INFO_TYPE(DO) \
	/* getInfo function exported */ \
	DO(ThroneRoomCamera, THRONEROOMCAM) \
	DO(MainMenu, MAINMENU) \
	DO(WaterPlane, WATERPLANE) \
	DO(Landscape, LANDSCAPE) \
	/* getNumInfos function exported */ \
	DO(CameraOverlay, CAMERAOVERLAY) \
	DO(UnitFormation, UNITFORMATION) \
	/* both exported */ \
	DO(RouteModel, ROUTEMODEL) \
	DO(RiverModel, RIVERMODEL) \
	DO(TerrainPlane, TERRAINPLANE) \
	DO(ThroneRoom, THRONEROOM) \
	DO(ThroneRoomStyle, THRONEROOMSTYLE) \
	DO(SlideShow, SLIDESHOW) \
	DO(SlideShowRandom, SLIDESHOWRAND) \
	DO(WorldPicker, WORLDPICKER) \
	DO(SpaceShip, SPACESHIP) \
	DO(Action, ACTION) \
	DO(Hint, HINT) \
	/* internal only */ \
	/* DO(Quest, QUEST) */ /* advc.003j: unused */ \
	DO(Diplomacy, DIPLOMACY) \
	DO(Tutorial, TUTORIAL)

#undef DOMAIN // defined in math.h
// Number of instances hardcoded in CvEnums.h
#define DO_FOR_EACH_STATIC_INFO_TYPE(DO) \
	/* exported */ \
	DO(AnimationPath, ANIMATIONPATH) \
	DO(InterfaceMode, INTERFACEMODE) \
	DO(GameOption, GAMEOPTION) \
	DO(MPOption, MPOPTION) \
	DO(PlayerOption, PLAYEROPTION) \
	DO(GraphicOption, GRAPHICOPTION) \
	DO(ForceControl, FORCECONTROL) \
	DO(Mission, MISSION) \
	/* internal only */ \
	DO(Yield, YIELD) \
	DO(Commerce, COMMERCE) \
	DO(Control, CONTROL) \
	DO(Command, COMMAND) \
	DO(Automate, AUTOMATE) \
	DO(Domain, DOMAIN) \
	DO(Attitude, ATTITUDE) \
	DO(Memory, MEMORY) \
	DO(CityTab, CITYTAB) \
	DO(Calendar, CALENDAR) \
	DO(UnitAI, UNITAI) \
	DO(Denial, DENIAL)

#define DO_FOR_EACH_INFO_TYPE(DO) \
	DO_FOR_EACH_DYN_INFO_TYPE(DO) \
	DO_FOR_EACH_STATIC_INFO_TYPE(DO) \
	DO_FOR_EACH_INT_INFO_TYPE(DO)

/*  These don't have a dedicated CvInfo class, and the macros for generating
	getter functions can't deal with that. (typedef would make it impossible
	to forward-declare them in CvGlobals.h.) */
#define CvHintInfo CvInfoBase
#define CvConceptInfo CvInfoBase
#define CvNewConceptInfo CvInfoBase
#define CvSeasonInfo CvInfoBase
#define CvMonthInfo CvInfoBase
#define CvUnitCombatInfo CvInfoBase
#define CvInvisibleInfo CvInfoBase
#define CvDomainInfo CvInfoBase
#define CvAttitudeInfo CvInfoBase
#define CvMemoryInfo CvInfoBase
#define CvCityTabInfo CvInfoBase
#define CvCalendarInfo CvInfoBase
#define CvUnitAIInfo CvInfoBase
#define CvDenialInfo CvInfoBase
// This one just has an irregular, exported name.
#define CvThroneRoomCameraInfo CvThroneRoomCamera

/*	Static enum types without any associated CvInfo data.
	Not a complete list; add types here if their traits need to be accessed. */
#define DO_FOR_EACH_STATIC_ENUM_TYPE(DO) \
	DO(Direction, DIRECTION) \
	DO(CardinalDirection, CARDINALDIRECTION) \
	DO(WarPlan, WARPLAN) \
	DO(CityPlot, CITYPLOT) \
	DO(Feat, FEAT) \
	DO(AreaAI, AREAAI) \
	DO(MissionAI, MISSIONAI) \
	DO(PlayerHistory, PLAYER_HISTORY) /* advc.004s */ \
	DO(Function, FUNC) \
	DO(CitySize, CITYSIZE) \
	DO(Contact, CONTACT) \
	DO(DiplomacyPower, DIPLOMACYPOWER) \
	DO(AIDemand, AI_DEMAND) /* advc.104m */

// For generating enum definitions and traits ...
#define NUM_ENUM_TYPES(INFIX) NUM_##INFIX##_TYPES
#define NO_ENUM_TYPE(SUFFIX) NO_##SUFFIX
#define SET_NO_ENUM_TYPE(SUFFIX) NO_ENUM_TYPE(SUFFIX) = -1

// Increment/decrement functions based on code in the "We the People" mod
#define DEFINE_INCREMENT_OPERATORS(EnumType) \
	inline EnumType& operator++(EnumType& e) \
	{ \
		e = static_cast<EnumType>(e + 1); \
		return e; \
	} \
	inline EnumType operator++(EnumType& e, int) \
	{ \
		EnumType eResult = e; \
		e = static_cast<EnumType>(e + 1); \
		return eResult; \
	} \
	inline EnumType& operator--(EnumType& e) \
	{ \
		e = static_cast<EnumType>(e - 1); \
		return e; \
	} \
	inline EnumType operator--(EnumType& e, int) \
	{ \
		EnumType eResult = e; \
		e = static_cast<EnumType>(e - 1); \
		return eResult; \
	}

#define MAKE_INFO_ENUM(Name, PREFIX) \
enum Name##Types \
{ \
	SET_NO_ENUM_TYPE(PREFIX), \
}; \
DEFINE_INCREMENT_OPERATORS(Name##Types)

/*  No variadic macros in MSVC03, so, without using an external code generator,
	this is all I can do: */
#define ENUM_START(Name, PREFIX) \
enum Name##Types \
{ \
	SET_NO_ENUM_TYPE(PREFIX),

#define ENUM_END(Name, PREFIX) \
	NUM_ENUM_TYPES(PREFIX) \
}; \
DEFINE_INCREMENT_OPERATORS(Name##Types)
// For enumerators that are supposed to be excluded from iteration
#define ENUM_END_HIDDEN(Name, PREFIX) \
}; \
DEFINE_INCREMENT_OPERATORS(Name##Types)
/*	(The original enum definitions had hidden most of the NUM_...._TYPES
	enumerators from the EXE through _USRDLL checks. Since we can't
	recompile the EXE, let's not bother with that.) */

// Macros for generating CvInfo accessor functions in CvGlobals ...
	
#define MAKE_INFO_ACCESSORS_DYN(Name, Dummy) \
	inline int getNum##Name##Infos() const \
	{ \
		return m_pa##Name##Info.size(); \
	} \
	inline Cv##Name##Info& getInfo(Name##Types e##Name) const \
	{ \
		FAssertBounds(0, getNum##Name##Infos(), e##Name); \
		return *m_pa##Name##Info[e##Name]; \
	} \
	/* (See SET_LOOP_INFO) */ \
	/*inline Cv##Name##Info& getLoopInfo(Name##Types e##Name) const*/ \
	/*{*/ \
	/*	return *m_pa##Name##Info[e##Name];*/ \
	/*}*/ \
	inline Cv##Name##Info& get##Name##Info(int i##Name) const \
	{ \
		return getInfo(static_cast<Name##Types>(i##Name)); \
	}
#define MAKE_INFO_ACCESSORS_INT(Name, Dummy) \
	inline int getNum##Name##Infos() const \
	{ \
		return m_pa##Name##Info.size(); \
	} \
	inline Cv##Name##Info& get##Name##Info(int i##Name) const \
	{ \
		FAssertBounds(0, getNum##Name##Infos(), i##Name); \
		return *m_pa##Name##Info[i##Name]; \
	}
#define MAKE_INFO_ACCESSORS_STATIC(Name, INFIX) \
	inline Cv##Name##Info& getInfo(Name##Types e##Name) const \
	{ \
		FAssertBounds(0, NUM_ENUM_TYPES(INFIX), e##Name); \
		return *m_pa##Name##Info[e##Name]; \
	} \
	/* (See SET_LOOP_INFO) */ \
	/*inline Cv##Name##Info& getLoopInfo(Name##Types e##Name) const*/ \
	/*{*/ \
	/*	return *m_pa##Name##Info[e##Name];*/ \
	/*}*/ \
	inline Cv##Name##Info& get##Name##Info(int i##Name) const \
	{ \
		return getInfo(static_cast<Name##Types>(i##Name)); \
	}

#endif
