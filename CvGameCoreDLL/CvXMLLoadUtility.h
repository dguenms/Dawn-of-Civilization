#pragma once
#ifndef XML_LOAD_UTILITY_H
#define XML_LOAD_UTILITY_H

/*	AUTHOR:  Eric MacDonald  --  8/2003
	PURPOSE: Group of functions to load in the xml files for Civilization 4
	Copyright (c) 2003 Firaxis Games, Inc. All rights reserved. */
/*  advc: Deleted most of the comments in this file and moved some to the
	implementation files (CvXMLLoadUtility.cpp, CvXMLLoadUtilityInit.cpp,
	CvXMLLoadUtilityGet.cpp and CvXMLLoadUtilitySet.cpp). Also deleted many
	non-informative comments from the implementation files. */

/*	advc: Ideally, that interface should be encapsulated by this class.
	Currently, however, most of the CvInfo::read functions contain some
	custom parsing code that uses gDLL->getXMLIFace() directly. */
#include "CvDLLXMLIFaceBase.h"

class FXmlSchemaCache;
class FXml;
class CvGameText;
class CvCacheObject;
class CvImprovementBonusInfo;


class CvXMLLoadUtility /* advc.003k: */ : private boost::noncopyable
{
public:
	DllExport CvXMLLoadUtility();
	DllExport ~CvXMLLoadUtility();

	bool CreateFXml();
	void DestroyFXml();

	DllExport bool LoadPostMenuGlobals();
	DllExport bool LoadPreMenuGlobals();
	DllExport bool LoadBasicInfos();
	DllExport bool LoadPlayerOptions();
	DllExport bool LoadGraphicOptions();
	// <advc.003v>
	bool LoadOptionalGlobals();
	bool LoadThroneRoomInfo(); // </advc.003v>

	bool ReadGlobalDefines(TCHAR const* szXMLFileName, CvCacheObject* cache);
	
	DllExport bool SetGlobalDefines();
	DllExport bool SetGlobalTypes();
	// advc.003j: Unused and has no definition
	//bool SetGlobals(); // calls various functions that load xml files that in turn load relevant global variables
	DllExport bool SetPostGlobalsGlobalDefines();
	DllExport void CleanUpGlobalVariables();

	DllExport void ResetLandscapeInfo();
	DllExport bool SetupGlobalLandscapeInfo();
	DllExport bool SetGlobalArtDefines();
	DllExport bool LoadGlobalText();
	bool SetHelpText();
	DllExport void ResetGlobalEffectInfo();

	// for progress bars  // advc.003k: all unused
	/*typedef void (*ProgressCB)(int iStepNum, int iTotalSteps, const char* szMessage);
	static int GetNumProgressSteps();
	void RegisterProgressCB(ProgressCB cbFxn);*/

	bool SkipToNextVal();

	void MapChildren();	// call this before GetChildXMLValByName for fast search
	bool GetChildXmlValByName(std::string& r, TCHAR const* szName, char const* szDefault = NULL);
	bool GetChildXmlValByName(std::wstring& r, TCHAR const* szName, wchar const* szDefault = NULL);
	bool GetChildXmlValByName(char* r, TCHAR const* szName, char const* szDefault = NULL);
	bool GetChildXmlValByName(wchar* r, TCHAR const* szName, wchar const* szDefault = NULL);
	/*  (advc: Returning by reference would be nicer than by pointer, but I don't want to change
		hundreds of call locations.) */
	bool GetChildXmlValByName(int* r, TCHAR const* szName,
			/*  advc.006b: Was 0. Instead use a value that no one wants to use so that
				the callee can check if the param was set. */
			int iDefault = MIN_INT);
	bool GetChildXmlValByName(float* r, TCHAR const* szName,
			float fDefault = FLT_MIN); // advc.006b: was 0.0f
	bool GetChildXmlValByName(bool* r, TCHAR const* szName,
			/*  advc.006b: Caller will have to set this to false to avoid an error
				if szName isn't found */
			bool bMandatory = true,
			bool bDefault = false);
	/*	advc.006j: Had required int type; can now work with enum types too,
		and will assert their bounds. */
	template<typename T>
	void SetInfoIDFromChildXmlVal(T& tResult, TCHAR const* szName)
	{	// Needs to go through a struct b/c functions can't be partially specialized
		InfoIDFromChild<T>::set(*this, tResult, szName);
	}
	// <advc.xmldefault>
	void SetGlobalTypeFromChildXmlVal(int& iR, TCHAR const* szName, bool bInfoType = false);
	int GetChildTypeIndex(); // </advc.xmldefault>
	/*  advc.006b: Unused for now. Can use this to disable the assertions added to
		GetChildXmlValByName temporarily, e.g. while loading a special CvInfo element
		that lacks tags which, normally, are mandatory. */
	void setAssertMandatoryEnabled(bool b);

