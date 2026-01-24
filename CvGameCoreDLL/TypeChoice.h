#pragma once

#ifndef TYPE_CHOICE_H
#define TYPE_CHOICE_H

/*	advc: Metaprogramming code to replace C++11 std::conditional, std::common_type.
	If more such functionality is needed, boost/mpl could help. */

// Replacement for std::is_same (and boost::is_same)
template<typename T1, typename T2>
struct is_same_type
{
	static const bool value = false;
};
template<typename T>
struct is_same_type<T,T>
{
	static const bool value = true;
};

// Replacement for std::is_pointer (and boost::is_pointer)
template<class T>
struct is_pointer_type
{
	static bool const value = false;
};
template<class T>
struct is_pointer_type<T*>
{
	static bool const value = true;
};

// Replacement for std::conditional
template<bool bCondition, typename T1, typename T2>
struct choose_type { typedef T1 type; };
template<typename T1, typename T2>
struct choose_type<false,T1,T2> { typedef T2 type; };

/*	Replacement for std::common_type. I need it only for integer types with 4 bytes
	or fewer (specifically for advc.fract). Chooses signed over unsigned.
	If both are signed or both unsigned, the larger type is chosen.
	Usage example: typename choose_int_type<short,uint>::type
	(will resolve to short) */
// Default: int; that also covers enum types.
template<typename IntType1, typename IntType2> struct choose_int_type
{
	BOOST_STATIC_ASSERT(sizeof(IntType1) <= 4);
	BOOST_STATIC_ASSERT(sizeof(IntType2) <= 4);
	BOOST_STATIC_ASSERT(std::numeric_limits<IntType1>::is_signed || std::numeric_limits<IntType2>::is_signed);
	typedef int type;
};
template<> struct choose_int_type<unsigned char,  unsigned char>  { typedef unsigned char  type; };
template<> struct choose_int_type<unsigned char,  char>           { typedef char           type; };
template<> struct choose_int_type<char,           unsigned char>  { typedef char           type; };
template<> struct choose_int_type<unsigned char,  short>          { typedef short          type; };
template<> struct choose_int_type<short,          unsigned char>  { typedef short          type; };
template<> struct choose_int_type<unsigned short, unsigned char>  { typedef unsigned short type; };
template<> struct choose_int_type<unsigned char,  unsigned short> { typedef unsigned short type; };
template<> struct choose_int_type<unsigned int,   unsigned char>  { typedef unsigned int   type; };
template<> struct choose_int_type<unsigned char,  unsigned int>   { typedef unsigned int   type; };
template<> struct choose_int_type<char,           char>           { typedef char           type; };
template<> struct choose_int_type<char,           short>          { typedef short          type; };
template<> struct choose_int_type<short,          char>           { typedef short          type; };
template<> struct choose_int_type<char,           unsigned short> { typedef char           type; };
template<> struct choose_int_type<unsigned short, char>           { typedef char           type; };
template<> struct choose_int_type<char,           unsigned int>   { typedef char           type; };
template<> struct choose_int_type<unsigned int,   char>           { typedef char           type; };
template<> struct choose_int_type<short,          short>          { typedef short          type; };
template<> struct choose_int_type<short,          unsigned short> { typedef short          type; };
template<> struct choose_int_type<unsigned short, short>          { typedef short          type; };
template<> struct choose_int_type<short,          unsigned int>   { typedef short          type; };
template<> struct choose_int_type<unsigned int,   short>          { typedef short          type; };
template<> struct choose_int_type<unsigned short, unsigned short> { typedef unsigned short type; };
template<> struct choose_int_type<unsigned short, unsigned int>   { typedef unsigned int   type; };
template<> struct choose_int_type<unsigned int,   unsigned short> { typedef unsigned int   type; };
template<> struct choose_int_type<unsigned int,   unsigned int>   { typedef unsigned int   type; };

