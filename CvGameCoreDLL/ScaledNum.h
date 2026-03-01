#pragma once

#ifndef SCALED_NUM_H
#define SCALED_NUM_H

// advc.fract: Header-only class template for fixed-point fractional numbers

#include "FixedPointPowTables.h"
/*	Other non-BtS dependencies (precompiled):
 +	The whole TypeChoice.h header.
 +	The whole IntegerConversion.h header. Two uses of enum_traits in that header
	can be replaced (see comment there) when porting ScaledNum into another mod.
 +	intdiv::round, fmath::round in ArithmeticUtils.h.
 +	intHash in CvGameCoreUtils.h.
 +	integer_limits in IntegerTraits.h.
	For precompiling this header, one may have to define NOMINMAX
	before including windows.h; see CvGameCoreDLL.h.
	The randSuccess function assumes that CvRandom can include two integer values
	in its log messages; see comment in randSuccess. */

// Defined in BaseTsd.h. Easy to get them mixed up with ScaledNum::INTMAX, INTMIN.
#undef MAXINT
#undef MININT
#undef MAXUINT

/*	Uncomment for some additional runtime assertions
	checking conditions that are really the user's responsibility. */
//#define SCALED_NUM_EXTRA_ASSERTS

// For members shared by all instantiations of ScaledNum
template<typename Dummy> // Just so that static data members can be defined in the header
class ScaledNumBase
{
protected:
	static CvString szBuf;
	template<typename OtherIntType>
	static int safeToInt(OtherIntType n)
	{
		// NB: uint is the only problematic OtherIntType that can occur here
		return safeIntCast<int>(n);
	}
};
template<typename Dummy>
CvString ScaledNumBase<Dummy>::szBuf = "";

/*	See comment below about EnumType parameter of ScaledNum. This assertion
	is a pretty crude way to implement that. */
#define STATIC_ASSERT_COMPATIBLE(EnumType1,EnumType2) \
	BOOST_STATIC_ASSERT( \
			(is_same_type<EnumType1,EnumType2>::value) || \
			(is_same_type<EnumType1,int>::value) || \
			(is_same_type<int,EnumType2>::value));

/*  class ScaledNum: Approximates a fractional number as an integer multiplied by a
	scale factor. For fixed-point arithmetic that can't lead to network sync issues.
	Performance: Generally comparable to floating-point types when the scale factor is
	a power of 2; see ScaledNumTest.cpp.
	Overloads commonly used arithmetic operators and offers some conveniences that the
	built-in types don't have, e.g. abs, clamp, approxEquals, randSuccess (coin flip).
	Compile-time converter from double: macro 'fixp'
	Conversion from percentage: macro 'per100' (also 'per1000', 'per10000')
	'scaled' and 'uscaled' typedefs for default precision.

	In code that uses Systems Hungarian notation, I propose the prefix 'r' for
	ScaledNum variables, or more generally for any types that represent
	rational numbers without a floating point.

	The difference between ScaledNum and boost::rational is that the latter allows
	the denominator to change at runtime, which allows for greater accuracy but
	isn't as fast. */

/*  iSCALE is the factor by which integer numbers are multiplied when converted
	to a ScaledNum (see constructor from int) and thus determines the precision
	of fractional numbers and affects the numeric limits (MAX, MIN) - the higher
	iSCALE, the greater the precision and the tighter the limits.

	IntType is the type of the underlying integer variable. Has to be an integral type.
	__int64 is not supported. For unsigned IntType, internal integer divisions are rounded
	to the nearest IntType value in order to improve precision. For signed IntType, this
	isn't guaranteed. Using an unsigned IntType also speeds up multiplication.

	ScaledNum instances of different iSCALE values or different IntTypes can be mixed.
	Multiplications, divisions and comparisons on differing scales will internally scale
	both operands up to the product of the two scales (using 64 bit if necessary) in order
	to minimize rounding errors in multiplication and division and to make comparisons exact.
	The return type of the arithmetic operators is a ScaledNum with iSCALE equal to the
	maximum of the two scales and IntType equal to the common type of the two integer types
	(see choose_int_type in TypeChoice.h; should be equivalent to std::common_type in C++11).

	EnumType (optional): If an enum type is given, the resulting ScaledNum type will
	be incompatible with ScaledNum types that use a different enum type.
	See usage example (MovementPts) in ScaledNumTest.
	Tbd.: The compiler errors from STATIC_ASSERT_COMPATIBLE are difficult to read.
	Is there some way to define the respective function templates only for arguments
	with compatible enum types? Or else, using something like
	{ EnumType eDummy = (OtherEnumType)0; }
	instead of BOOST_STATIC_ASSERT would already help a bit - but that would fail when
	EnumType is int and OtherEnumType isn't.

	To avoid (even more) template clutter, most of the functions are defined within
	the ScaledNum class definition.

	Tbd. -- in addition to "tbd." and "fixme" comments throughout this file:
	- Add logarithm function.
	- Add Natvis file.
	For background, see the replies and "To be done" in the initial post here:
	forums.civfanatics.com/threads/class-for-fixed-point-arithmetic.655037  */
#pragma pack(push, 1)
template<int iSCALE, typename IntType = int, typename EnumType = int>
class ScaledNum : ScaledNumBase<void> // Not named "ScaledInt" b/c what's being scaled isn't necessarily an integer
{
	IntType m_i;

	BOOST_STATIC_ASSERT(sizeof(IntType) <= 4);
	/*	Workaround for MSVC bug with dependent template argument in friend declaration:
		Make the scale parameter an int but cast it to IntType internally. This way,
		iSCALE can also precede IntType in the parameter list. */
	static IntType const SCALE = static_cast<IntType>(iSCALE);
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	friend class ScaledNum;

	static bool const bSIGNED = integer_limits<IntType>::is_signed;
	static IntType const INTMIN = integer_limits<IntType>::min;
	static IntType const INTMAX = integer_limits<IntType>::max;

public:
	typedef IntType int_t; // Expose int type for any type trait code
	static IntType const MAX = INTMAX / SCALE;
	static IntType const MIN = INTMIN / SCALE;

