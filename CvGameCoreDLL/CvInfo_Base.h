#pragma once

#ifndef CV_INFO_BASE_H
#define CV_INFO_BASE_H

#include "CyInfoWrapper.h" // advc.003x
#include "CvInfo_EnumMap.h" // advc.enum

/*  advc.003x: Cut from CvInfos.h; to be precompiled.
	CvInfoBase, CvScalableInfo, CvHotkeyInfo */

#define ENABLE_XML_FILE_CACHE 0 // advc.003i

class CvXMLLoadUtility;

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvInfoBase
//
//  The base class for all info classes to inherit from.  This gives us
//	the base description and type strings
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvInfoBase /* advc.003e: */ : private boost::noncopyable
{
public: // All the const functions are exposed to Python
	CvInfoBase();
	CvInfoBase(CvInfoBase const& kOther); // advc.xmldefault
	/*	advc (note): There is a call location in the EXE according to Dependency Walker,
		but it might be unreachable: I'm not crashing when I remove the destructor. */
	DllExport virtual ~CvInfoBase() {}

	virtual void reset();

	bool isGraphicalOnly() const;

	DllExport TCHAR const* getType() const;
	bool isDefaultsType() const; // advc.xmldefault
	virtual TCHAR const* getButton() const;

	// for python wide string handling
	std::wstring pyGetTextKey() { return getTextKeyWide(); }
	std::wstring pyGetDescription() { return getDescription(0); }
	std::wstring pyGetDescriptionForm(uint uiForm) { return getDescription(uiForm); }
	std::wstring pyGetText() { return getText(); }
	std::wstring pyGetCivilopedia() { return getCivilopedia(); }
	std::wstring pyGetHelp() { return getHelp(); }
	std::wstring pyGetStrategy() { return getStrategy(); }

	DllExport wchar const* getTextKeyWide() const;
	DllExport wchar const* getDescription(uint uiForm = 0) const;
	// advc.137: Allow this to be overridden
	virtual CvWString getDescriptionInternal() const;
	DllExport wchar const* getText() const;
	wchar const* getCivilopedia() const;
	DllExport wchar const* getHelp() const;
	wchar const* getStrategy() const;

	bool isMatchForLink(std::wstring szLink, bool bKeysOnly) const;
	#if ENABLE_XML_FILE_CACHE
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
	#endif
	/*	Reads in a Cv...Info definition from XML
		param: pXML Pointer to the XML loading object
		returns: true if the definition was read successfully, false otherwise.
		(advc: Cut this comment from CvAnimationPathInfo) */
	virtual bool read(CvXMLLoadUtility* pXML);
	virtual bool readPass2(CvXMLLoadUtility* pXML)
	{
		FErrorMsg("readPass2 has not been overridden");
		return false;
	}
	virtual bool readPass3()
	{
		FErrorMsg("readPass3 has not been overridden");
		return false;
	}

protected:
	/*	advc.003k (caveat): Changing the memory layout of this class is probably
		not safe b/c it's a base class of CvArtInfoScalableAsset, which employs
		multiple inheritance and gets cast unsafely in the EXE. */
	bool m_bGraphicalOnly;

	CvString m_szType;
	CvString m_szButton; // Used for Infos that don't require an ArtAssetInfo
	CvWString m_szTextKey;
	CvWString m_szCivilopediaKey;
	CvWString m_szHelpKey;
	CvWString m_szStrategyKey;

	// translated text
	std::vector<CvString> m_aszExtraXMLforPass3;
	mutable std::vector<CvWString> m_aCachedDescriptions;
	mutable CvWString m_szCachedText;
	mutable CvWString m_szCachedHelp;
	mutable CvWString m_szCachedStrategy;
	mutable CvWString m_szCachedCivilopedia;

	//bool doneReadingXML(CvXMLLoadUtility* pXML); // advc.003j: Never had an implementation
};