	bool LoadCivXml(FXml* pFXml, TCHAR const* szFilename);

	bool GetXmlVal(std::wstring& r, wchar const* szDefault = NULL);
	bool GetXmlVal(std::string& r, char const* szDefault = NULL);
	bool GetXmlVal(wchar* r, wchar const* szDefault = NULL);
	bool GetXmlVal(char* r, char const* szDefault = NULL);
	// advc: Return by reference (was pointer)
	bool GetXmlVal(int& r, int iDefault = 0);
	bool GetXmlVal(float& r, float fDefault = 0.0f);
	bool GetXmlVal(bool& r, bool bDefault = false);

	bool GetNextXmlVal(std::string& r, char const* szDefault = NULL);
	bool GetNextXmlVal(std::wstring& r, wchar const* szDefault = NULL);
	bool GetNextXmlVal(char* r, char const* szDefault = NULL);
	bool GetNextXmlVal(wchar* r, wchar const* szDefault = NULL);
	// advc: Return by reference (was pointer)
	bool GetNextXmlVal(int& r, int iDefault = 0);
	bool GetNextXmlVal(short& r, short iDefault = 0); // advc.003t
	bool GetNextXmlVal(char& r, char iDefault = 0); // advc.003t
	bool GetNextXmlVal(float& r, float fDefault = 0.0f);
	bool GetNextXmlVal(bool& r, bool bDefault = false);
	/*	<advc.enum>  (Could replace most of the above functions with a template too
		- one that doesn't get instantiated for enum types.) */
	template<typename T>
	bool GetNextXmlVal(T& r, T tDefault = (T)-1);
	// Need to make these casts explicit to avoid matching the template
	bool GetNextXmlVal(CvString& r, char const* szDefault = NULL)
	{
		return GetNextXmlVal(static_cast<std::string&>(r), szDefault);
	}
	bool GetNextXmlVal(CvWString& r, wchar const* szDefault = NULL)
	{
		return GetNextXmlVal(static_cast<std::wstring&>(r), szDefault);
	} // </advc.enum>

	bool GetChildXmlVal(std::string& r, char const* szDefault = NULL);
	bool GetChildXmlVal(std::wstring& r, wchar const* szDefault = NULL);
	bool GetChildXmlVal(char* r, char const* szDefault = NULL);
	bool GetChildXmlVal(wchar* r, wchar const* szDefault = NULL);
	// advc: Return by reference (was pointer)
	bool GetChildXmlVal(int& r, int iDefault = 0);
	bool GetChildXmlVal(float& r, float fDefault = 0.0f);
	bool GetChildXmlVal(bool& r, bool bDefault = false);

	#ifdef _USRDLL
	FXml* GetXML() { return m_pFXml; }
	#endif
	/*	advc: Wrapper that calls SetToParent. SetYields remains (functionally)
		unchanged - to avoid breaking XML loading code in mod-mods. Such errors
		would be difficult to debug b/c the parser level is stored in the EXE. */
	int SetYieldArray(int** ppiYield);
	int SetYields(int** ppiYield); // (advc: deprecated)
	#ifdef _USRDLL
	// <advc> See comment above
	template <class T>
	int SetCommerceArray(T** ppiCommerce); // </advc>
	template <class T>
	int SetCommerce(T** ppiCommerce); // (advc: deprecated)
	#endif

	void SetFeatureStruct(int** ppiFeatureTech, int** ppiFeatureTime, int** ppiFeatureProduction, bool** ppbFeatureRemove);
	void SetImprovementBonuses(CvImprovementBonusInfo** ppImprovementBonus);

