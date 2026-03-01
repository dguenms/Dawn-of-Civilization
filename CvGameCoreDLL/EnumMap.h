#pragma once
#ifndef ENUM_MAP_H
#define ENUM_MAP_H

class FDataStreamBase;

/*	Classes that map an enum key type E to a value type V.
	Based on Nightinggale's EnumMap class template in the "We the People" mod
	(WtP) prior to its Jan 2022 rewrite.
	Internally, keys and values may be represented more compactly through
	information from the enum_traits struct. For V, a compact representation
	can be set through an optional template parameter CV. V and CV can be any
	types so long as V values and 0 can be cast to CV. A default value can be
	set through a fourth template parameter iDEFAULT. The default value serves
	as the initial value and gets used by the reset and resetVal functions.
	If iDEFAULT isn't set, then the values default to -1 if V is an enum type,
	0 otherwise.
	Example: ArrayEnumMap<UnitTypes,DomainTypes,void*,DOMAIN_LAND>
			maps UnitTypes keys - represented internally as short int -
			to DomainTypes values - represented internally as signed char.
			CV=void* is a hack for setting iDEFAULT (to DOMAIN_LAND) while
			leaving the choice of CV up to enum_traits.
	The public interface of the enum map classes (not easy to see at a glance
	in the code) consists of:
		default constructor, copy constructor and assignment operator
		V get(E) const
		set(E, V)
		insert(int, V) -- Like set, but accepts int keys; for XML loading.
		setAll(V)
		reset() -- Resets all values to the map's default value.
		resetVal(E) -- Resets the value stored for the given enum key.
		int numNonDefault() const -- Number of keys with a non-default value.
		bool isAnyNonDefault() const
		write(FDataStream*) const -- serialize
		read(FDataStream*) -- deserialize
		V operator[](E) const -- Lookup that never checks array bounds
	(Non-const subscript is implemented only for array-based enum map types;
	not worth implementing for enum maps based on lists.)
	If V is an arithmetic type (according to the arithmetic_traits struct),
	then
		add(E, V)
		multiply(E, V)
		divide(E, V)
	are supported. If V is bool, then
		toggle(E)
	is supported instead. */
/*	Also part of the public interface: Macros for iterating over the
	non-default values (and the associated keys) in an enum map. For ListEnumMap,
	this is usually more efficient than looking up each key.
	The type information can, unfortunately, not be inferred from the
	kEnumMap instance. ValueType doesn't have to be the same type as V; can be
	any type that V can be safely converted to. */
