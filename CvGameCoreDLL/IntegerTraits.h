#pragma once

#ifndef INTEGER_TRAITS_H
#define INTEGER_TRAITS_H

/*	advc: Integer definitions cut from CvGameCoreDll.h.
	typedefs and defines may have been compiled into the EXE. */

typedef unsigned char		byte;
// advc (note): A little strange to me, but consistent with WORD in winnt.h.
typedef unsigned short		word;
typedef unsigned int		uint;
typedef unsigned long		dword;
typedef unsigned __int64	qword;
typedef wchar_t				wchar;

/*	advc.001q: Put minus operators into the negative constants, otherwise,
	if there's only a literal, it can get treated as an unsigned value. */
#define MAX_CHAR							(0x7f)
//#define MIN_CHAR							(0x80)
#define MIN_CHAR							(-MAX_CHAR - 1)
#define MAX_SHORT							(0x7fff)
//#define MIN_SHORT							(0x8000)
#define MIN_SHORT							(-MAX_SHORT - 1)
#define MAX_INT								(0x7fffffff)
//#define MIN_INT							(0x80000000)
#define MIN_INT								(-MAX_INT - 1)
#define MAX_UNSIGNED_CHAR					(0xff)
#define MIN_UNSIGNED_CHAR					(0x00)
#define MAX_UNSIGNED_SHORT					(0xffff)
#define MIN_UNSIGNED_SHORT					(0x0000)
#define MAX_UNSIGNED_INT					(0xffffffff)
#define MIN_UNSIGNED_INT					(0x00000000)
// <advc> Aliases (also same as WCHAR_MAX, WCHAR_MIN in wchar.h)
#define MAX_WCHAR							MAX_UNSIGNED_SHORT
#define MIN_WCHAR							MIN_UNSIGNED_SHORT
/*	These are unused. FLT_MAX and FLT_MIN are used in a few places,
	so let's keep using those exclusively. */ // </advc>
/*inline DWORD FtoDW( float f ) { return *(DWORD*)&f; }
inline float DWtoF( dword n ) { return *(float*)&n; }
inline float MaxFloat() { return DWtoF(0x7f7fffff); }*/

/*	advc: Structs that get the limits of an integer type.
	Replacing boost/integer_traits, so that the constants above are used
	and not e.g. INT_MAX. (I don't see why we have those custom constants,
	but, since I'm not sure and since some of them are widely used now,
	I'm not going to throw them out.) */
template<typename T>
struct integer_limits
{
	static bool const is_integer = false;
	static bool const is_signed = false;
};
template<>
struct integer_limits<bool>
{
	static bool const min = false;
	static bool const max = true;
	static bool const is_signed = false;
	// This differs from std::numeric_limits<T>::is_integer !
	static bool const is_integer = false;
};
template<>
struct integer_limits<char>
{
	static char const min = MIN_CHAR;
	static char const max = MAX_CHAR;
	static bool const is_signed = true;
	static bool const is_integer = true;
};
template<>
struct integer_limits<byte>
{
	static byte const min = MIN_UNSIGNED_CHAR;
	static byte const max = MAX_UNSIGNED_CHAR;
	static bool const is_signed = false;
	static bool const is_integer = true;
};
template<>
struct integer_limits<short>
{
	static short const min = MIN_SHORT;
	static short const max = MAX_SHORT;
	static bool const is_signed = true;
	static bool const is_integer = true;
};
template<>
struct integer_limits<word>
{
	static word const min = MIN_UNSIGNED_SHORT;
	static word const max = MAX_UNSIGNED_SHORT;
	static bool const is_signed = false;
	static bool const is_integer = true;
};
template<>
struct integer_limits<int>
{
	static int const min = MIN_INT;
	static int const max = MAX_INT;
	static bool const is_signed = true;
	static bool const is_integer = true;
};
template<>
struct integer_limits<uint>
{
	static uint const min = MIN_UNSIGNED_INT;
	static uint const max = MAX_UNSIGNED_INT;
	static bool const is_signed = false;
	static bool const is_integer = true;
};
/*	long has the same limits as int in MSVC03 x86,
	but they're still distinct types. */
template<>
struct integer_limits<long>
{
	static long const min = integer_limits<int>::min;
	static long const max = integer_limits<int>::max;
	static bool const is_signed = integer_limits<int>::is_signed;
	static bool const is_integer = integer_limits<int>::is_integer;
};
template<>
struct integer_limits<unsigned long>
{
	static unsigned long const min = integer_limits<uint>::min;
	static unsigned long const max = integer_limits<uint>::max;
	static bool const is_signed = integer_limits<uint>::is_signed;
	static bool const is_integer = integer_limits<uint>::is_integer;
};
template<>
struct integer_limits<long long>
{
	static long long const min = LLONG_MIN;
	static long long const max = LLONG_MAX;
	static bool const is_signed = true;
	static bool const is_integer = true;
};
template<>
struct integer_limits<unsigned long long>
{
	static unsigned long long const min = 0;
	static unsigned long long const max = ULLONG_MAX;
	static bool const is_signed = false;
	static bool const is_integer = true;
};

#endif