	static int FindInInfoClass(TCHAR const* szType, bool hideAssert = false);

	#ifdef _USRDLL
	template <class T>
	void InitList(T **ppList, int iListLen, T val = 0);
	#endif
	void InitStringList(CvString **ppszList, int iListLen, CvString szString);

	void InitImprovementBonusList(CvImprovementBonusInfo** ppImprovementBonus, int iListLen);
	void InitBuildingDefaults(int **ppiDefaults);
	void InitUnitDefaults(int **ppiDefaults);
	void Init2DIntList(int*** pppiList, int iSizeX, int iSizeY);
	void Init2DFloatList(float*** pppfList, int iSizeX, int iSizeY);
	void Init2DDirectionTypesList(DirectionTypes*** pppiList, int iSizeX, int iSizeY);
	void InitPointerIntList(int*** pppiList, int iSizeX);
	void InitPointerFloatList(float*** pppfList, int iSizeX);

	// (advc: HotKeyFromDescription, KeyStringFromKBCode moved to CvGameCoreUtils)

	bool SetAndLoadVar(int** ppiVar, int iDefault=0);
	bool SetStringList(CvString** ppszStringArray, int* piSize);
	int GetHotKeyInt(TCHAR const* pszHotKeyVal);

	// allocate and initialize a list from a tag pair in the xml
	void SetVariableListTagPair(CvString** ppszList, TCHAR const* szRootTagName,
			int iInfoBaseLength, CvString szDefaultListVal = "");
	void SetVariableListTagPairForAudioScripts(int **ppiList, TCHAR const* szRootTagName,
			int iInfoBaseLength, int iDefaultListVal = -1);
	/*	advc (19 Feb 2021): Deleted four versions (a fifth - AudioScripts - deleted
		much earlier) that took a param CvString* m_paszTagList.
		Those functions were for global non-info types. Now the versions above
		can handle any global types (through getGlobalEnumFromString). */
	/*	advc.003t: Move the parser logic into an iterator b/c I don't want
		that part to have an enum map type as a template parameter */
	class XMLTagPairIteratorBase
	{
	public:
		XMLTagPairIteratorBase(CvXMLLoadUtility& kUtil)
		:	m_util(kUtil), m_pParser(kUtil.GetXML()), m_iParserLevel(0)
		{}
		~XMLTagPairIteratorBase()
		{	/*	This relies on no two instances existing in the same scope.
				That should be fine. (Could also get it to work in 'next'.) */
			while (m_iParserLevel > 0)
			{
				setToParent();
				m_iParserLevel--;
			}
		}
	protected:
		CvXMLLoadUtility& m_util;
		FXml* m_pParser;
		int m_iParserLevel;
		void setToParent();
		static int const iNO_KEY = -1;
	};
	template<typename T>
	class XMLTagPairIterator : public XMLTagPairIteratorBase
	{
	public:
		XMLTagPairIterator(CvXMLLoadUtility& kUtil, TCHAR const* szRootTagName);
		std::pair<int,T> next();
	private:
		int m_iSiblingIndex;
		int m_iSiblings;
		TCHAR m_acTextVal[256]; // (Tbd.: Could we just use a CvString?)
		static std::pair<int,T> noPair()
		{
			return std::pair<int,T>(iNO_KEY, (T)0);
		}
	};
	/*	advc.enum: Load mapping from an enum key to a list of yield or commerce rates.
		Based on BtS code repeated in the CvInfo classes, e.g. CvInfo_Building. */
	template<class EncodableMap>
	class XMLTagPairRateIterator : public XMLTagPairIteratorBase
	{
	public:
		XMLTagPairRateIterator(CvXMLLoadUtility& kUtil, TCHAR const* szTagName,
				TCHAR const* szKeyTagName = NULL, TCHAR const* szRateTagName = NULL);
		~XMLTagPairRateIterator()
		{
			if (m_aiRates != NULL)
				delete[] m_aiRates;
		}
		std::pair<int,typename EncodableMap::enc_t> next();
	private:
		static int const iENUM_LEN = enum_traits<typename EncodableMap::EnumType>::len;
		int m_iSiblingIndex;
		int m_iSiblings;
		bool m_bFlat;
		CvString m_szKeyTagName;
		CvString m_szRateTagName;
		CvString m_szTextVal;
		int* m_aiRates;
		static std::pair<int,typename EncodableMap::enc_t> noPair()
		{
			return std::pair<int,typename EncodableMap::enc_t>(iNO_KEY, 0);
		}
	};
	/*  advc.003t (note): Will set the array that pptList points to to NULL if
		tDefaultListVal is 0 and no pairs are found or if all (index,value) pairs
		have the value 0. */
	template<typename T>
	void SetVariableListTagPair(T** pptList, TCHAR const* szRootTagName,
		// advc.003x: Unused param iInfoBaseSize removed
		int iInfoBaseLength, T tDefaultListVal = 0)
	{
		if (iInfoBaseLength <= 0)
		{
			char szMessage[1024];
			sprintf(szMessage,
					"Allocating zero or less memory.\nCurrent XML file is: %s",
					GC.getCurrentXMLFile().GetCString());
			errorMessage(szMessage);
		}
		bool bListModified = (*pptList != NULL); // advc.003t
		InitList(pptList, iInfoBaseLength, tDefaultListVal);
		XMLTagPairIterator<T> it(*this, szRootTagName);
		for (std::pair<int,T> pair = it.next(); pair.first != -1; pair = it.next())
		{
			if (pair.first >= iInfoBaseLength)
			{
				FErrorMsg("Key tag out of bounds"); // advc.006
				char szMessage[1024];
				sprintf(szMessage,
						/*	advc: This had said "too many siblings" - at this point,
							that error condition can't be distinguished from a
							wrong type being used in XML, e.g. a UNITCLASS_... where
							a UNITCOMBAT_... is expected. */
						"Key tag out of bounds.\nCurrent XML file is: %s",
						GC.getCurrentXMLFile().GetCString());
				errorMessage(szMessage);
			}
			(*pptList)[pair.first] = pair.second;
			// <advc.003t>
			if (pair.second != tDefaultListVal)
				bListModified = true;
		}
		if (!bListModified && tDefaultListVal == 0)
			SAFE_DELETE_ARRAY(*pptList); // </advc.003t>
	}
	// <advc.003t>
	template<class InfoMap>
	void SetVariableListTagPair(InfoMap& kMap, TCHAR const* szRootTagName)
	{
		XMLTagPairIterator<InfoMap::ValueType> it(*this, szRootTagName);
		for (std::pair<int,typename InfoMap::ValueType> pair = it.next();
			pair.first != -1; pair = it.next())
		{
			kMap.insert(pair.first, pair.second);
		}
	}
	/*	Wrappers for the SetYieldArray (int only) and
		SetCommerceArray (bool only) functions ... */
	template<class InfoMap>
	void SetVariableListPerYield(InfoMap& kMap, TCHAR const* szRootTagName)
	{
		if (!gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szRootTagName))
			return;
		int* piTmp = NULL;
		int iSet = SetYieldArray(&piTmp);
		if (piTmp != NULL)
		{
			FOR_EACH_ENUM(Yield)
			{
				if (eLoopYield >= iSet)
					break;
				int iVal = piTmp[eLoopYield];
				kMap.insert(eLoopYield, safeIntCast<typename kMap::ValueType>(iVal));
			}
			delete piTmp;
		}
	}
	template<class InfoMap>
	void SetVariableListPerCommerce(InfoMap& kMap, TCHAR const* szRootTagName)
	{
		BOOST_STATIC_ASSERT((is_same_type<typename InfoMap::ValueType,bool>::value));
		if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml, szRootTagName))
		{
			bool* pbTmp = NULL;
			int iSet = SetCommerceArray(&pbTmp);
			if (pbTmp != NULL)
			{
				FOR_EACH_ENUM(Commerce)
				{
					if (eLoopCommerce >= iSet)
						break;
					kMap.insert(eLoopCommerce, pbTmp[eLoopCommerce]);
				}
				delete pbTmp;
			}
		}
	}
	template<class EncodableMap>
	void SetVariableListTagRate(EncodableMap& kMap, TCHAR const* szTagName,
		TCHAR const* szKeyTagName = NULL, TCHAR const* szRateTagName = NULL)
	{
		XMLTagPairRateIterator<EncodableMap::enc_map_t> it(
				*this, szTagName, szKeyTagName, szRateTagName);
		for (std::pair<int,typename EncodableMap::enc_map_t::enc_t> pair = it.next();
			pair.first != -1; pair = it.next())
		{
			/*	This wouldn't allow multiple rate changes per outer key -
				which need to be allowed for a handful of random events. */
			//kMap.insert(pair.first, pair.second);
			EncodableMap::enc_map_t innerMap(pair.second);
			int iIter = 0;
			for (std::pair<typename EncodableMap::enc_map_t::EnumType,int> innerPair;
				innerMap.nextNonDefaultPair<int>(iIter, innerPair); )
			{
				kMap.insert(pair.first, innerPair.first, innerPair.second);
			}
		}
	}
	template<bool bYIELD, class InfoMap>
	void SetRateTagList(InfoMap& kMap, TCHAR const* szTagName)
	{	// Based on BtS code repeated throughout the CvInfo classes
		if (gDLL->getXMLIFace()->SetToChildByTagName(GetXML(), szTagName))
		{
			int* piArray=NULL;
			int iValuesSet = (bYIELD ? SetYieldArray(&piArray) : SetCommerceArray(&piArray));
			for (int i = 0; i < iValuesSet; i++)
			{
				kMap.insert(i, piArray[i]);
			}
			delete[] piArray;
		}
	}
	template<typename MapType>
	void SetYieldList(MapType& kMap, TCHAR const* szTagName)
	{
		SetRateTagList<true>(kMap, szTagName);
	}
	template<typename MapType>
	void SetCommerceList(MapType& kMap, TCHAR const* szTagName)
	{
		SetRateTagList<false>(kMap, szTagName);
	}
	// </advc.003t>