#define iANON_NON_DEFAULT_ITER CONCATVARNAME(iAnonNonDefaultIter_L, __LINE__)
#define FOR_EACH_NON_DEFAULT_PAIR(kEnumMap, EnumPrefix, ValueType) \
	int iANON_NON_DEFAULT_ITER = 0; \
	for (std::pair<EnumPrefix##Types,ValueType> per##EnumPrefix##Val; \
		(kEnumMap).nextNonDefaultPair<ValueType>(iANON_NON_DEFAULT_ITER, per##EnumPrefix##Val); )
/*	Example:
FOR_EACH_NON_DEFAULT_PAIR(m_aiBlockadedCount, Team, int)
	expands to
int iAnonNonDefaultIter_L3947 = 0; // (or sth. like that)
for (std::pair<TeamTypes,int> perTeamVal;
	m_aiBlockadedCount.nextNonDefaultPair<int>(iAnonNonDefaultIter_L3947, perTeamVal); )*/

// Mainly for boolean value type
#define FOR_EACH_NON_DEFAULT_KEY(kEnumMap, EnumPrefix) \
	int iANON_NON_DEFAULT_ITER = 0; \
	for (EnumPrefix##Types eLoop##EnumPrefix = \
		(kEnumMap).nextNonDefaultKey(iANON_NON_DEFAULT_ITER); \
		eLoop##EnumPrefix != (kEnumMap).endKey(); \
		eLoop##EnumPrefix = (kEnumMap).nextNonDefaultKey(iANON_NON_DEFAULT_ITER))

/*	Uncomment to enable additional assertions. These all concern conditions that
	the user of this class is supposed to ensure; mainly overflow checks.
	(Array bounds are checked in any case, i.e. so long as assertions are enabled.) */
//#define ENUM_MAP_EXTRA_ASSERTS

// Local helpers
#define FOR_EACH_KEY(eKey) \
	for (E eKey = enum_traits<E>::first; eKey < getLength(); ++eKey)
#define BITSIZE(T) \
	(sizeof(T) * 8)

/*	advc.xmldefault: Need copy-constructors in this hierarchy so that
	CvInfo classes with enum map members can be safely copied.
	Best to also define assignment operators then. Wrap that into a macro "ASSIGN"
	so that derived classes only need to provide the body of an "assign" function.
	Classes that are derived from derived classes and have no data members
	don't need to use the macro; their implicitly-defined copy functions will
	call the (explicitly-defined) base-class copy functions -- and will do
	nothing else b/c there won't be any derived-class data to copy. */
#define ASSIGN(T) \
	T(T const& kOther) \
	{ \
		assign<true>(kOther); \
	} \
	T& operator=(T const& kOther) \
	{ \
		assign<false>(kOther); \
		return *this; \
	} \
	/* Would prefer to make this protected, but whatever ... */ \
	template<bool bUNINITIALIZED> \
	void assign(T const& kOther)

// Memory shared by all enum map classes
// Actually, make it a template so that static data members can be defined in the header.
template<class Dummy>
class EnumMapNonTempl
{
protected:
	// A kind of /dev/null for assignments without any effect
	static long long m_lDummy;
};
template<class Dummy>
long long EnumMapNonTempl<Dummy>::m_lDummy = 0;

/*	iDEFAULT can't have type V b/c that wouldn't work for non-integral types.
	Meaning, unfortunately, that fractional default values (for float, ScaledNum)
	aren't possible. */
template<class Derived, typename E, class V, class CV, int iDEFAULT>
class EnumMapBase : EnumMapNonTempl<int>
{
protected:
	// CRT pattern (static polymorphism)
	Derived& derived() { return *static_cast<Derived*>(this); }
	Derived const& derived() const { return *static_cast<Derived const*>(this); }
	EnumMapBase() {} // abstract base class
	EnumMapBase(EnumMapBase const&) {}

	typedef uint BitBlock;
private: // Just a helper for readability (also in the debugger)
	typedef typename choose_type<
			(is_same_type<V,bool>::value), BitBlock, // Represent bool as bit blocks ...
			typename enum_traits<V>::compact_t>::type // ... and enum as short or char.
			DefaultCVType;
protected:
	// CV=void* means that we should use DefaultCVType for representing V compactly
	typedef typename choose_type<is_same_type<CV,void*>::value, DefaultCVType, CV>
			::type CompactV;
	typedef typename enum_traits<E>::compact_t CompactE;
	static V const vDEFAULT; // Can't initialize in-class b/c can be non-integral
	static CompactV const cvDEFAULT;
	static bool const bARITHMETIC = arithm_traits<V>::is_arithmetic;
	/*	For bool values, the only valid compact types are the BitBlock type
		and bool itself. */
	BOOST_STATIC_ASSERT((!is_same_type<V,bool>::value ||
			is_same_type<CompactV,bool>::value ||
			is_same_type<CompactV,BitBlock>::value));
	static bool const bBIT_BLOCKS = (is_same_type<V,bool>::value &&
			is_same_type<CompactV,BitBlock>::value);
	enum Operation { OP_ASSIGN, OP_ADD, OP_MULT, OP_DIV, OP_TOGGLE, OP_UNKNOWN };

public:
	// Externally visible statics ...
	static E getLength()
	{
		return enum_traits<E>::length();
	}
	typedef E EnumType;
	typedef V ValueType;
	static V const defaultValue;
	static bool const isArithmeticValues = bARITHMETIC;
	/*	Derived classes that only allocate memory in the constructor (or use only
		static memory) should set this to false */
	static bool const isLazyAllocation = true;
	/*	I've tried making endKey and ceEndKey variables, but there is some
		(MSVC03-specific?) problem with the order of initialization when a
		static const enum variable is initialized through another static variable;
		doesn't reliably get initialized that way. See also a comment about
		enum_traits<E>::len being of type int instead of E.*/
	static E endKey()
	{
		/*	Marking the end of the key sequence with a value greater than
			any valid key is arithmetically more helpful than using a
			"NO_..." enumerator (-1). */
		return static_cast<E>(enum_traits<E>::len);
	}
protected:
	static CompactE ceEndKey()
	{
		return compactKey(endKey());
	}

public:
	/*	At a minimum, derived classes need to define a reset function,
		a get function and a lookup function template.
		Derived classes with bARITHMETIC=false can implement setUnsafe
		(or setCompact) instead of lookup.*/
	V get(E eKey) const
	{	// Derived classes can assert that eKey is within its bounds here
		return derived().getUnsafe(eKey);
	}
	void set(E eKey, V vValue)
	{
		derived().changeValue<OP_ASSIGN>(eKey, vValue);
	}
	void add(E eKey, V vAddend)
	{
		derived().changeValue<OP_ADD>(eKey, vAddend);
	}
	void multiply(E eKey, V vMultiplier)
	{
		derived().changeValue<OP_MULT>(eKey, vMultiplier);
	}
	void divide(E eKey, V vDivisor)
	{
		derived().changeValue<OP_DIV>(eKey, vDivisor);
	}
	void toggle(E eKey)
	{
		derived().changeValue<OP_TOGGLE>(eKey, false);
	}
	void reset()
	{
		FOR_EACH_KEY(eKey)
			derived().resetVal(eKey);
	}
	void resetVal(E eKey)
	{
		derived().resetValUnsafe(eKey);
	}
	void setAll(V vValue)
	{
		FOR_EACH_KEY(eKey)
			derived().setUnsafe(eKey, vValue);
	}
	int numNonDefault() const
	{
		int iCount = 0;
		FOR_EACH_KEY(eKey)
		{
			if (derived().getUnsafe(eKey) != vDEFAULT)
				iCount++;
		}
		return iCount;
	}
	bool isAnyNonDefault() const
	{
		return (derived().numNonDefault() > 0);
	}
	V operator[](E eKey) const
	{
		return derived().getUnsafe(eKey);
	}

	// For FOR_EACH_NON_DEFAULT_... macros
	template<typename ValueType>
	bool nextNonDefaultPair(int& iIter, std::pair<E,ValueType>& kPair) const
	{
		// Allow caller to use a larger type for the map values
		BOOST_STATIC_ASSERT((is_same_type<V,ValueType>::value || // for bool
				// For int-encoded map (a more narrow check would be nicer ...)
				(!integer_limits<ValueType>::is_signed && sizeof(V) == sizeof(ValueType)) ||
				IS_SAFE_INT_CAST(CompactV, ValueType)));
		return derived()._nextNonDefaultPair<ValueType>(iIter, kPair);
	}
	// End of sequence signaled by returning endKey()
	E nextNonDefaultKey(int& iIter) const
	{
		// Indirection only to be consistent with nextNonDefaultPair
		return derived()._nextNonDefaultKey(iIter);
	}

	void insert(int iKey, V vValue)
	{
		E eKey = static_cast<E>(iKey);
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssertInfoEnum(eKey);
		// insert is not supposed to change values that are already stored
		FAssert(derived().get(eKey) == vDEFAULT);
		derived().setUnsafe(eKey, vValue);
	#else
		derived().set(eKey, vValue);
	#endif
	}
	/*	Make every write function a template - in order to prevent a
		failed static assertion in writeVal when all write functions are
		in fact unused. Turn the data stream into a template param
		when there would be none otherwise. */
	template<class DataStream>
	void write(DataStream* pStream) const
	{
		derived().writeArray<CompactV>(pStream);
	}
	void read(FDataStreamBase* pStream, int iSubtrahend = 0)
	{
		derived().readArray<CompactV>(pStream, iSubtrahend);
	}
	template<typename SizeType, typename ValueType>
	void writeLazyArray(FDataStreamBase* pStream) const
	{
		if (!isAnyNonDefault())
		{
			pStream->Write(static_cast<SizeType>(0));
			return;
		}
		derived().writeArray<ValueType>(pStream);
	}
	template<typename SizeType, typename ValueType>
	void readLazyArray(FDataStreamBase* pStream,
		int iSubtrahend = 0) // (Could also get this from sz)
	{
		SizeType sz;
		pStream->Read(&sz);
		if (sz == 0)
			return;
		derived().readArray<ValueType>(pStream, iSubtrahend);
	}
	template<class DataStream>
	void writeLazyIntArray(DataStream* pStream) const
	{
		derived().writeLazyArray<int,int>(pStream);
	}
	void readLazyIntArray(FDataStreamBase* pStream)
	{
		derived().readLazyArray<int,int>(pStream);
	}
	template<typename ValueType>
	void writeArray(FDataStreamBase* pStream) const
	{
		FOR_EACH_KEY(eKey)
			writeVal(pStream, safeCast<ValueType>(derived().getUnsafe(eKey)));
	}
	template<typename ValueType>
	void readArray(FDataStreamBase* pStream, int iSubtrahend = 0)
	{
		/*	Allocating an array and calling Read(getLength(), array) might be faster,
			might be slower. Reading one value at a time is at least easier to debug. */
		int const iLen = getLength() - std::max(0, iSubtrahend);
		for (E eKey = enum_traits<E>::first; eKey < iLen; ++eKey)
		{
			ValueType val;
			pStream->Read(&val);
			derived().setUnsafe(eKey, safeCast<V>(val));
		}
		/*	When a key type has become shorter, we discard the values that were
			saved for the removed keys. */
		for (E eKey = enum_traits<E>::first; eKey < -iSubtrahend; ++eKey)
		{
			ValueType val;
			pStream->Read(&val);
		}
	}

protected:
	V getUnsafe(E eKey) const
	{
		return uncompactValue<V,CompactV>(derived().getCompact(compactKey(eKey)), eKey);
	}
	CompactV getCompact(CompactE ceKey) const
	{
		return derived().getCompact(ceKey);
	}
	void setUnsafe(E eKey, V vValue)
	{
		derived().changeValueUnsafe<OP_ASSIGN>(eKey, vValue);
	}
	void resetValUnsafe(E eKey)
	{
		derived().setUnsafe(eKey, vDEFAULT);
	}
	template<Operation eOP>
	void changeValue(E eKey, V vOperand)
	{
		derived().changeValueUnsafe<eOP>(eKey, vOperand);
	}
	template<class T>
	static T& getDummy()
	{
		BOOST_STATIC_ASSERT((sizeof(T) <= sizeof(m_lDummy)));
		T* pDummy = reinterpret_cast<T*>(&m_lDummy);
		return *pDummy;
	}
	static CompactV& cvDummy()
	{
		CompactV& dummy = getDummy<CompactV>();
		dummy = cvDEFAULT;
		return dummy;
	}
	static V& vDummy()
	{
		V& dummy = getDummy<V>();
		dummy = vDEFAULT;
		return dummy;
	}
	/*	The operation and operand are given so that a derived class can decide
		not to allocate memory based on isNeutralToDefaultVal or other criteria.
		In that case cvDummy() should be returned, which means that any write
		operation of the caller will have no effect. */
	template<Operation eOP>
	CompactV& lookup(E eKey, CompactV cvOperand)
	{
		return derived().lookupUnsafe<eOP>(eKey, cvOperand);
	}
	template<Operation eOP>
	CompactV& lookupUnsafe(E eKey, CompactV cvOperand)
	{
		return derived().lookupCompact<eOP>(compactKey(eKey), cvOperand);
	}
	template<Operation eOP>
	CompactV& lookupCompact(CompactE ceKey, CompactV cvValue)
	{	// (Derived classes have to override one of the lookup function templates)
		return derived().lookupCompact<eOP>(ceKey, cvValue);
	}

	template<Operation eOP>
	void changeValueUnsafe(E eKey, V vOperand)
	{
		BOOST_STATIC_ASSERT(false); // eOP not supported
	}
	template<>
	void changeValueUnsafe<OP_ASSIGN>(E eKey, V vValue)
	{
		CompactV cvNewVal = compactValue(vValue);
		CompactV& cvVal = derived().lookup<OP_ASSIGN>(eKey, cvNewVal);
		CompactV cvOldVal = cvVal;
		// Specialize for bool
		derived().assignVal<CompactV,V>(cvVal, vValue, eKey);
		derived().processValueChange(cvOldVal, cvNewVal);
	}
	template<>
	void changeValueUnsafe<OP_ADD>(E eKey, V vAddend)
	{
		BOOST_STATIC_ASSERT(bARITHMETIC);
		CompactV cvAddend = compactValue(vAddend);
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		CompactV cOldVal = derived().getCompact(compactKey(eKey));
		FAssert(cvAddend > 0 ?
				(cOldVal <= arithm_traits<CompactV>::max - cvAddend) :
				(cOldVal >= arithm_traits<CompactV>::min - cvAddend));
	#endif
		derived().changeValueCompact<OP_ADD>(eKey, cvAddend);
	}
	template<>
	void changeValueUnsafe<OP_MULT>(E eKey, V vMultiplier)
	{
		BOOST_STATIC_ASSERT(bARITHMETIC);
		CompactV cvMultiplier = compactValue(vMultiplier);
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		CompactV cOldVal = derived().getCompact(compactKey(eKey));
		FAssert((cvMultiplier > -1 && cvMultiplier < 1) || // for fractions, 0
				(cOldVal <= arithm_traits<CompactV>::max / cvMultiplier &&
				cOldVal >= arithm_traits<CompactV>::min / cvMultiplier));
	#endif
		derived().changeValueCompact<OP_MULT>(eKey, cvMultiplier);
	}
	template<>
	void changeValueUnsafe<OP_DIV>(E eKey, V vDivisor)
	{
		BOOST_STATIC_ASSERT(bARITHMETIC);
		derived().changeValueCompact<OP_DIV>(eKey, compactValue(vDivisor));
	}
	template<>
	void changeValueUnsafe<OP_TOGGLE>(E eKey, V vDummy)
	{
		BOOST_STATIC_ASSERT((is_same_type<V,bool>::value));
		if (is_same_type<CompactV,bool>::value)
			derived().changeValueCompact<OP_TOGGLE>(eKey, compactValue(vDummy));
		// changeValueCompact doesn't support Bitblock as the CompactV type
		else
		{
			V vOldVal = get(eKey);
			V vNewVal = !vOldVal;
			derived().set(eKey, vNewVal);
			derived().processValueChange(vOldVal, vNewVal);
		}
	}
	template<class T>
	void processValueChange(T tOld, T tNew)
	{
		/*	Derived classes can update any cached data here.
			T can be either V or CompactV. */
	}
	template<Operation eOP>
	void changeValueCompact(E eKey, CompactV cvOperand)
	{
		CompactV& val = derived().lookup<eOP>(eKey, cvOperand);
		CompactV cvOldVal = val;
		applyOp<eOP>(val, cvOperand);
		derived().processValueChange(cvOldVal, val);
	}
	template<Operation eOP>
	void applyOp(CompactV&, CompactV) { BOOST_STATIC_ASSERT(false); }
	template<>
	void applyOp<OP_ADD>(CompactV& cvValue, CompactV cvAddend)
	{
		// Cast b/c CompactV might be an enum type, or e.g. short getting promoted to int.
		cvValue = static_cast<CompactV>(cvValue + cvAddend);
	}
	template<>
	void applyOp<OP_MULT>(CompactV& cvValue, CompactV cvMultiplier)
	{
		cvValue = static_cast<CompactV>(cvValue * cvMultiplier);
	}
	template<>
	void applyOp<OP_DIV>(CompactV& cvValue, CompactV cvDivisor)
	{
		cvValue = static_cast<CompactV>(cvValue / cvDivisor);
	}
	template<>
	void applyOp<OP_TOGGLE>(CompactV& cvValue, CompactV cvDummy)
	{
		cvValue = !cvValue;
	}
	/*	Will applying eOP to the default value and the given operand
		result in the default value? To help derived classes avoid unnecessary
		memory allocation when implementing lookup. */
	template<Operation eOP>
	bool isNeutralToDefaultVal(CompactV)
	{
		return false;
	}
	template<>
	bool isNeutralToDefaultVal<OP_ASSIGN>(CompactV cvOperand)
	{
		return (cvOperand == cvDEFAULT);
	}
	template<>
	bool isNeutralToDefaultVal<OP_ADD>(CompactV cvOperand)
	{
		return (cvOperand == 0);
	}
	template<>
	bool isNeutralToDefaultVal<OP_MULT>(CompactV cvOperand)
	{
		return (cvDEFAULT == 0 || cvOperand == static_cast<CompactV>(1));
	}
	template<>
	bool isNeutralToDefaultVal<OP_DIV>(CompactV cvOperand)
	{
		return isNeutralToDefaultVal<OP_MULT>(cvOperand);
	}

	template<typename ValueType>
	bool _nextNonDefaultPair(int& iIter, std::pair<E,ValueType>& kPair) const
	{
		for (; iIter < getLength(); iIter++)
		{
			V val = derived().getUnsafe(static_cast<E>(iIter));
			if (val != vDEFAULT)
			{
				kPair.first = static_cast<E>(iIter);
				kPair.second = static_cast<ValueType>(val);
				iIter++;
				return true;
			}
		}
		return false;
	}
	E _nextNonDefaultKey(int& iIter) const
	{
		for (; iIter < getLength(); iIter++)
		{
			V val = getUnsafe(static_cast<E>(iIter));
			if (val != vDEFAULT)
				return static_cast<E>(iIter++);
		}
		return endKey();
	}

	// (Can't overload these two under the name "compact" b/c E and V can coincide)
	static CompactE compactKey(E eKey)
	{
		return compactEnum(eKey);
	}
	static CompactV compactValue(V vValue)
	{	// Specialize for bool
		return _compact<CompactV,V>(vValue);
	}
	template<class ToType, class FromType>
	static ToType _compact(FromType fValue)
	{
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		return safeCast<ToType>(fValue);
	#else
		return (ToType)fValue;
	#endif
	}
	template<>
	static BitBlock _compact<BitBlock,bool>(bool bValue)
	{	// Bit block of all ones or all zeros
		return (bValue ? integer_limits<BitBlock>::max : 0);
	}
	// (Can't overload these two b/c CompactE and CompactV can coincide)
	static E uncompactKey(CompactE ceKey)
	{
		return static_cast<E>(ceKey);
	}
	static V uncompactValue(CompactV cvVal)
	{	// The one-argument version can't work for bBIT_BLOCKS
		return _uncompactValue<V,CompactV>(cvVal);
	}
	template<class ToType, class FromType>
	static ToType _uncompactValue(FromType fValue)
	{
		return (ToType)fValue;
	}
	template<>
	static bool _uncompactValue<bool,BitBlock>(BitBlock uiBlock)
	{
		BOOST_STATIC_ASSERT(false);
		return false;
	}
	template<class ToType, class FromType>
	static ToType uncompactValue(FromType fValue, E eKey)
	{
		return uncompactValue(fValue);
	}
	template<>
	static bool uncompactValue<bool,BitBlock>(BitBlock block, E eKey)
	{
		return BitUtil::GetBit(block, eKey % BITSIZE(BitBlock));
	}
	template<class ToType, class FromType>
	static void assignVal(ToType& to, FromType fValue, E eKey)
	{
		to = compactValue(fValue);
	}
	template<>
	static void assignVal<BitBlock,bool>(BitBlock& block, bool bValue, E eKey)
	{
		BitUtil::SetBit(block, eKey % BITSIZE(BitBlock), bValue);
	}
	template<typename ToType, typename FromType>
	static ToType safeCast(FromType fVal)
	{
		return int_cast<ToType,FromType,true,false,/*allow ptr*/true>::safe(fVal);
	}
	/*	Derived classes should use these wrappers for writing values. To ensure
		that no compact values that encode pointers get stored in savegames.
		Will unfortunately have to turn all write functions into templates -
		to allow pointer-type values for classes whose write function is unused. */
	template<class T>
	static void writeVal(FDataStreamBase* pStream, T tValue)
	{
		BOOST_STATIC_ASSERT((!is_pointer_type<V /* not T! */>::value));
		pStream->Write(tValue);
	}
	template<class T>
	static void writeVal(FDataStreamBase* pStream, int iCount, T const atValues[])
	{
		BOOST_STATIC_ASSERT((!is_pointer_type<V>::value));
		pStream->Write(iCount, atValues);
	}
	// For derived classes with vector-like behavior
	template<int iEXTRA_CAPACITY, class T>
	void growArrayAt(short iPos, T*& oldArray, short iOldSize)
	{
		T* newArray = new T[iOldSize + iEXTRA_CAPACITY + 1];
		if (iOldSize + iEXTRA_CAPACITY > 0)
		{
			if (iPos > 0)
			{
				std::memcpy(newArray, oldArray,
						iPos * sizeof(oldArray[0]));
			}
			if (iEXTRA_CAPACITY > 0 || iPos < iOldSize)
			{
				std::memcpy(newArray + iPos + 1, oldArray + iPos,
						(iOldSize + iEXTRA_CAPACITY - iPos) * sizeof(oldArray[0]));
			}
		}
		delete[] oldArray;
		oldArray = newArray;
	}
};

#define DEFINE_ENUM_MAP_BASE_VALUE_CONSTANT(ValueType, vVAR_NAME, VALUE) \
	template<class Derived, typename E, class V, class CV, int iDEFAULT> \
	ValueType const EnumMapBase<Derived,E,V,CV,iDEFAULT>::vVAR_NAME = (VALUE)
/*	Since V can be a pointer type, these can only be initialized out-of-class.
	Only C-style cast works here b/c a reinterpret cast is needed when V is
	a pointer -- see enum_traits<T*,false> -- and is disallowed otherwise. */
DEFINE_ENUM_MAP_BASE_VALUE_CONSTANT(V, vDEFAULT, (V)iDEFAULT);
DEFINE_ENUM_MAP_BASE_VALUE_CONSTANT(V, defaultValue, vDEFAULT);
#undef DEFINE_ENUM_MAP_BASE_VALUE_CONSTANT
// A macro can't handle this one ...
template<class Derived, typename E, class V, class CV, int iDEFAULT>
typename EnumMapBase<Derived,E,V,CV,iDEFAULT>::CompactV const
EnumMapBase<Derived,E,V,CV,iDEFAULT>::cvDEFAULT =
	(EnumMapBase<Derived,E,V,CV,iDEFAULT>::bBIT_BLOCKS && vDEFAULT != 0 ?
	arithm_traits<CompactV>::max :
	(typename EnumMapBase<Derived,E,V,CV,iDEFAULT>::CompactV)vDEFAULT);

/*	ListEnumMap: Keeps a list of key-value pairs whose values differ from the
	default value. This allows for fast iteration over non-default data, wastes
	no memory for storing default data, but makes random access somewhat slow.

	(A ListAndArrayEnumMap that stores data redundantly in order to allow both
	fast random access and fast iteration over non-default values had been
	implemented in CvInfo_EnumMap.h, but I haven't bothered to port it when
	I merged the WtP EnumMap with my own ArrayEnumMap and ListEnumMap classes.
	If such a class is needed, the AdvCiv code from July 2021 should be consulted.) */

#define ListEnumMapBase \
	EnumMapBase<ListEnumMap<E,V,CV,iDEFAULT,bMONOTONE,bEND_MARKER>, E, V, \
	/* void ptr means use the default. List-based maps have their own default */ \
	/* b/c they shouldn't use compact bit blocks for V=bool. */ \
	typename \
	choose_type<is_same_type<CV,void*>::value, typename enum_traits<V>::compact_t, CV> \
	::type, iDEFAULT>
template<typename E, class V,
	class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none,
	/*	Promises not to change a key from a value other than iDEFAULT to iDEFAULT
		except when the whole map is (explicitly) reset.
		The promise will not be enforced nor (reliably) asserted. */
	bool bMONOTONE = false,
	/*	Storing a dummy key and value at the end of the list avoids checking for
		the end of the list when searching for a key (and its value).
		Tbd.: Is that worth the extra memory? Perhaps only in mappings read
		from XML (offline vs. online performance)? */
	bool bEND_MARKER = false>
class ListEnumMap : public ListEnumMapBase
{
	friend class ListEnumMapBase; // Needed for CRT pattern
	/*	Since these lists are assumed to be short, the potential for optimizing
		this class for bool values is pretty small. For XML data,
		OfflineListEnumSet should be used instead. */
	BOOST_STATIC_ASSERT(!bBIT_BLOCKS);
protected:
	CompactE* m_aKeys;
	CompactV* m_aValues;
	short m_iSize;
	/*	Keeping this counter probably isn't gaining us much (nothing if bMONOTONE),
		but the memory would otherwise be used for padding. Alternatively, it could
		be used for a capacity variable (like std::vector) -- however, given that the
		arrays are sorted, a capacity mechanism would not be trivial to implement. */
	short m_iNonDefault;

public:
	ListEnumMap() : m_aKeys(NULL), m_aValues(NULL)
	{
		/*	Better use an array enum map if the enum is very short.
			Can't check getLength here at runtime b/c XML may not yet be loaded.
			Check that in the write function instead. */
		BOOST_STATIC_ASSERT((enum_traits<E>::len > 4));
		reset();
	}
	~ListEnumMap()
	{
		uninit();
	}
	ASSIGN(ListEnumMap) // advc.xmldefault
	{
		if (bUNINITIALIZED)
		{
			m_aKeys = NULL;
			m_aValues = NULL;
		}
		if (!kOther.isAnyNonDefault())
		{
			reset();
			return;
		}
		if (bUNINITIALIZED || m_iSize != kOther.m_iSize)
		{
			reset();
			m_iSize = kOther.m_iSize;
			m_iNonDefault = kOther.m_iNonDefault;
			allocate();
		}
		std::memcpy(m_aKeys, kOther.m_aKeys, m_iSize * sizeof(kOther.m_aKeys[0]));
		std::memcpy(m_aValues, kOther.m_aValues, m_iSize * sizeof(kOther.m_aValues[0]));
	}
	void reset()
	{
		uninit();
		if (bEND_MARKER)
			allocate();
	}
	void setAll(V vValue)
	{
		/*	Should probably use an array enum map if this function is used.
			But maybe it gets used only very rarely, so I'm not going to assert
			that it isn't used. */
		if (vValue == vDEFAULT)
		{
			reset();
			return;
		}
		uninit();
		m_iSize = compactKey(getLength());
		m_iNonDefault = m_iSize;
		allocate();
		CompactV cvValue = compactValue(vValue);
		fill<V,CompactV>(cvValue);
		FOR_EACH_KEY(eKey)
		{
			m_aKeys[eKey] = compactValue(eKey);
			m_aValues[eKey] = cvValue;
		}
	}
	int numNonDefault() const
	{
		return m_iNonDefault;
	}
	template<class DataStream>
	void write(DataStream pStream) const
	{
		// See comment in ctor
		FAssertMsg(getLength() > 4, "Should use an array enum map instead");
		// Serialization is a good opportunity to clean out default values
		pStream->Write(m_iNonDefault);
		if (m_iNonDefault <= 0)
			return;
	#ifdef FASSERT_ENABLE
		int iWritten = 0;
	#endif
		for (short i = 0; i < m_iSize; i++)
		{
			if (m_aValues[i] != cvDEFAULT)
			{
			#ifdef FASSERT_ENABLE
				iWritten++;
			#endif
				pStream->Write(m_aKeys[i]);
			}
			else if (bMONOTONE)
				FErrorMsg("bMONOTONE ListEnumMap storing non-default value");
		}
	#ifdef FASSERT_ENABLE
		FAssert(iWritten == m_iNonDefault);
	#endif
		for (short i = 0; i < m_iSize; i++)
		{
			if (m_aValues[i] != cvDEFAULT)
				writeVal(pStream, m_aValues[i]);
		}
	}
	void read(FDataStreamBase* pStream)
	{
		uninit(); // Drop end marker if present
		pStream->Read(&m_iSize);
		m_iNonDefault = m_iSize;
		allocate();
		for (short i = 0; i < m_iSize; i++)
		{
			pStream->Read(&m_aKeys[i]);
			FAssertInfoEnum(uncompactKey(m_aKeys[i]));
		}
		for (short i = 0; i < m_iSize; i++)
		{
			pStream->Read(&m_aValues[i]);
			// Shouldn't have written default values to the stream
			FAssert(m_aValues[i] != cvDEFAULT);
		}
	}
	/*	For compatibility with an earlier implementation of this type of enum map
		(SizeType=short, F=short or char) and with BtS vectors of pairs
		(SizeType=size_t, F=int). */
	template<typename SizeType, typename F, typename S>
	void readPair(FDataStreamBase* pStream)
	{
		uninit();
		SizeType sz;
		pStream->Read(&sz);
		m_iSize = safeCast<short>(sz);
		if (m_iSize <= 0)
		{
			allocate();
			return;
		}
		/*	Don't allocate yet b/c the data may contain default values
			that we don't want to store */
		std::vector<CompactE> aeKeys;
		std::vector<CompactV> aeValues;
		aeKeys.reserve(m_iSize);
		aeValues.reserve(m_iSize);
		for (short i = 0; i < m_iSize; i++)
		{
			F fFirst;
			pStream->Read(&fFirst);
			S sSecond;
			pStream->Read(&sSecond);
			CompactV cvValue = static_cast<CompactV>(sSecond);
			if (cvValue != cvDEFAULT)
			{	
				CompactE ceKey = static_cast<CompactE>(fFirst);
				FAssertInfoEnum(uncompactKey(ceKey));
				aeKeys.push_back(ceKey);
				aeValues.push_back(cvValue);
				m_iNonDefault++;
			}
		}
		m_iSize = (short)aeKeys.size();
		allocate();
		for (short i = 0; i < m_iSize; i++)
		{
			m_aKeys[i] = aeKeys[i];
			m_aValues[i] = aeValues[i];
		}
	}

protected:
	void uninit()
	{
		SAFE_DELETE_ARRAY(m_aKeys);
		SAFE_DELETE_ARRAY(m_aValues);
		m_iNonDefault = m_iSize = 0;
	}
	void incrementSize(short iFreePos)
	{
		growArrayAt<bEND_MARKER ? 1 : 0>(
				iFreePos, m_aKeys, m_iSize);
		growArrayAt<bEND_MARKER ? 1 : 0>(
				iFreePos, m_aValues, m_iSize);
		m_iSize++;
	}
	short capacity() const
	{
		return m_iSize + (bEND_MARKER ? 1 : 0);
	}
	void allocate()
	{
		FAssertBounds(0, getLength() + 1, m_iSize);
		short iCapacity = capacity();
		if (iCapacity <= 0)
			return;
		FAssert(m_aKeys == NULL && m_aValues == NULL);
		m_aKeys = new CompactE[iCapacity];
		m_aValues = new CompactV[iCapacity];
		if (bEND_MARKER)
		{
			m_aKeys[m_iSize] = ceEndKey();
			m_aValues[m_iSize] = cvDEFAULT;
		}
	}

	CompactV getCompact(CompactE ceKey) const
	{
		return _getCompact<!bEND_MARKER>(ceKey);
	}
	template<bool bCHECK_SIZE>
	CompactV _getCompact(CompactE) const;
	template<>
	CompactV _getCompact<true>(CompactE ceKey) const
	{
		/*	Typically, we'll only have a couple of pairs, or none.
			Not worth doing divisions and extra comparisons for interpolation. */
		for (short i = 0; i < m_iSize; i++)
		{
			CompactE const ceLoopKey = m_aKeys[i];
			if (ceLoopKey == ceKey)
				return m_aValues[i];
			if (ceLoopKey > ceKey)
				break;
		}
		return cvDEFAULT;
	}
	template<>
	CompactV _getCompact<false>(CompactE ceKey) const
	{
		CompactE ceLoopKey;
		for (int i = 0; (ceLoopKey = m_aKeys[i]) <= ceKey; i++)
		{
			if (ceLoopKey == ceKey)
				return m_aValues[i];
		}
		return cvDEFAULT;
	}

	template<Operation eOP>
	CompactV& lookupCompact(CompactE ceKey, CompactV cvOperand)
	{
		short iPos = 0;
		while (bEND_MARKER || iPos < m_iSize)
		{
			CompactE const ceLoopKey = m_aKeys[iPos];
			if (ceLoopKey == ceKey)
				return m_aValues[iPos];
			if (ceLoopKey > ceKey)
				break;
			iPos++;
		}
		/*	At this point, we know whether m_iNonDefault needs to be incremented.
			Will have to let processValueChange handle it though - resulting in two
			unnecessary comparisons. :( */
		if (isNeutralToDefaultVal<eOP>(cvOperand))
			return cvDummy();
		incrementSize(iPos);
		m_aKeys[iPos] = ceKey;
		m_aValues[iPos] = cvDEFAULT;
		return m_aValues[iPos];
	}
	/*	The T=V version exists only for the sake of bit arrays (bBIT_BLOCKS)
		-- which this class doesn't use. We always use CompactV=bool when V=bool. */
	template<class T>
	void processValueChange(T, T) { BOOST_STATIC_ASSERT(false); }
	template<>
	void processValueChange<CompactV>(CompactV cvOld, CompactV cvNew)
	{
		if (cvNew != cvDEFAULT)
			m_iNonDefault++;
		if (cvOld != cvDEFAULT)
		{
			if ((--m_iNonDefault) == 0)
			{
				if (bMONOTONE)
					FErrorMsg("bMONOTONE promise broken");
				/*	Otherwise not worth the risk of having to reallocate later.
					Well, a test suggests that this check helps marginally
					at best and that checking >=4 would hurt more than help. */
				if (m_iSize >= 2)
					reset();
			}
			else if (bMONOTONE)
			{
			#ifdef ENUM_MAP_EXTRA_ASSERTS
				FAssertMsg(cvNew != cvDEFAULT || m_iSize == 0, "bMONOTONE promise broken");
			#endif
			}
		}
	}

	template<typename ValueType>
	bool _nextNonDefaultPair(int& iIter, std::pair<E,ValueType>& kPair) const
	{
		if (bEND_MARKER) // (Might get inlined in this case)
		{
		#ifdef ENUM_MAP_EXTRA_ASSERTS
			FAssertBounds(0, m_iSize + 1, iIter);
		#endif
		}
		else
		{
			if (iIter >= m_iSize)
				return false;
		}
		kPair.first = uncompactKey(m_aKeys[iIter]);
		CompactV const val = m_aValues[iIter];
		kPair.second = static_cast<ValueType>(val);
		iIter++;
		bool bFound = (bEND_MARKER ? (kPair.first != endKey()) : true);
		if (!bMONOTONE) // Skip default values if they can exist
		{
			if (bFound && val == cvDEFAULT)
				return _nextNonDefaultPair(iIter, kPair); // tail recursion
		}
		return bFound;
	}
	E _nextNonDefaultKey(int& iIter) const
	{
		if (bEND_MARKER)
		{
		#ifdef ENUM_MAP_EXTRA_ASSERTS
			FAssertBounds(0, m_iSize + 1, iIter);
		#endif
		}
		else
		{
			if (iIter >= m_iSize)
				return endKey();
		}
		CompactE eKey = m_aKeys[iIter++];
		if (bMONOTONE || getCompact(eKey) != cvDEFAULT)
			return uncompactKey(eKey);
		return _nextNonDefaultKey(iIter);
	}
};
#undef ListEnumMapBase

template<typename E, class V, class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none, bool bEND_MARKER = false>
class NonDefaultEnumMap : public ListEnumMap<E, V, CV, iDEFAULT,
	/*bMONOTONE=*/true, bEND_MARKER>
{};

#define OfflineListEnumSetBase \
	EnumMapBase<OfflineListEnumSet<E>, E, bool, bool, false>
/*	A list enum map with boolean value type doesn't need to store values at all;
	can be represented as a set of keys. However, I haven't implemented an erase
	operation (set call with bValue=false), so this is an offline data structure,
	mainly for data loaded from XML. For data that changes dynamically, a
	normal ListEnumMap (or an ArrayEnumMap) might be more efficient anyway
	(... than a set that needs to reallocate memory whenever a value gets reset). */
template<typename E>
class OfflineListEnumSet : public OfflineListEnumSetBase
{
	friend class OfflineListEnumSetBase;
protected:
	CompactE* m_aKeys;
	short m_iSize;

public:
	OfflineListEnumSet() : m_aKeys(NULL)
	{
		reset();
	}
	~OfflineListEnumSet()
	{
		uninit();
	}
	ASSIGN(OfflineListEnumSet) // advc.xmldefault
	{
		if (bUNINITIALIZED)
			m_aKeys = NULL;
		if (kOther.m_iSize <= 0)
		{
			reset();
			return;
		}
		if (bUNINITIALIZED || m_iSize != kOther.m_iSize)
		{
			reset();
			m_iSize = kOther.m_iSize;
			allocate();
		}
		std::memcpy(m_aKeys, kOther.m_aKeys, m_iSize * sizeof(kOther.m_aKeys[0]));
	}

	void set(E eKey, bool bValue = !vDEFAULT)
	{
		setUnsafe(eKey, bValue);
	}
private: // Hide public base function
	void toggle(E eKey) {}
public:

	void reset()
	{
		uninit();
		allocate();
	}
	int numNonDefault() const
	{
		return m_iSize;
	}

	template<class DataStream>
	void write(DataStream* pStream) const
	{
		pStream->Write(m_iSize);
		if (m_iSize > 0)
			writeVal(pStream, m_iSize, m_aKeys);
	}
	void read(FDataStreamBase* pStream)
	{
		uninit();
		pStream->Read(&m_iSize);
		allocate();
		for (short i = 0; i < m_iSize; i++)
		{
			pStream->Read(&m_aKeys[i]);
			FAssertInfoEnum(uncompactKey(m_aKeys[i]));
		}
	}

protected:
	void uninit()
	{
		SAFE_DELETE_ARRAY(m_aKeys);
		m_iSize = 0;
	}
	void incrementSize(short iPos)
	{
		growArrayAt<1>(iPos, m_aKeys, m_iSize);
		m_iSize++;
	}
	void allocate()
	{
		FAssertBounds(0, getLength() + 1, m_iSize);
		FAssert(m_aKeys == NULL);
		m_aKeys = new CompactE[m_iSize + 1];
		m_aKeys[m_iSize] = ceEndKey();
	}

	/*	Nothing unsafe about this implementation (there are no array bounds to check),
		but our base class requires derived classes to implement setUnsafe. */
	void setUnsafe(E eKey, bool bValue)
	{
	#ifndef ENUM_MAP_EXTRA_ASSERTS
		if (bValue == vDEFAULT)
			return;
	#endif
		CompactE const ceKey = compactKey(eKey);
		// Check if key already exists
		short iPos = 0;
		for (CompactE ceLoopKey; (ceLoopKey = m_aKeys[iPos]) <= ceKey; iPos++)
		{
			if (ceLoopKey == ceKey)
			{
			#ifdef ENUM_MAP_EXTRA_ASSERTS
				FAssertMsg(bValue != vDEFAULT, "Removal from enum set not supported");
			#endif
				return;
			}
		}
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		if (bValue == vDEFAULT)
			return;
	#endif
		incrementSize(iPos);
		m_aKeys[iPos] = ceKey;
	}
	bool getCompact(CompactE ceKey) const
	{
		CompactE ceLoopKey;
		for (int i = 0; (ceLoopKey = m_aKeys[i]) <= ceKey; i++)
		{
			if (ceLoopKey == ceKey)
				return !vDEFAULT;
		}
		return vDEFAULT;
	}
	template<Operation eOP>
	bool& lookupCompact(CompactE ceKey, CompactV cvOperand)
	{	/*	Can't be reached, but compiler will warn about infinite recursion
			if no lookup function is defined. */
		FErrorMsg("Can only be modified through insert function");
		return cvDummy();
	}

	template<typename ValueType>
	bool _nextNonDefaultPair(int& iIter, std::pair<E,ValueType>& kPair) const
	{
		BOOST_STATIC_ASSERT(false); // Should use nextNonDefaultKey instead
		return false;
	}
	E _nextNonDefaultKey(int& iIter) const
	{
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssertBounds(0, m_iSize + 1, iIter);
	#endif
		return uncompactKey(m_aKeys[iIter++]);
	}
};
#undef OfflineListEnumSetBase

/*	ArrayEnumMap: Stores a value for every possible key except when all keys
	have the default value, in which case lazy allocation may or may not be used.
	Allows for fast random access (especially when allocating eagerly), but
	memory usage is relatively high when the key enum is large and most values
	are non-default and can't be represented compactly. */

#define ArrayEnumMapBase \
	EnumMapBase< \
		ArrayEnumMap<E,V,CV,iDEFAULT,bEAGER_ALLOC,iMAX_STATIC_BYTES>, \
		E, V, CV, iDEFAULT>
template<typename E, class V,
	class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none,
	/*	True forces the class to allocate all memory in the constructor.
		False leaves it up to the class whether to allocate eagerly or lazily. */
	bool bEAGER_ALLOC = false,
	/*	By default, use static memory if that would make the size of ArrayEnumMap
		at most twice as big as it would be using dynamic memory. Use of
		static memory also implies eager allocation, obviously.
		(The storage duration is going to be the same as that of our instance,
		so it could, ultimately, be dynamic memory, i.e. "static" might not be
		the best term to use here. WtP used the term "inline memory" - which I
		don't think is widely used or understood.) */
	int iMAX_STATIC_BYTES = 8>
class ArrayEnumMap : public ArrayEnumMapBase
{
	friend class ArrayEnumMapBase;

	static int const iBITS_PER_BYTE = 8; // just for readability
	// 64 bit to avoid overflow below (when enum_traits<E>::len is MAX_INT)
	static long long const lCOMPACT_VAL_BIT_SIZE = (bBIT_BLOCKS ? 1 :
			BITSIZE(CompactV));
	static bool const bSTATIC_MEMORY =
			(enum_traits<E>::is_static &&
			enum_traits<E>::len * lCOMPACT_VAL_BIT_SIZE <=
			iMAX_STATIC_BYTES * iBITS_PER_BYTE &&
			enum_traits<E>::len > 0);
	static int const iSTATIC_BYTES = (!bSTATIC_MEMORY ?
			sizeof(CompactV*) : // So that the unused array doesn't increase our size
			(enum_traits<E>::len * lCOMPACT_VAL_BIT_SIZE
			+ iBITS_PER_BYTE - 1) / iBITS_PER_BYTE); // round up
	static bool const bLAZY_ALLOC = (!bEAGER_ALLOC && !bSTATIC_MEMORY);
public:
	static bool const isLazyAllocation = bLAZY_ALLOC;
	static bool const isStaticMemory = bSTATIC_MEMORY;
protected:
	union
	{
		CompactV* m_aValues;
		byte m_aBytes[iSTATIC_BYTES];
	};
	CompactV* values()
	{
		return (bSTATIC_MEMORY ? reinterpret_cast<CompactV*>(m_aBytes) : m_aValues);
	}
	CompactV const* values() const
	{
		return (bSTATIC_MEMORY ? reinterpret_cast<CompactV const*>(m_aBytes) : m_aValues);
	}
	static int const iSTATIC_ARRAY_SIZE = (!bBIT_BLOCKS ? enum_traits<E>::len :
			(enum_traits<E>::len + BITSIZE(BitBlock) - 1) / BITSIZE(BitBlock)); // round up
	static int arraySize()
	{
		if (bSTATIC_MEMORY)
			return iSTATIC_ARRAY_SIZE;
		int iLen = getLength();
		if (bBIT_BLOCKS)
		{
			iLen += BITSIZE(BitBlock) - 1;
			iLen /= BITSIZE(BitBlock);
		}
		return iLen;
	}
	/*	Allow derived classes to handle initial values.
		(Cleaner solution might be to make this class CRT-poolymorphic.) */
	explicit ArrayEnumMap(bool) : m_aValues(NULL) {}

public:
	ArrayEnumMap() : m_aValues(NULL)
	{
		if (!bLAZY_ALLOC)
			init();
	}
	~ArrayEnumMap()
	{
		if (!bSTATIC_MEMORY)
			SAFE_DELETE_ARRAY(m_aValues);
	}
	ASSIGN(ArrayEnumMap) // advc.xmldefault
	{
		if (bUNINITIALIZED)
		{
			// Don't fill yet, may want to memcpy.
			m_aValues = NULL;
		}
		if (!kOther.isAllocated())
		{
			if (isAllocated())
				reset();
			// Not going to memcpy; complete initialization.
			else if (!bLAZY_ALLOC && bUNINITIALIZED)
				init();
			return;
		}
		// kOther is allocated, so ...
		if ((!bLAZY_ALLOC && bUNINITIALIZED) || // Can't rely on isAllocated
			!isAllocated())
		{
			allocate();
		}
		_memcpy<bSTATIC_MEMORY>(values(), kOther.values());
	}

	V get(E eKey) const
	{
		FAssertEnumBounds(eKey);
		return ArrayEnumMapBase::get(eKey);
	}
	void reset()
	{
		if (!bLAZY_ALLOC)
			fill();
		else SAFE_DELETE_ARRAY(m_aValues);
	}
	void setAll(V vValue)
	{
		if (isAllocated())
			fill(vValue);
		else if (vValue != vDEFAULT)
			init(vValue);
	}
	int numNonDefault() const
	{
		if (isAllocated())
			return ArrayEnumMapBase::numNonDefault();
		return 0;
	}
	bool isAnyNonDefault() const
	{
		if (isAllocated())
		{
			if (bBIT_BLOCKS)
			{
				for (int i = 0; i < arraySize(); i++)
				{
					if (values()[i] != cvDEFAULT)
						return true;
				}
			}
			else
			{
				FOR_EACH_KEY(eKey)
				{
					if (getUnsafe(eKey) != vDEFAULT)
						return true;
				}
			}
		}
		return false;
	}
	V& operator[](E eKey)
	{	/*	Can only implement this when V and CompactV coincide
			(unless we want to return CompactV - but I want that type to be used
			only internally). */
		return subscript<is_same_type<V,CompactV>::value>(eKey);
	}
	V operator[](E eKey) const
	{	// (I don't think we can unhide this through a using declaration)
		return ArrayEnumMapBase::operator[](eKey);
	}

	template<class DataStream>
	void write(DataStream pStream) const
	{
		// Even if we allocate eagerly, we shouldn't spam savegames with default values.
		if (isAnyNonDefault())
		{
			pStream->Write(true);
			writeVal(pStream, arraySize(), values());
		}
		else
		{
			/*	The WtP EnumMap did this in isAnyNonDefault, but I like it
				better here; more predictable/ less unanticipated this way, and
				most isAnyNonDefault calls occur during serialization. Indeed,
				for calls in other contexts, it seems difficult to predict
				whether memory will soon have to be reallocated. I think
				the const_cast isn't entirely safe in this implementation b/c
				a const instance could be initialized through a copy-ctor (whereas,
				in WtP, a const instance would always be empty). That said,
				normally, only data members are serialized, and those can't use
				the copy-ctor. Also, const instances - of any classes - aren't used
				anywhere in our codebase, so this problem is really academic. */
			if (bLAZY_ALLOC && isAllocated())
				const_cast<ArrayEnumMap*>(this)->reset();
			pStream->Write(false);
		}
	}
	void read(FDataStreamBase* pStream, int iSubtrahend = 0)
	{
		FAssert(!bBIT_BLOCKS || iSubtrahend == 0);
		bool bAnyNonDefault;
		pStream->Read(&bAnyNonDefault);
		if (bAnyNonDefault)
		{
			if (!isAllocated())
				allocate();
			pStream->Read(arraySize() - iSubtrahend, values());
		}
	}

protected:
	int keyToIndex(CompactE ceKey) const
	{
		if (bBIT_BLOCKS)
		{
			/*	WtP comment: Hardcode only using first block in arrays
				hardcoded to only use one block. With a bit of luck,
				the compiler can optimize the array code away completely. */
			if (bSTATIC_MEMORY && iSTATIC_ARRAY_SIZE == 1)
				return 0;
			return ceKey / BITSIZE(BitBlock);
		}
		return ceKey;
	}
	template<Operation eOP>
	CompactV& lookup(E eKey, CompactV cvOperand)
	{
		FAssertEnumBounds(eKey);
		return ArrayEnumMapBase::lookup<eOP>(eKey, cvOperand);
	}
	CompactV getCompact(CompactE ceKey) const
	{
		if (isAllocated())
			return values()[keyToIndex(ceKey)];
		return cvDEFAULT;
	}
	template<Operation eOP>
	CompactV& lookupCompact(CompactE ceKey, CompactV cvOperand)
	{
		if (!isAllocated())
		{
			if (isNeutralToDefaultVal<eOP>(cvOperand))
				return cvDummy();
			init();
		}
		return values()[keyToIndex(ceKey)];
	}
	bool isAllocated() const
	{
		return (!bLAZY_ALLOC || values() != NULL);
	}
	void init(V vValue = vDEFAULT)
	{
		allocate();
		fill(vValue);
	}
	void allocate()
	{
		if (bSTATIC_MEMORY)
			return;
		FAssert(values() == NULL);
		FAssertMsg(arraySize() > 0, "Enum length not yet loaded from XML?");
		m_aValues = new CompactV[arraySize()];
	}
	void fill(V vValue = vDEFAULT)
	{
		_fill<bSTATIC_MEMORY>(compactValue(vValue));
	}
	template<bool bSTATIC>
	void _fill(CompactV);
	template<>
	void _fill<false>(CompactV cvValue)
	{
		std::fill_n(values(), arraySize(), cvValue);
	}
	template<>
	void _fill<true>(CompactV cvValue)
	{	// This loop should get optimized away
		for (int i = 0; i < iSTATIC_ARRAY_SIZE; i++)
			values()[i] = cvValue;
	}
	template<bool bSTATIC>
	static void _memcpy(CompactV*, CompactV const*);
	template<>
	static void _memcpy<false>(CompactV* pDest, CompactV const* pSource)
	{
		std::memcpy(pDest, pSource, arraySize() * sizeof(CompactV));
	}
	template<>
	static void _memcpy<true>(CompactV* pDest, CompactV const* pSource)
	{	// This loop should get optimized away
		for (int i = 0; i < iSTATIC_ARRAY_SIZE; i++)
			pDest[i] = pSource[i];
	}
	template<bool bVALID>
	V& subscript(E);
	template<>
	V& subscript<false>(E)
	{	// No V instances exist in this map, only CompactV.
		BOOST_STATIC_ASSERT(false);
		return vDummy();
	}
	template<>
	V& subscript<true>(E eKey) // When V and CompactV coincide
	{
		return derived().lookupUnsafe<OP_UNKNOWN>(eKey, 0);
	}
};
#undef ArrayEnumMapBase

/*	AdvCiv 1.08 fixes a bug in ArrayEnumMap. Convenient to wrap code for
	maintaining save-compatibility in a derived class. */
template<typename E, class V,
	class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none>
class LegacyArrayEnumMap : public ArrayEnumMap<E,V,CV,iDEFAULT,false,8>
{
private: LegacyArrayEnumMap() {} // Not going to instantiate this
public:
	template<class OtherEnumMap>
	static void convert(OtherEnumMap& kOther, FDataStreamBase* pStream, int iSubtrahend = 0)
	{
		BOOST_STATIC_ASSERT(bBIT_BLOCKS && !isStaticMemory);
		bool bAnyNonDefault;
		pStream->Read(&bAnyNonDefault);
		if (!bAnyNonDefault)
			return;
		int const iLen = getLength() - iSubtrahend;
		/*	Allocate one 4-byte block per value.
			(That's the bug that got fixed in AdvCiv 1.08.) */
		CompactV* aValues = new CompactV[iLen];
		pStream->Read(iLen, aValues);
		for (E eKey = enum_traits<E>::first; eKey < std::min<int>(iLen, getLength()); eKey++)
		{
			bool bVal = BitUtil::GetBit(
					aValues[eKey / BITSIZE(BitBlock)],
					eKey % BITSIZE(BitBlock));
			kOther.set(eKey, bVal);
		}
		delete[] aValues;
	}
};

// For convenience - as the bEAGER_ALLOC param is pretty far down the list.
template<typename E, class V,
	class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none,
	int iMAX_STATIC_BYTES = 8>
class EagerEnumMap : public ArrayEnumMap<E,V,CV,iDEFAULT,true,iMAX_STATIC_BYTES>
{};

#define IntegerEncodableMapBase \
	ArrayEnumMap<E, V, CV, 0, true, sizeof(EncodeT)>
/*	Enum map with a key sequence known (at compile time) to be short enough
	to fit -- when represented as a sequence of CompactV values --
	into a single value of the unsigned integer type EncodeT. */
template<typename E, typename V, typename CV, typename EncodeT>
class IntegerEncodableMap : public IntegerEncodableMapBase
{
	BOOST_STATIC_ASSERT(integer_limits<EncodeT>::is_integer);
	BOOST_STATIC_ASSERT(!integer_limits<EncodeT>::is_signed);

public:
	typedef EncodeT enc_t;
	/*	Expose the compact type b/c that's what the subscript operator
		will have to return. Want that operator so that encodable maps are
		interchangeable with yield and commerce arrays in BtS code. */
	typedef CompactV compact_t;

	IntegerEncodableMap() {}
	explicit IntegerEncodableMap(EncodeT ui)
	:	IntegerEncodableMapBase(false) // don't initialize
	{
		BOOST_STATIC_ASSERT(isStaticMemory);
		FAssert(sizeof(*this) == sizeof(ui));
		reinterpret_cast<EncodeT*>(values())[0] = ui;
	}

	EncodeT encode() const
	{
		return reinterpret_cast<EncodeT const*>(values())[0];
	}

	compact_t& operator[](E eKey)
	{
		return lookupUnsafe<OP_UNKNOWN>(eKey, 0);
	}
	V operator[](E eKey) const
	{	// (I don't think we can unhide this through a using declaration)
		return IntegerEncodableMapBase::operator[](eKey);
	}
};

#define YieldChangeMapBase \
	IntegerEncodableMap<YieldTypes, int, char, uint>
class YieldChangeMap : public YieldChangeMapBase
{
public:
	YieldChangeMap() {}
	YieldChangeMap(uint ui) : YieldChangeMapBase(ui) {}
};
#undef YieldChangeMapBase

#define CommerceChangeMapBase \
	IntegerEncodableMap<CommerceTypes, int, char, uint>
class CommerceChangeMap : public CommerceChangeMapBase
{
public:
	CommerceChangeMap() {}
	CommerceChangeMap(uint ui) : CommerceChangeMapBase(ui) {}
};
#undef CommerceChangeMapBase

#define YieldPercentMapBase \
	IntegerEncodableMap<YieldTypes, int, short, unsigned __int64>
class YieldPercentMap : public YieldPercentMapBase
{
public:
	YieldPercentMap() {}
	YieldPercentMap(unsigned __int64 ui) : YieldPercentMapBase(ui) {}
};
#undef YieldPercentMapBase
/*	YieldChangeMap is too small for yields summed up over multiple plots,
	but YieldPercentMap is a misleading name in that case. (It's still an
	absolute yield rate, not a percent modifier.) */
typedef YieldPercentMap YieldTotalMap;

#define CommercePercentMapBase \
	IntegerEncodableMap<CommerceTypes, int, short, unsigned __int64>
class CommercePercentMap : public CommercePercentMapBase
{
public:
	CommercePercentMap() {}
	CommercePercentMap(unsigned __int64 ui) : CommercePercentMapBase(ui) {}
};
#undef CommercePercentMapBase
typedef CommercePercentMap CommerceTotalMap;

/*	Enum map whose public interface works interchangeably with two different
	enum types, one (E) being a subsequence of the other (SuperE). The enum map
	can only store keys of type E; the SuperE functions are only provided for
	the convenience of the user.
	Can't easily implement this at EnumMapBase because the overloaded
	public functions will clash when SuperE is set to E by default.
	Hence in a separate class derived from the SubSeqEnumMapBase template param. */
template<class SubSeqEnumMapBase, typename SuperE>
class SubSeqEnumMap : public SubSeqEnumMapBase
{
	typedef typename SubSeqEnumMapBase::EnumType E;
	typedef typename SubSeqEnumMapBase::ValueType V;

	static E subKey(SuperE eKey)
	{
		E eResult = static_cast<E>(eKey);
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		// (Redundant when Base=ArrayEnumMap; see ArrayEnumMap::get.)
		FAssertEnumBounds(eResult);
	#endif
		return eResult;
	}
public:
	// Unhide ...
	using SubSeqEnumMapBase::get;
	using SubSeqEnumMapBase::set;
	using SubSeqEnumMapBase::resetVal;
	using SubSeqEnumMapBase::add;
	using SubSeqEnumMapBase::multiply;
	using SubSeqEnumMapBase::divide;
	using SubSeqEnumMapBase::toggle;
	V get(SuperE eKey) const
	{
		return get(subKey(eKey));
	}
	void set(SuperE eKey, V vValue)
	{
		set(subKey(eKey), vValue);
	}
	void resetVal(SuperE eKey)
	{
		resetVal(subKey(eKey));
	}
	void add(SuperE eKey, V vAddend)
	{
		add(subKey(eKey), vAddend);
	}
	void multiply(SuperE eKey, V vMultiplier)
	{
		multiply(subKey(eKey), vMultiplier);
	}
	void divide(SuperE eKey, V vDivisor)
	{
		divide(subKey(eKey), vDivisor);
	}
	void toggle(SuperE eKey)
	{
		toggle(subKey(eKey));
	}
};

template<class V, class CV = void*, int iDEFAULT = (int)enum_traits<V>::none>
class CivPlayerMap : public SubSeqEnumMap<ArrayEnumMap<CivPlayerTypes,V,CV,iDEFAULT>, PlayerTypes>
{};

template<class V, class CV = void*, int iDEFAULT = (int)enum_traits<V>::none>
class CivTeamMap : public SubSeqEnumMap<ArrayEnumMap<CivTeamTypes,V,CV,iDEFAULT>, TeamTypes>
{};

typedef ArrayEnumMap<CivicOptionTypes,CivicTypes> CivicMap; // Needed rather frequently
// Replacing a vector of pairs that had been defined in CvCityAI.h
typedef ListEnumMap<UnitAITypes,int> UnitAIWeightMap;

#undef FOR_EACH_KEY

#define FOR_EACH_OUTER_KEY(eOuterKey) \
	for (EOuter eOuterKey = enum_traits<EOuter>::first; \
		eOuterKey < getLength(); ++eOuterKey)

/*	EnumMap2D: Maps keys of an outer enum type to pointers to enum maps that,
	in turn, map keys of an inner enum type to an inner value type. The
	outer values - i.e. the (pointers to) the inner enum maps - are owned by
	the EnumMap2D; users don't need to handle the outer values at all. */

/*	Will forward to m_outer (composition) because that's potentially
	more efficient than making EnumMap2D identical to the outer map. Still,
	deriving EnumMap2D from EnumMapBase gains us some (static) conveniences. */
#define EnumMap2DBase \
	EnumMapBase<EnumMap2D<OuterEnumMap,InnerEnumMap>, \
	typename OuterEnumMap::EnumType, \
	typename OuterEnumMap::ValueType, \
	int /* (Don't want to make EnumMapBase::CompactV public) */, 0>
template<class OuterEnumMap, class InnerEnumMap>
class EnumMap2D : public EnumMap2DBase
{
	friend class EnumMap2DBase;
	/*	Caveat: Compiler error messages may at times omit the "*" after
		pointer types; this appears to be only a problem with the error output. */
	BOOST_STATIC_ASSERT((is_same_type<
			InnerEnumMap*, typename OuterEnumMap::ValueType>
			::value));
	BOOST_STATIC_ASSERT((!isArithmeticValues && !OuterEnumMap::isArithmeticValues));
	typedef typename OuterEnumMap::EnumType  EOuter;
	typedef typename InnerEnumMap::EnumType  EInner;
	typedef typename InnerEnumMap::ValueType VInner;
protected:
    OuterEnumMap m_outer;
public:
	static bool const isLazyAllocation = OuterEnumMap::isLazyAllocation;

	EnumMap2D()
	{
		// (No static assert b/c defaultValue is not a compile-time constant)
		FAssert(OuterEnumMap::defaultValue == defaultValue);
		if (!isLazyAllocation)
		{
			FOR_EACH_OUTER_KEY(eOuterKey)
				setUnsafe(eOuterKey, new InnerEnumMap());
		}
	}
	~EnumMap2D()
	{
		reset();
	}
	ASSIGN(EnumMap2D) // advc.xmldefault
	{
		reset();
		FOR_EACH_OUTER_KEY(eOuterKey)
		{
			InnerEnumMap const* pOtherInner = kOther.getUnsafe(eOuterKey);
			if (!isLazyAllocation || pOtherInner != NULL)
				setUnsafe(eOuterKey, new InnerEnumMap(*pOtherInner));
		}
	}

    VInner get(EOuter eOuterKey, EInner eInnerKey) const
    {
        InnerEnumMap* pInnerMap = get(eOuterKey);
        if (isLazyAllocation && pInnerMap == NULL)
            return InnerEnumMap::defaultValue;
        return pInnerMap->get(eInnerKey);
    }
	using::EnumMap2DBase::get; // unhide
protected: // reduce visibility
	void set(EOuter eOuterKey, InnerEnumMap* pInnerMap)
	{
		FAssertMsg(pInnerMap != NULL, "Memory leak; use resetVal instead.");
		EnumMap2DBase::set(eOuterKey, pInnerMap);
	}
public:
	void set(EOuter eOuterKey, EInner eInnerKey, VInner vInnerValue)
	{
		InnerEnumMap* pInnerMap = get(eOuterKey);
		if (isLazyAllocation && pInnerMap == NULL)
		{
			// Avoid unnecessary allocation of inner map
			if (vInnerValue == InnerEnumMap::defaultValue)
				return;
			pInnerMap = new InnerEnumMap();
			setUnsafe(eOuterKey, pInnerMap);
		}
		pInnerMap->set(eInnerKey, vInnerValue);
	}

	// (These will hide the two-argument versions)
	void add(EOuter eOuterKey, EInner eInnerKey, VInner vAddend)
	{
		lookup(eOuterKey).add(eInnerKey, vAddend);
	}
	void multiply(EOuter eOuterKey, EInner eInnerKey, VInner vMultiplier)
	{
		lookup(eOuterKey).multiply(eInnerKey, vMultiplier);
	}
	void divide(EOuter eOuterKey, EInner eInnerKey, VInner vDivisor)
	{
		lookup(eOuterKey).divide(eInnerKey, vDivisor);
	}
	void toggle(EOuter eOuterKey, EInner eInnerKey)
	{
		InnerEnumMap* pInnerMap = get(eOuterKey);
		if (isLazyAllocation && pInnerMap == NULL)
			set(eOuterKey, eInnerKey, !InnerEnumMap::defaultValue);
		else return pInnerMap->toggle(eInnerKey);
	}

	void reset()
	{
		if (!isLazyAllocation || m_outer.isAnyNonDefault())
		{
			FOR_EACH_OUTER_KEY(eOuterKey)
				resetVal(eOuterKey);
		}
		m_outer.reset();
	}
	void resetVal(EOuter eOuterKey)
	{
		// m_outer doesn't own the inner map instances; we have to delete them.
		InnerEnumMap* pInnerMap = get(eOuterKey);
		if (!isLazyAllocation || pInnerMap != NULL)
			delete pInnerMap;
		m_outer.resetVal(eOuterKey);
	}
	void resetVal(EOuter eOuterKey, EInner eInnerKey)
	{
		set(eOuterKey, eInnerKey, InnerEnumMap::defaultValue);
	}
	void setAll(VInner vInnerValue)
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
			setAll(eOuterKey, vInnerValue);
	}
	void setAll(EOuter eOuterKey, VInner vInnerValue)
	{
		/*	Don't do a default check (see set(EOuter, EInner, VInner))
			-- caller would probably use reset for that. */
		lookup(eOuterKey).setAll(vInnerValue);
	}
	bool isAnyNonDefault() const
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
		{
			if (isAnyNonDefault(eOuterKey))
				return true;
		}
		return false;
	}
	bool isAnyNonDefault(EOuter eOuterKey) const
	{
		InnerEnumMap* pInnerMap = get(eOuterKey);
		if (isLazyAllocation && pInnerMap == NULL)
			return false;
		return pInnerMap->isAnyNonDefault();
	}
	int numNonDefault() const
	{
		int iSum = 0;
		FOR_EACH_OUTER_KEY(eOuterKey)
			iSum += numNonDefault(eOuterKey);
		return iSum;
	}
	int numNonDefault(EOuter eOuterKey) const
	{
		InnerEnumMap* pInnerMap = get(eOuterKey);
		if (isLazyAllocation && pInnerMap == NULL)
			return 0;
		return pInnerMap->numNonDefault();
	}

	void insert(int iOuterKey, int iInnerKey, VInner vInnerValue)
	{
		EOuter eOuterKey = static_cast<EOuter>(iOuterKey);
		EInner eInnerKey = static_cast<EInner>(iInnerKey);
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssertInfoEnum(eOuterKey);
		FAssertInfoEnum(eInnerKey);
		setUnsafe(eOuterKey, eInnerKey, vInnerValue);
	#else
		set(eOuterKey, eInnerKey, vInnerValue);
	#endif
	}

	template<class DataStream>
	void write(DataStream pStream) const
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
		{
			InnerEnumMap* pInnerMap = get(eOuterKey);
			bool bEmpty = (isLazyAllocation && pInnerMap == NULL);
			pStream->Write(!bEmpty);
			if (!bEmpty)
				pInnerMap->write(pStream);
		}
	}
	void read(FDataStreamBase* pStream,
		uint uiOuterSubtrahend = 0, uint uiInnerSubtrahend = 0)
	{
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssert(!isAnyNonDefault());
	#endif
		for (EOuter eOuterKey = enum_traits<EOuter>::first;
			eOuterKey < getLength() - (int)uiOuterSubtrahend; ++eOuterKey)
		{
			bool bNonEmpty;
			pStream->Read(&bNonEmpty);
			if (bNonEmpty)
			{
				InnerEnumMap* pInnerMap = new InnerEnumMap();
				setUnsafe(eOuterKey, pInnerMap);
				pInnerMap->read(pStream, uiInnerSubtrahend);
			}
		}
	}
	template<typename OuterSizeType, typename InnerSizeType, typename ValueType>
	void writeLazyArray(FDataStreamBase* pStream) const
	{
		if (!isAnyNonDefault())
		{
			pStream->Write(static_cast<OuterSizeType>(0));
			return;
		}
		FOR_EACH_OUTER_KEY(eOuterKey)
		{
			InnerEnumMap* pInnerMap = m_outer.getUnsafe(eOuterKey);
			if (isLazyAllocation && pInnerMap == NULL)
				pStream->write(static_cast<InnerSizeType>(0));
			else pInner->writeLazyArray<InnerSizeType,ValueType>(pStream);
		}
	}
	template<typename OuterSizeType, typename InnerSizeType, typename ValueType>
	void readLazyArray(FDataStreamBase* pStream,
		uint uiOuterSubtrahend = 0, uint uiInnerSubtrahend = 0)
	{
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssert(!isAnyNonDefault());
	#endif
		OuterSizeType outerSz;
		pStream->Read(&outerSz);
		if (outerSz == 0)
			return;
		for (EOuter eOuterKey = enum_traits<EOuter>::first;
			eOuterKey < getLength() - (int)uiOuterSubtrahend; ++eOuterKey)
		{
			InnerSizeType innerSz;
			pStream->Read(&innerSz);
			if (innerSz == 0)
				continue;
			InnerEnumMap* pInnerMap = new InnerEnumMap();
			setUnsafe(eOuterKey, pInnerMap);
			pInnerMap->readArray<ValueType>(pStream, uiInnerSubtrahend);
		}
	}
	template<typename ValueType>
	void writeArray(FDataStreamBase* pStream) const
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
		{
			InnerEnumMap* pInnerMap = m_outer.getUnsafe(eOuterKey);
			if (isLazyAllocation && pInnerMap == NULL)
			{
				pInnerMap = new InnerEnumMap();
				pInnerMap->writeArray<ValueType>(pStream);
				delete pInnerMap;
				return;
			}
			pInnerMap->writeArray<ValueType>(pStream);
		}
	}
	template<typename ValueType>
	void readArray(FDataStreamBase* pStream,
		uint uiOuterSubtrahend = 0, uint uiInnerSubtrahend = 0)
	{
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssert(!isAnyNonDefault());
	#endif
		for (EOuter eOuterKey = enum_traits<EOuter>::first;
			eOuterKey < getLength() - (int)uiOuterSubtrahend; ++eOuterKey)
		{
			// Temporary array-based map
			ArrayEnumMap<EInner,VInner,VInner,InnerEnumMap::defaultValue> innerArray;
			innerArray.readArray<ValueType>(pStream, uiInnerSubtrahend);
			if (!innerArray.isAnyNonDefault())
				continue;
			InnerEnumMap* pInnerMap = new InnerEnumMap();
			setUnsafe(eOuterKey, pInnerMap);
			int iIter = 0;
			for (std::pair<EInner,VInner> nonDefaultPair;
				innerArray.nextNonDefaultPair<VInner>(iIter, nonDefaultPair); )
			{
				pInnerMap->set(nonDefaultPair.first, nonDefaultPair.second);
			}
		}
	}
	// For compatibility with earlier "SparseEnumMap2D" implementation
	template<typename F, typename S, typename T> // first, second, third
	void readTuple(FDataStreamBase* pStream)
	{
		short iSize;
		pStream->Read(&iSize);
		if (iSize == 0)
			return;
		for (short i = 0; i < iSize; i++)
		{
			F f; S s; T t;
			pStream->Read(&f); pStream->Read(&s); pStream->Read(&t);
			FAssertInfoEnum(static_cast<EOuter>(f));
			FAssertInfoEnum(static_cast<EInner>(s));
			set(static_cast<EOuter>(f), static_cast<EInner>(s), static_cast<VInner>(t));
		}
	}

