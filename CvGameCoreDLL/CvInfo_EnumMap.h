#pragma once

#ifndef CV_INFO_ENUM_MAP_H
#define CV_INFO_ENUM_MAP_H

/*	advc.003t: Macros for defining enum map instances and their accessor functions
	as members of CvInfo classes. */

#define DEF_INFO_ENUM_MAP_HELPER(TagName, EnumPrefix, ValueType, CompactValueType, \
		InfoMapTempl, iDefault, getterPrefix, PyValueType) \
	/* for the FOR_EACH_NON_DEFAULT... macros */ \
	InfoMapTempl<EnumPrefix##Types,ValueType,CompactValueType,iDefault> const& \
	getterPrefix##TagName() const \
	{ \
		return m_map##TagName; \
	} \
	private: \
	/* Non-const accessor for XML loading. */ \
	/* Can't have the same name as the public version above b/c the */ \
	/* compiler will assume that the (inaccessible) private version is meant */ \
	/* when the callee is non-const. */ \
	InfoMapTempl<EnumPrefix##Types,ValueType,CompactValueType,iDefault>& TagName() \
	{ \
		return m_map##TagName; \
	} \
	/* data member declaration */ \
	InfoMapTempl<EnumPrefix##Types,ValueType,CompactValueType,iDefault> m_map##TagName; \
	/* Python export (will have to prepend "py_" in CyInfoInterface*.cpp) */ \
	PY_WRAP(PyValueType, getterPrefix##TagName, EnumPrefix); \
	public: \
	/* random access */ \
	ValueType getterPrefix##TagName(EnumPrefix##Types e##EnumPrefix) const \
	{ \
		return m_map##TagName.get(e##EnumPrefix); \
	}
#define DEF_INFO_ENUM_MAP_DEFAULT(TagName, EnumPrefix, ValueType, CompactValueType, InfoMapTempl, iDefault) \
	DEF_INFO_ENUM_MAP_HELPER(TagName, EnumPrefix, ValueType, CompactValueType, InfoMapTempl, iDefault, get, int)
#define DEF_INFO_ENUM_MAP(TagName, EnumPrefix, ValueType, CompactValueType, InfoMapTempl) \
	DEF_INFO_ENUM_MAP_DEFAULT(TagName, EnumPrefix, ValueType, CompactValueType, InfoMapTempl, 0)
// Will want to use the default compact value type when mapping to enum values
#define DEF_INFO_ENUM2ENUM_MAP_DEFAULT(TagName, EnumPrefix, ValuePrefix, InfoMapTempl, iDefault) \
	DEF_INFO_ENUM_MAP_HELPER(TagName, EnumPrefix, ValuePrefix##Types, void*, \
	InfoMapTempl, iDefault, get, int)
#define DEF_INFO_ENUM2ENUM_MAP(TagName, EnumPrefix, ValuePrefix, InfoMapTempl) \
	DEF_INFO_ENUM_MAP_DEFAULT(TagName, EnumPrefix, ValuePrefix##Types, void*, InfoMapTempl, 0)
// Separate macros just so that the getter functions get named "is..."
#define DEF_INFO_ENUM_MAP_BOOL_DEFAULT(TagName, EnumPrefix, InfoMapTempl, iDefault) \
	DEF_INFO_ENUM_MAP_HELPER(TagName, EnumPrefix, bool, void*, \
	InfoMapTempl, iDefault, is, bool)
#define DEF_INFO_ENUM_MAP_BOOL(TagName, EnumPrefix, InfoMapTempl) \
	DEF_INFO_ENUM_MAP_BOOL_DEFAULT(TagName, EnumPrefix, InfoMapTempl, 0)
/*	Use an adapter template with dummy parameters so that the EnumSet template
	can be used in the ..._HELPER macro above */
template<typename E, class V, class CV, int iDEFAULT>
class OfflineListEnumSetAdapter : public OfflineListEnumSet<E> {};
#define DEF_INFO_ENUM_SET_DEFAULT(TagName, EnumPrefix, iDefault) \
	DEF_INFO_ENUM_MAP_HELPER(TagName, EnumPrefix, bool, void*, \
	OfflineListEnumSetAdapter, iDefault, is, bool)
#define DEF_INFO_ENUM_SET(TagName, EnumPrefix) \
	DEF_INFO_ENUM_SET_DEFAULT(TagName, EnumPrefix, 0)

// Can't use the same macro for yield and commerce maps b/c those aren't class templates
#define DEF_SHORT_INFO_ENUM_MAP(TagName, EnumPrefix, ShortMapType) \
	/* for game text */ \
	ShortMapType const& get##TagName() const \
	{ \
		return m_map##TagName; \
	} \
	private: \
	ShortMapType& TagName() \
	{ \
		return m_map##TagName; \
	} \
	ShortMapType m_map##TagName; \
	PY_WRAP(int, get##TagName, EnumPrefix); \
	public: \
	ShortMapType::ValueType get##TagName(EnumPrefix##Types e##EnumPrefix) const \
	{ \
		return m_map##TagName.get(e##EnumPrefix); \
	}

// Mappings to yield and commerce maps that get encoded in a single integer value
#define DEF_INFO_ENUM2SHORT_MAP(TagName, OuterEnumPrefix, InnerEnumPrefix, \
		InnerMapType, OuterMapTempl) \
	/* To allow iteration over the non-empty inner maps */ \
	Enum2IntEncMap<OuterMapTempl<OuterEnumPrefix##Types,InnerMapType::enc_t>,InnerMapType> const& get##TagName() const \
	{ \
		return m_map##TagName; \
	} \
	private: \
	Enum2IntEncMap<OuterMapTempl<OuterEnumPrefix##Types,InnerMapType::enc_t>,InnerMapType>& TagName() \
	{ \
		return m_map##TagName; \
	} \
	Enum2IntEncMap<OuterMapTempl<OuterEnumPrefix##Types,InnerMapType::enc_t>,InnerMapType> m_map##TagName; \
	public: \
	InnerMapType get##TagName(OuterEnumPrefix##Types e##OuterEnumPrefix) const \
	{ \
		return InnerMapType(m_map##TagName.get(e##OuterEnumPrefix)); \
	} \
	private: \
	PY_WRAP_2D(InnerMapType::ValueType, get##TagName, OuterEnumPrefix, InnerEnumPrefix) \
	public: \
	InnerMapType::ValueType get##TagName(OuterEnumPrefix##Types e##OuterEnumPrefix, \
		InnerEnumPrefix##Types e##InnerEnumPrefix) const \
	{ \
		return m_map##TagName.get(e##OuterEnumPrefix, e##InnerEnumPrefix); \
	}

#endif