	/*	Factory function for creating fractions (with wrapper macro 'fixp').
		Numerator and denominator as template parameters ensure
		that the conversion to SCALE happens at compile time, so that
		floating-point math can be used for maximal accuracy. */
	template<int iNUM, int iDEN>
	static ScaledNum fromRational()
	{
		BOOST_STATIC_ASSERT(iDEN != 0);
		BOOST_STATIC_ASSERT(bSIGNED || (iDEN > 0 && iNUM >= 0));
		return fromDouble(iNUM / static_cast<double>(iDEN));
	}
	// Smallest positive number that can be represented
	static ScaledNum epsilon()
	{
		ScaledNum r;
		r.m_i = 1;
		return r;
	}

	static ScaledNum max(ScaledNum r1, ScaledNum r2)
	{
		return std::max(r1, r2);
	}
	static ScaledNum min(ScaledNum r1, ScaledNum r2)
	{
		return std::min(r1, r2);
	}
	template<typename LoType, typename HiType>
	static ScaledNum clamp(ScaledNum r, LoType lo, HiType hi)
	{
		r.clamp(lo, hi);
		return r;
	}

	// Result in the half-open interval [0, 1)
	static ScaledNum rand(CvRandom& kRand, TCHAR const* szLog)
	{
		BOOST_STATIC_ASSERT(SCALE <= MAX_UNSIGNED_SHORT);
		ScaledNum r;
		r.m_i = static_cast<IntType>(kRand.get(static_cast<unsigned short>(iSCALE), szLog));
		return r;
	}
	/*	See intHash (ArithmeticUtils.h) about the parameters.
		Result in the half-open interval [0, 1). */
	static ScaledNum hash(std::vector<int> const& x, PlayerTypes ePlayer = NO_PLAYER)
	{
		CvRandom rng;
		rng.init(::intHash(x, ePlayer));
		return rand(rng, NULL);
	}
	// For hashing just a single input
	static ScaledNum hash(int x, PlayerTypes ePlayer = NO_PLAYER)
	{
		std::vector<int> v;
		v.push_back(x);
		return hash(v, ePlayer);
	}

	ScaledNum() : m_i(static_cast<IntType>(0)) {}
	ScaledNum(int i) : m_i(static_cast<IntType>(SCALE * i))
	{
		// Respecting the limits is really the caller's responsibility
		#ifdef SCALED_NUM_EXTRA_ASSERTS
			FAssert(static_cast<IntType>(i) >= INTMIN / SCALE);
			FAssert(static_cast<IntType>(i) <= INTMAX / SCALE);
		#endif
	}
	ScaledNum(uint u) : m_i(static_cast<IntType>(SCALE * u))
	{
		#ifdef SCALED_NUM_EXTRA_ASSERTS
			FAssert(u <= static_cast<uint>(INTMAX) / static_cast<uint>(SCALE));
		#endif
	}
	/*	Construction from rational
		Note: It's easy to accidentally call the single-arg ctor by typing
		scaled ratio(iDen / iNum);
		Static factory functions could avoid that, but are too unwieldy, e.g.
		scaled ratio = scaled::rational(iDen, iNum); */
	ScaledNum(int iNum, int iDen)
	{
		m_i = safeCast(mulDiv(SCALE, iNum, iDen));
	}
	ScaledNum(uint uiNum, uint uiDen)
	{
		m_i = safeCast(mulDiv(SCALE, uiNum, uiDen));
	}

	// Scale and integer type conversion constructor
	template<int iFROM_SCALE, typename OtherIntType, typename OtherEnumType>
	ScaledNum(ScaledNum<iFROM_SCALE,OtherIntType,OtherEnumType> const& rOther);

	/*	Explicit conversion to default EnumType
		(can't overload explicit cast operator in C++03) */
	ScaledNum<iSCALE,IntType> convert() const
	{
		ScaledNum<iSCALE,IntType> r;
		r.m_i = m_i;
		return r;
	}

	/*	Better be explicit about rounding. Since conversion to int should
		not be extremely frequent, I recommend rounding in most cases. */
	//int getInt() const { return round(); }
	// Cast operator - again, better to be explicit.
	//operator int() const { return getInt(); }
	int round() const; // Expect this to get inlined for unsigned IntType
	/*	Only for signed IntType. Non-branching, expect this to get inlined always,
		but only works on non-negative numbers. Asserts non-negativity, so using
		this over round may also help uncover bugs. */
	int uround() const;
	int floor() const
	{
		return static_cast<int>(m_i / SCALE);
	}
	int ceil() const
	{
		int iR = floor();
		return iR + ((m_i >= 0 && m_i - iR * SCALE > 0) ? 1 : 0);
	}
	int uceil() const;
	bool isInt() const
	{
		return (m_i % SCALE == 0);
	}

	int getPercent() const
	{
		return safeToInt(mulDivRound(m_i, 100, SCALE));
	}
	int getPermille() const
	{
		return safeToInt(mulDivRound(m_i, 1000, SCALE));
	}
	int roundToMultiple(int iMultiple) const
	{
		return mulDivRound(m_i, 1, SCALE * iMultiple) * iMultiple;
	}
	int toMultipleFloor(int iMultiple) const
	{
		return (m_i / (SCALE * iMultiple)) * iMultiple;
	}
	double getDouble() const
	{
		return m_i / static_cast<double>(SCALE);
	}
	float getFloat() const
	{
		return m_i / static_cast<float>(SCALE);
	}
	/*	Tbd.: A static cache returned by reference doesn't work when
		inserting into a stream, e.g.
		out << r1.str() << "," << r2.str()
		Simply return by value instead? */
	CvString const& str(int iDen = iSCALE) const
	{
		if (iDen == 1)
			szBuf.Format("%s%d", isInt() ? "" : "ca. ", round());
		else if (iDen == 100)
			szBuf.Format("%d percent", getPercent());
		else if (iDen == 1000)
			szBuf.Format("%d permille", getPermille());
		else szBuf.Format("%d/%d", safeToInt(mulDivByScale(m_i, iDen)), iDen);
		return szBuf;
	} // No overloaded operator<< b/c there isn't a good default display format