protected:
	InnerEnumMap* getUnsafe(EOuter eOuterKey) const
	{
		return m_outer.get(eOuterKey);
	}
	void setUnsafe(EOuter eOuterKey, InnerEnumMap* pInnerMap)
	{
		m_outer.set(eOuterKey, pInnerMap);
	}
	InnerEnumMap& lookup(EOuter eOuterKey)
	{
		InnerEnumMap* pInnerMap = get(eOuterKey);
		if (isLazyAllocation && pInnerMap == NULL)
		{
			pInnerMap = new InnerEnumMap();
			setUnsafe(eOuterKey, pInnerMap);
		}
		return *pInnerMap;
	}
	template<typename ValueType>
	bool _nextNonDefaultPair(int& iIter, std::pair<EOuter,ValueType>& kPair) const
	{
		BOOST_STATIC_ASSERT((is_same_type<ValueType,InnerMap*>::value));
		return m_outer.nextNonDefaultPair(iIter, kPair);
	}
	EOuter _nextNonDefaultKey(int& iIter) const
	{
		return m_outer.nextNonDefaultKey(iIter);
	}
};

template<typename EOuter, typename EInner, class V,
	class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none>
class ArrayEnumMap2D : public EnumMap2D<
	ArrayEnumMap<EOuter,
	/*	(Since EInner tends to be or should be the shorter enum type,
		I reckon that eager allocation for the inner map might be faster.) */
	ArrayEnumMap<EInner, V, CV, iDEFAULT, /*bEAGER_ALLOC=*/true>*>,
	ArrayEnumMap<EInner, V, CV, iDEFAULT, /*bEAGER_ALLOC=*/true> >
{};

