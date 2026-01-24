#pragma once
#ifndef INTEGER_CONVERSION_H
#define INTEGER_CONVERSION_H

// advc.make: Level-4 c4244 warnings make such integer cast helpers pretty indispensable

// Compile-time check
#define IS_SAFE_INT_CAST(FromType, ToType) \
	(integer_limits<FromType>::is_integer && \
	integer_limits<ToType>::is_integer && \
	/* If they have the same signedness, then */ \
	/* ToType only needs to be at least as big as FromType. */ \
	((integer_limits<FromType>::is_signed == \
	integer_limits<ToType>::is_signed && \
	sizeof(ToType) >= sizeof(FromType)) || \
	/* Signedness differs: this is always problematic if ToType is unsigned; */ \
	/* FromType being unsigned is OK if ToType is strictly bigger. */ \
	((!integer_limits<FromType>::is_signed || \
	integer_limits<ToType>::is_signed) && \
	sizeof(ToType) > sizeof(FromType))))

/*	Run-time check.
	Wrapping this into a struct template b/c function templates
	can't be partially specialized. Then wrapping that in global functions
	for inference of FromType. */
template<typename ToType, typename FromType,
	bool bASSERT = true, bool bTRUNCATE = false, bool bALLOW_POINTER = false>
struct int_cast
{
	BOOST_STATIC_ASSERT(bASSERT || bTRUNCATE); // Should use built in cast otherwise
	/*	Can use these instead when enum types don't need to be supported
		(i.e. when porting this header into a different mod). */
	//typedef ToType T; typedef FromType F;
	typedef typename choose_type<enum_traits<ToType>::is_enum, int, ToType>::type T;
	typedef typename choose_type<enum_traits<FromType>::is_enum, int, FromType>::type F;
public:
	static ToType safe(FromType f)
	{
		static bool const bPOINTER = (sizeof(T) == sizeof(F) &&
				(is_pointer_type<F>::value || is_pointer_type<T>::value));
		static bool const bINTEGRAL =
				// NB: std treats bool as integer (integer_limits does not)
				(std::numeric_limits<T>::is_integer &&
				std::numeric_limits<F>::is_integer);
		BOOST_STATIC_ASSERT((bINTEGRAL ||
				(bALLOW_POINTER && bPOINTER) ||
				(std::numeric_limits<F>::has_infinity &&
				std::numeric_limits<T>::has_infinity) ||
				is_same_type<F,T>::value));
		#ifndef FASSERT_ENABLE
		if (!bTRUNCATE)
			return (ToType)f;
		#endif
		return _safe<(!IS_SAFE_INT_CAST(F, T) && bINTEGRAL),
				(bALLOW_POINTER && bPOINTER)>(f);
	}
private:
	template<bool bCHECK_LIMITS, bool bPOINTER>
	static ToType _safe(FromType f)
	{
		return reinterpret_cast<ToType>(f);
	}
	template<>
	static ToType _safe<false,false>(FromType f)
	{
		return static_cast<ToType>(f);
	}

	template<>
	static ToType _safe<true,false>(FromType f)
	{
		// Handle potentially unsafe integer casts ...
		if (!integer_limits<T>::is_signed)
		{
			#pragma warning(push)
			#pragma warning(disable: 804) // "unsafe use of type bool in operation"
			FAssert(f >= 0);
			#pragma warning(pop)
			// (No need to check max if ToType is at least as big as FromType)
			if (sizeof(F) > sizeof(T))
				f = safeUpper(f);
		}
		else if (!integer_limits<F>::is_signed)
		{	// (No need to check min if FromType is unsigned.)
			/*	Cast of max to FromType in safeUpper is safe b/c of failed
				IS_SAFE_INT_CAST check upfront. */
			f = safeUpper(f);
		}
		else
		{	/*	Both signed: Failed IS_SAFE_INT_CAST implies that
				FromType is strictly bigger, so casting the limits in SafeUpper/
				safeLower is safe. */
			f = safeLower(f);
			f = safeUpper(f);
		}
		return (ToType)f;
	}
	static FromType safeUpper(FromType f)
	{
		F fMax = (F)integer_limits<T>::max;
		if (f > fMax)
		{
			if (bASSERT)
				FErrorMsg("integer limit exceeded (number too big)");
			if (bTRUNCATE)
				f = static_cast<FromType>(fMax);
		}
		return f;
	}
	static FromType safeLower(FromType f)
	{
		F fMin = (F)integer_limits<T>::min;
		if (f < fMin)
		{
			if (bASSERT)
				FErrorMsg("integer limit exceeded (number too small)");
			if (bTRUNCATE)
				f = static_cast<FromType>(fMin);
		}
		return f;
	}
};

template<typename ToType, typename FromType>
__inline static ToType safeIntCast(FromType iVal)
{
	return int_cast<ToType,FromType,true,false>::safe(iVal);
}

/*	Don't know about the function names here ...
	truncIntCast will clamp (i.e. safely enforce the limits of ToType)
	but also assert that clamping isn't necessary,
	clampIntCast will treat clamping as acceptable (no assertion). */
template<typename ToType, typename FromType>
__inline static ToType truncIntCast(FromType iVal)
{
	return int_cast<ToType,FromType,true,true>::safe(iVal);
}

template<typename ToType, typename FromType>
__inline static ToType clampIntCast(FromType iVal)
{
	return int_cast<ToType,FromType,false,true>::safe(iVal);
}

#endif