	void write(FDataStreamBase* pStream) const
	{
		pStream->Write(m_i);
	}
	void read(FDataStreamBase* pStream)
	{
		pStream->Read(&m_i);
	}

	void mulDiv(int iMultiplier, int iDivisor)
	{
		m_i = safeCast(mulDiv(m_i, iMultiplier, iDivisor));
	}

	// Bernoulli trial (coin flip) with success probability equal to m_i/SCALE
	bool randSuccess(CvRandom& kRand, char const* szLog,
			int iLogData1 = MIN_INT, int iLogData2 = MIN_INT) const;

	ScaledNum pow(int iExp) const;
	ScaledNum pow(ScaledNum rExp) const
	{
		return _pow<rExp.bSIGNED>(rExp);
	}
	ScaledNum sqrt() const
	{
		FAssert(!isNegative());
		return powNonNegative(fromRational<1,2>());
	}
	ScaledNum exp() const
	{
		return fromRational<27182818,10000000>().pow(*this);
	}
	void exponentiate(int iExp)
	{
		*this = pow(iExp);
	}
	void exponentiate(ScaledNum rExp)
	{
		*this = pow(rExp);
	}

	ScaledNum abs() const
	{
		return _abs<bSIGNED>();
	}

	template<typename LoType, typename HiType>
	void clamp(LoType lo, HiType hi)
	{
		FAssert(lo <= hi);
		increaseTo(lo);
		decreaseTo(hi);
	}
	template<typename LoType>
	void increaseTo(LoType lo)
	{
		// (std::max doesn't allow differing types)
		if (*this < lo)
			*this = lo; // (Will fail to compile for floating point operand)
	}
	template<typename HiType>
	void decreaseTo(HiType hi)
	{
		if (*this > hi)
			*this = hi;
	}
	/*	Too easy to use these by accident instead of the non-const functions above.
		Could let the above return *this though (tbd.?). */
	/*template<typename LoType>
	ScaledNum increasedTo(LoType lo) const
	{
		ScaledNum rCopy(*this);
		rCopy.increaseTo(lo);
		return rCopy;
	}
	template<typename HiType>
	ScaledNum decreasedTo(HiType hi) const
	{
		ScaledNum rCopy(*this);
		rCopy.decreaseTo(hi);
		return rCopy;
	}*/

	template<typename NumType, typename Epsilon>
	bool approxEquals(NumType num, Epsilon e) const;

	bool isPositive() const { return (m_i > 0); }
	bool isNegative() const { return (bSIGNED && m_i < 0); }
	/*	Typically, the 0 sign doesn't matter, so this function wouldn't be
		as efficient as it could be in most cases. */
	//char getSign() const { return (isPositive() ? 1 : (isNegative() ? -1 : 0)); }