template<typename EOuter, typename EInner, class V,
	class CV = void*,
	int iDEFAULT = (int)enum_traits<V>::none,
	bool bMONOTONE = false>
class ListEnumMap2D : public EnumMap2D<
	ListEnumMap<EOuter,
	ArrayEnumMap<EInner, V, CV, iDEFAULT, true>*, void*, NULL, bMONOTONE>,
	ArrayEnumMap<EInner, V, CV, iDEFAULT, true> >
{};

/*	This requires the user to specify the inner map type twice,
	but the alternative -- taking the outer map as a template --
	won't work because array enum map and list enum map don't have
	the same template parameters (and there may be other obstancles as well).
	Might be possible to implement this class as a specialization of EnumMap2D. */
template<class OuterEnumMap, class InnerEncodableMap>
class Enum2IntEncMap : public OuterEnumMap
{
public:
	typedef InnerEncodableMap enc_map_t;
protected:
	typedef typename OuterEnumMap::EnumType EOuter;
	typedef typename InnerEncodableMap::EnumType EInner;
	BOOST_STATIC_ASSERT((is_same_type<
			typename OuterEnumMap::ValueType,
			typename InnerEncodableMap::enc_t>::value));
	typedef typename InnerEncodableMap::ValueType VInner;

public:
	using OuterEnumMap::get;
	using OuterEnumMap::set;
	using OuterEnumMap::resetVal;
	using OuterEnumMap::isAnyNonDefault;
	using OuterEnumMap::insert;