// holds the scale for scalable objects
class CvScalableInfo /* advc.003e: */ : private boost::noncopyable
{
public:
	// advc.003k (note): Used to be exported, may have been inlined in the EXE.
	CvScalableInfo() : m_fScale(1.0f), m_fInterfaceScale(1.0f) {}

	DllExport float getScale() const; // Exposed to Python

	// the scale of the unit appearing in the interface screens
	DllExport float getInterfaceScale() const; // Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected: // advc.003k (caveat): Probably not safe to rearrange or remove these
	float m_fScale;
	float m_fInterfaceScale; 
};
BOOST_STATIC_ASSERT(sizeof(CvScalableInfo) == 8); // advc.003k

/*	advc.tag: Abstract class that allows simple XML elements
	(i.e. w/o child elements) to be added and accessed through enum values.
	For elements that map an enum key to a value, see CvInfo_EnumMap.h instead. */
class CvXMLInfo : public CvInfoBase
{
public:
	// To be extended by derived classes (see CvImprovementInfo for an example)
	enum IntElementTypes
	{
		NUM_INT_ELEMENT_TYPES
	};
	enum BoolElementTypes
	{
		NUM_BOOL_ELEMENT_TYPES
	};
	short get(IntElementTypes e) const
	{
		FAssertBounds(0, m_aiData.size(), e);
		return m_aiData[e];
	}
	bool get(BoolElementTypes e) const
	{
		FAssertBounds(0, m_abData.size(), e);
		return m_abData[e];
	}
	bool read(CvXMLLoadUtility* pXML);
	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
	#endif

protected:
	enum ElementDataType
	{
		INT_ELEMENT,
		BOOL_ELEMENT,
	};
	template<typename ContentType>
	class XMLElement
	{
	public:
		XMLElement(int iID, char const* szName)
		:	m_iID(iID), m_sName(szName), m_bMandatory(true),
			m_defaultValue(0)
		{}
		XMLElement(int iID, CvString szName, ContentType defaultValue)
		:	m_iID(iID), m_sName(szName), m_bMandatory(false),
			m_defaultValue(defaultValue)
		{}
		virtual ~XMLElement() {};
		int getID() const { return m_iID; }
		CvString getName() const { return m_sName; }
		ContentType getDefaultValue() const
		{
			return m_defaultValue;
		}
		bool isMandatory() const { return m_bMandatory; }
	private:
		CvString m_sName;
		int m_iID;
		ContentType m_defaultValue;
		bool m_bMandatory;
	};
	typedef XMLElement<int> IntElement;
	typedef XMLElement<bool> BoolElement;

	class ElementList
	{
	public:
		~ElementList()
		{
			for (size_t i = 0; i < m_intElements.size(); i++)
				delete m_intElements[i];
			for (size_t i = 0; i < m_boolElements.size(); i++)
				delete m_boolElements[i];
		}
		void addMandatoryInt(int iID, char const* szName)
		{
			m_intElements.push_back(new IntElement(iID, szName));
		}
		void addInt(int iID, char const* szName, int iDefault = 0)
		{
			m_intElements.push_back(new IntElement(iID, szName, iDefault));
		}
		void addMandatoryBool(int iID, char const* szName)
		{
			m_boolElements.push_back(new BoolElement(iID, szName));
		}
		void addBool(int iID, char const* szName, bool bDefault = false)
		{
			m_boolElements.push_back(new BoolElement(iID, szName, bDefault));
		}
		int numIntElements() const { return (int)m_intElements.size(); }
		int numBoolElements() const { return (int)m_boolElements.size(); }
		IntElement const& intElementAt(int iPos) const
		{
			return *m_intElements.at(iPos);
		}
		BoolElement const& boolElementAt(int iPos) const
		{
			return *m_boolElements.at(iPos);
		}
	private:
		std::vector<IntElement*> m_intElements;
		std::vector<BoolElement*> m_boolElements;
	};