	void flipSign() { *this = -(*this); }
	void flipFraction() { *this = 1 / *this; }
	ScaledNum operator-() const;

	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	bool operator<(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const;
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	bool operator>(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const;
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	bool operator==(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const;
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	bool operator!=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const;
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	bool operator<=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const;
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	bool operator>=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const;

	// Exact comparisons with int - to be consistent with int-float comparisons.
	bool operator<(int i) const
	{
		return (m_i < scaleForComparison(i));
	}
	bool operator>(int i) const
	{
		return (m_i > scaleForComparison(i));
	}
	bool operator==(int i) const
	{
		return (m_i == scaleForComparison(i));
	}
	bool operator!=(int i) const
	{
		return (m_i != scaleForComparison(i));
	}
	bool operator<=(int i) const
	{
		return (m_i <= scaleForComparison(i));
	}
	bool operator>=(int i) const
	{
		return (m_i >= scaleForComparison(i));
	}
	bool operator<(uint i) const
	{
		return (m_i < scaleForComparison(u));
	}
	bool operator>(uint u) const
	{
		return (m_i > scaleForComparison(u));
	}
	bool operator==(uint u) const
	{
		return (m_i == scaleForComparison(u));
	}
	bool operator!=(uint u) const
	{
		return (m_i != scaleForComparison(i));
	}
	bool operator<=(uint u) const
	{
		return (m_i <= scaleForComparison(u));
	}
	bool operator>=(uint u) const
	{
		return (m_i >= scaleForComparison(u));
	}

	/*	Couldn't guarantee here that only const expressions are used.
		So floating-point operands will have to be wrapped in fixp. */
	/*bool operator<(double d) const
	{
		return (getDouble() < d);
	}
	bool operator>(double d) const
	{
		return (getDouble() > d);
	}*/

	// Operand on different scale: Let ctor implicitly convert it to ScaledNum
	__forceinline ScaledNum& operator+=(ScaledNum rOther);
	__forceinline ScaledNum& operator-=(ScaledNum rOther);

	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	ScaledNum& operator*=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther);
	template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
	ScaledNum& operator/=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther);

	ScaledNum& operator++()
	{
		(*this) += 1;
		return *this;
	}
	ScaledNum& operator--()
	{
		(*this) -= 1;
		return *this;
	}
	ScaledNum operator++(int)
	{
		ScaledNum rCopy(*this);
		(*this) += 1;
		return rCopy;
	}
	ScaledNum operator--(int)
	{
		ScaledNum rCopy(*this);
		(*this) -= 1;
		return rCopy;
	}

	ScaledNum& operator+=(int i)
	{
		(*this) += ScaledNum(i);
		return (*this);
	}
	ScaledNum& operator-=(int i)
	{
		(*this) -= ScaledNum(i);
		return (*this);
	}
	ScaledNum& operator*=(int i)
	{
		(*this) *= ScaledNum(i);
		return (*this);
	}
	ScaledNum& operator/=(int i)
	{
		(*this) /= ScaledNum(i);
		return (*this);
	}
	ScaledNum& operator+=(uint u)
	{
		(*this) += ScaledNum(u);
		return (*this);
	}
	ScaledNum& operator-=(uint u)
	{
		(*this) -= ScaledNum(u);
		return (*this);
	}
	ScaledNum& operator*=(uint u)
	{
		(*this) *= ScaledNum(u);
		return (*this);
	}
	ScaledNum& operator/=(uint u)
	{
		(*this) /= ScaledNum(u);
		return (*this);
	}

	ScaledNum operator+(int i) const
	{
		ScaledNum rCopy(*this);
		rCopy += i;
		return rCopy;
	}
	ScaledNum operator-(int i) const
	{
		ScaledNum rCopy(*this);
		rCopy -= i;
		return rCopy;
	}
	ScaledNum operator*(int i) const
	{
		ScaledNum rCopy(*this);
		rCopy *= i;
		return rCopy;
	}
	ScaledNum operator/(int i) const
	{
		ScaledNum rCopy(*this);
		rCopy /= i;
		return rCopy;
	}
	ScaledNum operator+(uint u) const
	{
		ScaledNum rCopy(*this);
		rCopy += u;
		return rCopy;
	}
	ScaledNum operator-(uint u) const
	{
		ScaledNum rCopy(*this);
		rCopy -= u;
		return rCopy;
	}
	ScaledNum operator*(uint u) const
	{
		ScaledNum rCopy(*this);
		rCopy *= u;
		return rCopy;
	}
	ScaledNum operator/(uint u) const
	{
		ScaledNum rCopy(*this);
		rCopy /= u;
		return rCopy;
	}

private:
	template<bool bBY_SCALE>
	struct mulDivHelper // Wrapper struct to work around limitations of function templates
	{
	template<typename MultiplicandType, typename MultiplierType, typename DivisorType>
	static typename choose_int_type
		< typename choose_int_type<MultiplicandType,MultiplierType>::type, DivisorType >::type
	mulDiv(MultiplicandType multiplicand, MultiplierType multiplier, DivisorType divisor)
	{
		typedef typename choose_int_type
				< typename choose_int_type<MultiplicandType,MultiplierType>::type, DivisorType >::type
				ReturnType;
		BOOST_STATIC_ASSERT(sizeof(MultiplierType) <= 4);
		BOOST_STATIC_ASSERT(sizeof(DivisorType) <= 4);
		#ifdef SCALED_NUM_EXTRA_ASSERTS
			FAssert(divisor != 0);
		#endif
		if (integer_limits<ReturnType>::is_signed)
		{
			int i;
			if (sizeof(MultiplierType) == 4 || sizeof(MultiplicandType) == 4)
			{
				/*	For multiplying signed int, MulDiv (WinBase.h) is fastest.
					NB: Rounds to nearest, can't take advantage of bBY_SCALE. */
				i = MulDiv(static_cast<int>(multiplicand),
						static_cast<int>(multiplier),
						static_cast<int>(divisor));
			}
			else
			{
				// For smaller signed types, int can't overflow.
				i = multiplicand;
				i *= multiplier;
				/*	Rounding to nearest here would add a branch instruction.
					To force rounding, call mulDivRound. */
				if (bBY_SCALE)
					i /= SCALE;
				else i /= divisor;
			}
			return static_cast<ReturnType>(i);
		}
		else
		{
			typedef typename choose_type<
					(sizeof(MultiplicandType) >= 4 || sizeof(MultiplierType) >= 4),
					unsigned __int64, unsigned int>::type ProductType;
			ProductType n = multiplicand;
			n *= multiplier;
			// Will round to nearest b/c it's almost free
			if (bBY_SCALE)
			{
				n += SCALE / 2u; 
				n /= SCALE;
			}
			else
			{
				n += divisor / 2u; 
				n /= divisor;
			}
			return static_cast<ReturnType>(n);
		}
	}
	};
	// Wrappers around the helper struct, for type inference and readable syntax.
	template<typename MultiplicandType, typename MultiplierType, typename DivisorType>
	static typename choose_int_type
		< typename choose_int_type<MultiplicandType,MultiplierType>::type, DivisorType >::type
	mulDiv(MultiplicandType multiplicand, MultiplierType multiplier, DivisorType divisor)
	{	// (Don't know if divisor is a power of 2, and a runtime check isn't worth it.)
		return mulDivHelper<false>::mulDiv(multiplicand, multiplier, divisor);
	}
	template<typename MultiplicandType, typename MultiplierType>
	static typename choose_int_type
		< typename choose_int_type<IntType,MultiplierType>::type, MultiplicandType >::type
	mulDivByScale(MultiplicandType multiplicand, MultiplierType multiplier)
	{
		/*	Tbd.: Try using SSE2 intrinsics when SCALE is a power of 2,
			i.e. when SCALE & (SCALE - 1) == 0. Currently, an int division is
			executed unless the types have fewer than 4 byte. */
		return mulDivHelper<true>::mulDiv(multiplicand, multiplier, SCALE);
	}

	template<typename MultiplierType, typename DivisorType>
	static typename choose_int_type
		< typename choose_int_type<IntType,MultiplierType>::type, DivisorType >::type
	mulDivRound(IntType multiplicand, MultiplierType multiplier, DivisorType divisor)
	{
		typedef typename choose_int_type
				< typename choose_int_type<IntType,MultiplierType>::type, DivisorType >::type
				ReturnType;
		BOOST_STATIC_ASSERT(sizeof(MultiplierType) <= 4);
		BOOST_STATIC_ASSERT(sizeof(DivisorType) <= 4);	
		if (bSIGNED && sizeof(MultiplierType) < 4 && sizeof(IntType) < 4)
		{
			int i = multiplicand;
			i *= multiplier;
			i = intdiv::round(i, divisor);
			i /= divisor;
			return static_cast<ReturnType>(i);
		} // In all remaining cases, mulDiv rounds too.
		return mulDiv(multiplicand, multiplier, divisor);
	}

	template<typename OtherIntType>
	static IntType safeCast(OtherIntType n)
	{
		return safeIntCast<IntType>(n);
	}

	/*	Specialize b/c the sign inversion code wouldn't compile for
		unsigned IntType. */
	template<bool bSigned>
	ScaledNum _pow(ScaledNum rExp) const;
	template<>
	ScaledNum _pow<true>(ScaledNum rExp) const
	{
		FAssert(!isNegative());
		if (rExp.isNegative())
			return 1 / powNonNegative(-rExp);
		return powNonNegative(rExp);
	}
	template<>
	ScaledNum _pow<false>(ScaledNum rExp) const
	{
		return powNonNegative(rExp);
	}

	ScaledNum powNonNegative(int iExp) const
	{
		ScaledNum rCopy(*this);
		/*  This can be done faster in general by squaring.
			However, I doubt that it would be faster for
			the small exponents I'm expecting to deal with. */
		ScaledNum r = 1;
		for (int i = 0; i < iExp; i++)
			r *= rCopy;
		return r;
	}
	/*	Custom algorithm.
		There is a reasonably recent paper "A Division-Free Algorithm for Fixed-Point
		Power Exponential Function in Embedded System" [sic] based on Newton's method.
		That's probably faster and more accurate, but an implementation isn't
		spelled out. Perhaps tbd.
		I use the current implementation in some frequently executed code, and
		replacing it with std::pow for a benchmark test made no appreciable difference. */
	ScaledNum powNonNegative(ScaledNum rExp) const
	{
		/*	Base 0 or too close to it to make a difference given the precision of the algorithm.
			Fixme: rExp could also be close to 0. Should somehow use x=y*z => b^x = (b^y)^z. */
		if (m_i < SCALE / 64)
		{
			// This would be rather expensive and could overflow
			/*if (m_i > 0)
				return 1 / powNonNegative(1 / *this);*/
			return 0;
		}
		/*	Recall that: If x=y+z, then b^x=(b^y)*(b^z).
						 If b=a*c, then b^x=(a^x)*(c^x). */
		/*	Split rExp into the sum of an integer and a (scaled) fraction between 0 and 1.
			(Due to rounding, the fractional part can take the value 1.) */
		// Running example: 5.2^2.1 at SCALE 1024, i.e. (5325/1024)^(2150/1024)
		IntType nExpInt = rExp.m_i / SCALE; // 2 in the example
		// Use uint in all local ScaledNum variables for more accurate rounding
		ScaledNum<128,uint> rExpFrac(rExp - nExpInt); // Ex.: 13/128
		/*	Factorize the base into powers of 2 and, as the last factor, the base divided
			by the product of the 2-bases. */
		ScaledNum<iSCALE,uint> rProductOfPowersOfTwo(1);
		// Will need this as IntType, but our ceil functions return int.
		int iBaseDiv = 1;
		// Look up approximate result of 2^rExpFrac in precomputed table
		#ifdef SCALED_NUM_EXTRA_ASSERTS
			FAssertBounds(0, 129, rExpFrac.m_i);
		#endif
		ScaledNum<256,uint> rPowOfTwo; // Ex.: Array position [13] is 19, so rPowOfTwo=19/256
		rPowOfTwo.m_i = FixedPointPowTables::powersOfTwoNormalized_256[rExpFrac.m_i];
		++rPowOfTwo; // Denormalize (Ex.: 275/256; approximating 2^0.1)
		/*	Tbd.: Try replacing this loop with _BitScanReverse (using the /EHsc compiler flag).
			Or perhaps not available in MSVC03? See: github.com/danaj/Math-Prime-Util/pull/10/
			*/
		{	//while (iBaseDiv < *this) // Would result in expensive overflow handling
			int const iCeil = ceil();
			while (iBaseDiv < iCeil)
			{
				iBaseDiv *= 2;
				// This is expensive b/c it will generally use 64 bit :(
				rProductOfPowersOfTwo *= rPowOfTwo;
			}
		} // Ex.: iBaseDiv=8 and rProductOfPowersOfTwo=1270/1024, approximating (2^0.1)^3.
		ScaledNum<256,uint> rLastFactor(1);
		// Look up approximate result of ((*this)/iBaseDiv)^rExpFrac in precomputed table
		int iLastBaseTimes64 = (ScaledNum<64,uint>(*this / iBaseDiv)).m_i; // Ex.: 42/64 approximating 5.2/8
		#ifdef SCALED_NUM_EXTRA_ASSERTS
			FAssertBounds(0, 64+1, iLastBaseTimes64);
		#endif
		if (rExpFrac.m_i != 0 && iLastBaseTimes64 != 64)
		{
			// Could be prone to cache misses, but tests so far haven't confirmed this.
			rLastFactor.m_i = FixedPointPowTables::powersUnitInterval_256
					[iLastBaseTimes64-1][rExpFrac.m_i-1] + 1; // Table and values are shifted by 1
			// Ex.: Position [41][12] is 244, i.e. rLastFactor=245/256. Approximation of (5.2/8)^0.1
		}
		ScaledNum r(ScaledNum<iSCALE,uint>(pow(nExpInt)) *
				rProductOfPowersOfTwo * ScaledNum<iSCALE,uint>(rLastFactor));
		return r;
		/*	Ex.: First factor is 27691/1024, approximating 5.2^2,
			second factor: 1270/1024, approximating (2^0.1)^3,
			last factor: 980/1024, approximating (5.2/8)^0.1.
			Result: 32867/1024, which is ca. 32.097, whereas 5.2^2.1 is ca. 31.887. */
	}

	template<typename OtherIntType>
	static typename product_int_type<IntType,OtherIntType>::type
	scaleForComparison(OtherIntType n)
	{
		// Tbd.: Perhaps some intrinsic function could do this faster (on the caller's side)?
		typedef typename product_int_type<IntType,OtherIntType>::type LongType;
		LongType lNum = n;
		return lNum * SCALE;
	}

	/*	Tbd.: Public only as a temporary measure for codebases that use
		floating-point numbers and can't immediately replace them all with ScaledNum.
		Converting from double to ScaledNum at runtime really defeats the
		purpose of the ScaledNum class. */
	public:
	static ScaledNum fromDouble(double d)
	{
		ScaledNum r;
		r.m_i = safeCast(fmath::round(d * SCALE));
		return r;
	}
	private:

	// Use specialization so that the non-branching (unsigned) version can be inlined
	template<bool bSigned>
	ScaledNum _abs() const;
	template<>
	ScaledNum _abs<false>() const
	{
		return *this;
	}
	template<>
	ScaledNum _abs<true>() const
	{
		return (isNegative() ? -(*this) : *this);
	}
};
#pragma pack(pop)

/*	To unclutter template parameter lists and make it easier to add more parameters.
	Un-defined at the end of the file. */
#define ScaledNum_PARAMS int iSCALE, typename IntType, typename EnumType
#define ScaledNum_T ScaledNum<iSCALE,IntType,EnumType>

template<ScaledNum_PARAMS>
template<int iFROM_SCALE, typename OtherIntType, typename OtherEnumType>
/*	Take the argument by reference although this isn't technically a copy constructor.
	Taking it by value leads to peculiar compiler errors when an assignment is followed 
	by an opening curly brace (compiler demands a semicolon then). */
ScaledNum_T::ScaledNum(ScaledNum<iFROM_SCALE,OtherIntType,OtherEnumType> const& rOther)
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	static OtherIntType const FROM_SCALE = ScaledNum<iFROM_SCALE,OtherIntType,OtherEnumType>::SCALE;
	if (FROM_SCALE == SCALE)
		m_i = safeCast(rOther.m_i);
	else
	{
		m_i = safeCast(ScaledNum<iFROM_SCALE,OtherIntType,OtherEnumType>::
				mulDivByScale(rOther.m_i, SCALE));
	}
}

