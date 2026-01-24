#pragma once
#ifndef ENUM_TRAITS_H
#define ENUM_TRAITS_H

/*  advc.enum: Type traits and macros for enum types used globally
	(included in the precompiled header) by the game core DLL.
	Enum types that don't correspond to CvInfo classes aren't fully covered
	but can be added to DO_FOR_EACH_STATIC_ENUM_TYPE in CvEnumMacros.h as needed. */

struct enum_trait_base
{
	static bool const is_enum = true;
};
template<class T,
	bool bINTEGER = integer_limits<T>::is_integer,
	bool bSCALED = is_scaled_num<T>::value,
	bool bPOINTER = is_pointer_type<T>::value>
struct enum_traits
{
	static bool const is_enum = false;
	/*	We don't know how T could be represented more compactly.
		(Useful for the enum map classes to define this for all types.) */
	typedef T compact_t;
};
/*	The none trait is going to be -1 (NO_...) for enum types and
	0 for all non-enum types that can be 0. (Unavailable otherwise.) */
template<class T> // integer types (except bool)
struct enum_traits<T, true, false, false>
{
	static bool const is_enum = false;
	typedef T compact_t;
	static T const none = 0;
};
template<> // bool
struct enum_traits<bool, false, false, false>
{
	static bool const is_enum = false;
	typedef bool compact_t;
	static bool const none = false;
};
template<class T> // pointer types
struct enum_traits<T, false, false, true>
{
	static bool const is_enum = false;
	/*	Represent pointers as int so that the NULL pointer can be a
		compile-time constant. Prefer int over uint b/c the iDEFAULT param
		of EnumMapBase will need to allow negative integer values. */
	typedef int compact_t;
	static int const none = NULL;
};
template<> // float
struct enum_traits<float, false, false, false>
{
	static bool const is_enum = false;
	typedef float compact_t;
	// Can't be .0f b/c it needs to be a compile-time constant
	static char const none = 0;
};
template<> // double
struct enum_traits<double, false, false, false>
{
	static bool const is_enum = false;
	typedef double compact_t;
	static char const none = 0;
};
template<class T> // ScaledNum
struct enum_traits<T, false, true, false>
{
	static bool const is_enum = false;
	typedef T compact_t;
	static char const none = 0;
};

/*	Regarding the choice of compact_t: Shifting enum values by +1
	and using unsigned char could, in principle, be useful; however,
	it would make a difference for few, if any, relevant types. */
#define SET_TRAITS_FOR_STATIC_ENUM(Prefix, INFIX) \
	template<> \
	struct enum_traits<Prefix##Types,false,false,false> : enum_trait_base \
	{ \
		/* Using Prefix##Types for len leads to peculiar behavior; */ \
		/* perhaps a problem w/ the static initialization order. */ \
		static int const len = NUM_ENUM_TYPES(INFIX); \
		static Prefix##Types const none = NO_ENUM_TYPE(INFIX); \
		static Prefix##Types const first = (len == 0 ? none : \
				static_cast<Prefix##Types>(0)); \
		typedef choose_type< \
				(len > MAX_CHAR), short, char \
				>::type compact_t; \
		static bool const is_static = true; \
		static Prefix##Types length() \
		{ \
			return static_cast<Prefix##Types>(len); \
		} \
	};
DO_FOR_EACH_STATIC_INFO_TYPE(SET_TRAITS_FOR_STATIC_ENUM);
DO_FOR_EACH_STATIC_ENUM_TYPE(SET_TRAITS_FOR_STATIC_ENUM);

#define SET_TRAITS_FOR_DYN_ENUM(Prefix, SUFFIX, IntType, LengthExpression) \
	template<> \
	struct enum_traits<Prefix##Types,false,false,false> : enum_trait_base \
	{ \
		BOOST_STATIC_ASSERT(std::numeric_limits<IntType>::is_signed && sizeof(IntType) <= 4); \
		/* The theoretical upper limit */ \
		static int const len = static_cast<int>(integer_limits<IntType>::max); \
		static Prefix##Types const none = NO_ENUM_TYPE(SUFFIX); \
		/* Won't be valid if the enum is empty, but it's convenient to */ \
		/* define a first element in any case. */ \
		static Prefix##Types const first = static_cast<Prefix##Types>(0); \
		typedef IntType compact_t; \
		static bool const is_static = false; \
		static Prefix##Types length() \
		{ \
			return static_cast<Prefix##Types>(LengthExpression); \
		} \
	};

