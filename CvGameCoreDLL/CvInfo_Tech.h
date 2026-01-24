#pragma once

#ifndef CV_INFO_TECH_H
#define CV_INFO_TECH_H

// advc.003x: Cut from CvInfos.h. Just CvTechInfo b/c I want to precompile this one.
class CvTechInfo : /* <advc.tag> */ public CvXMLInfo
{
	typedef CvXMLInfo base_t;
protected:
	void addElements(ElementList& kElements) const
	{
		base_t::addElements(kElements);
		kElements.addBool(NoFearForSafety, "NoFearForSafety"); // advc.500c
		kElements.addInt(BarbarianFreeTechModifier, "BarbarianFreeTechModifier"); // advc.301
	}
public:
	enum IntElementTypes
	{
		BarbarianFreeTechModifier = base_t::NUM_INT_ELEMENT_TYPES, // advc.301
		NUM_INT_ELEMENT_TYPES
	};
	int get(IntElementTypes e) const
	{
		return base_t::get(static_cast<base_t::IntElementTypes>(e));
	}
	enum BoolElementTypes
	{
		NoFearForSafety = base_t::NUM_BOOL_ELEMENT_TYPES, // advc.500c
		NUM_BOOL_ELEMENT_TYPES
	};
	PY_IS_ELEMENT(NoFearForSafety)
	bool get(BoolElementTypes e) const
	{
		return base_t::get(static_cast<base_t::BoolElementTypes>(e));
	}
	// </advc.tag>
	friend class CvXMLLoadUtility;
public: // advc: All the const functions are exposed to Python except those added by mods
	CvTechInfo();
	~CvTechInfo();

	int getAdvisorType() const { return m_iAdvisorType; }
	int getAIWeight() const { return m_iAIWeight; }
	int getAITradeModifier() const { return m_iAITradeModifier; }
	int getResearchCost() const { return m_iResearchCost; }
	int getAdvancedStartCost() const { return m_iAdvancedStartCost; }
	int getAdvancedStartCostIncrease() const { return m_iAdvancedStartCostIncrease; }
	EraTypes getEra() const { return (EraTypes)m_iEra; }
	int getTradeRoutes() const { return m_iTradeRoutes; }
	int getFeatureProductionModifier() const { return m_iFeatureProductionModifier; }
	int getWorkerSpeedModifier() const { return m_iWorkerSpeedModifier; }
	int getFirstFreeUnitClass() const { return m_iFirstFreeUnitClass; }
	int getHealth() const { return m_iHealth; }
	int getHappiness() const { return m_iHappiness; }
	int getFirstFreeTechs() const { return m_iFirstFreeTechs; }
	int getAssetValue() const { return m_iAssetValue; }
	int getPowerValue() const { return m_iPowerValue; }

	int getGridX() const { return m_iGridX; }
	int getGridY() const { return m_iGridY; }

	bool isRepeat() const { return m_bRepeat; }
	bool isTrade() const { return m_bTrade; }
	bool isDisable() const { return m_bDisable; }
	bool isGoodyTech() const { return m_bGoodyTech; }
	bool isExtraWaterSeeFrom() const { return m_bExtraWaterSeeFrom; }
	bool isMapCentering() const { return m_bMapCentering; }
	bool isMapVisible() const { return m_bMapVisible; }
	bool isMapTrading() const { return m_bMapTrading; }
	bool isTechTrading() const { return m_bTechTrading; }
	bool isGoldTrading() const { return m_bGoldTrading; }
	bool isOpenBordersTrading() const { return m_bOpenBordersTrading; }
	bool isDefensivePactTrading() const { return m_bDefensivePactTrading; }
	bool isPermanentAllianceTrading() const { return m_bPermanentAllianceTrading; }
	bool isVassalStateTrading() const { return m_bVassalStateTrading; }
	bool isBridgeBuilding() const { return m_bBridgeBuilding; }
	bool isIrrigation() const { return m_bIrrigation; }
	bool isIgnoreIrrigation() const { return m_bIgnoreIrrigation; }
	bool isWaterWork() const { return m_bWaterWork; }
	bool isRiverTrade() const { return m_bRiverTrade; }

	std::wstring getQuote() const;
	const TCHAR* getSound() const;
	const TCHAR* getSoundMP() const;

	// Array access:

	int getDomainExtraMoves(int i) const;
	int getFlavorValue(int i) const;
	// <advc.003t>
	int getNumOrTechPrereqs() const { return (int)m_aePrereqOrTechs.size(); }
	int getNumAndTechPrereqs() const { return (int)m_aePrereqAndTechs.size(); }
	TechTypes getPrereqOrTechs(int i) const
	{
		FAssertBounds(0, getNumOrTechPrereqs(), i);
		return m_aePrereqOrTechs[i];
	}
	TechTypes getPrereqAndTechs(int i) const
	{
		FAssertBounds(0, getNumAndTechPrereqs(), i);
		return m_aePrereqAndTechs[i];
	}
	int py_getPrereqOrTechs(int i) const;
	int py_getPrereqAndTechs(int i) const;
	// </advc.003t>
	// K-Mod, exposed to Python
	int getCommerceModifier(int i) const;
	int* getCommerceModifierArray() const;
	int getSpecialistExtraCommerce(int i) const;
	int* getSpecialistExtraCommerceArray() const;
	// K-Mod end
	bool isCommerceFlexible(int i) const;
	bool isTerrainTrade(int i) const;
	bool isAnyTerrainTrade() const { return (m_pbTerrainTrade != NULL); } // advc.003t

	#if ENABLE_XML_FILE_CACHE
	void read(FDataStreamBase* );
	void write(FDataStreamBase* );
	#endif
	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

protected:
	int m_iAdvisorType;
	int m_iAIWeight;
	int m_iAITradeModifier;
	int m_iResearchCost;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iEra;
	int m_iTradeRoutes;
	int m_iFeatureProductionModifier;
	int m_iWorkerSpeedModifier;
	int m_iFirstFreeUnitClass;
	int m_iHealth;
	int m_iHappiness;
	int m_iFirstFreeTechs;
	int m_iAssetValue;
	int m_iPowerValue;

	int m_iGridX;
	int m_iGridY;

	bool m_bRepeat;
	bool m_bTrade;
	bool m_bDisable;
	bool m_bGoodyTech;
	bool m_bExtraWaterSeeFrom;
	bool m_bMapCentering;
	bool m_bMapVisible;
	bool m_bMapTrading;
	bool m_bTechTrading;
	bool m_bGoldTrading;
	bool m_bOpenBordersTrading;
	bool m_bDefensivePactTrading;
	bool m_bPermanentAllianceTrading;
	bool m_bVassalStateTrading;
	bool m_bBridgeBuilding;
	bool m_bIrrigation;
	bool m_bIgnoreIrrigation;
	bool m_bWaterWork;
	bool m_bRiverTrade;

	CvString m_szQuoteKey;
	CvString m_szSound;
	CvString m_szSoundMP;

	int* m_piDomainExtraMoves;
	int* m_piFlavorValue;

	std::vector<TechTypes> m_aePrereqOrTechs; // advc.003t: was int*
	std::vector<TechTypes> m_aePrereqAndTechs; // advc.003t: was int*

	int* m_piCommerceModifier; // K-Mod
	int* m_piSpecialistExtraCommerce; // K-Mod
	bool* m_pbCommerceFlexible;
	bool* m_pbTerrainTrade;
};

#endif