template<ScaledNum_PARAMS>
int ScaledNum_T::round() const
{
	BOOST_STATIC_ASSERT(INTMAX >= SCALE);
	if (bSIGNED)
	{
		FAssert(m_i > 0 ?
				m_i <= static_cast<IntType>(INTMAX - SCALE / 2) :
				m_i >= static_cast<IntType>(INTMIN + SCALE / 2));
		return (m_i + SCALE / static_cast<IntType>(m_i >= 0 ? 2 : -2)) / SCALE;
	}
	FAssert(m_i <= static_cast<IntType>(INTMAX - SCALE / 2u));
	return (m_i + SCALE / 2u) / SCALE;
}

template<ScaledNum_PARAMS>
int ScaledNum_T::uround() const
{
	BOOST_STATIC_ASSERT(bSIGNED); // Use round() instead
	BOOST_STATIC_ASSERT(INTMAX >= SCALE);
	FAssert(m_i >= 0 && m_i <= static_cast<IntType>(INTMAX - SCALE / 2));
	return (m_i + SCALE / 2) / SCALE;
}


template<ScaledNum_PARAMS>
int ScaledNum_T::uceil() const
{
	BOOST_STATIC_ASSERT(bSIGNED); // Use ceil() instead
	BOOST_STATIC_ASSERT(INTMAX >= SCALE);
	FAssert(m_i >= 0 && m_i <= static_cast<IntType>(INTMAX - SCALE + 1));
	return (m_i + SCALE - 1) / SCALE;
}