// Smallest int type that can safely represent both arguments
template<typename IntType1, typename IntType2> struct choose_safe_int_type
{
	// Need more than 32 bits when signs don't match and the unsigned type takes up 32 bit
	BOOST_STATIC_ASSERT(sizeof(IntType1) >= 4 || sizeof(IntType2) >= 4);
	BOOST_STATIC_ASSERT(std::numeric_limits<IntType1>::is_signed != std::numeric_limits<IntType2>::is_signed);
	BOOST_STATIC_ASSERT(sizeof(IntType1) <= 4);
	BOOST_STATIC_ASSERT(sizeof(IntType2) <= 4);
	typedef __int64 type;
};
template<> struct choose_safe_int_type<int,            int>            { typedef int type; };
template<> struct choose_safe_int_type<int,            short>          { typedef int type; };
template<> struct choose_safe_int_type<short,          int>            { typedef int type; };
template<> struct choose_safe_int_type<int,            char>           { typedef int type; };
template<> struct choose_safe_int_type<char,           int>            { typedef int type; };
template<> struct choose_safe_int_type<int,            unsigned short> { typedef int type; };
template<> struct choose_safe_int_type<unsigned short, int>            { typedef int type; };
template<> struct choose_safe_int_type<int,            unsigned char>  { typedef int type; };
template<> struct choose_safe_int_type<unsigned char,  int>            { typedef int type; };
template<> struct choose_safe_int_type<unsigned int,   unsigned int>   { typedef unsigned int type; };
template<> struct choose_safe_int_type<short,          short>          { typedef short type; };
template<> struct choose_safe_int_type<short,          unsigned short> { typedef int type; };
template<> struct choose_safe_int_type<unsigned short, short>          { typedef int type; };
template<> struct choose_safe_int_type<unsigned short, unsigned short> { typedef unsigned short type; };
template<> struct choose_safe_int_type<short,          char>           { typedef short type; };
template<> struct choose_safe_int_type<short,          unsigned char>  { typedef short type; };
template<> struct choose_safe_int_type<char,           short>          { typedef short type; };
template<> struct choose_safe_int_type<unsigned char,  short>          { typedef int type; };
template<> struct choose_safe_int_type<unsigned short, char>           { typedef int type; };
template<> struct choose_safe_int_type<unsigned short, unsigned char>  { typedef unsigned short type; };
template<> struct choose_safe_int_type<char,           unsigned short> { typedef int type; };
template<> struct choose_safe_int_type<unsigned char,  unsigned short> { typedef unsigned short type; };
template<> struct choose_safe_int_type<char,           char>           { typedef char type; };
template<> struct choose_safe_int_type<char,           unsigned char>  { typedef short type; };
template<> struct choose_safe_int_type<unsigned char,  char>           { typedef short type; };
template<> struct choose_safe_int_type<unsigned char,  unsigned char>  { typedef unsigned char type; };

// Safe for storing the product of an IntType1 and an IntType2 factor
template<typename IntType1, typename IntType2> struct product_int_type
{
	BOOST_STATIC_ASSERT(sizeof(IntType1) >= 4 || sizeof(IntType2) >= 4);
	BOOST_STATIC_ASSERT(std::numeric_limits<IntType1>::is_signed || std::numeric_limits<IntType2>::is_signed);
	BOOST_STATIC_ASSERT(sizeof(IntType1) <= 4);
	BOOST_STATIC_ASSERT(sizeof(IntType2) <= 4);
	typedef __int64 type;
};
template<> struct product_int_type<unsigned int,   unsigned int>   { typedef unsigned __int64 type; };
template<> struct product_int_type<unsigned int,   unsigned short> { typedef unsigned __int64 type; };
template<> struct product_int_type<unsigned short, unsigned int>   { typedef unsigned __int64 type; };
template<> struct product_int_type<unsigned int,   unsigned char>  { typedef unsigned __int64 type; };
template<> struct product_int_type<unsigned char,  unsigned int>   { typedef unsigned __int64 type; };
template<> struct product_int_type<short,          short>          { typedef int type; };
template<> struct product_int_type<unsigned short, unsigned short> { typedef unsigned int type; };
template<> struct product_int_type<short,          char>           { typedef int type; };
template<> struct product_int_type<short,          unsigned char>  { typedef int type; };
template<> struct product_int_type<char,           short>          { typedef int type; };
template<> struct product_int_type<unsigned char,  short>          { typedef int type; };
template<> struct product_int_type<unsigned short, char>           { typedef int type; };
template<> struct product_int_type<unsigned short, unsigned char>  { typedef unsigned int type; };
template<> struct product_int_type<char,           unsigned short> { typedef int type; };
template<> struct product_int_type<unsigned char,  unsigned short> { typedef unsigned int type; };
template<> struct product_int_type<char,           char>           { typedef short type; };
template<> struct product_int_type<char,           unsigned char>  { typedef int type; };
template<> struct product_int_type<unsigned char,  char>           { typedef int type; };
template<> struct product_int_type<unsigned char,  unsigned char>  { typedef unsigned short type; };

#endif