private:
	FXml* m_pFXml;
	// keep a single schema cache, instead of loading the same schemas multiple times
	FXmlSchemaCache* m_pSchemaCache;
	static CvString szAssertMsg; // advc.006b
	// <advc.003k>
	class Data
	{
		bool bAssertMandatory; // advc.006b
		bool bEventsLoaded, bThroneRoomLoaded; // advc.003v
		bool bTrueStartsDataLoaded; // advc.tsl
		friend CvXMLLoadUtility;
	};
	//int m_iCurProgressStep; // Unused, remove it to make room.
	//ProgressCB m_pCBFxn;// Also unused, but have no other use for that memory, so:
	void* m_pDummy;
	Data* m; // additional members

	// <advc.006j> Helper struct for asserting bounds of enum values read from XML
	template<typename T, bool bENUM = enum_traits<T>::is_enum>
	struct InfoIDFromChild;
	template<typename T>
	struct InfoIDFromChild<T, false>
	{
		static void set(CvXMLLoadUtility& kUtil, T& tValue, TCHAR const* szName)
		{	// advc.xmldefault:
			kUtil.SetGlobalTypeFromChildXmlVal(static_cast<int&>(tValue), szName, true);
		}
	};
	template<typename T>
	struct InfoIDFromChild<T, true>
	{
		static void set(CvXMLLoadUtility& kUtil, T& tValue, TCHAR const* szName)
		{	// advc.xmldefault:
			int iValue = static_cast<int>(tValue); // Safe way to cast to int&
			kUtil.SetGlobalTypeFromChildXmlVal(iValue, szName, true);
			tValue = static_cast<T>(iValue);
			/*	If the upper bound is 0 here, then the value may need to be loaded
				in a later pass (readPass2 or readPass3). */
			FAssertInfoEnum(tValue);
		}
	}; // </advc.006j>

	// Still called, still has no effect:  // </advc.003k>
	void UpdateProgressCB(const char* szMessage=NULL);

	void SetGlobalStringArray(CvString** ppszString, char* szTagName, int* iNumVals, bool bUseEnum = false);
	void SetDiplomacyCommentTypes(CvString** ppszString, int* iNumVals);
	static int getGlobalEnumFromString(TCHAR const* szType); // advc
	static void handleUnknownTypeString(TCHAR const* szType); // advc
	//void MakeMaskFromString(unsigned int *puiMask, char* szMask); // advc.003j (unused)
	//void SetGlobalUnitScales(float& fLargeScale, float& fSmallScale, char const* szTagName); // advc.003j (unused)

	#ifdef _USRDLL
	template <class T>
	void SetGlobalDefine(const char* szDefineName, T*& piDefVal)
	{
		GC.getDefinesVarSystem()->GetValue(szDefineName, piDefVal); }
	// template which can handle all info classes
	// a dynamic value for the list size
	template <class T>
	void LoadGlobalClassInfo(std::vector<T*>& aInfos, const char* szFileRoot,
			const char* szFileDirectory, const char* szXmlPath, bool bTwoPass,
			CvCacheObject* (CvDLLUtilityIFaceBase::*pArgFunction)(TCHAR const*) = NULL);
	template <class T>
	void SetGlobalClassInfo(std::vector<T*>& aInfos, const char* szTagName, bool bTwoPass,
			bool bFinalCall = false); // advc.xmldefault
	#endif
	void SetDiplomacyInfo(std::vector<CvDiplomacyInfo*>& DiploInfos, const char* szTagName);
	void LoadDiplomacyInfo(std::vector<CvDiplomacyInfo*>& DiploInfos, const char* szFileRoot,
			const char* szFileDirectory, const char* szXmlPath,
			CvCacheObject* (CvDLLUtilityIFaceBase::*pArgFunction) (TCHAR const*));
	//
	// special cases of set class info which don't use the template because of extra code they have
	//
	void SetGlobalActionInfo();

	void SetGlobalAnimationPathInfo(CvAnimationPathInfo** ppAnimationPathInfo, char* szTagName, int* iNumVals);
	//void SetGameText(const char* szTextGroup, const char* szTagName);
	void SetGameText(const char* szTextGroup, const char* szTagName, const std::string& language_name); // K-Mod

	/*	<advc.006g> (The BtS code sometimes said "XML Error", sometimes "XML Load Error"
		not sure if that's meaningful, but I'm going to preserve it.)*/
	enum XMLErrorTypes
	{
		GENERAL_XML_ERROR,
		XML_LOAD_ERROR,
	};
	static void errorMessage(char const* szMessage, XMLErrorTypes eErrType = GENERAL_XML_ERROR);
	// </advc.006g>
	void logMsg(char* format, ...);
};