template<ScaledNum_PARAMS>
bool ScaledNum_T::randSuccess(CvRandom& kRand, char const* szLog,
	int iLogData1, int iLogData2) const
{
	// Guards for better performance and to avoid unnecessary log output
	if (m_i <= 0)
		return false;
	if (m_i >= SCALE)
		return true;
	BOOST_STATIC_ASSERT(SCALE <= USHRT_MAX);
	/*	When porting ScaledNum to another mod, one may want to use:
		return (kRand.get(static_cast<unsigned short>(SCALE), szLog) < m_i); */
	return (kRand.getInt(SCALE, szLog, iLogData1, iLogData2) < m_i);
}

template<ScaledNum_PARAMS>
ScaledNum_T ScaledNum_T::pow(int iExp) const
{
	if (iExp < 0)
		return 1 / powNonNegative(-iExp);
	return powNonNegative(iExp);
}

template<ScaledNum_PARAMS>
template<typename NumType, typename Epsilon>
bool ScaledNum_T::approxEquals(NumType num, Epsilon e) const
{
	/*	Can't be allowed for floating-point types; will have to use fixp to wrap.
		(Wouldn't compile anyway b/c arithmetic and comparison operators aren't
		overloaded for float. The assert is just for clarity.) */
	BOOST_STATIC_ASSERT(!std::numeric_limits<NumType>::has_infinity);
	BOOST_STATIC_ASSERT(!std::numeric_limits<Epsilon>::has_infinity);
	if (!bSIGNED)
		return (*this <= num + e && *this + e >= num);
	return ((*this - num).abs() <= e);
}