    VInner get(EOuter eOuterKey, EInner eInnerKey) const
    {
		return lookup(eOuterKey).get(eInnerKey);
    }
	void set(EOuter eOuterKey, EInner eInnerKey, VInner vValue)
	{
		InnerEncodableMap innerMap(get(eOuterKey));
		innerMap.set(eInnerKey, vValue);
		set(eOuterKey, innerMap.encode());
	}
	void add(EOuter eOuterKey, EInner eInnerKey, VInner vAddend)
	{
		InnerEncodableMap innerMap(get(eOuterKey));
		innerMap.add(eInnerKey, vAddend);
		set(eOuterKey, innerMap.encode());
	}
	void multiply(EOuter eOuterKey, EInner eInnerKey, VInner vMultiplier)
	{
		InnerEncodableMap innerMap(get(eOuterKey));
		innerMap.multiply(eInnerKey, vMultiplier);
		set(eOuterKey, innerMap.encode());
	}
	void divide(EOuter eOuterKey, EInner eInnerKey, VInner vDivisor)
	{
		InnerEncodableMap innerMap(get(eOuterKey));
		innerMap.divide(eInnerKey, vDivisor);
		set(eOuterKey, innerMap.encode());
	}
	void resetVal(EOuter eOuterKey, EInner eInnerKey)
	{
		set(eOuterKey, eInnerKey, InnerEncodableMap::defaultValue);
	}
	void setAll(VInner vValue)
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
			setAll(eOuterKey, vValue);
	}
	void setAll(EOuter eOuterKey, VInner vValue)
	{
		InnerEncodableMap innerMap(get(eOuterKey));
		innerMap.setAll(vValue);
		set(eOuterKey, innerMap.encode());
	}
	bool isAnyNonDefault(EOuter eOuterKey) const
	{
		return lookup(eOuterKey).isAnyNonDefault();
	}
	int numNonDefault() const
	{
		int iSum = 0;
		FOR_EACH_OUTER_KEY(eOuterKey)
			iSum += numNonDefault(eOuterKey);
		return iSum;
	}
	int numNonDefault(EOuter eOuterKey) const
	{
		return lookup(eOuterKey).numNonDefault();
	}
	void insert(int iOuterKey, int iInnerKey, VInner vValue)
	{
		EOuter eOuterKey = static_cast<EOuter>(iOuterKey);
		EInner eInnerKey = static_cast<EInner>(iInnerKey);
	#ifdef ENUM_MAP_EXTRA_ASSERTS
		FAssertInfoEnum(eOuterKey);
		FAssertInfoEnum(eInnerKey);
	#else
		set(eOuterKey, eInnerKey, vValue);
	#endif
	}
	template<typename ValueType>
	void writeArray(FDataStreamBase* pStream) const
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
			lookup(eOuterKey).writeArray<ValueType>(pStream);
	}
	template<typename ValueType>
	void readArray(FDataStreamBase* pStream, int iSubtrahend = 0)
	{
		FOR_EACH_OUTER_KEY(eOuterKey)
		{
			InnerEncodableMap innerMap;
			innerMap.readArray<ValueType>(pStream, iSubtrahend);
			set(eOuterKey, innerMap.encode());
		}
	}
	template<typename SizeType, typename ValueType>
	void writeLazyArray(FDataStreamBase* pStream) const
	{	// Not sure if this is helpful for anything (i.e. if BtS uses this format anywhere)
		FOR_EACH_OUTER_KEY(eOuterKey)
			lookup(eOuterKey).writeLazyArray<SizeType,ValueType>(pStream);
	}
	template<typename OuterSizeType, typename InnerSizeType, typename ValueType>
	void readLazyArray(FDataStreamBase* pStream,
		uint uiOuterSubtrahend, uint uiInnerSubtrahend)
	{
		for (EOuter eOuterKey = enum_traits<EOuter>::first;
			eOuterKey < getLength() - (int)uiOuterSubtrahend; ++eOuterKey)
		{
			InnerEncodableMap innerMap;
			innerMap.readLazyArray<SizeType,ValueType>(pStream, uiInnerSubtrahend);
			set(eOuterKey, innerMap.encode());
		}
	}
	// For compatibility with BtS vectors of 3-tuple structs
	template<typename SizeType>
	void readTuple(FDataStreamBase* pStream)
	{
		SizeType sz;
		pStream->Read(&sz);
		for (SizeType i = 0; i < sz; i++)
		{
			int iFirst, iSecond, iThird;
			pStream->Read(&iFirst);
			pStream->Read(&iSecond);
			pStream->Read(&iThird);
			FAssertInfoEnum(static_cast<EOuter>(iFirst));
			FAssertInfoEnum(static_cast<EInner>(iSecond));
			InnerEncodableMap innerMap;
			innerMap.set(static_cast<EInner>(iSecond), static_cast<VInner>(iThird));
			set(static_cast<EOuter>(iFirst), innerMap.encode());
		}
	}

protected:
	InnerEncodableMap lookup(EOuter eOuterKey) const
	{
		return InnerEncodableMap(get(eOuterKey));
	}
	template<typename ValueType>
	bool _nextNonDefaultPair(int& iIter, std::pair<EOuter,ValueType>& kPair) const
	{
		BOOST_STATIC_ASSERT((is_same_type<ValueType,InnerEncodableMap::enc_t>::value));
		return nextNonDefaultPair(iIter, kPair);
	}
};

#undef FOR_EACH_OUTER_KEY
#undef BITSIZE
#undef ASSIGN

#endif