// Size 20 also seems OK, 28 definitely not, causes Wine to crash.
BOOST_STATIC_ASSERT(sizeof(CvXMLLoadUtility) == 16);

#ifdef _USRDLL
// inlines / templates ...

template <class T>
void CvXMLLoadUtility::InitList(T **ppList, int iListLen, T val)
{
	// <advc.xmldefault>
	if (*ppList != NULL) // Already initialized w/ default values
		return; // </advc.xmldefault>
	FAssertMsg(0 <= iListLen, "list size to allocate is less than 0");
	*ppList = new T[iListLen];
	for (int i=0; i < iListLen; i++)
		(*ppList)[i] = val;
}

/*	advc: All call locations call SetToParent after SetCommerce, so let's do that
	only once in a single place. */
template <class T>
int CvXMLLoadUtility::SetCommerceArray(T** ppbCommerce)
{
	int iSet = SetCommerce(ppbCommerce);
	gDLL->getXMLIFace()->SetToParent(m_pFXml);
	return iSet;
}

template <class T>
int CvXMLLoadUtility::SetCommerce(T** ppbCommerce)
{
	T *pbCommerce; // local pointer for the Commerce memory
	// Skip any comments and stop at the next value we might want
	if (!SkipToNextVal())
		return 0;

	int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
	InitList(ppbCommerce, NUM_COMMERCE_TYPES);
	pbCommerce = *ppbCommerce;
	if (iNumSibs > 0)
	{
		if (GetChildXmlVal(pbCommerce[0]))
		{
			FAssertMsg((iNumSibs <= NUM_COMMERCE_TYPES) , "For loop iterator is greater than array size");
			// loop through all the siblings, we start at 1 since we already have the first value
			for (int i = 1; i < iNumSibs; i++)
			{
				if (!GetNextXmlVal(pbCommerce[i]))
					break;
			}
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
	}
	return iNumSibs;
}
#endif // _USRDLL

#endif