template<ScaledNum_PARAMS>
ScaledNum_T ScaledNum_T::operator-() const
{
	BOOST_STATIC_ASSERT(bSIGNED);
	#ifdef SCALED_NUM_EXTRA_ASSERTS
		FAssertMsg(m_i != INTMIN, "INTMIN can't be inverted");
	#endif
	ScaledNum_T r;
	r.m_i = -m_i;
	return r;
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
bool ScaledNum_T::operator<(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	if (iOTHER_SCALE == iSCALE)
	{
		typedef typename choose_safe_int_type<IntType,OtherIntType>::type SafeIntType;
		return (static_cast<SafeIntType>(m_i) < static_cast<SafeIntType>(rOther.m_i));
	}
	return (ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::scaleForComparison(m_i) <
			scaleForComparison(rOther.m_i));
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
bool ScaledNum_T::operator>(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	if (iOTHER_SCALE == iSCALE)
	{
		typedef typename choose_safe_int_type<IntType,OtherIntType>::type SafeIntType;
		return (static_cast<SafeIntType>(m_i) > static_cast<SafeIntType>(rOther.m_i));
	}
	return (ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::scaleForComparison(m_i) >
			scaleForComparison(rOther.m_i));
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
bool ScaledNum_T::operator==(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	if (iOTHER_SCALE == iSCALE)
	{
		typedef typename choose_safe_int_type<IntType,OtherIntType>::type SafeIntType;
		return (static_cast<SafeIntType>(m_i) == static_cast<SafeIntType>(rOther.m_i));
	}
	return (ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::scaleForComparison(m_i) ==
			scaleForComparison(rOther.m_i));
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
bool ScaledNum_T::operator!=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	if (iOTHER_SCALE == iSCALE)
	{
		typedef typename choose_safe_int_type<IntType,OtherIntType>::type SafeIntType;
		return (static_cast<SafeIntType>(m_i) != static_cast<SafeIntType>(rOther.m_i));
	}
	return (ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::scaleForComparison(m_i) !=
			scaleForComparison(rOther.m_i));
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
bool ScaledNum_T::operator<=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	if (iOTHER_SCALE == iSCALE)
	{
		typedef typename choose_safe_int_type<IntType,OtherIntType>::type SafeIntType;
		return (static_cast<SafeIntType>(m_i) <= static_cast<SafeIntType>(rOther.m_i));
	}
	return (ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::scaleForComparison(m_i) <=
			scaleForComparison(rOther.m_i));
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
bool ScaledNum_T::operator>=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther) const
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	if (iOTHER_SCALE == iSCALE)
	{
		typedef typename choose_safe_int_type<IntType,OtherIntType>::type SafeIntType;
		return (static_cast<SafeIntType>(m_i) >= static_cast<SafeIntType>(rOther.m_i));
	}
	return (ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::scaleForComparison(m_i) >=
			scaleForComparison(rOther.m_i));
}

template<ScaledNum_PARAMS>
ScaledNum_T& ScaledNum_T::operator+=(ScaledNum rOther)
{
	#ifdef SCALED_NUM_EXTRA_ASSERTS
		FAssert(rOther <= 0 || m_i <= INTMAX - rOther.m_i);
		FAssert(rOther >= 0 || m_i >= INTMIN - rOther.m_i);
	#endif
	m_i += rOther.m_i;
	return *this;
}

template<ScaledNum_PARAMS>
ScaledNum_T& ScaledNum_T::operator-=(ScaledNum rOther)
{
	#ifdef SCALED_NUM_EXTRA_ASSERTS
		FAssert(rOther >= 0 || m_i <= INTMAX + rOther.m_i);
		FAssert(rOther <= 0 || m_i >= INTMIN + rOther.m_i);
	#endif
	// Signedness may differ here
	m_i = static_cast<IntType>(m_i - rOther.m_i);
	return *this;
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
ScaledNum_T& ScaledNum_T::operator*=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther)
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	m_i = safeCast(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::mulDivByScale(m_i, rOther.m_i));
	return *this;
}

template<ScaledNum_PARAMS>
template<int iOTHER_SCALE, typename OtherIntType, typename OtherEnumType>
ScaledNum_T& ScaledNum_T::operator/=(ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType> rOther)
{
	STATIC_ASSERT_COMPATIBLE(EnumType,OtherEnumType);
	m_i = safeCast(mulDiv(m_i, ScaledNum<iOTHER_SCALE,OtherIntType,OtherEnumType>::SCALE, rOther.m_i));
	return *this;
}

#define COMMON_SCALED_NUM \
	typename choose_type<(iLEFT_SCALE >= iRIGHT_SCALE), \
		ScaledNum< \
			iLEFT_SCALE, \
			typename choose_int_type<LeftIntType,RightIntType>::type, \
			typename choose_type<is_same_type<LeftEnumType,int>::value,RightEnumType,LeftEnumType>::type \
		>, \
		ScaledNum< \
			iRIGHT_SCALE, \
			typename choose_int_type<LeftIntType,RightIntType>::type, \
			typename choose_type<is_same_type<LeftEnumType,int>::value,RightEnumType,LeftEnumType>::type \
		> \
	>::type
/*	Simpler, but crashes the compiler (i.e. the above is a workaround).
#define COMMON_SCALED_NUM \
	ScaledNum<(iLEFT_SCALE > iRIGHT_SCALE ? iLEFT_SCALE : iRIGHT_SCALE), \
	typename choose_int_type<LeftIntType,RightIntType>::type, \
	typename choose_type<is_same_type<LeftEnumType,int>::value,RightEnumType,LeftEnumType>::type > */

template<int iLEFT_SCALE,  typename LeftIntType,  typename LeftEnumType,
		 int iRIGHT_SCALE, typename RightIntType, typename RightEnumType>
COMMON_SCALED_NUM
operator+(
	ScaledNum<iLEFT_SCALE,  LeftIntType,  LeftEnumType>  rLeft,
	ScaledNum<iRIGHT_SCALE, RightIntType, RightEnumType> rRight)
{
	STATIC_ASSERT_COMPATIBLE(LeftEnumType,RightEnumType);
	/*	Note: No accuracy would be gained by scaling both operands up to
		iLEFT_SCALE*iRIGHT_SCALE before adding them. */
	COMMON_SCALED_NUM r(rLeft);
	r += rRight;
	return r;
}
template<int iLEFT_SCALE,  typename LeftIntType,  typename LeftEnumType,
		 int iRIGHT_SCALE, typename RightIntType, typename RightEnumType>
COMMON_SCALED_NUM
operator-(
	ScaledNum<iLEFT_SCALE,  LeftIntType,  LeftEnumType>  rLeft,
	ScaledNum<iRIGHT_SCALE, RightIntType, RightEnumType> rRight)
{
	STATIC_ASSERT_COMPATIBLE(LeftEnumType,RightEnumType);
	COMMON_SCALED_NUM r(rLeft);
	r -= rRight;
	return r;
}
template<int iLEFT_SCALE,  typename LeftIntType,  typename LeftEnumType,
		 int iRIGHT_SCALE, typename RightIntType, typename RightEnumType>
__forceinline COMMON_SCALED_NUM
operator*(
	ScaledNum<iLEFT_SCALE,  LeftIntType,  LeftEnumType>  rLeft,
	ScaledNum<iRIGHT_SCALE, RightIntType, RightEnumType> rRight)
{
	STATIC_ASSERT_COMPATIBLE(LeftEnumType,RightEnumType);
	if (iLEFT_SCALE >= iRIGHT_SCALE)
	{
		COMMON_SCALED_NUM r(rLeft);
		r *= rRight;
		return r;
	}
	else
	{
		COMMON_SCALED_NUM r(rRight);
		r *= rLeft;
		return r;
	}
}
template<int iLEFT_SCALE,  typename LeftIntType,  typename LeftEnumType,
		 int iRIGHT_SCALE, typename RightIntType, typename RightEnumType>
__forceinline COMMON_SCALED_NUM
operator/(
	ScaledNum<iLEFT_SCALE,  LeftIntType,  LeftEnumType>  rLeft,
	ScaledNum<iRIGHT_SCALE, RightIntType, RightEnumType> rRight)
{
	STATIC_ASSERT_COMPATIBLE(LeftEnumType,RightEnumType);
	if (iLEFT_SCALE >= iRIGHT_SCALE)
	{
		COMMON_SCALED_NUM r(rLeft);
		r /= rRight;
		return r;
	}
	else
	{
		COMMON_SCALED_NUM rDen(rRight);
		rLeft /= rDen;
		return rLeft;
	}
}

// Commutativity ...

template<ScaledNum_PARAMS>
ScaledNum_T operator+(int i, ScaledNum_T r)
{
	return r + i;
}
/*	As we don't implement an int cast operator, assignment to int
	should be forbidden as well. (No implicit getInt.) */
/*template<ScaledNum_PARAMS>
int& operator+=(int& i, ScaledNum_T r)
{
	i = (r + i).getInt();
	return i;
}*/
template<ScaledNum_PARAMS>
ScaledNum_T operator-(int i, ScaledNum_T r)
{
	return ScaledNum_T(i) - r;
}
/*template<ScaledNum_PARAMS>
int& operator-=(int& i, ScaledNum_T r)
{
	i = (ScaledNum_T(i) - r).getInt();
	return i;
}*/
template<ScaledNum_PARAMS>
ScaledNum_T operator*(int i, ScaledNum_T r)
{
	return r * i;
}
/*template<ScaledNum_PARAMS>
int& operator*=(int& i, ScaledNum_T r)
{
	i = (r * i).getInt();
	return i;
}*/
template<ScaledNum_PARAMS>
ScaledNum_T operator/(int i, ScaledNum_T r)
{
	return ScaledNum_T(i) / r;
}
/*template<ScaledNum_PARAMS>
int& operator/=(int& i, ScaledNum_T r)
{
	i = (ScaledNum_T(i) / r).getInt();
	return i;
}*/
template<ScaledNum_PARAMS>
ScaledNum_T operator+(uint u, ScaledNum_T r)
{
	return r + u;
}
template<ScaledNum_PARAMS>
ScaledNum_T operator-(uint u, ScaledNum_T r)
{
	return r - u;
}
template<ScaledNum_PARAMS>
ScaledNum_T operator*(uint ui, ScaledNum_T r)
{
	return r * ui;
}
template<ScaledNum_PARAMS>
ScaledNum_T operator/(uint u, ScaledNum_T r)
{
	return r / u;
}
template<ScaledNum_PARAMS>
bool operator<(int i, ScaledNum_T r)
{
	return (r > i);
}
template<ScaledNum_PARAMS>
bool operator>(int i, ScaledNum_T r)
{
	return (r < i);
}
template<ScaledNum_PARAMS>
bool operator==(int i, ScaledNum_T r)
{
	return (r == i);
}
template<ScaledNum_PARAMS>
bool operator!=(int i, ScaledNum_T r)
{
	return (r != i);
}
template<ScaledNum_PARAMS>
bool operator<=(int i, ScaledNum_T r)
{
	return (r >= i);
}
template<ScaledNum_PARAMS>
bool operator>=(int i, ScaledNum_T r)
{
	return (r <= i);
}
/*	Couldn't guarantee here that only const expressions are used.
	So floating-point operands will have to be wrapped in fixp. */
/*template<ScaledNum_PARAMS>
bool operator<(double d, ScaledNum_T r)
{
	return (r > d);
}
template<ScaledNum_PARAMS>
bool operator>(double d, ScaledNum_T r)
{
	return (r < d);
}*/

// Scale 2048 leads to MAX=1048575, i.e. 1024*1024-1.
typedef ScaledNum<2048,int> scaled;
typedef ScaledNum<2048,uint> uscaled;

#define TYPEDEF_SCALED_ENUM(iScale,IntType,TypeName) \
	enum TypeName##Types {}; /* Not really supposed to be used anywhere else */ \
	typedef ScaledNum<iScale,IntType,TypeName##Types> TypeName;

/*	Note that the uint versions will not be called when
	the caller passes a positive signed int literal (e.g. 5);
	will have to be an unsigned literal (e.g. 5u). */
inline uscaled per100(uint uiNum)
{
	return uscaled(uiNum, 100u);
}
inline scaled per100(int iNum)
{
	return scaled(iNum, 100);
}
inline uscaled per1000(uint uiNum)
{
	return uscaled(uiNum, 1000u);
}
inline scaled per1000(int iNum)
{
	return scaled(iNum, 1000);
}
inline uscaled per10000(uint uiNum)
{
	return uscaled(uiNum, 10000u);
}
inline scaled per10000(int iNum)
{
	return scaled(iNum, 10000);
}
/*	'scaled' construction from double. Only const expressions are allowed.
	Can only make sure of that through a macro (as we want to spare the caller
	the use of angle brackets). Tbd.: Could return a uscaled
	when the double expression is non-negative:
	choose_type<(dConstExpr) >= 0,uscaled,scaled>::type::fromRational
	Arithmetic operations are faster on uscaled, but mixing the two types
	isn't going to be helpful. So perhaps create a separate ufixp macro instead(?). */
#define fixp(dConstExpr) \
		((dConstExpr) >= ((int)MAX_INT) / 10000 - 1 || \
		(dConstExpr) <= ((int)MIN_INT) / 10000 + 1 ? \
		scaled(-1) : \
		scaled::fromRational<(int)( \
		(dConstExpr) * 10000 + ((dConstExpr) > 0 ? 0.5 : -0.5)), 10000>())
/*#define ufixp(dConstExpr) \
		((dConstExpr) >= ((uint)MAX_UNSIGNED_INT) / 10000u - 1u || \
		(dConstExpr) < 0 ? \
		uscaled(0u) : \
		uscaled::fromRational<(uint)( \
		(dConstExpr) * 10000 + 0.5), 10000u>())*/

#undef ScaledNum_PARAMS
#undef ScaledNum_T
#undef INT_TYPE_CHOICE

#endif