	/*	Derived classes that extend any of the element type enums need to override this.
		The overridden function needs to call the base function and then append its
		own elements to kElements. */
	virtual void addElements(ElementList& kElements) const
	{
		// Could add elements common to all info classes here
	}
	// Allow derived classes to overwrite data (but don't expose the data structures)
	void set(IntElementTypes e, int iNewValue)
	{
		FAssertBounds(0, m_aiData.size(), e);
		m_aiData[e] = safeIntCast<short>(iNewValue);
	}
	void set(BoolElementTypes e, bool bNewValue)
	{
		FAssertBounds(0, m_abData.size(), e);
		m_abData[e] = bNewValue;
	}

private:
	std::vector<short> m_aiData;
	std::vector<bool> m_abData; // Should use a dynamic bitfield internally
};

/*	advc.tag: (To expose a tag to Python, this macro needs to be called in the
	public section of the concrete XML info class that defines the tag, and a
	py_get... def needs to be added in the appropriate CyInfoPythonInterface*.cpp.) */
#define PY_GET_ELEMENT(TagName) \
	private: \
		FRIEND_CY_INFO_PYTHON_INTERFACE; \
		int py_get##TagName() const \
		{ \
			return get(TagName); \
		} \
	public:
// advc.tag: (See above; this one is for BoolElements.)
#define PY_IS_ELEMENT(TagName) \
	private: \
		FRIEND_CY_INFO_PYTHON_INTERFACE; \
		bool py_is##TagName() const \
		{ \
			return get(TagName); \
		} \
	public:

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvHotkeyInfo
//  holds the hotkey info for an info class
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHotkeyInfo : public /* <advc.tag> */ CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	// All unused here, just to exemplify the pattern.
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
	}
public:
	enum IntElementTypes
	{
		NUM_INT_ELEMENT_TYPES = base_t::NUM_BOOL_ELEMENT_TYPES
	};
	enum BoolElementTypes
	{
		NUM_BOOL_ELEMENT_TYPES = base_t::NUM_BOOL_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	}
	int get(BoolElementTypes e) const
	{
		return base_t::get(static_cast<base_t::BoolElementTypes>(e));
	} // </advc.tag>

	CvHotkeyInfo();

	bool read(CvXMLLoadUtility* pXML);
	#if ENABLE_XML_FILE_CACHE
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
	#endif
	int getActionInfoIndex() const;
	void setActionInfoIndex(int i);

	int getHotKeyVal() const;
	int getHotKeyPriority() const;
	int getHotKeyValAlt() const;
	int getHotKeyPriorityAlt() const;
	int getOrderPriority() const;

	bool isAltDown() const;
	bool isShiftDown() const;
	bool isCtrlDown() const;
	bool isAltDownAlt() const;
	bool isShiftDownAlt() const;
	bool isCtrlDownAlt() const;

	const TCHAR* getHotKey() const; // Exposed to Python

	std::wstring getHotKeyDescription() const;
	void setHotKeyDescription(const wchar* szHotKeyDescKey, const wchar* szHotKeyAltDescKey,
			const wchar* szHotKeyString);
	std::wstring getHotKeyShortDesc() const; // advc.154

protected:
	int m_iActionInfoIndex;
	int m_iHotKeyVal;
	int m_iHotKeyPriority;
	int m_iHotKeyValAlt;
	int m_iHotKeyPriorityAlt;
	int m_iOrderPriority;

	bool m_bAltDown;
	bool m_bShiftDown;
	bool m_bCtrlDown;
	bool m_bAltDownAlt;
	bool m_bShiftDownAlt;
	bool m_bCtrlDownAlt;

	CvString m_szHotKey;
	/*	advc (tbd.?): Caching these seems like a bad tradeoff; could generate
		them as needed. See the xml_reader branch of WtP. */
	CvWString m_szHotKeyDescriptionKey;
	CvWString m_szHotKeyAltDescriptionKey;
	CvWString m_szHotKeyString;
};

#endif