#define SET_TRAITS_FOR_SMALL_ENUM(Prefix, SUFFIX) \
	SET_TRAITS_FOR_DYN_ENUM(Prefix, SUFFIX, char, GC.getNum##Prefix##Infos())

DO_FOR_EACH_SMALL_DYN_INFO_TYPE(SET_TRAITS_FOR_SMALL_ENUM);
SET_TRAITS_FOR_DYN_ENUM(WorldSize, WORLDSIZE, char, GC.getNumWorldInfos());
SET_TRAITS_FOR_DYN_ENUM(Flavor, FLAVOR, char, GC.getNumFlavorTypes());
SET_TRAITS_FOR_DYN_ENUM(ArtStyle, ARTSTYLE, char, GC.getNumArtStyleTypes());
namespace plot_num_traits
{
	// Forward declaration; defined in CvMap.h.
	inline PlotNumTypes getNumMapPlots();
}
SET_TRAITS_FOR_DYN_ENUM(PlotNum, PLOT_NUM, PlotNumInt, plot_num_traits::getNumMapPlots());

#define SET_TRAITS_FOR_BIG_ENUM(Prefix, SUFFIX) \
	SET_TRAITS_FOR_DYN_ENUM(Prefix, SUFFIX, short, GC.getNum##Prefix##Infos())

DO_FOR_EACH_BIG_DYN_INFO_TYPE(SET_TRAITS_FOR_BIG_ENUM);

#define SET_TRAITS_FOR_CIV_ID(Prefix, INFIX) \
	template<> \
	struct enum_traits<Prefix##Types,false,false,false> : enum_trait_base \
	{ \
		static int const len = MAX_##INFIX##S; \
		BOOST_STATIC_ASSERT(len > 0); \
		static Prefix##Types const none = NO_ENUM_TYPE(INFIX); \
		static Prefix##Types const first = static_cast<Prefix##Types>(0); \
		typedef char compact_t; \
		BOOST_STATIC_ASSERT(len <= static_cast<int>(integer_limits<compact_t>::max)); \
		static bool const is_static = true; \
		static Prefix##Types length() \
		{ \
			return static_cast<Prefix##Types>(len); \
		} \
	}
SET_TRAITS_FOR_CIV_ID(Player, PLAYER);
SET_TRAITS_FOR_CIV_ID(Team, TEAM);
SET_TRAITS_FOR_CIV_ID(CivPlayer, CIV_PLAYER);
SET_TRAITS_FOR_CIV_ID(CivTeam, CIV_TEAM);

template<> // Weird one; shouldn't be iterated over.
struct enum_traits<PlayerVoteTypes,false,false,false> : enum_trait_base
{
	static int const len = enum_traits<CivPlayerTypes>::len;
	static PlayerVoteTypes const none = NO_PLAYER_VOTE;
	static PlayerVoteTypes const first = FIRST_PLAYER_VOTE;
	typedef char compact_t;
	static bool const is_static = true;
};

#undef SET_TRAITS_FOR_STATIC_ENUM
#undef SET_TRAITS_FOR_DYN_ENUM
#undef SET_TRAITS_FOR_SMALL_ENUM
#undef SET_TRAITS_FOR_BIG_ENUM
#undef SET_TRAITS_FOR_CIV_ID

/*	Neither cast nor assignment operator can be defined out of class,
	so I don't think we can somehow allow e.g. an enum to short assignment.
	This seems like the next best thing: */
template<typename E>
__inline typename enum_traits<E>::compact_t compactEnum(E e)
{
	return static_cast<enum_traits<E>::compact_t>(e);
}

template<typename E>
bool checkEnumBounds(E eIndex)
{
	return (eIndex >= 0 && eIndex < enum_traits<E>::length());
}
namespace enum_traits_detail
{
	template<typename E>
	void assertEnumBounds(E eIndex)
	{
		FAssertBounds(0, enum_traits<E>::length(), eIndex);
	}
	template<typename E>
	void assertInfoEnum(E eIndex)
	{
		FAssertBounds(-1, enum_traits<E>::length(), eIndex);
	}
};
#ifdef FASSERT_ENABLE
#define FAssertEnumBounds(eIndex) enum_traits_detail::assertEnumBounds(eIndex)
#define FAssertInfoEnum(eIndex) enum_traits_detail::assertInfoEnum(eIndex)
#else
#define FAssertEnumBounds(eIndex) (void)0
#define FAssertInfoEnum(eIndex) (void)0
#endif

#define FOR_EACH_ENUM(TypeName) \
	for (TypeName##Types eLoop##TypeName = (TypeName##Types)0; \
			eLoop##TypeName < enum_traits<TypeName##Types>::length(); \
			eLoop##TypeName = (TypeName##Types)(eLoop##TypeName + 1))
// With a 2nd argument for a variable name
#define FOR_EACH_ENUM2(TypeName, eVar) \
	for (TypeName##Types eVar = (TypeName##Types)0; \
			eVar < enum_traits<TypeName##Types>::length(); \
			eVar = (TypeName##Types)(eVar + 1))
/*	Random order. The macro needs to declare two variables before the loop. Use __LINE__
	for those, so that it's possible for loops to coexist in the same scope. */
#define FOR_EACH_ENUM_RAND(TypeName, kRand) \
	std::vector<int> CONCATVARNAME(aiLoop##TypeName##Indices_, __LINE__) \
			(enum_traits<TypeName##Types>::length()); \
	(kRand).shuffle(CONCATVARNAME(aiLoop##TypeName##Indices_, __LINE__)); \
	int CONCATVARNAME(iLoop##TypeName##Counter_, __LINE__) = 0; \
	for ( TypeName##Types eLoop##TypeName; \
			CONCATVARNAME(iLoop##TypeName##Counter_, __LINE__) < \
			enum_traits<TypeName##Types>::length() && \
			/* Do the increment in the termination check, but don't branch on it. */ \
			(eLoop##TypeName = (TypeName##Types)CONCATVARNAME(aiLoop##TypeName##Indices_, __LINE__) \
			[CONCATVARNAME(iLoop##TypeName##Counter_, __LINE__)], \
			(CONCATVARNAME(iLoop##TypeName##Counter_, __LINE__)++, true)); )
/*	Example. FOR_EACH_ENUM_RAND(CardinalDirection, mapRand())
	expands to:
	std::vector<int> aiLoopCardinalDirectionIndices_443(getEnumLength((CardinalDirectionTypes)0));
	(mapRand()).shuffle(aiLoopCardinalDirectionIndices_443);
	int iLoopCardinalDirectionCounter_443 = 0;
	for ( CardinalDirectionTypes eLoopCardinalDirection;
			iLoopCardinalDirectionCounter_443 <
			enum_traits<CardinalDirectionTypes>::length() &&
			(eLoopCardinalDirection = (CardinalDirectionTypes)aiLoopCardinalDirectionIndices_443
			[iLoopCardinalDirectionCounter_443],
			(iLoopCardinalDirectionCounter_443++, true)); )
*/
// Reversed order
#define FOR_EACH_ENUM_REV(TypeName) \
	for (TypeName##Types eLoop##TypeName = (TypeName##Types) \
			(enum_traits<TypeName##Types>::length() - 1); \
			eLoop##TypeName >= 0; \
			eLoop##TypeName = (TypeName##Types)(eLoop##TypeName - 1))
/*	To be used only in the body of a FOR_EACH_ENUM loop. Don't need to assert
	array bounds then. Not really feasible though to replace all the
	CvGlobals::getInfo calls, so maybe better not to use this at all ... */
/*#define LOOP_INFO(TypeName) \
	GC.getLoopInfo(eLoop##TypeName)
#define SET_LOOP_INFO(TypeName) \
	Cv##TypeName##Info const& kLoop##TypeName = LOOP_INFO(TypeName)
// To go with FOR_EACH_ENUM2
#define SET_LOOP_INFO2(TypeName, kVar) \
	Cv##TypeName##Info const& kVar = LOOP_INFO(TypeName)*/

#endif
