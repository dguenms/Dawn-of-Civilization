#pragma once

//  $Header:
//------------------------------------------------------------------------------------------------
//
//  FILE:    CvInfos.h
//
//  PURPOSE: All Civ4 info classes and the base class for them
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------
#ifndef CV_INFO_H
#define CV_INFO_H

#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class
#pragma warning( disable: 4127 )

class CvXMLLoadUtility;

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvInfoBase
//
//  DESC:   The base class for all info classes to inherit from.  This gives us
//			the base description and type strings
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	DllExport CvInfoBase();
	DllExport virtual ~CvInfoBase();

	virtual void reset();

	DllExport bool isGraphicalOnly() const;										// Exposed to Python

	DllExport const TCHAR* getType() const;										// Exposed to Python
	virtual const TCHAR* getButton() const;					// Exposed to Python

	// for python wide string handling
	std::wstring pyGetTextKey() { return getTextKeyWide(); }						// Exposed to Python
	std::wstring pyGetDescription() { return getDescription(0); }					// Exposed to Python
	std::wstring pyGetDescriptionForm(uint uiForm) { return getDescription(uiForm); }	// Exposed to Python
	std::wstring pyGetText() { return getText(); }									// Exposed to Python
	std::wstring pyGetCivilopedia() { return getCivilopedia(); }					// Exposed to Python
	std::wstring pyGetHelp() { return getHelp(); }									// Exposed to Python
	std::wstring pyGetStrategy() { return getStrategy(); }							// Exposed to Python

	DllExport const wchar* getTextKeyWide() const;
	DllExport const wchar* getDescription(uint uiForm = 0) const;
	DllExport const wchar* getText() const;
	const wchar* getCivilopedia() const;
	DllExport const wchar* getHelp() const;		
	const wchar* getStrategy() const;	

	bool isMatchForLink(std::wstring szLink, bool bKeysOnly) const;

	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

	virtual bool read(CvXMLLoadUtility* pXML);
	virtual bool readPass2(CvXMLLoadUtility* pXML) { pXML; FAssertMsg(false, "Override this"); return false; }
	virtual bool readPass3() { FAssertMsg(false, "Override this"); return false; }

protected:

	bool doneReadingXML(CvXMLLoadUtility* pXML);

	bool m_bGraphicalOnly;

	CvString m_szType;
	CvString m_szButton;				// Used for Infos that don't require an ArtAssetInfo
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
};

//
// holds the scale for scalable objects
//
class CvScalableInfo
{
public:

	DllExport CvScalableInfo() : m_fScale(1.0f), m_fInterfaceScale(1.0f) { }

	DllExport float getScale() const;
	DllExport void setScale(float fScale);

	DllExport float getInterfaceScale() const;
	DllExport void setInterfaceScale(float fInterfaceScale);

	bool read(CvXMLLoadUtility* pXML);

protected:

	float m_fScale;			// Exposed to Python
	float m_fInterfaceScale;	//!< the scale of the unit appearing in the interface screens
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  CLASS:      CvHotkeyInfo
//!  \brief			holds the hotkey info for an info class
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHotkeyInfo : public CvInfoBase
{
public:
	//constructor
	DllExport CvHotkeyInfo();
	//destructor
	DllExport virtual ~CvHotkeyInfo();

	bool read(CvXMLLoadUtility* pXML);

	DllExport virtual void read(FDataStreamBase* pStream);
	DllExport virtual void write(FDataStreamBase* pStream);

	DllExport int getActionInfoIndex() const;
	DllExport void setActionInfoIndex(int i);

	DllExport int getHotKeyVal() const;
	DllExport void setHotKeyVal(int i);
	DllExport int getHotKeyPriority() const;
	DllExport void setHotKeyPriority(int i);
	DllExport int getHotKeyValAlt() const;
	DllExport void setHotKeyValAlt(int i);
	DllExport int getHotKeyPriorityAlt() const;
	DllExport void setHotKeyPriorityAlt(int i);
	DllExport int getOrderPriority() const;
	DllExport void setOrderPriority(int i);

	DllExport bool isAltDown() const;
	DllExport void setAltDown(bool b);
	DllExport bool isShiftDown() const;
	DllExport void setShiftDown(bool b);
	DllExport bool isCtrlDown() const;
	DllExport void setCtrlDown(bool b);
	DllExport bool isAltDownAlt() const;
	DllExport void setAltDownAlt(bool b);
	DllExport bool isShiftDownAlt() const;
	DllExport void setShiftDownAlt(bool b);
	DllExport bool isCtrlDownAlt() const;
	DllExport void setCtrlDownAlt(bool b);

	DllExport const TCHAR* getHotKey() const;			// Exposed to Python
	DllExport void setHotKey(const TCHAR* szVal);

	DllExport std::wstring getHotKeyDescription() const;
	DllExport void setHotKeyDescription(const wchar* szHotKeyDescKey, const wchar* szHotKeyAltDescKey, const wchar* szHotKeyString);

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
	CvWString m_szHotKeyDescriptionKey;
	CvWString m_szHotKeyAltDescriptionKey;
	CvWString m_szHotKeyString;

};

class CvDiplomacyResponse
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvDiplomacyResponse();
	DllExport virtual ~CvDiplomacyResponse();

	DllExport int getNumDiplomacyText();
	DllExport void setNumDiplomacyText(int i);

	DllExport bool getCivilizationTypes(int i);
	DllExport bool* getCivilizationTypes() const;
	DllExport void setCivilizationTypes(int i, bool bVal);

	DllExport bool getLeaderHeadTypes(int i);
	DllExport bool* getLeaderHeadTypes() const;
	DllExport void setLeaderHeadTypes(int i, bool bVal);

	DllExport bool getAttitudeTypes(int i) const;
	DllExport bool* getAttitudeTypes() const;
	DllExport void setAttitudeTypes(int i, bool bVal);

	DllExport bool getDiplomacyPowerTypes(int i);
	DllExport bool* getDiplomacyPowerTypes() const;
	DllExport void setDiplomacyPowerTypes(int i, bool bVal);

	DllExport const TCHAR* getDiplomacyText(int i) const;
	DllExport const CvString* getDiplomacyText() const;
	DllExport void setDiplomacyText(int i, CvString szText);

	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);

protected:
	int m_iNumDiplomacyText;
	bool* m_pbCivilizationTypes;
	bool* m_pbLeaderHeadTypes;
	bool* m_pbAttitudeTypes;
	bool* m_pbDiplomacyPowerTypes;
	CvString* m_paszDiplomacyText;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialistInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialistInfo : public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialistInfo();
	virtual ~CvSpecialistInfo();

	int getGreatPeopleUnitClass() const;		// Exposed to Python
	int getGreatPeopleRateChange() const;		// Exposed to Python
	int getMissionType() const;							// Exposed to Python
	void setMissionType(int iNewType);
	int getExperience() const;				// Exposed to Python

	bool isVisible() const;				// Exposed to Python

	// Arrays

	int getYieldChange(int i) const;		// Exposed to Python
	const int* getYieldChangeArray() const;		// Exposed to Python - For Moose - CvWidgetData
	int getCommerceChange(int i) const;		// Exposed to Python
	int getFlavorValue(int i) const;		// Exposed to Python

	const TCHAR* getTexture() const;				// Exposed to Python
	void setTexture(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iGreatPeopleUnitClass;		// Exposed to Python
	int m_iGreatPeopleRateChange;		// Exposed to Python
	int m_iMissionType;
	int m_iExperience;

	bool m_bVisible;				// Exposed to Python

	CvString m_szTexture;

	// Arrays

	int* m_piYieldChange;
	int* m_piCommerceChange;
	int* m_piFlavorValue;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTechInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTechInfo : public CvInfoBase
{

friend class CvXMLLoadUtility;

//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTechInfo();
	virtual ~CvTechInfo();

	int getAdvisorType() const;						// Exposed to Python
	int getAIWeight() const;							// Exposed to Python
	int getAITradeModifier() const;				// Exposed to Python
	int getResearchCost() const;					// Exposed to Python
	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python
	int getEra() const;										// Exposed to Python
	int getTradeRoutes() const;						// Exposed to Python
	int getFeatureProductionModifier() const;	// Exposed to Python
	int getWorkerSpeedModifier() const;		// Exposed to Python
	int getFirstFreeUnitClass() const;		// Exposed to Python
	int getHealth() const;								// Exposed to Python
	int getHappiness() const;							// Exposed to Python
	int getFirstFreeTechs() const;				// Exposed to Python
	int getAssetValue() const;						// Exposed to Python
	int getPowerValue() const;						// Exposed to Python

	int getGridX() const;									// Exposed to Python
	int getGridY() const;									// Exposed to Python

	bool isRepeat() const;								// Exposed to Python
	bool isTrade() const;									// Exposed to Python
	bool isDisable() const;								// Exposed to Python
	bool isGoodyTech() const;							// Exposed to Python
	bool isExtraWaterSeeFrom() const;			// Exposed to Python
	bool isMapCentering() const;					// Exposed to Python
	bool isMapVisible() const;						// Exposed to Python
	bool isMapTrading() const;						// Exposed to Python
	bool isTechTrading() const;						// Exposed to Python
	bool isGoldTrading() const;						// Exposed to Python
	bool isOpenBordersTrading() const;		// Exposed to Python
	bool isDefensivePactTrading() const;	// Exposed to Python
	bool isPermanentAllianceTrading() const;	// Exposed to Python
	bool isVassalStateTrading() const;	// Exposed to Python
	bool isBridgeBuilding() const;				// Exposed to Python
	bool isIrrigation() const;						// Exposed to Python
	bool isIgnoreIrrigation() const;			// Exposed to Python
	bool isWaterWork() const;							// Exposed to Python
	bool isRiverTrade() const;							// Exposed to Python

	std::wstring getQuote() const;	// Exposed to Python
	void setQuoteKey(const TCHAR* szVal);
	const TCHAR* getSound() const;				// Exposed to Python
	void setSound(const TCHAR* szVal);
	const TCHAR* getSoundMP() const;			// Exposed to Python
	void setSoundMP(const TCHAR* szVal);

	// Arrays

	int getDomainExtraMoves(int i) const;	// Exposed to Python
	int getFlavorValue(int i) const;			// Exposed to Python
	int getPrereqOrTechs(int i) const;		// Exposed to Python
	int getPrereqAndTechs(int i) const;		// Exposed to Python

	bool isCommerceFlexible(int i) const;	// Exposed to Python
	bool isTerrainTrade(int i) const;			// Exposed to Python

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

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

	// Arrays

	int* m_piDomainExtraMoves;
	int* m_piFlavorValue;

	int* m_piPrereqOrTechs;
	int* m_piPrereqAndTechs;

	bool* m_pbCommerceFlexible;
	bool* m_pbTerrainTrade;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPromotionInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPromotionInfo :	public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	CvPromotionInfo();
	virtual ~CvPromotionInfo();

	int getLayerAnimationPath() const;
	int getPrereqPromotion() const;				// Exposed to Python
	void setPrereqPromotion(int i);				// Exposed to Python
	int getPrereqOrPromotion1() const;				// Exposed to Python
	void setPrereqOrPromotion1(int i);				// Exposed to Python
	int getPrereqOrPromotion2() const;				// Exposed to Python
	void setPrereqOrPromotion2(int i);				// Exposed to Python

	int getTechPrereq() const;				// Exposed to Python
	int getStateReligionPrereq() const;				// Exposed to Python
	int getVisibilityChange() const;				// Exposed to Python
	int getMovesChange() const;				// Exposed to Python
	int getMoveDiscountChange() const;				// Exposed to Python
	int getAirRangeChange() const;				// Exposed to Python
	int getInterceptChange() const;				// Exposed to Python
	int getEvasionChange() const;				// Exposed to Python
	int getWithdrawalChange() const;				// Exposed to Python
	int getCargoChange() const;				// Exposed to Python
	int getCollateralDamageChange() const;				// Exposed to Python
	int getBombardRateChange() const;				// Exposed to Python
	int getFirstStrikesChange() const;				// Exposed to Python
	int getChanceFirstStrikesChange() const;				// Exposed to Python
	int getEnemyHealChange() const;				// Exposed to Python
	int getNeutralHealChange() const;				// Exposed to Python
	int getFriendlyHealChange() const;				// Exposed to Python
	int getSameTileHealChange() const;				// Exposed to Python
	int getAdjacentTileHealChange() const;				// Exposed to Python
	int getCombatPercent() const;				// Exposed to Python
	int getCityAttackPercent() const;				// Exposed to Python
	int getCityDefensePercent() const;				// Exposed to Python
	int getHillsAttackPercent() const;				// Exposed to Python
	int getHillsDefensePercent() const;				// Exposed to Python
	int getCommandType() const;									// Exposed to Python
	void setCommandType(int iNewType);

	int getRevoltProtection() const;				// Exposed to Python
	int getCollateralDamageProtection() const;				// Exposed to Python
	int getPillageChange() const;				// Exposed to Python
	int getUpgradeDiscount() const;				// Exposed to Python
	int getExperiencePercent() const;				// Exposed to Python
	int getKamikazePercent() const;				// Exposed to Python

	bool isLeader() const;				// Exposed to Python
	bool isBlitz() const;				// Exposed to Python
	bool isAmphib() const;				// Exposed to Python
	bool isRiver() const;				// Exposed to Python
	bool isEnemyRoute() const;				// Exposed to Python
	bool isAlwaysHeal() const;				// Exposed to Python
	bool isHillsDoubleMove() const;				// Exposed to Python
	bool isImmuneToFirstStrikes() const;				// Exposed to Python

	const TCHAR* getSound() const;				// Exposed to Python
	void setSound(const TCHAR* szVal);

	// Arrays

	int getTerrainAttackPercent(int i) const;				// Exposed to Python
	int getTerrainDefensePercent(int i) const;				// Exposed to Python
	int getFeatureAttackPercent(int i) const;				// Exposed to Python
	int getFeatureDefensePercent(int i) const;				// Exposed to Python
	int getUnitCombatModifierPercent(int i) const;				// Exposed to Python
	int getDomainModifierPercent(int i) const;				// Exposed to Python

	bool getTerrainDoubleMove(int i) const;				// Exposed to Python
	bool getFeatureDoubleMove(int i) const;				// Exposed to Python
	bool getUnitCombat(int i) const;				// Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iLayerAnimationPath;
	int m_iPrereqPromotion;
	int m_iPrereqOrPromotion1;
	int m_iPrereqOrPromotion2;

	int m_iTechPrereq;							
	int m_iStateReligionPrereq;							
	int m_iVisibilityChange;					
	int m_iMovesChange;						
	int m_iMoveDiscountChange;
	int m_iAirRangeChange;
	int m_iInterceptChange;
	int m_iEvasionChange;
	int m_iWithdrawalChange;				
	int m_iCargoChange;				
	int m_iCollateralDamageChange;	
	int m_iBombardRateChange;			
	int m_iFirstStrikesChange;				
	int m_iChanceFirstStrikesChange;	
	int m_iEnemyHealChange;				
	int m_iNeutralHealChange;				
	int m_iFriendlyHealChange;				
	int m_iSameTileHealChange;			
	int m_iAdjacentTileHealChange;		
	int m_iCombatPercent;
	int m_iCityAttackPercent;
	int m_iCityDefensePercent;
	int m_iHillsAttackPercent;
	int m_iHillsDefensePercent;
	int m_iCommandType;
	int m_iRevoltProtection;
	int m_iCollateralDamageProtection;
	int m_iPillageChange;
	int m_iUpgradeDiscount;
	int m_iExperiencePercent;
	int m_iKamikazePercent;

	bool m_bLeader;
	bool m_bBlitz;									
	bool m_bAmphib;								
	bool m_bRiver;									
	bool m_bEnemyRoute;						
	bool m_bAlwaysHeal;						
	bool m_bHillsDoubleMove;				
	bool m_bImmuneToFirstStrikes;				

	CvString m_szSound;

	// Arrays

	int* m_piTerrainAttackPercent;
	int* m_piTerrainDefensePercent;
	int* m_piFeatureAttackPercent;
	int* m_piFeatureDefensePercent;
	int* m_piUnitCombatModifierPercent;
	int* m_piDomainModifierPercent;

	bool* m_pbTerrainDoubleMove;
	bool* m_pbFeatureDoubleMove;
	bool* m_pbUnitCombat;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvMissionInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMissionInfo : public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvMissionInfo();
	DllExport virtual ~CvMissionInfo();

	DllExport int getTime() const;								// Exposed to Python

	DllExport bool isSound() const;								// Exposed to Python
	DllExport bool isTarget() const;							// Exposed to Python
	DllExport bool isBuild() const;								// Exposed to Python
	DllExport bool getVisible() const;						// Exposed to Python
	DllExport EntityEventTypes getEntityEvent() const;

	DllExport const TCHAR* getWaypoint() const;		// effect type, Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iTime;

	bool m_bSound;
	bool m_bTarget;
	bool m_bBuild;
	bool m_bVisible;
	EntityEventTypes m_eEntityEvent;

	CvString m_szWaypoint;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvControlInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvControlInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvControlInfo();
	DllExport virtual ~CvControlInfo();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCommandInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCommandInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvCommandInfo();
	DllExport virtual ~CvCommandInfo();

	DllExport int getAutomate() const;
	DllExport void setAutomate(int i);

	DllExport bool getConfirmCommand() const;
	DllExport bool getVisible() const;
	DllExport bool getAll() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	int m_iAutomate;

	bool m_bConfirmCommand;
	bool m_bVisible;
	bool m_bAll;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAutomateInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAutomateInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvAutomateInfo();
	DllExport virtual ~CvAutomateInfo();

	DllExport int getCommand() const;
	DllExport void setCommand(int i);
	DllExport int getAutomate() const;
	DllExport void setAutomate(int i);

	DllExport bool getConfirmCommand() const;
	DllExport void setConfirmCommand(bool bVal);
	DllExport bool getVisible() const;
	DllExport void setVisible(bool bVal);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	int m_iCommand;
	int m_iAutomate;

	bool m_bConfirmCommand;
	bool m_bVisible;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvActionInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvActionInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvActionInfo();
	DllExport virtual ~CvActionInfo();

	DllExport int getMissionData() const;				// Exposed to Python
	DllExport int getCommandData() const;				// Exposed to Python

	DllExport int getAutomateType() const;
	DllExport int getInterfaceModeType() const;				// Exposed to Python
	DllExport int getMissionType() const;				// Exposed to Python
	DllExport int getCommandType() const;				// Exposed to Python
	DllExport int getControlType() const;				// Exposed to Python
	DllExport int getOriginalIndex() const;
	DllExport void setOriginalIndex(int i);

	DllExport bool isConfirmCommand() const;				// Exposed to Python
	DllExport bool isVisible() const;				// Exposed to Python
	DllExport ActionSubTypes getSubType() const;
	DllExport void setSubType(ActionSubTypes eSubType);

	// functions to replace the CvInfoBase calls
	DllExport const TCHAR* getType() const;
	DllExport const wchar* getDescription() const;
	DllExport const wchar* getCivilopedia() const;
	DllExport const wchar* getHelp() const;
	DllExport const wchar* getStrategy() const;
	DllExport virtual const TCHAR* getButton() const;
	DllExport const wchar* getTextKeyWide() const;

	// functions to replace the CvHotkey calls
	DllExport int getActionInfoIndex() const;
	DllExport int getHotKeyVal() const;
	DllExport int getHotKeyPriority() const;
	DllExport int getHotKeyValAlt() const;
	DllExport int getHotKeyPriorityAlt() const;
	DllExport int getOrderPriority() const;

	DllExport bool isAltDown() const;
	DllExport bool isShiftDown() const;
	DllExport bool isCtrlDown() const;
	DllExport bool isAltDownAlt() const;
	DllExport bool isShiftDownAlt() const;
	DllExport bool isCtrlDownAlt() const;

	DllExport const TCHAR* getHotKey() const;			// Exposed to Python

	DllExport std::wstring getHotKeyDescription() const;	// Exposed to Python

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iOriginalIndex;
	ActionSubTypes m_eSubType;

private:
	CvHotkeyInfo* getHotkeyInfo() const;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUnitInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoUnit;
class CvUnitInfo : public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	CvUnitInfo();
	virtual ~CvUnitInfo();

	int getAIWeight() const;				// Exposed to Python
	int getProductionCost() const;				// Exposed to Python
	int getHurryCostModifier() const;				// Exposed to Python
	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python
	int getMinAreaSize() const;				// Exposed to Python
	int getMoves() const;				// Exposed to Python
	int getAirRange() const;				// Exposed to Python
	int getAirUnitCap() const;				// Exposed to Python
	int getDropRange() const;				// Exposed to Python
	int getNukeRange() const;				// Exposed to Python
	int getWorkRate() const;				// Exposed to Python
	int getBaseDiscover() const;		// Exposed to Python
	int getDiscoverMultiplier() const;		// Exposed to Python
	int getBaseHurry() const;				// Exposed to Python
	int getHurryMultiplier() const;				// Exposed to Python
	int getBaseTrade() const;				// Exposed to Python
	int getTradeMultiplier() const;				// Exposed to Python
	int getGreatWorkCulture() const;				// Exposed to Python
	int getEspionagePoints() const;				// Exposed to Python
	int getCombat() const;				// Exposed to Python
	void setCombat(int iNum);				// Exposed to Python
	int getCombatLimit() const;				// Exposed to Python
	int getAirCombat() const;				// Exposed to Python
	int getAirCombatLimit() const;				// Exposed to Python
	int getXPValueAttack() const;				// Exposed to Python
	int getXPValueDefense() const;				// Exposed to Python
	int getFirstStrikes() const;				// Exposed to Python
	int getChanceFirstStrikes() const;				// Exposed to Python
	int getInterceptionProbability() const;		// Exposed to Python
	int getEvasionProbability() const;				// Exposed to Python
	int getWithdrawalProbability() const;			// Exposed to Python
	int getCollateralDamage() const;					// Exposed to Python
	int getCollateralDamageLimit() const;			// Exposed to Python
	int getCollateralDamageMaxUnits() const;	// Exposed to Python
	int getCityAttackModifier() const;				// Exposed to Python
	int getCityDefenseModifier() const;				// Exposed to Python
	int getAnimalCombatModifier() const;			// Exposed to Python
	int getHillsAttackModifier() const;			// Exposed to Python
	int getHillsDefenseModifier() const;			// Exposed to Python
	int getBombRate() const;									// Exposed to Python
	int getBombardRate() const;								// Exposed to Python
	int getSpecialCargo() const;							// Exposed to Python
	int getDomainCargo() const;								// Exposed to Python

	int getCargoSpace() const;								// Exposed to Python
	int getConscriptionValue() const;					// Exposed to Python
	int getCultureGarrisonValue() const;			// Exposed to Python
	int getExtraCost() const;									// Exposed to Python
	int getAssetValue() const;								// Exposed to Python
	int getPowerValue() const;								// Exposed to Python
	int getUnitClassType() const;							// Exposed to Python
	int getSpecialUnitType() const;						// Exposed to Python
	int getUnitCaptureClassType() const;			// Exposed to Python
	int getUnitCombatType() const;						// Exposed to Python
	int getDomainType() const;								// Exposed to Python
	int getDefaultUnitAIType() const;					// Exposed to Python
	int getInvisibleType() const;							// Exposed to Python
	int getSeeInvisibleType(int i) const;					// Exposed to Python
	int getNumSeeInvisibleTypes() const;					// Exposed to Python
	int getAdvisorType() const;								// Exposed to Python
	int getHolyCity() const;									// Exposed to Python
	int getReligionType() const;							// Exposed to Python
	int getStateReligion() const;							// Exposed to Python
	int getPrereqReligion() const;						// Exposed to Python
	int getPrereqCorporation() const;						// Exposed to Python
	int getPrereqBuilding() const;						// Exposed to Python
	int getPrereqAndTech() const;							// Exposed to Python
	int getPrereqAndBonus() const;						// Exposed to Python
	int getGroupSize() const;									// Exposed to Python - the initial number of individuals in the unit group
	int getGroupDefinitions() const;					// Exposed to Python - the number of UnitMeshGroups for this unit
	int getMeleeWaveSize() const;							// Exposed to Python
	int getRangedWaveSize() const;						// Exposed to Python
	int getNumUnitNames() const;							// Exposed to Python
	int getCommandType() const;								// Exposed to Python
	void setCommandType(int iNewType);

	bool isAnimal() const;				// Exposed to Python
	bool isFoodProduction() const;				// Exposed to Python
	bool isNoBadGoodies() const;				// Exposed to Python
	bool isOnlyDefensive() const;				// Exposed to Python
	bool isNoCapture() const;				// Exposed to Python
	bool isQuickCombat() const;				// Exposed to Python
	bool isRivalTerritory() const;				// Exposed to Python
	bool isMilitaryHappiness() const;				// Exposed to Python
	bool isMilitarySupport() const;				// Exposed to Python
	bool isMilitaryProduction() const;				// Exposed to Python
	bool isPillage() const;				// Exposed to Python
	bool isSpy() const;				// Exposed to Python
	bool isSabotage() const;				// Exposed to Python
	bool isDestroy() const;				// Exposed to Python
	bool isStealPlans() const;				// Exposed to Python
	bool isInvestigate() const;				// Exposed to Python
	bool isCounterSpy() const;				// Exposed to Python
	bool isFound() const;				// Exposed to Python
	bool isGoldenAge() const;				// Exposed to Python
	bool isInvisible() const;				// Exposed to Python
	void setInvisible(bool bEnable) ;			// Exposed to Python
	bool isFirstStrikeImmune() const;				// Exposed to Python
	bool isNoDefensiveBonus() const;				// Exposed to Python
	bool isIgnoreBuildingDefense() const;				// Exposed to Python
	bool isCanMoveImpassable() const;				// Exposed to Python
	bool isCanMoveAllTerrain() const;				// Exposed to Python
	bool isFlatMovementCost() const;				// Exposed to Python
	bool isIgnoreTerrainCost() const;				// Exposed to Python
	bool isNukeImmune() const;				// Exposed to Python
	bool isPrereqBonuses() const;				// Exposed to Python
	bool isPrereqReligion() const;				// Exposed to Python
	bool isMechUnit() const;							// Exposed to Python
	bool isRenderBelowWater() const;			// Exposed to Python
	bool isRenderAlways() const;			// Exposed to Python
	bool isSuicide() const;			// Exposed to Python
	bool isLineOfSight() const;			// Exposed to Python
	bool isHiddenNationality() const;			// Exposed to Python
	bool isAlwaysHostile() const;			// Exposed to Python
	bool isNoRevealMap() const;			// Exposed to Python

	float getUnitMaxSpeed() const;					// Exposed to Python
	float getUnitPadTime() const;					// Exposed to Python

	// Arrays

	int getPrereqAndTechs(int i) const;				// Exposed to Python
	int getPrereqOrBonuses(int i) const;				// Exposed to Python
	int getProductionTraits(int i) const;				// Exposed to Python
	int getFlavorValue(int i) const;				// Exposed to Python
	int getTerrainAttackModifier(int i) const;				// Exposed to Python
	int getTerrainDefenseModifier(int i) const;				// Exposed to Python
	int getFeatureAttackModifier(int i) const;				// Exposed to Python
	int getFeatureDefenseModifier(int i) const;				// Exposed to Python
	int getUnitClassAttackModifier(int i) const;				// Exposed to Python
	int getUnitClassDefenseModifier(int i) const;				// Exposed to Python
	int getUnitCombatModifier(int i) const;				// Exposed to Python
	int getUnitCombatCollateralImmune(int i) const;				// Exposed to Python
	int getDomainModifier(int i) const;				// Exposed to Python
	int getBonusProductionModifier(int i) const;				// Exposed to Python
	int getUnitGroupRequired(int i) const;				// Exposed to Python
	int getReligionSpreads(int i) const;		// Exposed to Python
	int getCorporationSpreads(int i) const;		// Exposed to Python
	int getTerrainPassableTech(int i) const;		// Exposed to Python
	int getFeaturePassableTech(int i) const;		// Exposed to Python
	int getFlankingStrikeUnitClass(int i) const;	// Exposed to Python

	bool getUpgradeUnitClass(int i) const;	// Exposed to Python
	bool getTargetUnitClass(int i) const;	// Exposed to Python
	bool getTargetUnitCombat(int i) const;	// Exposed to Python
	bool getDefenderUnitClass(int i) const;	// Exposed to Python
	bool getDefenderUnitCombat(int i) const;	// Exposed to Python
	bool getUnitAIType(int i) const;				// Exposed to Python
	bool getNotUnitAIType(int i) const;			// Exposed to Python
	bool getBuilds(int i) const;						// Exposed to Python
	bool getGreatPeoples(int i) const;			// Exposed to Python
	bool getBuildings(int i) const;					// Exposed to Python
	bool getForceBuildings(int i) const;		// Exposed to Python
	bool getTerrainImpassable(int i) const;				// Exposed to Python
	bool getFeatureImpassable(int i) const;				// Exposed to Python
	bool getTerrainNative(int i) const;			// Exposed to Python
	bool getFeatureNative(int i) const;			// Exposed to Python
	bool getFreePromotions(int i) const;		// Exposed to Python
	int getLeaderPromotion() const;   // Exposed to Python
	int getLeaderExperience() const;				// Exposed to Python

	const TCHAR* getEarlyArtDefineTag(int i, UnitArtStyleTypes eStyle) const;				// Exposed to Python
	void setEarlyArtDefineTag(int i, const TCHAR* szVal);
	const TCHAR* getLateArtDefineTag(int i, UnitArtStyleTypes eStyle) const;				// Exposed to Python
	void setLateArtDefineTag(int i, const TCHAR* szVal);
	const TCHAR* getMiddleArtDefineTag(int i, UnitArtStyleTypes eStyle) const;				// Exposed to Python
	void setMiddleArtDefineTag(int i, const TCHAR* szVal);
	const TCHAR* getUnitNames(int i) const;
	const TCHAR* getFormationType() const;

	const TCHAR* getButton() const;
	void updateArtDefineButton();

	const CvArtInfoUnit* getArtInfo(int i, EraTypes eEra, UnitArtStyleTypes eStyle) const;

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iAIWeight;
	int m_iProductionCost;
	int m_iHurryCostModifier;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iMinAreaSize;
	int m_iMoves;
	int m_iAirRange;
	int m_iAirUnitCap;
	int m_iDropRange;
	int m_iNukeRange;
	int m_iWorkRate;
	int m_iBaseDiscover;
	int m_iDiscoverMultiplier;
	int m_iBaseHurry;
	int m_iHurryMultiplier;
	int m_iBaseTrade;
	int m_iTradeMultiplier;
	int m_iGreatWorkCulture;
	int m_iEspionagePoints;
	int m_iCombat;
	int m_iCombatLimit;
	int m_iAirCombat;
	int m_iAirCombatLimit;
	int m_iXPValueAttack;
	int m_iXPValueDefense;
	int m_iFirstStrikes;
	int m_iChanceFirstStrikes;
	int m_iInterceptionProbability;
	int m_iEvasionProbability;
	int m_iWithdrawalProbability;
	int m_iCollateralDamage;
	int m_iCollateralDamageLimit;
	int m_iCollateralDamageMaxUnits;
	int m_iCityAttackModifier;
	int m_iCityDefenseModifier;
	int m_iAnimalCombatModifier;
	int m_iHillsAttackModifier;
	int m_iHillsDefenseModifier;
	int m_iBombRate;
	int m_iBombardRate;
	int m_iSpecialCargo;

	int m_iDomainCargo;					
	int m_iCargoSpace;						
	int m_iConscriptionValue;
	int m_iCultureGarrisonValue;
	int m_iExtraCost;							
	int m_iAssetValue;						
	int m_iPowerValue;						
	int m_iUnitClassType;
	int m_iSpecialUnitType;				
	int m_iUnitCaptureClassType;		
	int m_iUnitCombatType;				
	int m_iDomainType;
	int m_iDefaultUnitAIType;
	int m_iInvisibleType;					
	int m_iAdvisorType;
	int m_iHolyCity;							
	int m_iReligionType;					
	int m_iStateReligion;					
	int m_iPrereqReligion;					
	int m_iPrereqCorporation;					
	int m_iPrereqBuilding;					
	int m_iPrereqAndTech;					
	int m_iPrereqAndBonus;				
	int m_iGroupSize;
	int m_iGroupDefinitions;
	int m_iUnitMeleeWaveSize;
	int m_iUnitRangedWaveSize;
	int m_iNumUnitNames;
	int m_iCommandType;
	int m_iLeaderExperience;

	bool m_bAnimal;
	bool m_bFoodProduction;
	bool m_bNoBadGoodies;
	bool m_bOnlyDefensive;
	bool m_bNoCapture;
	bool m_bQuickCombat;
	bool m_bRivalTerritory;
	bool m_bMilitaryHappiness;
	bool m_bMilitarySupport;
	bool m_bMilitaryProduction;
	bool m_bPillage;
	bool m_bSpy;
	bool m_bSabotage;
	bool m_bDestroy;
	bool m_bStealPlans;
	bool m_bInvestigate;
	bool m_bCounterSpy;
	bool m_bFound;
	bool m_bGoldenAge;
	bool m_bInvisible;
	bool m_bFirstStrikeImmune;
	bool m_bNoDefensiveBonus;
	bool m_bIgnoreBuildingDefense;
	bool m_bCanMoveImpassable;
	bool m_bCanMoveAllTerrain;
	bool m_bFlatMovementCost;
	bool m_bIgnoreTerrainCost;
	bool m_bNukeImmune;
	bool m_bPrereqBonuses;
	bool m_bPrereqReligion;
	bool m_bMechanized;
	bool m_bRenderBelowWater;
	bool m_bRenderAlways;
	bool m_bSuicide;
	bool m_bLineOfSight;
	bool m_bHiddenNationality;
	bool m_bAlwaysHostile;
	bool m_bNoRevealMap;
	int m_iLeaderPromotion;

	float m_fUnitMaxSpeed;
	float m_fUnitPadTime;

	// Arrays

	int* m_piPrereqAndTechs;
	int* m_piPrereqOrBonuses;
	int* m_piProductionTraits;
	int* m_piFlavorValue;
	int* m_piTerrainAttackModifier;
	int* m_piTerrainDefenseModifier;
	int* m_piFeatureAttackModifier;
	int* m_piFeatureDefenseModifier;
	int* m_piUnitClassAttackModifier;
	int* m_piUnitClassDefenseModifier;
	int* m_piUnitCombatModifier;
	int* m_piUnitCombatCollateralImmune;
	int* m_piDomainModifier;
	int* m_piBonusProductionModifier;
	int* m_piUnitGroupRequired;
	int* m_piReligionSpreads;
	int* m_piCorporationSpreads;
	int* m_piTerrainPassableTech;
	int* m_piFeaturePassableTech;
	int* m_piFlankingStrikeUnitClass;

	bool* m_pbUpgradeUnitClass;
	bool* m_pbTargetUnitClass;
	bool* m_pbTargetUnitCombat;
	bool* m_pbDefenderUnitClass;
	bool* m_pbDefenderUnitCombat;
	bool* m_pbUnitAIType;
	bool* m_pbNotUnitAIType;
	bool* m_pbBuilds;
	bool* m_pbGreatPeoples;
	bool* m_pbBuildings;
	bool* m_pbForceBuildings;
	bool* m_pbTerrainNative;
	bool* m_pbFeatureNative;
	bool* m_pbTerrainImpassable;
	bool* m_pbFeatureImpassable;
	bool* m_pbFreePromotions;

	CvString* m_paszEarlyArtDefineTags;
	CvString* m_paszLateArtDefineTags;
	CvString* m_paszMiddleArtDefineTags;
	CvString* m_paszUnitNames;
	CvString m_szFormationType;
	CvString m_szArtDefineButton;

	std::vector<int> m_aiSeeInvisibleTypes;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// 
// class	: CvUnitFormationInfo
//
// \brief	: Holds information relating to the formation of sub-units within a unit
// 
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class CvUnitEntry
{
public:
	CvUnitEntry()
	{
	}

	CvUnitEntry(const NiPoint2 &position, float radius, float facingDirection, float facingVariance) :
	m_position(position),
	m_fRadius(radius),
	m_fFacingDirection(facingDirection),
	m_fFacingVariance(facingVariance)
	{
	}

	NiPoint2 m_position;
	float m_fRadius;
	float m_fFacingDirection;
	float m_fFacingVariance;
};

class CvUnitFormationInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvUnitFormationInfo();
	DllExport virtual ~CvUnitFormationInfo();

	DllExport const TCHAR* getFormationType() const;
	DllExport const std::vector<EntityEventTypes> & getEventTypes() const;
	
	DllExport int getNumUnitEntries() const;
	DllExport const CvUnitEntry &getUnitEntry(int index) const;
	DllExport void addUnitEntry(const CvUnitEntry &unitEntry);
	DllExport int getNumGreatUnitEntries() const;
	DllExport const CvUnitEntry &getGreatUnitEntry(int index) const;
	DllExport int getNumSiegeUnitEntries() const;
	DllExport const CvUnitEntry &getSiegeUnitEntry(int index) const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------

protected:
	
	CvString m_szFormationType;
	std::vector<EntityEventTypes>	m_vctEventTypes;		//!< The list of EntityEventTypes that this formation is intended for

	std::vector<CvUnitEntry> m_vctUnitEntries;
	std::vector<CvUnitEntry> m_vctGreatUnitEntries;
	std::vector<CvUnitEntry> m_vctSiegeUnitEntries;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialUnitInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialUnitInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialUnitInfo();
	virtual ~CvSpecialUnitInfo();

	bool isValid() const;
	bool isCityLoad() const;

	// Arrays

	bool isCarrierUnitAIType(int i) const; 		// Exposed to Python
	int getProductionTraits(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	bool m_bValid;
	bool m_bCityLoad;

	// Arrays
	bool* m_pbCarrierUnitAITypes;
	int* m_piProductionTraits;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCivicOptionInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivicOptionInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCivicOptionInfo();
	virtual ~CvCivicOptionInfo();

	bool getTraitNoUpkeep(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	bool* m_pabTraitNoUpkeep;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCivicInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivicInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCivicInfo();
	virtual ~CvCivicInfo();

	int getCivicOptionType() const;				// Exposed to Python					
	int getAnarchyLength() const;				// Exposed to Python
	int getUpkeep() const;				// Exposed to Python
	int getAIWeight() const;				// Exposed to Python
	int getGreatPeopleRateModifier() const;				// Exposed to Python
	int getGreatGeneralRateModifier() const;				// Exposed to Python
	int getDomesticGreatGeneralRateModifier() const;				// Exposed to Python
	int getStateReligionGreatPeopleRateModifier() const;				// Exposed to Python
	int getDistanceMaintenanceModifier() const;				// Exposed to Python
	int getNumCitiesMaintenanceModifier() const;				// Exposed to Python
	int getCorporationMaintenanceModifier() const;				// Exposed to Python
	int getExtraHealth() const;						// Exposed to Python
	int getFreeExperience() const;				// Exposed to Python
	int getWorkerSpeedModifier() const;				// Exposed to Python
	int getImprovementUpgradeRateModifier() const;				// Exposed to Python
	int getMilitaryProductionModifier() const;				// Exposed to Python
	int getBaseFreeUnits() const;				// Exposed to Python
	int getBaseFreeMilitaryUnits() const;				// Exposed to Python
	int getFreeUnitsPopulationPercent() const;				// Exposed to Python
	int getFreeMilitaryUnitsPopulationPercent() const;				// Exposed to Python
	int getGoldPerUnit() const;				// Exposed to Python
	int getGoldPerMilitaryUnit() const;				// Exposed to Python
	int getHappyPerMilitaryUnit() const;				// Exposed to Python
	int getLargestCityHappiness() const;					// Exposed to Python
	int getWarWearinessModifier() const;					// Exposed to Python
	int getFreeSpecialist() const;				// Exposed to Python
	int getTradeRoutes() const;				// Exposed to Python
	int getTechPrereq() const;				// Exposed to Python
	int getCivicPercentAnger() const;				// Exposed to Python
	int getMaxConscript() const;				// Exposed to Python
	int getStateReligionHappiness() const;				// Exposed to Python
	int getNonStateReligionHappiness() const;				// Exposed to Python
	int getStateReligionUnitProductionModifier() const;				// Exposed to Python
	int getStateReligionBuildingProductionModifier() const;				// Exposed to Python
	int getStateReligionFreeExperience() const;								// Exposed to Python
	int getExpInBorderModifier() const;				// Exposed to Python

	bool isMilitaryFoodProduction() const;				// Exposed to Python
	bool isNoUnhealthyPopulation() const;				// Exposed to Python
	bool isBuildingOnlyHealthy() const;				// Exposed to Python
	bool isNoForeignTrade() const;				// Exposed to Python
	bool isNoCorporations() const;				// Exposed to Python
	bool isNoForeignCorporations() const;				// Exposed to Python
	bool isStateReligion() const;				// Exposed to Python
	bool isNoNonStateReligionSpread() const;				// Exposed to Python

	std::wstring pyGetWeLoveTheKing() { return getWeLoveTheKing(); }			// Exposed to Python
	const wchar* getWeLoveTheKing();
	void setWeLoveTheKingKey(const TCHAR* szVal);

	// Arrays

	int getYieldModifier(int i) const;				// Exposed to Python
	int* getYieldModifierArray() const;
	int getCapitalYieldModifier(int i) const;				// Exposed to Python
	int* getCapitalYieldModifierArray() const;
	int getTradeYieldModifier(int i) const;				// Exposed to Python
	int* getTradeYieldModifierArray() const;
	int getCommerceModifier(int i) const;				// Exposed to Python
	int* getCommerceModifierArray() const;
	int getCapitalCommerceModifier(int i) const;				// Exposed to Python
	int* getCapitalCommerceModifierArray() const;
	int getSpecialistExtraCommerce(int i) const;				// Exposed to Python
	int* getSpecialistExtraCommerceArray() const;
	int getBuildingHappinessChanges(int i) const;				// Exposed to Python
	int getBuildingHealthChanges(int i) const;				// Exposed to Python
	int getFeatureHappinessChanges(int i) const;				// Exposed to Python

	bool isHurry(int i) const;													// Exposed to Python
	bool isSpecialBuildingNotRequired(int i) const;			// Exposed to Python
	bool isSpecialistValid(int i) const;								// Exposed to Python

	int getImprovementYieldChanges(int i, int j) const;				// Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCivicOptionType;
	int m_iAnarchyLength;
	int m_iUpkeep;
	int m_iAIWeight;
	int m_iGreatPeopleRateModifier;					
	int m_iGreatGeneralRateModifier;					
	int m_iDomesticGreatGeneralRateModifier;					
	int m_iStateReligionGreatPeopleRateModifier;					
	int m_iDistanceMaintenanceModifier;					
	int m_iNumCitiesMaintenanceModifier;					
	int m_iCorporationMaintenanceModifier;					
	int m_iExtraHealth;
	int m_iFreeExperience;
	int m_iWorkerSpeedModifier;
	int m_iImprovementUpgradeRateModifier;
	int m_iMilitaryProductionModifier;
	int m_iBaseFreeUnits;											
	int m_iBaseFreeMilitaryUnits;								
	int m_iFreeUnitsPopulationPercent;						
	int m_iFreeMilitaryUnitsPopulationPercent;			
	int m_iGoldPerUnit;												
	int m_iGoldPerMilitaryUnit;									
	int m_iHappyPerMilitaryUnit;
	int m_iLargestCityHappiness;
	int m_iWarWearinessModifier;
	int m_iFreeSpecialist;
	int m_iTradeRoutes;												
	int m_iTechPrereq;												
	int m_iCivicPercentAnger;									
	int m_iMaxConscript;											
	int m_iStateReligionHappiness;							
	int m_iNonStateReligionHappiness;						
	int m_iStateReligionUnitProductionModifier;			
	int m_iStateReligionBuildingProductionModifier;	
	int m_iStateReligionFreeExperience;	
	int m_iExpInBorderModifier;

	bool m_bMilitaryFoodProduction;
	bool m_bNoUnhealthyPopulation;
	bool m_bBuildingOnlyHealthy;
	bool m_bNoForeignTrade;
	bool m_bNoCorporations;
	bool m_bNoForeignCorporations;
	bool m_bStateReligion;
	bool m_bNoNonStateReligionSpread;

	CvWString m_szWeLoveTheKingKey;

	// Arrays

	int* m_piYieldModifier;
	int* m_piCapitalYieldModifier;
	int* m_piTradeYieldModifier;
	int* m_piCommerceModifier;
	int* m_piCapitalCommerceModifier;
	int* m_piSpecialistExtraCommerce;
	int* m_paiBuildingHappinessChanges;
	int* m_paiBuildingHealthChanges;
	int* m_paiFeatureHappinessChanges;

	bool* m_pabHurry;
	bool* m_pabSpecialBuildingNotRequired;
	bool* m_pabSpecialistValid;

	int** m_ppiImprovementYieldChanges;
	
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvDiplomacyInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyInfo :
	public CvInfoBase
{

	friend class CvXMLLoadUtility;		// so it can access private vars to initialize the class
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvDiplomacyInfo();
	DllExport virtual ~CvDiplomacyInfo();

	DllExport void uninit();			

	DllExport const CvDiplomacyResponse& getResponse(int iNum) const;	// Exposed to Python
	DllExport int getNumResponses() const;															// Exposed to Python

	DllExport bool getCivilizationTypes(int i, int j) const;						// Exposed to Python
	DllExport bool getLeaderHeadTypes(int i, int j) const;							// Exposed to Python
	DllExport bool getAttitudeTypes(int i, int j) const;								// Exposed to Python
	DllExport bool getDiplomacyPowerTypes(int i, int j) const;					// Exposed to Python

	DllExport int getNumDiplomacyText(int i) const;											// Exposed to Python

	DllExport const TCHAR* getDiplomacyText(int i, int j) const;				// Exposed to Python

	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);

private:
	std::vector<CvDiplomacyResponse*> m_pResponses;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUnitClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUnitClassInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvUnitClassInfo();
	virtual ~CvUnitClassInfo();

	int getMaxGlobalInstances() const;				// Exposed to Python
	int getMaxTeamInstances() const;				// Exposed to Python
	int getMaxPlayerInstances() const;				// Exposed to Python
	int getInstanceCostModifier() const;				// Exposed to Python
	int getDefaultUnitIndex() const;				// Exposed to Python
	void setDefaultUnitIndex(int i);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMaxGlobalInstances;	
	int m_iMaxTeamInstances;	
	int m_iMaxPlayerInstances;	
	int m_iInstanceCostModifier;
	int m_iDefaultUnitIndex;		


};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBuildingInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoBuilding;
class CvArtInfoMovie;
class CvBuildingInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBuildingInfo();
	virtual ~CvBuildingInfo();

	int getBuildingClassType() const;				// Exposed to Python
	int getVictoryPrereq() const;				// Exposed to Python
	int getFreeStartEra() const;						// Exposed to Python
	int getMaxStartEra() const;				// Exposed to Python
	int getObsoleteTech() const;				// Exposed to Python
	int getPrereqAndTech() const;				// Exposed to Python
	int getNoBonus() const;				// Exposed to Python
	int getPowerBonus() const;				// Exposed to Python
	int getFreeBonus() const;				// Exposed to Python
	int getNumFreeBonuses() const;				// Exposed to Python
	int getFreeBuildingClass() const;				// Exposed to Python
	void setNumFreeBuildingClass(int i);
	int getFreePromotion() const;				// Exposed to Python
	int getCivicOption() const;				// Exposed to Python
	int getAIWeight() const;				// Exposed to Python
	int getProductionCost() const;				// Exposed to Python
	int getHurryCostModifier() const;				// Exposed to Python
	int getHurryAngerModifier() const;				// Exposed to Python
	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python
	int getMinAreaSize() const;				// Exposed to Python
	int getNumCitiesPrereq() const;				// Exposed to Python
	int getNumTeamsPrereq() const;				// Exposed to Python
	int getUnitLevelPrereq() const;				// Exposed to Python
	int getMinLatitude() const;				// Exposed to Python
	int getMaxLatitude() const;				// Exposed to Python
	int getGreatPeopleRateModifier() const;				// Exposed to Python
	int getGreatGeneralRateModifier() const;				// Exposed to Python
	int getDomesticGreatGeneralRateModifier() const;				// Exposed to Python
	int getGlobalGreatPeopleRateModifier() const;				// Exposed to Python
	int getAnarchyModifier() const;				// Exposed to Python
	int getGoldenAgeModifier() const;				// Exposed to Python
	int getGlobalHurryModifier() const;				// Exposed to Python
	int getFreeExperience() const;				// Exposed to Python
	int getGlobalFreeExperience() const;				// Exposed to Python
	int getFoodKept() const;				// Exposed to Python
	int getAirlift() const;				// Exposed to Python
	int getAirModifier() const;				// Exposed to Python
	int getAirUnitCapacity() const;				// Exposed to Python
	int getNukeModifier() const;				// Exposed to Python
	int getNukeExplosionRand() const;				// Exposed to Python
	int getFreeSpecialist() const;				// Exposed to Python
	int getAreaFreeSpecialist() const;				// Exposed to Python
	int getGlobalFreeSpecialist() const;				// Exposed to Python
	int getHappiness() const;				// Exposed to Python
	int getAreaHappiness() const;				// Exposed to Python
	int getGlobalHappiness() const;				// Exposed to Python
	int getStateReligionHappiness() const;				// Exposed to Python
	int getWorkerSpeedModifier() const;				// Exposed to Python
	int getMilitaryProductionModifier() const;				// Exposed to Python
	int getSpaceProductionModifier() const;				// Exposed to Python
	int getGlobalSpaceProductionModifier() const;				// Exposed to Python
	int getTradeRoutes() const;				// Exposed to Python
	int getCoastalTradeRoutes() const;				// Exposed to Python
	int getGlobalTradeRoutes() const;				// Exposed to Python
	int getTradeRouteModifier() const;				// Exposed to Python
	int getForeignTradeRouteModifier() const;				// Exposed to Python
	int getAssetValue() const;				// Exposed to Python
	int getPowerValue() const;				// Exposed to Python
	int getSpecialBuildingType() const;				// Exposed to Python
	int getAdvisorType() const;				// Exposed to Python
	int getHolyCity() const;				// Exposed to Python
	int getReligionType() const;				// Exposed to Python
	int getStateReligion() const;				// Exposed to Python
	int getPrereqReligion() const;				// Exposed to Python
	int getPrereqCorporation() const;				// Exposed to Python
	int getFoundsCorporation() const;				// Exposed to Python
	int getGlobalReligionCommerce() const;				// Exposed to Python
	int getGlobalCorporationCommerce() const;				// Exposed to Python
	int getPrereqAndBonus() const;				// Exposed to Python
	int getGreatPeopleUnitClass() const;				// Exposed to Python
	int getGreatPeopleRateChange() const;				// Exposed to Python
	int getConquestProbability() const;				// Exposed to Python
	int getMaintenanceModifier() const;				// Exposed to Python
	int getWarWearinessModifier() const;				// Exposed to Python
	int getGlobalWarWearinessModifier() const;				// Exposed to Python
	int getEnemyWarWearinessModifier() const;				// Exposed to Python
	int getHealRateChange() const;				// Exposed to Python
	int getHealth() const;				// Exposed to Python
	int getAreaHealth() const;				// Exposed to Python
	int getGlobalHealth() const;				// Exposed to Python
	int getGlobalPopulationChange() const;				// Exposed to Python
	int getFreeTechs() const;				// Exposed to Python
	int getDefenseModifier() const;					// Exposed to Python
	int getBombardDefenseModifier() const;					// Exposed to Python
	int getAllCityDefenseModifier() const;				// Exposed to Python
	int getEspionageDefenseModifier() const;					// Exposed to Python
	int getMissionType() const;											// Exposed to Python
	void setMissionType(int iNewType);
	int getVoteSourceType() const;				// Exposed to Python

	float getVisibilityPriority() const;

	bool isTeamShare() const;				// Exposed to Python
	bool isWater() const;				// Exposed to Python
	bool isRiver() const;				// Exposed to Python
	bool isPower() const;				// Exposed to Python
	bool isDirtyPower() const;				// Exposed to Python
	bool isAreaCleanPower() const;		// Exposed to Python
	bool isAreaBorderObstacle() const;		// Exposed to Python
	bool isForceTeamVoteEligible() const;				// Exposed to Python
	bool isCapital() const;				// Exposed to Python
	bool isGovernmentCenter() const;				// Exposed to Python
	bool isGoldenAge() const;				// Exposed to Python
	bool isMapCentering() const;				// Exposed to Python
	bool isNoUnhappiness() const;				// Exposed to Python
	bool isNoUnhealthyPopulation() const;				// Exposed to Python
	bool isBuildingOnlyHealthy() const;				// Exposed to Python
	bool isNeverCapture() const;				// Exposed to Python
	bool isNukeImmune() const;				// Exposed to Python
	bool isPrereqReligion() const;				// Exposed to Python
	bool isCenterInCity() const;				// Exposed to Python
	bool isStateReligion() const;				// Exposed to Python
	bool isAllowsNukes() const;				// Exposed to Python

	const TCHAR* getConstructSound() const;				// Exposed to Python
	void setConstructSound(const TCHAR* szVal);
	const TCHAR* getArtDefineTag() const;				// Exposed to Python
	void setArtDefineTag(const TCHAR* szVal);
	const TCHAR* getMovieDefineTag() const;				// Exposed to Python
	void setMovieDefineTag(const TCHAR* szVal);

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int* getYieldChangeArray() const;
	int getYieldModifier(int i) const;;				// Exposed to Python
	int* getYieldModifierArray() const;
	int getPowerYieldModifier(int i) const;				// Exposed to Python
	int* getPowerYieldModifierArray() const;
	int getAreaYieldModifier(int i) const;				// Exposed to Python
	int* getAreaYieldModifierArray() const;
	int getGlobalYieldModifier(int i) const;				// Exposed to Python
	int* getGlobalYieldModifierArray() const;
	int getSeaPlotYieldChange(int i) const;				// Exposed to Python
	int* getSeaPlotYieldChangeArray() const;
	int getRiverPlotYieldChange(int i) const;				// Exposed to Python
	int* getRiverPlotYieldChangeArray() const;
	int getGlobalSeaPlotYieldChange(int i) const;				// Exposed to Python
	int* getGlobalSeaPlotYieldChangeArray() const;

	int getCommerceChange(int i) const;				// Exposed to Python
	int* getCommerceChangeArray() const;
	int getObsoleteSafeCommerceChange(int i) const;				// Exposed to Python
	int* getObsoleteSafeCommerceChangeArray() const;
	int getCommerceChangeDoubleTime(int i) const;				// Exposed to Python
	int getCommerceModifier(int i) const;				// Exposed to Python
	int* getCommerceModifierArray() const;
	int getGlobalCommerceModifier(int i) const;				// Exposed to Python
	int* getGlobalCommerceModifierArray() const;
	int getSpecialistExtraCommerce(int i) const;	// Exposed to Python
	int* getSpecialistExtraCommerceArray() const;
	int getStateReligionCommerce(int i) const;				// Exposed to Python
	int* getStateReligionCommerceArray() const;
	int getCommerceHappiness(int i) const;				// Exposed to Python
	int getReligionChange(int i) const;				// Exposed to Python
	int getSpecialistCount(int i) const;				// Exposed to Python
	int getFreeSpecialistCount(int i) const;				// Exposed to Python
	int getBonusHealthChanges(int i) const;				// Exposed to Python
	int getBonusHappinessChanges(int i) const;				// Exposed to Python
	int getBonusProductionModifier(int i) const;				// Exposed to Python
	int getUnitCombatFreeExperience(int i) const;				// Exposed to Python
	int getDomainFreeExperience(int i) const;						// Exposed to Python
	int getDomainProductionModifier(int i) const;				// Exposed to Python
	int getPrereqAndTechs(int i) const;				// Exposed to Python
	int getPrereqOrBonuses(int i) const;				// Exposed to Python
	int getProductionTraits(int i) const;				// Exposed to Python
	int getHappinessTraits(int i) const;				// Exposed to Python
	int getBuildingHappinessChanges(int i) const;				// Exposed to Python
	int getPrereqNumOfBuildingClass(int i) const;				// Exposed to Python
	int getFlavorValue(int i) const;				// Exposed to Python
	int getImprovementFreeSpecialist(int i) const;				// Exposed to Python

	bool isCommerceFlexible(int i) const;				// Exposed to Python
	bool isCommerceChangeOriginalOwner(int i) const;				// Exposed to Python
	bool isBuildingClassNeededInCity(int i) const;				// Exposed to Python

	int getSpecialistYieldChange(int i, int j) const;			// Exposed to Python
	int* getSpecialistYieldChangeArray(int i) const;

	int getBonusYieldModifier(int i, int j) const;				// Exposed to Python
	int* getBonusYieldModifierArray(int i) const;

	// Other

	const CvArtInfoBuilding* getArtInfo() const;
	const CvArtInfoMovie* getMovieInfo() const;
	const TCHAR* getButton() const;
	const TCHAR* getMovie() const;

	// serialization
	void read(FDataStreamBase*);
	void write(FDataStreamBase*);
	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------
protected:

	int m_iBuildingClassType;						
	int m_iVictoryPrereq;
	int m_iFreeStartEra;
	int m_iMaxStartEra;
	int m_iObsoleteTech;								
	int m_iPrereqAndTech;								
	int m_iNoBonus;									
	int m_iPowerBonus;									
	int m_iFreeBonus;									
	int m_iNumFreeBonuses;							
	int m_iFreeBuildingClass;									
	int m_iFreePromotion;								
	int m_iCivicOption;									
	int m_iAIWeight;
	int m_iProductionCost;
	int m_iHurryCostModifier;
	int m_iHurryAngerModifier;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iMinAreaSize;									
	int m_iNumCitiesPrereq;							
	int m_iNumTeamsPrereq;							
	int m_iUnitLevelPrereq;							
	int m_iMinLatitude;									
	int m_iMaxLatitude;									
	int m_iGreatPeopleRateModifier;				
	int m_iGreatGeneralRateModifier;				
	int m_iDomesticGreatGeneralRateModifier;						
	int m_iGlobalGreatPeopleRateModifier;	
	int m_iAnarchyModifier;							
	int m_iGoldenAgeModifier;							
	int m_iGlobalHurryModifier;						
	int m_iFreeExperience;
	int m_iGlobalFreeExperience;						
	int m_iFoodKept;
	int m_iAirlift;
	int m_iAirModifier;									
	int m_iAirUnitCapacity;									
	int m_iNukeModifier;
	int m_iNukeExplosionRand;
	int m_iFreeSpecialist;								
	int m_iAreaFreeSpecialist;						
	int m_iGlobalFreeSpecialist;						
	int m_iHappiness;									
	int m_iAreaHappiness;								
	int m_iGlobalHappiness;							
	int m_iStateReligionHappiness;				
	int m_iWorkerSpeedModifier;					
	int m_iMilitaryProductionModifier;				
	int m_iSpaceProductionModifier;				
	int m_iGlobalSpaceProductionModifier;	
	int m_iTradeRoutes;									
	int m_iCoastalTradeRoutes;						
	int m_iGlobalTradeRoutes;						
	int m_iTradeRouteModifier;						
	int m_iForeignTradeRouteModifier;						
	int m_iAssetValue;									
	int m_iPowerValue;									
	int m_iSpecialBuildingType;						
	int m_iAdvisorType;
	int m_iHolyCity;										
	int m_iReligionType;								
	int m_iStateReligion;								
	int m_iPrereqReligion;								
	int m_iPrereqCorporation;								
	int m_iFoundsCorporation;					
	int m_iGlobalReligionCommerce;
	int m_iGlobalCorporationCommerce;
	int m_iPrereqAndBonus;							
	int m_iGreatPeopleUnitClass;					
	int m_iGreatPeopleRateChange;				
	int m_iConquestProbability;						
	int m_iMaintenanceModifier;					
	int m_iWarWearinessModifier;					
	int m_iGlobalWarWearinessModifier;
	int m_iEnemyWarWearinessModifier;					
	int m_iHealRateChange;
	int m_iHealth;
	int m_iAreaHealth;
	int m_iGlobalHealth;
	int m_iGlobalPopulationChange;
	int m_iFreeTechs;
	int m_iDefenseModifier;
	int m_iBombardDefenseModifier;
	int m_iAllCityDefenseModifier;
	int m_iEspionageDefenseModifier;
	int m_iMissionType;
	int m_iVoteSourceType;

	float m_fVisibilityPriority;

	bool m_bTeamShare;
	bool m_bWater;								
	bool m_bRiver;									
	bool m_bPower;								
	bool m_bDirtyPower;
	bool m_bAreaCleanPower;
	bool m_bAreaBorderObstacle;
	bool m_bForceTeamVoteEligible;
	bool m_bCapital;
	bool m_bGovernmentCenter;
	bool m_bGoldenAge;
	bool m_bMapCentering;
	bool m_bNoUnhappiness;
	bool m_bNoUnhealthyPopulation;
	bool m_bBuildingOnlyHealthy;			
	bool m_bNeverCapture;					
	bool m_bNukeImmune;					
	bool m_bPrereqReligion;					
	bool m_bCenterInCity;
	bool m_bStateReligion;
	bool m_bAllowsNukes;

	CvString m_szConstructSound;
	CvString m_szArtDefineTag;
	CvString m_szMovieDefineTag;

	// Arrays

	int* m_piPrereqAndTechs;
	int* m_piPrereqOrBonuses;
	int* m_piProductionTraits;
	int* m_piHappinessTraits;
	int* m_piSeaPlotYieldChange;
	int* m_piRiverPlotYieldChange;
	int* m_piGlobalSeaPlotYieldChange;
	int* m_piYieldChange;
	int* m_piYieldModifier;
	int* m_piPowerYieldModifier;
	int* m_piAreaYieldModifier;
	int* m_piGlobalYieldModifier;
	int* m_piCommerceChange;
	int* m_piObsoleteSafeCommerceChange;
	int* m_piCommerceChangeDoubleTime;
	int* m_piCommerceModifier;
	int* m_piGlobalCommerceModifier;
	int* m_piSpecialistExtraCommerce;
	int* m_piStateReligionCommerce;
	int* m_piCommerceHappiness;
	int* m_piReligionChange;
	int* m_piSpecialistCount;
	int* m_piFreeSpecialistCount;
	int* m_piBonusHealthChanges;
	int* m_piBonusHappinessChanges;
	int* m_piBonusProductionModifier;
	int* m_piUnitCombatFreeExperience;
	int* m_piDomainFreeExperience;
	int* m_piDomainProductionModifier;
	int* m_piBuildingHappinessChanges;
	int* m_piPrereqNumOfBuildingClass;
	int* m_piFlavorValue;
	int* m_piImprovementFreeSpecialist;

	bool* m_pbCommerceFlexible;
	bool* m_pbCommerceChangeOriginalOwner;
	bool* m_pbBuildingClassNeededInCity;

	int** m_ppaiSpecialistYieldChange;
	int** m_ppaiBonusYieldModifier;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialBuildingInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialBuildingInfo :
	public CvInfoBase
{

	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialBuildingInfo();
	virtual ~CvSpecialBuildingInfo();

	int getObsoleteTech( void ) const;					// Exposed to Python
	int getTechPrereq( void ) const;						// Exposed to Python
	int getTechPrereqAnyone( void ) const;						// Exposed to Python

	bool isValid( void ) const;									// Exposed to Python

	// Arrays

	int getProductionTraits(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iObsoleteTech;
	int m_iTechPrereq;
	int m_iTechPrereqAnyone;

	bool m_bValid;

	// Arrays

	int* m_piProductionTraits;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBuildingClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBuildingClassInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBuildingClassInfo();
	virtual ~CvBuildingClassInfo();

	int getMaxGlobalInstances() const;				// Exposed to Python
	int getMaxTeamInstances() const;				// Exposed to Python
	int getMaxPlayerInstances() const;				// Exposed to Python
	int getExtraPlayerInstances() const;				// Exposed to Python
	int getDefaultBuildingIndex() const;				// Exposed to Python
	void setDefaultBuildingIndex(int i);

	bool isNoLimit() const;				// Exposed to Python
	bool isMonument() const;				// Exposed to Python

	// Arrays

	int getVictoryThreshold(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iMaxPlayerInstances;
	int m_iExtraPlayerInstances;
	int m_iDefaultBuildingIndex;

	bool m_bNoLimit;
	bool m_bMonument;

	// Arrays

	int* m_piVictoryThreshold;

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRiverInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRiverInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvRiverInfo();
	virtual ~CvRiverInfo();

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
	
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRiverModelInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRiverModelInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvRiverModelInfo();
	DllExport virtual ~CvRiverModelInfo();

	DllExport const TCHAR* getModelFile() const;				// Exposed to Python
	DllExport void setModelFile(const TCHAR* szVal);				// The model filename
	DllExport const TCHAR* getBorderFile() const;				// Exposed to Python
	DllExport void setBorderFile(const TCHAR* szVal);				// The model filename

	DllExport int getTextureIndex() const;
	DllExport const TCHAR* getDeltaString() const;				//Exposed to Python
	DllExport const TCHAR* getConnectString() const;				// Exposed to Python
	DllExport const TCHAR* getRotateString() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	CvString m_szModelFile;					// The model filename
	CvString m_szBorderFile;				// The border filename

	TCHAR		m_szDeltaString[32];		// The delta type
	TCHAR		m_szConnectString[32];		// The connections this cell makes ( N S E W NE NW SE SW )
	TCHAR		m_szRotateString[32];		// The possible rotations for this cell ( 0 90 180 270 )
	int			m_iTextureIndex;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRouteModelInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRouteModelInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvRouteModelInfo();
	DllExport virtual ~CvRouteModelInfo();

	DllExport RouteTypes getRouteType() const;				// The route type

	DllExport const TCHAR* getModelFile() const;				// Exposed to Python
	DllExport void setModelFile(const TCHAR* szVal);				// The model filename
	DllExport const TCHAR* getLateModelFile() const;				// Exposed to Python
	DllExport void setLateModelFile(const TCHAR* szVal);				// The model filename
	DllExport const TCHAR* getModelFileKey() const;				// Exposed to Python
	DllExport void setModelFileKey(const TCHAR* szVal);				// The model filename Key

	DllExport bool isAnimated() const;

	DllExport const TCHAR* getConnectString() const;				// Exposed to Python
	DllExport const TCHAR* getModelConnectString() const;			// Exposed to Python
	DllExport const TCHAR* getRotateString() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	RouteTypes	m_eRouteType;			// The route type

	CvString m_szModelFile;				// The model filename
	CvString m_szLateModelFile;				// The model filename
	CvString m_szModelFileKey;			// The model file key reference 
	bool m_bAnimated;

	TCHAR		m_szConnectString[32];	// The connections this cell makes ( N S E W NE NW SE SW )
	TCHAR		m_szModelConnectString[32];	// The connections this model makes ( N S E W NE NW SE SW )
	TCHAR		m_szRotateString[32];	// The possible rotations for this cell ( 0 90 180 270 )
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCivilizationInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoCivilization;
class CvCivilizationInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvCivilizationInfo();
	DllExport virtual ~CvCivilizationInfo();
	DllExport virtual void reset();

	DllExport int getDefaultPlayerColor() const;				// Expose to Python
	DllExport int getArtStyleType() const;				// Expose to Python
	DllExport int getUnitArtStyleType() const;         // Expose to Python
	DllExport int getNumCityNames() const;				// Expose to Python
	DllExport int getNumLeaders() const;				// Exposed to Python - the number of leaders the Civ has, this is needed so that random leaders can be generated easily
	DllExport int getSelectionSoundScriptId() const;				// Expose to Python
	DllExport int getActionSoundScriptId() const;				// Expose to Python

	DllExport bool isAIPlayable() const;				// Expose to Python
	DllExport bool isPlayable() const;				// Expose to Python

	std::wstring pyGetShortDescription(uint uiForm) { return getShortDescription(uiForm); }				// Exposed to Python
	DllExport const wchar* getShortDescription(uint uiForm = 0);
	DllExport const wchar* getShortDescriptionKey() const;				// Exposed to Python
	std::wstring pyGetShortDescriptionKey() { return getShortDescriptionKey(); }				// Exposed to Python
	
	std::wstring pyGetAdjective(uint uiForm) { return getAdjective(uiForm);  }	// Exposed to Python
	DllExport const wchar* getAdjective(uint uiForm = 0);				
	DllExport const wchar* getAdjectiveKey() const;				// Exposed to Python
	std::wstring pyGetAdjectiveKey() { return getAdjectiveKey(); }				// Exposed to Python

	DllExport const TCHAR* getFlagTexture() const;
	DllExport const TCHAR* getArtDefineTag() const;
	DllExport void setArtDefineTag(const TCHAR* szVal);
	// Arrays

	DllExport int getCivilizationBuildings(int i) const;				// Exposed to Python
	DllExport int getCivilizationUnits(int i) const;				// Exposed to Python
	DllExport int getCivilizationFreeUnitsClass(int i) const;				// Exposed to Python
	DllExport int getCivilizationInitialCivics(int i) const;				// Exposed to Python

	DllExport bool isLeaders(int i) const;				// Exposed to Python
	DllExport bool isCivilizationFreeBuildingClass(int i) const;				// Exposed to Python
	DllExport bool isCivilizationFreeTechs(int i) const;				// Exposed to Python
	DllExport bool isCivilizationDisableTechs(int i) const;				// Exposed to Python

	DllExport std::string getCityNames(int i) const;				// Exposed to Python

	DllExport const CvArtInfoCivilization* getArtInfo() const;
	DllExport const TCHAR* getButton() const;

	DllExport int getDerivativeCiv() const;																// Exposed to Python
	void setDerivativeCiv(int iCiv);

	bool read(CvXMLLoadUtility* pXML);
	DllExport bool readPass2(CvXMLLoadUtility* pXML);
	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iDefaultPlayerColor;	
	int m_iArtStyleType;				
	int m_iUnitArtStyleType;  // FlavorUnits by Impaler[WrG]
	int m_iNumCityNames;			
	int m_iNumLeaders;				 // the number of leaders the Civ has, this is needed so that random leaders can be generated easily
	int m_iSelectionSoundScriptId;
	int m_iActionSoundScriptId;
	int m_iDerivativeCiv;

	bool m_bAIPlayable;			
	bool m_bPlayable;				

	CvString m_szArtDefineTag;
	CvWString m_szShortDescriptionKey;
	CvWString m_szAdjectiveKey;
	// Arrays

	int* m_piCivilizationBuildings;
	int* m_piCivilizationUnits;
	int* m_piCivilizationFreeUnitsClass;
	int* m_piCivilizationInitialCivics;

	bool* m_pbLeaders;
	bool* m_pbCivilizationFreeBuildingClass;
	bool* m_pbCivilizationFreeTechs;
	bool* m_pbCivilizationDisableTechs;

	CvString* m_paszCityNames;

	mutable std::vector<CvWString> m_aszShortDescription;
	mutable std::vector<CvWString> m_aszAdjective;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvVictoryInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVictoryInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvVictoryInfo();
	virtual ~CvVictoryInfo();

	int getPopulationPercentLead() const;				// Exposed to Python
	int getLandPercent() const;				// Exposed to Python
	int getMinLandPercent() const;				// Exposed to Python
	int getReligionPercent() const;				// Exposed to Python
	int getCityCulture() const;				// Exposed to Python
	int getNumCultureCities() const;				// Exposed to Python
	int getTotalCultureRatio() const;				// Exposed to Python
	int getVictoryDelayTurns() const;				// Exposed to Python

	bool isTargetScore() const;				// Exposed to Python
	bool isEndScore() const;					// Exposed to Python
	bool isConquest() const;					// Exposed to Python
	bool isDiploVote() const;					// Exposed to Python
	DllExport bool isPermanent() const;					// Exposed to Python

	const char* getMovie() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iPopulationPercentLead;
	int m_iLandPercent;
	int m_iMinLandPercent;
	int m_iReligionPercent;
	int m_iCityCulture;
	int m_iNumCultureCities;
	int m_iTotalCultureRatio;
	int m_iVictoryDelayTurns;

	bool m_bTargetScore;
	bool m_bEndScore;
	bool m_bConquest;
	bool m_bDiploVote;
	bool m_bPermanent;

	CvString m_szMovie;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvHurryInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHurryInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		CvHurryInfo();
		virtual ~CvHurryInfo();

		int getGoldPerProduction() const;					// Exposed to Python
		int getProductionPerPopulation() const;		// Exposed to Python

		bool isAnger() const;											// Exposed to Python

		bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------
	protected:

		int m_iGoldPerProduction;
		int m_iProductionPerPopulation;

		bool m_bAnger;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvHandicapInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHandicapInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvHandicapInfo();
	virtual ~CvHandicapInfo();

	int getFreeWinsVsBarbs() const;				// Exposed to Python
	int getAnimalAttackProb() const;				// Exposed to Python
	int getStartingLocationPercent() const;				// Exposed to Python
	int getAdvancedStartPointsMod() const;				// Exposed to Python
	int getStartingGold() const;				// Exposed to Python
	int getFreeUnits() const;				// Exposed to Python
	int getUnitCostPercent() const;				// Exposed to Python
	int getResearchPercent() const;				// Exposed to Python
	int getDistanceMaintenancePercent() const;				// Exposed to Python
	int getNumCitiesMaintenancePercent() const;				// Exposed to Python
	int getMaxNumCitiesMaintenance() const;				// Exposed to Python
	int getColonyMaintenancePercent() const;				// Exposed to Python
	int getMaxColonyMaintenance() const;				// Exposed to Python
	int getCorporationMaintenancePercent() const;				// Exposed to Python
	int getCivicUpkeepPercent() const;				// Exposed to Python
	int getInflationPercent() const;				// Exposed to Python
	int getHealthBonus() const;				// Exposed to Python
	int getHappyBonus() const;				// Exposed to Python
	int getAttitudeChange() const;				// Exposed to Python
	int getNoTechTradeModifier() const;				// Exposed to Python
	int getTechTradeKnownModifier() const;				// Exposed to Python
	int getUnownedTilesPerGameAnimal() const;				// Exposed to Python
	int getUnownedTilesPerBarbarianUnit() const;				// Exposed to Python
	int getUnownedWaterTilesPerBarbarianUnit() const;				// Exposed to Python
	int getUnownedTilesPerBarbarianCity() const;				// Exposed to Python
	int getBarbarianCreationTurnsElapsed() const;				// Exposed to Python
	int getBarbarianCityCreationTurnsElapsed() const;				// Exposed to Python
	int getBarbarianCityCreationProb() const;				// Exposed to Python
	int getAnimalCombatModifier() const;				// Exposed to Python
	int getBarbarianCombatModifier() const;				// Exposed to Python
	int getAIAnimalCombatModifier() const;				// Exposed to Python
	int getAIBarbarianCombatModifier() const;				// Exposed to Python

	int getStartingDefenseUnits() const;						// Exposed to Python
	int getStartingWorkerUnits() const;							// Exposed to Python
	int getStartingExploreUnits() const;						// Exposed to Python
	int getAIStartingUnitMultiplier() const;				// Exposed to Python
	int getAIStartingDefenseUnits() const;				// Exposed to Python
	int getAIStartingWorkerUnits() const;				// Exposed to Python
	int getAIStartingExploreUnits() const;				// Exposed to Python
	int getBarbarianInitialDefenders() const;				// Exposed to Python
	int getAIDeclareWarProb() const;								// Exposed to Python
	int getAIWorkRateModifier() const;				// Exposed to Python
	int getAIGrowthPercent() const;				// Exposed to Python
	int getAITrainPercent() const;				// Exposed to Python
	int getAIWorldTrainPercent() const;				// Exposed to Python
	int getAIConstructPercent() const;				// Exposed to Python
	int getAIWorldConstructPercent() const;				// Exposed to Python
	int getAICreatePercent() const;				// Exposed to Python
	int getAIWorldCreatePercent() const;				// Exposed to Python
	int getAICivicUpkeepPercent() const;				// Exposed to Python
	int getAIUnitCostPercent() const;				// Exposed to Python
	int getAIUnitSupplyPercent() const;				// Exposed to Python
	int getAIUnitUpgradePercent() const;				// Exposed to Python
	int getAIInflationPercent() const;				// Exposed to Python
	int getAIWarWearinessPercent() const;				// Exposed to Python
	int getAIPerEraModifier() const;						// Exposed to Python
	int getAIAdvancedStartPercent() const;						// Exposed to Python
	int getNumGoodies() const;				// Exposed to Python

	// Arrays

	int getGoodies(int i) const;				// Exposed to Python
	int isFreeTechs(int i) const;				// Exposed to Python
	int isAIFreeTechs(int i) const;				// Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iFreeWinsVsBarbs;
	int m_iAnimalAttackProb;
	int m_iStartingLocationPercent;						
	int m_iAdvancedStartPointsMod;											
	int m_iStartingGold;											
	int m_iFreeUnits;												
	int m_iUnitCostPercent;									
	int m_iResearchPercent;									
	int m_iDistanceMaintenancePercent;				
	int m_iNumCitiesMaintenancePercent;				
	int m_iMaxNumCitiesMaintenance;					
	int m_iColonyMaintenancePercent;				
	int m_iMaxColonyMaintenance;					
	int m_iCorporationMaintenancePercent;				
	int m_iCivicUpkeepPercent;								
	int m_iInflationPercent;									
	int m_iHealthBonus;									
	int m_iHappyBonus;										
	int m_iAttitudeChange;
	int m_iNoTechTradeModifier;
	int m_iTechTradeKnownModifier;
	int m_iUnownedTilesPerGameAnimal;				
	int m_iUnownedTilesPerBarbarianUnit;			
	int m_iUnownedWaterTilesPerBarbarianUnit;	
	int m_iUnownedTilesPerBarbarianCity;			
	int m_iBarbarianCreationTurnsElapsed;			
	int m_iBarbarianCityCreationTurnsElapsed;	
	int m_iBarbarianCityCreationProb;					
	int m_iAnimalCombatModifier;
	int m_iBarbarianCombatModifier;
	int m_iAIAnimalCombatModifier;
	int m_iAIBarbarianCombatModifier;

	int m_iStartingDefenseUnits;
	int m_iStartingWorkerUnits;
	int m_iStartingExploreUnits;
	int m_iAIStartingUnitMultiplier;					
	int m_iAIStartingDefenseUnits;				
	int m_iAIStartingWorkerUnits;					
	int m_iAIStartingExploreUnits;					
	int m_iBarbarianInitialDefenders;			
	int m_iAIDeclareWarProb;
	int m_iAIWorkRateModifier;
	int m_iAIGrowthPercent;
	int m_iAITrainPercent;
	int m_iAIWorldTrainPercent;
	int m_iAIConstructPercent;
	int m_iAIWorldConstructPercent;
	int m_iAICreatePercent;
	int m_iAIWorldCreatePercent;
	int m_iAICivicUpkeepPercent;
	int m_iAIUnitCostPercent;
	int m_iAIUnitSupplyPercent;
	int m_iAIUnitUpgradePercent;
	int m_iAIInflationPercent;
	int m_iAIWarWearinessPercent;
	int m_iAIPerEraModifier;
	int m_iAIAdvancedStartPercent;
	int m_iNumGoodies;

	CvString m_szHandicapName;

	// Arrays

	int* m_piGoodies;

	bool* m_pbFreeTechs;
	bool* m_pbAIFreeTechs;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGameSpeedInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameSpeedInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvGameSpeedInfo();
	virtual ~CvGameSpeedInfo();

	int getGrowthPercent() const;						// Exposed to Python
	int getTrainPercent() const;						// Exposed to Python
	int getConstructPercent() const;				// Exposed to Python
	int getCreatePercent() const;						// Exposed to Python
	int getResearchPercent() const;					// Exposed to Python
	int getBuildPercent() const;						// Exposed to Python
	int getImprovementPercent() const;			// Exposed to Python
	int getGreatPeoplePercent() const;			// Exposed to Python
	int getAnarchyPercent() const;					// Exposed to Python
	int getBarbPercent() const;							// Exposed to Python
	int getFeatureProductionPercent() const;				// Exposed to Python
	int getUnitDiscoverPercent() const;			// Exposed to Python
	int getUnitHurryPercent() const;				// Exposed to Python
	int getUnitTradePercent() const;				// Exposed to Python
	int getUnitGreatWorkPercent() const;		// Exposed to Python
	int getGoldenAgePercent() const;				// Exposed to Python
	int getHurryPercent() const;						// Exposed to Python
	int getHurryConscriptAngerPercent() const;	// Exposed to Python
	int getInflationOffset() const;					// Exposed to Python
	int getInflationPercent() const;				// Exposed to Python
	int getVictoryDelayPercent() const;				// Exposed to Python
	int getNumTurnIncrements() const;				// Exposed to Python

	GameTurnInfo& getGameTurnInfo(int iIndex) const;				// Exposed to Python
	void allocateGameTurnInfos(const int iSize);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iGrowthPercent;
	int m_iTrainPercent;
	int m_iConstructPercent;
	int m_iCreatePercent;
	int m_iResearchPercent;
	int m_iBuildPercent;
	int m_iImprovementPercent;
	int m_iGreatPeoplePercent;
	int m_iAnarchyPercent;
	int m_iBarbPercent;
	int m_iFeatureProductionPercent;
	int m_iUnitDiscoverPercent;
	int m_iUnitHurryPercent;
	int m_iUnitTradePercent;
	int m_iUnitGreatWorkPercent;
	int m_iGoldenAgePercent;
	int m_iHurryPercent;
	int m_iHurryConscriptAngerPercent;
	int m_iInflationOffset;
	int m_iInflationPercent;
	int m_iVictoryDelayPercent;
	int m_iNumTurnIncrements;

	CvString m_szGameSpeedName;
	GameTurnInfo* m_pGameTurnInfo;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTurnTimerInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTurnTimerInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTurnTimerInfo();
	virtual ~CvTurnTimerInfo();

	int getBaseTime() const;				// Exposed to Python
	int getCityBonus() const;				// Exposed to Python
	int getUnitBonus() const;				// Exposed to Python
	int getFirstTurnMultiplier() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iBaseTime;
	int m_iCityBonus;
	int m_iUnitBonus;
	int m_iFirstTurnMultiplier;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBuildInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBuildInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBuildInfo();
	virtual ~CvBuildInfo();

	int getTime() const;				// Exposed to Python
	int getCost() const;				// Exposed to Python
	int getTechPrereq() const;				// Exposed to Python
	int getImprovement() const;				// Exposed to Python
	int getRoute() const;				// Exposed to Python
	DllExport int getEntityEvent() const;				// Exposed to Python
	DllExport int getMissionType() const;				// Exposed to Python
	void setMissionType(int iNewType);

	bool isKill() const;				// Exposed to Python

	// Arrays

	int getFeatureTech(int i) const;				// Exposed to Python
	int getFeatureTime(int i) const;				// Exposed to Python
	int getFeatureProduction(int i) const;				// Exposed to Python

	bool isFeatureRemove(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iTime;					
	int m_iCost;					
	int m_iTechPrereq;		
	int m_iImprovement;	
	int m_iRoute;				
	int m_iEntityEvent;		
	int m_iMissionType;

	bool m_bKill;

	// Arrays

	int* m_paiFeatureTech;
	int* m_paiFeatureTime;
	int* m_paiFeatureProduction;

	bool* m_pabFeatureRemove;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGoodyInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGoodyInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvGoodyInfo();
	virtual ~CvGoodyInfo();

	int getGold() const;				// Exposed to Python
	int getGoldRand1() const;				// Exposed to Python
	int getGoldRand2() const;				// Exposed to Python
	int getMapOffset() const;				// Exposed to Python
	int getMapRange() const;				// Exposed to Python
	int getMapProb() const;				// Exposed to Python
	int getExperience() const;				// Exposed to Python
	int getHealing() const;				// Exposed to Python
	int getDamagePrereq() const;				// Exposed to Python
	int getBarbarianUnitProb() const;				// Exposed to Python
	int getMinBarbarians() const;				// Exposed to Python
	int getUnitClassType() const;				// Exposed to Python
	int getBarbarianUnitClass() const;				// Exposed to Python

	bool isTech() const;				// Exposed to Python
	bool isBad() const;				// Exposed to Python

	const TCHAR* getSound() const;				// Exposed to Python
	void setSound(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iGold;							
	int m_iGoldRand1;				
	int m_iGoldRand2;				
	int m_iMapOffset;					
	int m_iMapRange;				
	int m_iMapProb;					
	int m_iExperience;				
	int m_iHealing;						
	int m_iDamagePrereq;			
	int m_iBarbarianUnitProb;	
	int m_iMinBarbarians;			
	int m_iUnitClassType;			
	int m_iBarbarianUnitClass;	

	bool m_bTech;						
	bool m_bBad;						

	CvString m_szSound;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRouteInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRouteInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvRouteInfo();
	virtual ~CvRouteInfo();

	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python

	int getValue() const;								// Exposed to Python
	int getMovementCost() const;				// Exposed to Python
	int getFlatMovementCost() const;		// Exposed to Python
	int getPrereqBonus() const;					// Exposed to Python

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int getTechMovementChange(int i) const;				// Exposed to Python
	int getPrereqOrBonus(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;

	int m_iValue;
	int m_iMovementCost;
	int m_iFlatMovementCost;	
	int m_iPrereqBonus;

	// Arrays

	int* m_piYieldChange;
	int* m_piTechMovementChange;
	int* m_piPrereqOrBonuses;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvImprovementBonusInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvImprovementBonusInfo :
	public CvInfoBase
{

friend class CvImprovementInfo;
friend class CvXMLLoadUtility;

	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvImprovementBonusInfo();
	virtual ~CvImprovementBonusInfo();

	int getDiscoverRand() const;				// Exposed to Python

	bool isBonusMakesValid() const;				// Exposed to Python
	bool isBonusTrade() const;				// Exposed to Python

	int getYieldChange(int i) const;				// Exposed to Python
	
	// Serialize

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iDiscoverRand;

	bool m_bBonusMakesValid;
	bool m_bBonusTrade;

	// Arrays

	int* m_piYieldChange;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvImprovementInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoImprovement;
class CvImprovementInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvImprovementInfo();
	virtual ~CvImprovementInfo();

	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python

	int getTilesPerGoody() const;				// Exposed to Python
	int getGoodyUniqueRange() const;				// Exposed to Python
	int getFeatureGrowthProbability() const;				// Exposed to Python
	int getUpgradeTime() const;				// Exposed to Python
	int getAirBombDefense() const;				// Exposed to Python
	int getDefenseModifier() const;				// Exposed to Python
	int getHappiness() const;				// Exposed to Python
	int getPillageGold() const;				// Exposed to Python
	int getImprovementPillage() const;				// Exposed to Python
	void setImprovementPillage(int i);
	int getImprovementUpgrade() const;				// Exposed to Python
	void setImprovementUpgrade(int i);

	bool isActsAsCity() const;				// Exposed to Python
	bool isHillsMakesValid() const;				// Exposed to Python
	bool isFreshWaterMakesValid() const;				// Exposed to Python
	bool isRiverSideMakesValid() const;				// Exposed to Python
	bool isNoFreshWater() const;				// Exposed to Python
	bool isRequiresFlatlands() const;				// Exposed to Python
	DllExport bool isRequiresRiverSide() const;				// Exposed to Python
	bool isRequiresIrrigation() const;				// Exposed to Python
	bool isCarriesIrrigation() const;				// Exposed to Python
	bool isRequiresFeature() const;				// Exposed to Python
	bool isWater() const;				// Exposed to Python
	DllExport bool isGoody() const;				// Exposed to Python
	bool isPermanent() const;				// Exposed to Python
	bool isOutsideBorders() const;				// Exposed to Python

	const TCHAR* getArtDefineTag() const;
	void setArtDefineTag(const TCHAR* szVal);

	int getWorldSoundscapeScriptId() const;

	// Arrays

	int getPrereqNatureYield(int i) const;				// Exposed to Python
	int* getPrereqNatureYieldArray();			
	int getYieldChange(int i) const;				// Exposed to Python
	int* getYieldChangeArray();			
	int getRiverSideYieldChange(int i) const;				// Exposed to Python
	int* getRiverSideYieldChangeArray();			
	int getHillsYieldChange(int i) const;				// Exposed to Python
	int* getHillsYieldChangeArray();			
	int getIrrigatedYieldChange(int i) const;				// Exposed to Python
	int* getIrrigatedYieldChangeArray();				// For Moose - CvWidgetData XXX

	bool getTerrainMakesValid(int i) const;				// Exposed to Python
	bool getFeatureMakesValid(int i) const;				// Exposed to Python

	int getTechYieldChanges(int i, int j) const;				// Exposed to Python
	int* getTechYieldChangesArray(int i);
	int getRouteYieldChanges(int i, int j) const;				// Exposed to Python
	int* getRouteYieldChangesArray(int i);				// For Moose - CvWidgetData XXX

	int getImprovementBonusYield(int i, int j) const;				// Exposed to Python
	bool isImprovementBonusMakesValid(int i) const;				// Exposed to Python
	bool isImprovementBonusTrade(int i) const;				// Exposed to Python
	int getImprovementBonusDiscoverRand(int i) const;				// Exposed to Python
	
	// Other

	const TCHAR* getButton() const;
	DllExport const CvArtInfoImprovement* getArtInfo() const;

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);




	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;

	int m_iTilesPerGoody;
	int m_iGoodyUniqueRange;
	int m_iFeatureGrowthProbability;
	int m_iUpgradeTime;
	int m_iAirBombDefense;
	int m_iDefenseModifier;
	int m_iHappiness;
	int m_iPillageGold;
	int m_iImprovementPillage;
	int m_iImprovementUpgrade;

	bool m_bActsAsCity;				
	bool m_bHillsMakesValid;				
	bool m_bFreshWaterMakesValid;	
	bool m_bRiverSideMakesValid;	
	bool m_bNoFreshWater;				
	bool m_bRequiresFlatlands;							
	bool m_bRequiresRiverSide;		
	bool m_bRequiresIrrigation;		
	bool m_bCarriesIrrigation;			
	bool m_bRequiresFeature;
	bool m_bWater;							
	bool m_bGoody;
	bool m_bPermanent;
	bool m_bOutsideBorders;

	CvString m_szArtDefineTag;


	int m_iWorldSoundscapeScriptId;

	// Arrays

	int* m_piPrereqNatureYield;
	int* m_piYieldChange;
	int* m_piRiverSideYieldChange;
	int* m_piHillsYieldChange;
	int* m_piIrrigatedChange;

	bool* m_pbTerrainMakesValid;
	bool* m_pbFeatureMakesValid;

	int** m_ppiTechYieldChanges;
	int** m_ppiRouteYieldChanges;

	CvImprovementBonusInfo* m_paImprovementBonus;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBonusClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBonusClassInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBonusClassInfo();
	virtual ~CvBonusClassInfo();

	int getUniqueRange() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iUniqueRange; 

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBonusInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoBonus;
class CvBonusInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBonusInfo();
	virtual ~CvBonusInfo();

	int getBonusClassType() const;			// Exposed to Python
	int getChar() const;								// Exposed to Python
	void setChar(int i);								// Exposed to Python
	int getTechReveal() const;					// Exposed to Python
	int getTechCityTrade() const;				// Exposed to Python
	int getTechObsolete() const;				// Exposed to Python
	int getAITradeModifier() const;			// Exposed to Python
	int getAIObjective() const;			// Exposed to Python
	int getHealth() const;							// Exposed to Python
	int getHappiness() const;						// Exposed to Python
	int getMinAreaSize() const;					// Exposed to Python
	int getMinLatitude() const;					// Exposed to Python
	int getMaxLatitude() const;					// Exposed to Python
	int getPlacementOrder() const;			// Exposed to Python
	int getConstAppearance() const;			// Exposed to Python
	int getRandAppearance1() const;			// Exposed to Python
	int getRandAppearance2() const;			// Exposed to Python
	int getRandAppearance3() const;			// Exposed to Python
	int getRandAppearance4() const;			// Exposed to Python
	int getPercentPerPlayer() const;		// Exposed to Python
	int getTilesPer() const;						// Exposed to Python
	int getMinLandPercent() const;			// Exposed to Python
	int getUniqueRange() const;					// Exposed to Python
	int getGroupRange() const;					// Exposed to Python
	int getGroupRand() const;						// Exposed to Python

	bool isOneArea() const;							// Exposed to Python
	bool isHills() const;								// Exposed to Python
	bool isFlatlands() const;						// Exposed to Python
	bool isNoRiverSide() const;					// Exposed to Python
	bool isNormalize() const;						// Exposed to Python

	const TCHAR* getArtDefineTag() const;
	void setArtDefineTag(const TCHAR* szVal);

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int* getYieldChangeArray();				// Exposed to Python
	int getImprovementChange(int i) const;

	bool isTerrain(int i) const;				// Exposed to Python
	bool isFeature(int i) const;				// Exposed to Python
	bool isFeatureTerrain(int i) const;				// Exposed to Python

	// Other

	const TCHAR* getButton() const; // Exposed to Python
	DllExport const CvArtInfoBonus* getArtInfo() const; // Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------

protected:

	int m_iBonusClassType;
	int m_iChar;
	int m_iTechReveal;
	int m_iTechCityTrade;
	int m_iTechObsolete;
	int m_iAITradeModifier;
	int m_iAIObjective;
	int m_iHealth;
	int m_iHappiness;
	int m_iMinAreaSize;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iPlacementOrder;
	int m_iConstAppearance;
	int m_iRandAppearance1;
	int m_iRandAppearance2;
	int m_iRandAppearance3;
	int m_iRandAppearance4;
	int m_iPercentPerPlayer;
	int m_iTilesPer;
	int m_iMinLandPercent;
	int m_iUniqueRange;
	int m_iGroupRange;
	int m_iGroupRand;

	bool m_bOneArea;
	bool m_bHills;
	bool m_bFlatlands;
	bool m_bNoRiverSide;
	bool m_bNormalize;

	CvString m_szArtDefineTag;

	// Arrays

	int* m_piYieldChange;
	int* m_piImprovementChange;

	bool* m_pbTerrain;
	bool* m_pbFeature;
	bool* m_pbFeatureTerrain;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvFeatureInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoFeature;
class CvFeatureInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvFeatureInfo();
	virtual ~CvFeatureInfo();

	int getMovementCost() const;							// Exposed to Python
	int getSeeThroughChange() const;					// Exposed to Python
	int getHealthPercent() const;							// Exposed to Python
	int getAppearanceProbability() const;			// Exposed to Python
	int getDisappearanceProbability() const;	// Exposed to Python
	int getGrowthProbability() const;					// Exposed to Python
	int getDefenseModifier() const;						// Exposed to Python
	int getAdvancedStartRemoveCost() const;						// Exposed to Python
	int getTurnDamage() const;						// Exposed to Python
	
	bool isNoCoast() const;						// Exposed to Python
	bool isNoRiver() const;						// Exposed to Python
	bool isNoAdjacent() const;				// Exposed to Python
	bool isRequiresFlatlands() const;	// Exposed to Python
	bool isRequiresRiver() const;			// Exposed to Python
	bool isAddsFreshWater() const;		// Exposed to Python
	bool isImpassable() const;				// Exposed to Python
	bool isNoCity() const;						// Exposed to Python
	bool isNoImprovement() const;			// Exposed to Python
	bool isVisibleAlways() const;			// Exposed to Python
	bool isNukeImmune() const;			// Exposed to Python
	const TCHAR* getOnUnitChangeTo() const;

	const TCHAR* getArtDefineTag() const;			
	void setArtDefineTag(const TCHAR* szTag);			

	int getWorldSoundscapeScriptId() const;

	const TCHAR* getEffectType() const;
	int getEffectProbability() const;

	// Arrays

	int getYieldChange(int i) const;						// Exposed to Python
	int getRiverYieldChange(int i) const;				// Exposed to Python
	int getHillsYieldChange(int i) const;				// Exposed to Python
	int get3DAudioScriptFootstepIndex(int i) const;

	bool isTerrain(int i) const;								// Exposed to Python
	int getNumVarieties() const;

	// Other

	DllExport const CvArtInfoFeature* getArtInfo() const;
	const TCHAR* getButton() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMovementCost;
	int m_iSeeThroughChange;
	int m_iHealthPercent;
	int m_iAppearanceProbability;
	int m_iDisappearanceProbability;
	int m_iGrowthProbability;
	int m_iDefenseModifier;
	int m_iAdvancedStartRemoveCost;
	int m_iTurnDamage;
	
	bool m_bNoCoast;				
	bool m_bNoRiver;					
	bool m_bNoAdjacent;			
	bool m_bRequiresFlatlands;
	bool m_bRequiresRiver;
	bool m_bAddsFreshWater;	
	bool m_bImpassable;			
	bool m_bNoCity;					
	bool m_bNoImprovement;	
	bool m_bVisibleAlways;	
	bool m_bNukeImmune;	
	CvString m_szOnUnitChangeTo;

	int m_iWorldSoundscapeScriptId;

	CvString m_szEffectType;
	int m_iEffectProbability;

	// Arrays

	int* m_piYieldChange;
	int* m_piRiverYieldChange;
	int* m_piHillsYieldChange;
	int* m_pi3DAudioScriptFootstepIndex;

	bool* m_pbTerrain;

private:

	CvString m_szArtDefineTag;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCommerceInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCommerceInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCommerceInfo();
	virtual ~CvCommerceInfo();

	int getChar() const;				// Exposed to Python
	void setChar(int i);			
	int getInitialPercent() const;				// Exposed to Python
	int getInitialHappiness() const;				// Exposed to Python
	int getAIWeightPercent() const;				// Exposed to Python

	bool isFlexiblePercent() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;												
	int m_iInitialPercent;								
	int m_iInitialHappiness;							
	int m_iAIWeightPercent;							

	bool m_bFlexiblePercent;							

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvYieldInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvYieldInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvYieldInfo();
	virtual ~CvYieldInfo();

	int getChar() const;				// Exposed to Python
	void setChar(int i);			
	int getHillsChange() const;				// Exposed to Python
	int getPeakChange() const;				// Exposed to Python
	int getLakeChange() const;				// Exposed to Python
	int getCityChange() const;				// Exposed to Python
	int getPopulationChangeOffset() const;				// Exposed to Python
	int getPopulationChangeDivisor() const;				// Exposed to Python
	int getMinCity() const;				// Exposed to Python
	int getTradeModifier() const;				// Exposed to Python
	int getGoldenAgeYield() const;				// Exposed to Python
	int getGoldenAgeYieldThreshold() const;				// Exposed to Python
	int getAIWeightPercent() const;				// Exposed to Python
	int getColorType() const;				// Exposed to Python

	// Arrays

	const TCHAR* getSymbolPath(int i) const;			

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;										
	int m_iHillsChange;							
	int m_iPeakChange;
	int m_iLakeChange;
	int m_iCityChange;							
	int m_iPopulationChangeOffset;		
	int m_iPopulationChangeDivisor;		
	int m_iMinCity;									
	int m_iTradeModifier;						
	int m_iGoldenAgeYield;					
	int m_iGoldenAgeYieldThreshold;		
	int m_iAIWeightPercent;
	int m_iColorType;

	CvString* m_paszSymbolPath;

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTerrainInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoTerrain;
class CvTerrainInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTerrainInfo();
	virtual ~CvTerrainInfo();

	int getMovementCost() const;				// Exposed to Python
	int getSeeFromLevel() const;				// Exposed to Python
	int getSeeThroughLevel() const;			// Exposed to Python
	int getBuildModifier() const;				// Exposed to Python
	int getDefenseModifier() const;			// Exposed to Python

	bool isWater() const;								// Exposed to Python
	bool isImpassable() const;					// Exposed to Python
	bool isFound() const;								// Exposed to Python
	bool isFoundCoast() const;					// Exposed to Python
	bool isFoundFreshWater() const;			// Exposed to Python

	DllExport const TCHAR* getArtDefineTag() const;			
	void setArtDefineTag(const TCHAR* szTag);			

	int getWorldSoundscapeScriptId() const;

	// Arrays

	int getYield(int i) const;				// Exposed to Python
	int getRiverYieldChange(int i) const;				// Exposed to Python
	int getHillsYieldChange(int i) const;				// Exposed to Python
	int get3DAudioScriptFootstepIndex(int i) const;

	// Other

	const CvArtInfoTerrain* getArtInfo() const;
	const TCHAR* getButton() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMovementCost;			
	int m_iSeeFromLevel;			
	int m_iSeeThroughLevel;		
	int m_iBuildModifier;				
	int m_iDefenseModifier;	

	bool m_bWater;					
	bool m_bImpassable;
	bool m_bFound;
	bool m_bFoundCoast;
	bool m_bFoundFreshWater;

	int m_iWorldSoundscapeScriptId;

	// Arrays

	int* m_piYields;
	int* m_piRiverYieldChange;
	int* m_piHillsYieldChange;
	int* m_pi3DAudioScriptFootstepIndex;

private:

	CvString m_szArtDefineTag;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvInterfaceModeInfo (ADD to Python)
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvInterfaceModeInfo :
	public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvInterfaceModeInfo();
	DllExport virtual ~CvInterfaceModeInfo();

	DllExport int getCursorIndex() const;
	DllExport int getMissionType() const;

	DllExport bool getVisible() const;
	DllExport bool getGotoPlot() const;
	DllExport bool getHighlightPlot() const;
	DllExport bool getSelectType() const;
	DllExport bool getSelectAll() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCursorIndex;
	int m_iMissionType;

	bool m_bVisible;
	bool m_bGotoPlot;
	bool m_bHighlightPlot;
	bool m_bSelectType;
	bool m_bSelectAll;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAdvisorInfo (ADD to Python)
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAdvisorInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvAdvisorInfo();
	virtual ~CvAdvisorInfo();

	const TCHAR* getTexture() const;				// Exposed to Python
	void setTexture(const TCHAR* szVal);			
	int getNumCodes() const;
	int getEnableCode(uint uiCode) const;
	int getDisableCode(uint uiCode) const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
	CvString m_szTexture;
	std::vector< std::pair< int, int > > m_vctEnableDisableCodes;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvLeaderHeadInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoLeaderhead;
class CvLeaderHeadInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvLeaderHeadInfo();
	virtual ~CvLeaderHeadInfo();

	int getWonderConstructRand() const;				// Exposed to Python
	int getBaseAttitude() const;				// Exposed to Python
	int getBasePeaceWeight() const;				// Exposed to Python
	int getPeaceWeightRand() const;				// Exposed to Python
	int getWarmongerRespect() const;				// Exposed to Python
	int getEspionageWeight() const;				// Exposed to Python
	int getRefuseToTalkWarThreshold() const;				// Exposed to Python
	int getNoTechTradeThreshold() const;				// Exposed to Python
	int getTechTradeKnownPercent() const;				// Exposed to Python
	int getMaxGoldTradePercent() const;				// Exposed to Python
	int getMaxGoldPerTurnTradePercent() const;				// Exposed to Python
	int getMaxWarRand() const;				// Exposed to Python
	int getMaxWarNearbyPowerRatio() const;				// Exposed to Python
	int getMaxWarDistantPowerRatio() const;				// Exposed to Python
	int getMaxWarMinAdjacentLandPercent() const;				// Exposed to Python
	int getLimitedWarRand() const;				// Exposed to Python
	int getLimitedWarPowerRatio() const;				// Exposed to Python
	int getDogpileWarRand() const;				// Exposed to Python
	int getMakePeaceRand() const;				// Exposed to Python
	int getDeclareWarTradeRand() const;				// Exposed to Python
	int getDemandRebukedSneakProb() const;				// Exposed to Python
	int getDemandRebukedWarProb() const;				// Exposed to Python
	int getRazeCityProb() const;				// Exposed to Python
	int getBuildUnitProb() const;				// Exposed to Python
	int getBaseAttackOddsChange() const;				// Exposed to Python
	int getAttackOddsChangeRand() const;				// Exposed to Python
	int getWorseRankDifferenceAttitudeChange() const;				// Exposed to Python
	int getBetterRankDifferenceAttitudeChange() const;				// Exposed to Python
	int getCloseBordersAttitudeChange() const;				// Exposed to Python
	int getLostWarAttitudeChange() const;				// Exposed to Python
	int getAtWarAttitudeDivisor() const;				// Exposed to Python
	int getAtWarAttitudeChangeLimit() const;				// Exposed to Python
	int getAtPeaceAttitudeDivisor() const;				// Exposed to Python
	int getAtPeaceAttitudeChangeLimit() const;				// Exposed to Python
	int getSameReligionAttitudeChange() const;				// Exposed to Python
	int getSameReligionAttitudeDivisor() const;				// Exposed to Python
	int getSameReligionAttitudeChangeLimit() const;				// Exposed to Python
	int getDifferentReligionAttitudeChange() const;				// Exposed to Python
	int getDifferentReligionAttitudeDivisor() const;				// Exposed to Python
	int getDifferentReligionAttitudeChangeLimit() const;				// Exposed to Python
	int getBonusTradeAttitudeDivisor() const;				// Exposed to Python
	int getBonusTradeAttitudeChangeLimit() const;				// Exposed to Python
	int getOpenBordersAttitudeDivisor() const;				// Exposed to Python
	int getOpenBordersAttitudeChangeLimit() const;				// Exposed to Python
	int getDefensivePactAttitudeDivisor() const;				// Exposed to Python
	int getDefensivePactAttitudeChangeLimit() const;				// Exposed to Python
	int getShareWarAttitudeChange() const;				// Exposed to Python
	int getShareWarAttitudeDivisor() const;				// Exposed to Python
	int getShareWarAttitudeChangeLimit() const;				// Exposed to Python
	int getFavoriteCivicAttitudeChange() const;				// Exposed to Python
	int getFavoriteCivicAttitudeDivisor() const;				// Exposed to Python
	int getFavoriteCivicAttitudeChangeLimit() const;				// Exposed to Python
	int getDemandTributeAttitudeThreshold() const;				// Exposed to Python
	int getNoGiveHelpAttitudeThreshold() const;				// Exposed to Python
	int getTechRefuseAttitudeThreshold() const;				// Exposed to Python
	int getStrategicBonusRefuseAttitudeThreshold() const;				// Exposed to Python
	int getHappinessBonusRefuseAttitudeThreshold() const;				// Exposed to Python
	int getHealthBonusRefuseAttitudeThreshold() const;					// Exposed to Python
	int getMapRefuseAttitudeThreshold() const;									// Exposed to Python
	int getDeclareWarRefuseAttitudeThreshold() const;						// Exposed to Python
	int getDeclareWarThemRefuseAttitudeThreshold() const;				// Exposed to Python
	int getStopTradingRefuseAttitudeThreshold() const;					// Exposed to Python
	int getStopTradingThemRefuseAttitudeThreshold() const;			// Exposed to Python
	int getAdoptCivicRefuseAttitudeThreshold() const;						// Exposed to Python
	int getConvertReligionRefuseAttitudeThreshold() const;			// Exposed to Python
	int getOpenBordersRefuseAttitudeThreshold() const;					// Exposed to Python
	int getDefensivePactRefuseAttitudeThreshold() const;				// Exposed to Python
	int getPermanentAllianceRefuseAttitudeThreshold() const;		// Exposed to Python
	int getVassalRefuseAttitudeThreshold() const;				// Exposed to Python
	int getVassalPowerModifier() const;				// Exposed to Python
	int getFavoriteCivic() const;																// Exposed to Python
	int getFavoriteReligion() const;																// Exposed to Python
	int getFreedomAppreciation() const;																// Exposed to Python

	const TCHAR* getArtDefineTag() const;				// Exposed to Python
	void setArtDefineTag(const TCHAR* szVal);
	
	// Arrays

	bool hasTrait(int i) const;				// Exposed to Python

	int getFlavorValue(int i) const;				// Exposed to Python
	int getContactRand(int i) const;				// Exposed to Python
	int getContactDelay(int i) const;				// Exposed to Python
	int getMemoryDecayRand(int i) const;				// Exposed to Python
	int getMemoryAttitudePercent(int i) const;				// Exposed to Python
	int getNoWarAttitudeProb(int i) const;				// Exposed to Python
	int getUnitAIWeightModifier(int i) const;				// Exposed to Python
	int getImprovementWeightModifier(int i) const;				// Exposed to Python
	int getDiploPeaceIntroMusicScriptIds(int i) const;
	int getDiploPeaceMusicScriptIds(int i) const;
	int getDiploWarIntroMusicScriptIds(int i) const;
	int getDiploWarMusicScriptIds(int i) const;

	// Other

	DllExport const CvArtInfoLeaderhead* getArtInfo() const;
	const TCHAR* getLeaderHead() const;
	const TCHAR* getButton() const;

	void write(FDataStreamBase* stream);
	void read(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iWonderConstructRand;
	int m_iBaseAttitude;
	int m_iBasePeaceWeight;
	int m_iPeaceWeightRand;
	int m_iWarmongerRespect;
	int m_iEspionageWeight;
	int m_iRefuseToTalkWarThreshold;
	int m_iNoTechTradeThreshold;
	int m_iTechTradeKnownPercent;
	int m_iMaxGoldTradePercent;
	int m_iMaxGoldPerTurnTradePercent;
	int m_iMaxWarRand;
	int m_iMaxWarNearbyPowerRatio;
	int m_iMaxWarDistantPowerRatio;
	int m_iMaxWarMinAdjacentLandPercent;
	int m_iLimitedWarRand;
	int m_iLimitedWarPowerRatio;
	int m_iDogpileWarRand;
	int m_iMakePeaceRand;
	int m_iDeclareWarTradeRand;
	int m_iDemandRebukedSneakProb;
	int m_iDemandRebukedWarProb;
	int m_iRazeCityProb;
	int m_iBuildUnitProb;
	int m_iBaseAttackOddsChange;
	int m_iAttackOddsChangeRand;
	int m_iWorseRankDifferenceAttitudeChange;
	int m_iBetterRankDifferenceAttitudeChange;
	int m_iCloseBordersAttitudeChange;
	int m_iLostWarAttitudeChange;
	int m_iAtWarAttitudeDivisor;
	int m_iAtWarAttitudeChangeLimit;
	int m_iAtPeaceAttitudeDivisor;
	int m_iAtPeaceAttitudeChangeLimit;
	int m_iSameReligionAttitudeChange;
	int m_iSameReligionAttitudeDivisor;
	int m_iSameReligionAttitudeChangeLimit;
	int m_iDifferentReligionAttitudeChange;
	int m_iDifferentReligionAttitudeDivisor;
	int m_iDifferentReligionAttitudeChangeLimit;
	int m_iBonusTradeAttitudeDivisor;
	int m_iBonusTradeAttitudeChangeLimit;
	int m_iOpenBordersAttitudeDivisor;
	int m_iOpenBordersAttitudeChangeLimit;
	int m_iDefensivePactAttitudeDivisor;
	int m_iDefensivePactAttitudeChangeLimit;
	int m_iShareWarAttitudeChange;
	int m_iShareWarAttitudeDivisor;
	int m_iShareWarAttitudeChangeLimit;
	int m_iFavoriteCivicAttitudeChange;
	int m_iFavoriteCivicAttitudeDivisor;
	int m_iFavoriteCivicAttitudeChangeLimit;
	int m_iDemandTributeAttitudeThreshold;
	int m_iNoGiveHelpAttitudeThreshold;
	int m_iTechRefuseAttitudeThreshold;
	int m_iStrategicBonusRefuseAttitudeThreshold;
	int m_iHappinessBonusRefuseAttitudeThreshold;
	int m_iHealthBonusRefuseAttitudeThreshold;
	int m_iMapRefuseAttitudeThreshold;
	int m_iDeclareWarRefuseAttitudeThreshold;
	int m_iDeclareWarThemRefuseAttitudeThreshold;
	int m_iStopTradingRefuseAttitudeThreshold;
	int m_iStopTradingThemRefuseAttitudeThreshold;
	int m_iAdoptCivicRefuseAttitudeThreshold;
	int m_iConvertReligionRefuseAttitudeThreshold;
	int m_iOpenBordersRefuseAttitudeThreshold;
	int m_iDefensivePactRefuseAttitudeThreshold;
	int m_iPermanentAllianceRefuseAttitudeThreshold;
	int m_iVassalRefuseAttitudeThreshold;
	int m_iVassalPowerModifier;
	int m_iFreedomAppreciation;
	int m_iFavoriteCivic;
	int m_iFavoriteReligion;

	CvString m_szArtDefineTag;

	// Arrays

	bool* m_pbTraits;

	int* m_piFlavorValue;
	int* m_piContactRand;
	int* m_piContactDelay;
	int* m_piMemoryDecayRand;
	int* m_piMemoryAttitudePercent;
	int* m_piNoWarAttitudeProb;
	int* m_piUnitAIWeightModifier;
	int* m_piImprovementWeightModifier;
	int* m_piDiploPeaceIntroMusicScriptIds;
	int* m_piDiploPeaceMusicScriptIds;
	int* m_piDiploWarIntroMusicScriptIds;
	int* m_piDiploWarMusicScriptIds;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvWorldInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvWorldInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvWorldInfo();
	virtual ~CvWorldInfo();

	DllExport int getDefaultPlayers() const;				// Exposed to Python
	int getUnitNameModifier() const;				// Exposed to Python
	int getTargetNumCities() const;				// Exposed to Python
	int getNumFreeBuildingBonuses() const;				// Exposed to Python
	int getBuildingClassPrereqModifier() const;				// Exposed to Python
	int getMaxConscriptModifier() const;				// Exposed to Python
	int getWarWearinessModifier() const;				// Exposed to Python
	int getGridWidth() const;				// Exposed to Python
	int getGridHeight() const;				// Exposed to Python
	int getTerrainGrainChange() const;				// Exposed to Python
	int getFeatureGrainChange() const;				// Exposed to Python
	int getResearchPercent() const;				// Exposed to Python
	int getTradeProfitPercent() const;				// Exposed to Python
	int getDistanceMaintenancePercent() const;				// Exposed to Python
	int getNumCitiesMaintenancePercent() const;				// Exposed to Python
	int getColonyMaintenancePercent() const;				// Exposed to Python
	int getCorporationMaintenancePercent() const;				// Exposed to Python
	int getNumCitiesAnarchyPercent() const;				// Exposed to Python
	int getAdvancedStartPointsMod() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iDefaultPlayers;
	int m_iUnitNameModifier;
	int m_iTargetNumCities;
	int m_iNumFreeBuildingBonuses;
	int m_iBuildingClassPrereqModifier;
	int m_iMaxConscriptModifier;
	int m_iWarWearinessModifier;
	int m_iGridWidth;
	int m_iGridHeight;
	int m_iTerrainGrainChange;
	int m_iFeatureGrainChange;
	int m_iResearchPercent;
	int m_iTradeProfitPercent;
	int m_iDistanceMaintenancePercent;
	int m_iNumCitiesMaintenancePercent;
	int m_iColonyMaintenancePercent;
	int m_iCorporationMaintenancePercent;
	int m_iNumCitiesAnarchyPercent;
	int m_iAdvancedStartPointsMod;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvClimateInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvClimateInfo :	public CvInfoBase
{
public:

	CvClimateInfo();
	virtual ~CvClimateInfo();

	int getDesertPercentChange() const;							// Exposed to Python
	int getJungleLatitude() const;									// Exposed to Python
	int getHillRange() const;												// Exposed to Python
	int getPeakPercent() const;											// Exposed to Python

	float getSnowLatitudeChange() const;						// Exposed to Python
	float getTundraLatitudeChange() const;					// Exposed to Python
	float getGrassLatitudeChange() const;						// Exposed to Python
	float getDesertBottomLatitudeChange() const;		// Exposed to Python
	float getDesertTopLatitudeChange() const;				// Exposed to Python
	float getIceLatitude() const;										// Exposed to Python
	float getRandIceLatitude() const;								// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:

	int m_iDesertPercentChange;
	int m_iJungleLatitude;
	int m_iHillRange;
	int m_iPeakPercent;

	float m_fSnowLatitudeChange;
	float m_fTundraLatitudeChange;
	float m_fGrassLatitudeChange;
	float m_fDesertBottomLatitudeChange;
	float m_fDesertTopLatitudeChange;
	float m_fIceLatitude;
	float m_fRandIceLatitude;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvSeaLevelInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSeaLevelInfo :	public CvInfoBase
{
public:

	CvSeaLevelInfo();
	virtual ~CvSeaLevelInfo();

	int getSeaLevelChange() const;		// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:

	int m_iSeaLevelChange;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvProcessInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvProcessInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvProcessInfo();
	virtual ~CvProcessInfo();

	int getTechPrereq() const;				// Exposed to Python

	// Arrays

	int getProductionToCommerceModifier(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iTechPrereq;

	// Arrays

	int* m_paiProductionToCommerceModifier;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvVoteInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVoteInfo :	public CvInfoBase
{
public:
	CvVoteInfo();
	virtual ~CvVoteInfo();

	int getPopulationThreshold() const;	// Exposed to Python
	int getStateReligionVotePercent() const;	// Exposed to Python
	int getTradeRoutes() const;					// Exposed to Python
	int getMinVoters() const;					// Exposed to Python

	bool isSecretaryGeneral() const;		// Exposed to Python
	bool isVictory() const;							// Exposed to Python
	bool isFreeTrade() const;						// Exposed to Python
	bool isNoNukes() const;							// Exposed to Python
	bool isCityVoting() const;	// Exposed to Python
	bool isCivVoting() const;	// Exposed to Python
	bool isDefensivePact() const;	// Exposed to Python
	bool isOpenBorders() const;	// Exposed to Python
	bool isForcePeace() const;	// Exposed to Python
	bool isForceNoTrade() const;	// Exposed to Python
	bool isForceWar() const;	// Exposed to Python
	bool isAssignCity() const;	// Exposed to Python

	// Arrays

	bool isForceCivic(int i) const;			// Exposed to Python
	bool isVoteSourceType(int i) const;			// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:

	int m_iPopulationThreshold;
	int m_iStateReligionVotePercent;
	int m_iTradeRoutes;
	int m_iMinVoters;

	bool m_bSecretaryGeneral;
	bool m_bVictory;
	bool m_bFreeTrade;
	bool m_bNoNukes;
	bool m_bCityVoting;
	bool m_bCivVoting;
	bool m_bDefensivePact;
	bool m_bOpenBorders;
	bool m_bForcePeace;
	bool m_bForceNoTrade;
	bool m_bForceWar;
	bool m_bAssignCity;

	// Arrays

	bool* m_pbForceCivic;
	bool* m_abVoteSourceTypes;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvProjectInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvProjectInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvProjectInfo();
	virtual ~CvProjectInfo();

	int getVictoryPrereq() const;									// Exposed to Python
	int getTechPrereq() const;										// Exposed to Python
	int getAnyoneProjectPrereq() const;						// Exposed to Python
	void setAnyoneProjectPrereq(int i);
	int getMaxGlobalInstances() const;						// Exposed to Python
	int getMaxTeamInstances() const;							// Exposed to Python
	int getProductionCost() const;								// Exposed to Python
	int getNukeInterception() const;							// Exposed to Python
	int getTechShare() const;											// Exposed to Python
	int getEveryoneSpecialUnit() const;						// Exposed to Python
	int getEveryoneSpecialBuilding() const;				// Exposed to Python
	int getVictoryDelayPercent() const;				// Exposed to Python
	int getSuccessRate() const;				// Exposed to Python

	bool isSpaceship() const;											// Exposed to Python
	bool isAllowsNukes() const;											// Exposed to Python
	const char* getMovieArtDef() const;						// Exposed to Python

	const TCHAR* getCreateSound() const;					// Exposed to Python
	void setCreateSound(const TCHAR* szVal);

	// Arrays

	int getBonusProductionModifier(int i) const;	// Exposed to Python
	int getVictoryThreshold(int i) const;					// Exposed to Python
	int getVictoryMinThreshold(int i) const;					// Exposed to Python
	int getProjectsNeeded(int i) const;						// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iVictoryPrereq;
	int m_iTechPrereq;
	int m_iAnyoneProjectPrereq;
	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iProductionCost;
	int m_iNukeInterception;
	int m_iTechShare;
	int m_iEveryoneSpecialUnit;
	int m_iEveryoneSpecialBuilding;
	int m_iVictoryDelayPercent;
	int m_iSuccessRate;

	bool m_bSpaceship;
	bool m_bAllowsNukes;

	CvString m_szCreateSound;
	CvString m_szMovieArtDef;

	// Arrays

	int* m_piBonusProductionModifier;
	int* m_piVictoryThreshold;
	int* m_piVictoryMinThreshold;
	int* m_piProjectsNeeded;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvReligionInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvReligionInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE----------------------------------------
public:

	CvReligionInfo();
	virtual ~CvReligionInfo();

	int getChar() const;								// Exposed to Python
	void setChar(int i);			
	int getHolyCityChar() const;				// Exposed to Python
	void setHolyCityChar(int i);			
	int getTechPrereq() const;					// Exposed to Python
	int getFreeUnitClass() const;				// Exposed to Python
	int getNumFreeUnits() const;				// Exposed to Python
	int getSpreadFactor() const;				// Exposed to Python
	int getMissionType() const;					// Exposed to Python
	void setMissionType(int iNewType);

	const TCHAR* getTechButton() const;				// Exposed to Python
	void setTechButton(const TCHAR* szVal);	
	const TCHAR* getGenericTechButton() const;				// Exposed to Python
	void setGenericTechButton(const TCHAR* szVal);	
	const TCHAR* getMovieFile() const;				// Exposed to Python
	void setMovieFile(const TCHAR* szVal);	
	const TCHAR* getMovieSound() const;				// Exposed to Python
	void setMovieSound(const TCHAR* szVal);	
	const TCHAR* getSound() const;						// Exposed to Python
	void setSound(const TCHAR* szVal);			

	const TCHAR* getButtonDisabled() const;		//	Exposed to Python

	void setAdjectiveKey(const TCHAR* szVal);
	const wchar* getAdjectiveKey() const;				// Exposed to Python
	std::wstring pyGetAdjectiveKey() { return getAdjectiveKey(); }				// Exposed to Python

	// Arrays

	int getGlobalReligionCommerce(int i) const;		// Exposed to Python
	int* getGlobalReligionCommerceArray() const;			
	int getHolyCityCommerce(int i) const;					// Exposed to Python
	int* getHolyCityCommerceArray() const;
	int getStateReligionCommerce(int i) const;		// Exposed to Python
	int* getStateReligionCommerceArray() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;					
	int m_iHolyCityChar;	
	int m_iTechPrereq;
	int m_iFreeUnitClass;
	int m_iNumFreeUnits;
	int m_iSpreadFactor;
	int m_iMissionType;

	CvString m_szTechButton;
	CvString m_szGenericTechButton;
	CvString m_szMovieFile;
	CvString m_szMovieSound;
	CvString m_szSound;
	CvWString m_szAdjectiveKey;

	// Arrays

	int* m_paiGlobalReligionCommerce;		
	int* m_paiHolyCityCommerce;
	int* m_paiStateReligionCommerce;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCorporationInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCorporationInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE----------------------------------------
public:

	CvCorporationInfo();
	virtual ~CvCorporationInfo();

	int getChar() const;								// Exposed to Python
	void setChar(int i);			
	int getHeadquarterChar() const;				// Exposed to Python
	void setHeadquarterChar(int i);			
	int getTechPrereq() const;					// Exposed to Python
	int getFreeUnitClass() const;				// Exposed to Python
	int getSpreadFactor() const;				// Exposed to Python
	int getSpreadCost() const;				// Exposed to Python
	int getMaintenance() const;				// Exposed to Python
	int getMissionType() const;					// Exposed to Python
	void setMissionType(int iNewType);

	int getBonusProduced() const;					// Exposed to Python

	const TCHAR* getMovieFile() const;				// Exposed to Python
	void setMovieFile(const TCHAR* szVal);	
	const TCHAR* getMovieSound() const;				// Exposed to Python
	void setMovieSound(const TCHAR* szVal);	
	const TCHAR* getSound() const;						// Exposed to Python
	void setSound(const TCHAR* szVal);			

	// Arrays

	int getPrereqBonus(int i) const;					// Exposed to Python
	int getHeadquarterCommerce(int i) const;					// Exposed to Python
	int* getHeadquarterCommerceArray() const;
	int getCommerceProduced(int i) const;					// Exposed to Python
	int* getCommerceProducedArray() const;
	int getYieldProduced(int i) const;					// Exposed to Python
	int* getYieldProducedArray() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;					
	int m_iHeadquarterChar;	
	int m_iTechPrereq;
	int m_iFreeUnitClass;
	int m_iSpreadFactor;
	int m_iSpreadCost;
	int m_iMaintenance;
	int m_iMissionType;
	int m_iBonusProduced;

	CvString m_szMovieFile;
	CvString m_szMovieSound;
	CvString m_szSound;

	// Arrays

	int* m_paiPrereqBonuses;
	int* m_paiHeadquarterCommerce;
	int* m_paiCommerceProduced;
	int* m_paiYieldProduced;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTraitInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTraitInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTraitInfo();
	virtual ~CvTraitInfo();

	int getHealth() const;				// Exposed to Python
	int getHappiness() const;				// Exposed to Python
	int getMaxAnarchy() const;				// Exposed to Python
	int getUpkeepModifier() const;				// Exposed to Python
	int getLevelExperienceModifier() const;				// Exposed to Python
	int getGreatPeopleRateModifier() const;				// Exposed to Python
	int getGreatGeneralRateModifier() const;				// Exposed to Python
	int getDomesticGreatGeneralRateModifier() const;				// Exposed to Python
	int getMaxGlobalBuildingProductionModifier() const;				// Exposed to Python
	int getMaxTeamBuildingProductionModifier() const;				// Exposed to Python
	int getMaxPlayerBuildingProductionModifier() const;				// Exposed to Python

	const TCHAR* getShortDescription() const;				// Exposed to Python
	void setShortDescription(const TCHAR* szVal);			

	// Arrays

	int getExtraYieldThreshold(int i) const;				// Exposed to Python
	int getTradeYieldModifier(int i) const;				// Exposed to Python
	int getCommerceChange(int i) const;				// Exposed to Python
	int getCommerceModifier(int i) const;				// Exposed to Python

	int isFreePromotion(int i) const;				// Exposed to Python
	int isFreePromotionUnitCombat(int i) const;			

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iHealth;													
	int m_iHappiness;
	int m_iMaxAnarchy;											
	int m_iUpkeepModifier;									
	int m_iLevelExperienceModifier;									
	int m_iGreatPeopleRateModifier;						
	int m_iGreatGeneralRateModifier;						
	int m_iDomesticGreatGeneralRateModifier;						
	int m_iMaxGlobalBuildingProductionModifier;	
	int m_iMaxTeamBuildingProductionModifier;		
	int m_iMaxPlayerBuildingProductionModifier;	

	CvString m_szShortDescription;

	// Arrays

	int* m_paiExtraYieldThreshold;
	int* m_paiTradeYieldModifier;
	int* m_paiCommerceChange;
	int* m_paiCommerceModifier;

	bool* m_pabFreePromotion;
	bool* m_pabFreePromotionUnitCombat;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCursorInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCursorInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCursorInfo();
	virtual ~CvCursorInfo();

	DllExport const TCHAR* getPath();				// Exposed to Python
	void setPath(const TCHAR* szVal);			

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szPath;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvThroneRoomCamera
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomCamera : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvThroneRoomCamera();
	virtual ~CvThroneRoomCamera();

	DllExport const TCHAR* getFileName();
	void setFileName(const TCHAR* szVal);			

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szFileName;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvThroneRoomInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvThroneRoomInfo();
	DllExport virtual ~CvThroneRoomInfo();

	DllExport const TCHAR* getEvent();
	DllExport void setEvent(const TCHAR* szVal);			
	DllExport const TCHAR* getNodeName();
	DllExport void setNodeName(const TCHAR* szVal);			
	DllExport int getFromState();
	DllExport void setFromState(int iVal);			
	DllExport int getToState();
	DllExport void setToState(int iVal);			
	DllExport int getAnimation();
	DllExport void setAnimation(int iVal);			

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iFromState;
	int m_iToState;
	int m_iAnimation;
	CvString m_szEvent;
	CvString m_szNodeName;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvThroneRoomStyleInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomStyleInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvThroneRoomStyleInfo();
	DllExport virtual ~CvThroneRoomStyleInfo();

	DllExport const TCHAR* getArtStyleType();
	DllExport void setArtStyleType(const TCHAR* szVal);	
	DllExport const TCHAR* getEraType();
	DllExport void setEraType(const TCHAR* szVal);	
	DllExport const TCHAR* getFileName();
	DllExport void setFileName(const TCHAR* szVal);	

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szArtStyleType;
	CvString m_szEraType;
	CvString m_szFileName;
	std::vector<CvString> m_aNodeNames;
	std::vector<CvString> m_aTextureNames;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSlideShowInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSlideShowInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSlideShowInfo();
	DllExport virtual ~CvSlideShowInfo();

	DllExport const TCHAR* getPath();
	DllExport void setPath(const TCHAR* szVal);			
	DllExport const TCHAR* getTransitionType();
	DllExport void setTransitionType(const TCHAR* szVal);			
	DllExport float getStartTime();
	DllExport void setStartTime(float fVal);			

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	float m_fStartTime;
	CvString m_szPath;
	CvString m_szTransitionType;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSlideShowRandomInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSlideShowRandomInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSlideShowRandomInfo();
	DllExport virtual ~CvSlideShowRandomInfo();

	DllExport const TCHAR* getPath();
	DllExport void setPath(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szPath;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvWorldPickerInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvWorldPickerInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvWorldPickerInfo();
	DllExport virtual ~CvWorldPickerInfo();

	DllExport const TCHAR* getMapName();
	DllExport void setMapName(const TCHAR* szVal);
	DllExport const TCHAR* getModelFile();
	DllExport void setModelFile(const TCHAR* szVal);	
	DllExport int getNumSizes();
	DllExport float getSize(int index);
	DllExport int getNumClimates();
	DllExport const TCHAR* getClimatePath(int index);
	DllExport int getNumWaterLevelDecals();
	DllExport const TCHAR* getWaterLevelDecalPath(int index);
	DllExport int getNumWaterLevelGloss();
	DllExport const TCHAR* getWaterLevelGlossPath(int index);

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szMapName;
	CvString m_szModelFile;
	std::vector<float> m_aSizes;
	std::vector<CvString> m_aClimates;
	std::vector<CvString> m_aWaterLevelDecals;
	std::vector<CvString> m_aWaterLevelGloss;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpaceShipInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpaceShipInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSpaceShipInfo();
	DllExport virtual ~CvSpaceShipInfo();

	DllExport const TCHAR* getNodeName();
	DllExport void setNodeName(const TCHAR* szVal);
	DllExport const TCHAR* getProjectName();
	DllExport void setProjectName(const TCHAR* szVal);
	DllExport ProjectTypes getProjectType();
	DllExport AxisTypes getCameraUpAxis();
	DllExport SpaceShipInfoTypes getSpaceShipInfoType();
	DllExport int getPartNumber();
	DllExport int getArtType();
	DllExport int getEventCode();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szNodeName;
	CvString m_szProjectName;
	ProjectTypes m_eProjectType;
	AxisTypes m_eCameraUpAxis;
	int m_iPartNumber;
	int m_iArtType;
	int m_iEventCode;
	SpaceShipInfoTypes m_eSpaceShipInfoType;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAnimationInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
typedef std::vector<std::pair<int,float> > CvAnimationPathDefinition;
typedef std::pair<int,int >			CvAnimationCategoryDefinition;

class CvAnimationPathInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		DllExport CvAnimationPathInfo();
		DllExport virtual ~CvAnimationPathInfo();

		DllExport int getPathCategory( int i );
		DllExport float getPathParameter( int i );
		DllExport int getNumPathDefinitions();
		DllExport CvAnimationPathDefinition * getPath( );
		DllExport bool isMissionPath() const;

		bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PRIVATE MEMBER VARIABLES---------------------------------
	private:

		CvAnimationPathDefinition 	m_vctPathDefinition;	//!< Animation path definitions, pair(category,param).
		bool						m_bMissionPath;			//!< True if this animation is used in missions
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAnimationInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAnimationCategoryInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		DllExport CvAnimationCategoryInfo();
		DllExport virtual ~CvAnimationCategoryInfo();

		DllExport int getCategoryBaseID( );
		DllExport int getCategoryDefaultTo( );

		bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PRIVATE MEMBER VARIABLES---------------------------------
	private:

		CvAnimationCategoryDefinition	m_kCategory;		//!< The pair(base IDs, default categories) defining the animation categories
		CvString						m_szDefaultTo;		//!< Holds the default to parameter, until all categories are read
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEntityEventInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEntityEventInfo : public CvInfoBase
{
		//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		DllExport CvEntityEventInfo();
		DllExport virtual ~CvEntityEventInfo();

		bool read(CvXMLLoadUtility* pXML);

		DllExport AnimationPathTypes getAnimationPathType(int iIndex = 0) const;
		DllExport EffectTypes getEffectType(int iIndex = 0) const;
		DllExport int getAnimationPathCount() const;
		DllExport int getEffectTypeCount() const;

		DllExport bool getUpdateFormation() const;

		//---------------------------------------PRIVATE MEMBER VARIABLES---------------------------------
	private:

		std::vector<AnimationPathTypes>	m_vctAnimationPathType;
		std::vector<EffectTypes>		m_vctEffectTypes;
		bool							m_bUpdateFormation;
};

// The below classes are for the ArtFile Management
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  classes : CvArtInfos
//
// This is also an abstract BASE class
//
//  DESC:  Used to store data from Art\Civ4ArtDefines.xml
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAssetInfoBase : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvAssetInfoBase()  {}
	DllExport virtual ~CvAssetInfoBase() {}

	DllExport const TCHAR* getTag() const;				// Exposed to Python
	DllExport void setTag(const TCHAR* szDesc);				// Exposed to Python
	
	DllExport const TCHAR* getPath() const;				// Exposed to Python
	DllExport void setPath(const TCHAR* szDesc);				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szPath;

};

class CvArtInfoAsset : 	public CvAssetInfoBase
{
public:

	DllExport CvArtInfoAsset() {}
	DllExport virtual ~CvArtInfoAsset() {}

	DllExport const TCHAR* getNIF() const;				// Exposed to Python
	DllExport const TCHAR* getKFM() const;				// Exposed to Python
	
	DllExport void setNIF(const TCHAR* szDesc);				// Exposed to Python
	DllExport void setKFM(const TCHAR* szDesc);				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szKFM;
	CvString m_szNIF;
};

//
//////////////////////////////////////////////////////////////////////////
// Another base class
//////////////////////////////////////////////////////////////////////////

class CvArtInfoScalableAsset : 
	public CvArtInfoAsset,
	public CvScalableInfo
{
public:

	bool read(CvXMLLoadUtility* pXML);

};

// todoJS: Remove empty classes if additional items are not added

class CvArtInfoInterface : 	public CvArtInfoAsset
{
public:

	DllExport CvArtInfoInterface() {}
	DllExport virtual ~CvArtInfoInterface() {}

};

class CvArtInfoMisc : 	public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoMisc() {}
	DllExport virtual ~CvArtInfoMisc() {}

};

class CvArtInfoMovie : 	public CvArtInfoAsset
{
public:

	DllExport CvArtInfoMovie() {}
	DllExport virtual ~CvArtInfoMovie() {}

};

class CvArtInfoUnit : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoUnit();
	DllExport virtual ~CvArtInfoUnit();

	DllExport bool getActAsRanged() const;
	DllExport bool getActAsLand() const;
	DllExport bool getActAsAir() const;

	DllExport const TCHAR* getShaderNIF() const;
	DllExport void setShaderNIF(const TCHAR* szDesc);

	DllExport const TCHAR* getShadowNIF() const;
	DllExport float getShadowScale() const;
	DllExport const TCHAR* getShadowAttachNode() const;
	DllExport int getDamageStates() const;

	DllExport const TCHAR* getTrailTexture() const;
	DllExport float getTrailWidth() const;
	DllExport float getTrailLength() const;
	DllExport float getTrailTaper() const;
	DllExport float getTrailFadeStarTime() const;
	DllExport float getTrailFadeFalloff() const;

	DllExport float getBattleDistance() const;
	DllExport float getRangedDeathTime() const;
	DllExport float getExchangeAngle() const;
	DllExport bool getCombatExempt() const;
	DllExport bool getSmoothMove() const;
	DllExport float getAngleInterpRate() const;
	DllExport float getBankRate() const;

	bool read(CvXMLLoadUtility* pXML);

	DllExport const TCHAR* getTrainSound() const;
	DllExport void setTrainSound(const TCHAR* szVal);
	DllExport int getRunLoopSoundTag() const;
	DllExport int getRunEndSoundTag() const;
	DllExport int getPatrolSoundTag() const;
	DllExport int getSelectionSoundScriptId() const;
	DllExport int getActionSoundScriptId() const;

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
	CvString m_szShaderNIF;		//!< The NIF used if the graphics card supports shaders
	CvString m_szShadowNIF;		//!< The shadow blob NIF to use for the unit
	CvString m_szShadowAttach;	//!< The name of the node to which the shadow takes its x,y position

	float m_fShadowScale;		//!< the scale of the unit's shadow.

	int m_iDamageStates;		//!< The maximum number of damage states this unit type supports
	bool m_bActAsRanged;		//!< true if the unit acts as a ranged unit in combat (but may or may not be actually a ranged unit)
	bool m_bActAsLand;
	bool m_bActAsAir;
	bool m_bCombatExempt;		//!< true if the unit is 'exempt' from combat - ie. it just flees instead of dying
	bool m_bSmoothMove;			//!< true if the unit should do non-linear interpolation for moves

	CvString m_szTrailTexture;	//!< The trail texture of the unit
	float m_fTrailWidth;		//!< The width of the trail
	float m_fTrailLength;		//!< The length of the trail
	float m_fTrailTaper;		//!< Tapering of the trail
	float m_fTrailFadeStartTime;//!< Time after which the trail starts to fade
	float m_fTrailFadeFalloff;	//!< Speed at which the fade happens

	float m_fBattleDistance;	//!< The preferred attack distance of this unit (1.0 == plot size)
	float m_fRangedDeathTime;	//!< The offset from firing in which an opponent should die
	float m_fExchangeAngle;		//!< The angle at which the unit does combat.
	float m_fAngleInterRate;	//!< The rate at which the units' angle interpolates
	float m_fBankRate;

	CvString m_szTrainSound;
	int m_iRunLoopSoundTag;
	int m_iRunEndSoundTag;
	int m_iPatrolSoundTag;
	int m_iSelectionSoundScriptId;
	int m_iActionSoundScriptId;
};

class CvArtInfoBuilding : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoBuilding();
	DllExport virtual ~CvArtInfoBuilding();

	DllExport bool isAnimated() const;				// Exposed to Python
	DllExport const TCHAR* getLSystemName() const;

	bool read(CvXMLLoadUtility* pXML);

protected:

	bool m_bAnimated;
	CvString m_szLSystemName;

};

class CvArtInfoCivilization : public CvArtInfoAsset
{
public:

	DllExport CvArtInfoCivilization();
	DllExport virtual ~CvArtInfoCivilization();

	DllExport bool isWhiteFlag() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:

	bool m_bWhiteFlag;

};

class CvArtInfoLeaderhead : public CvArtInfoAsset
{
public:

	DllExport CvArtInfoLeaderhead() {}
	DllExport virtual ~CvArtInfoLeaderhead() {}

	DllExport const TCHAR* getNoShaderNIF() const;
	DllExport void setNoShaderNIF(const TCHAR* szNIF);
	DllExport const TCHAR* getBackgroundKFM() const;
	DllExport void setBackgroundKFM( const TCHAR* szKFM);

	bool read(CvXMLLoadUtility* pXML);

protected:

	CvString m_szNoShaderNIF;
	CvString m_szBackgroundKFM;
};

class CvArtInfoBonus : public CvArtInfoScalableAsset
{
public:
	DllExport CvArtInfoBonus();
	DllExport virtual ~CvArtInfoBonus() {}

	DllExport int getFontButtonIndex() const;

	DllExport const TCHAR* getShaderNIF() const;
	DllExport void setShaderNIF(const TCHAR* szDesc);

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szShaderNIF;		//!< The NIF used if the graphics card supports shaders
	int m_iFontButtonIndex;
};

class CvArtInfoImprovement : public CvArtInfoScalableAsset 
{
public:

	DllExport CvArtInfoImprovement();
	DllExport virtual ~CvArtInfoImprovement();

	DllExport const TCHAR* getShaderNIF() const;
	DllExport void setShaderNIF(const TCHAR* szDesc);

	DllExport bool isExtraAnimations() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

protected:
	CvString m_szShaderNIF;		//!< The NIF used if the graphics card supports shaders

	bool m_bExtraAnimations;

};

typedef std::vector<std::pair<int, int> > CvTextureBlendSlotList;

class CvArtInfoTerrain : public CvArtInfoAsset
{
public:

	DllExport CvArtInfoTerrain();
	DllExport virtual ~CvArtInfoTerrain();

	DllExport const TCHAR* getBaseTexture();			
	DllExport void setBaseTexture(const TCHAR* szTmp );			
	DllExport const TCHAR* getGridTexture();			
	DllExport void setGridTexture(const TCHAR* szTmp );			
	DllExport const TCHAR* getDetailTexture();			
	DllExport void setDetailTexture(const TCHAR* szTmp);
	DllExport int getLayerOrder();
	DllExport bool useAlphaShader();
	DllExport CvTextureBlendSlotList &getBlendList(int blendMask);

	bool read(CvXMLLoadUtility* pXML);

protected:

	CvString m_szDetailTexture;				//!< Detail texture associated with the Terrain base texture
	CvString m_szGridTexture;

	int m_iLayerOrder;									//!< Layering order of texture
	bool m_bAlphaShader;						
	int m_numTextureBlends;						//!< number to blend textures. 
	CvTextureBlendSlotList  **m_pTextureSlots;	//!< Array of Textureslots per blend tile
};

class CvArtInfoFeature : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoFeature();
	DllExport virtual ~CvArtInfoFeature();

	DllExport bool isAnimated() const;				// Exposed to Python
	DllExport bool isRiverArt() const;				// Exposed to Python
	DllExport TileArtTypes getTileArtType() const;	
	DllExport LightTypes getLightType() const;

	bool read(CvXMLLoadUtility* pXML);

	class FeatureArtModel
	{
	public:
		FeatureArtModel(const CvString &modelFile, RotationTypes rotation)
		{
			m_szModelFile = modelFile;
			m_eRotation = rotation;
		}

		const CvString &getModelFile() const
		{
			return m_szModelFile;
		}

		RotationTypes getRotation() const
		{
			return m_eRotation;
		}

	private:
		CvString m_szModelFile;
		RotationTypes m_eRotation;
	};

	class FeatureArtPiece
	{
	public:
		FeatureArtPiece(int connectionMask)
		{
			m_iConnectionMask = connectionMask;
		}

		int getConnectionMask() const
		{
			return m_iConnectionMask;
		}

		int getNumArtModels() const
		{
			return m_aArtModels.size();
		}

		const FeatureArtModel &getArtModel(int index) const
		{
			FAssertMsg((index >= 0) && (index < (int) m_aArtModels.size()), "[Jason] Invalid feature model file index.");
			return m_aArtModels[index];
		}

	private:
		std::vector<FeatureArtModel> m_aArtModels;
		int m_iConnectionMask;

		friend CvArtInfoFeature;
	};

	class FeatureDummyNode
	{
	public:
		FeatureDummyNode(const CvString &tagName, const CvString &nodeName)
		{
			m_szTag = tagName;
			m_szName = nodeName;
		}

		const CvString getTagName() const
		{
			return m_szTag;
		}

		const CvString getNodeName() const
		{
			return m_szName;
		}

	private:
		CvString m_szTag;
		CvString m_szName;
	};

	class FeatureVariety
	{
	public:
		FeatureVariety()
		{
		}

		const CvString &getVarietyButton() const
		{
			return m_szVarietyButton;
		}

		const FeatureArtPiece &getFeatureArtPiece(int index) const
		{
			FAssertMsg((index >= 0) && (index < (int) m_aFeatureArtPieces.size()), "[Jason] Invalid feature art index.");
			return m_aFeatureArtPieces[index];
		}

		const FeatureArtPiece &getFeatureArtPieceFromConnectionMask(int connectionMask) const
		{
			for(int i=0;i<(int)m_aFeatureArtPieces.size();i++)
				if(m_aFeatureArtPieces[i].getConnectionMask() == connectionMask)
					return m_aFeatureArtPieces[i];

			FAssertMsg(false, "[Jason] Failed to find feature art piece with valid connection mask.");
			return m_aFeatureArtPieces[0];
		}

		const CvString getFeatureDummyNodeName(const CvString &tagName) const
		{
			for(int i=0;i<(int)m_aFeatureDummyNodes.size();i++)
			{
				if(m_aFeatureDummyNodes[i].getTagName().CompareNoCase(tagName) == 0)
					return m_aFeatureDummyNodes[i].getNodeName();
			}

			FAssertMsg(false, "[Jason] Failed to find dummy tag name.");
			return "";
		}

		const CvString getFeatureDummyTag(const CvString &nodeName) const
		{
			for(int i=0;i<(int)m_aFeatureDummyNodes.size();i++)
			{
				if(m_aFeatureDummyNodes[i].getNodeName().CompareNoCase(nodeName) == 0)
					return m_aFeatureDummyNodes[i].getTagName();
			}

			return "";
		}

		FeatureArtPiece &createFeatureArtPieceFromConnectionMask(int connectionMask)
		{
			for(int i=0;i<(int)m_aFeatureArtPieces.size();i++)
				if(m_aFeatureArtPieces[i].getConnectionMask() == connectionMask)
					return m_aFeatureArtPieces[i];

			m_aFeatureArtPieces.push_back(FeatureArtPiece(connectionMask));
			return m_aFeatureArtPieces.back();
		}

		void createFeatureDummyNode(const CvString &tagName, const CvString &nodeName)
		{
			m_aFeatureDummyNodes.push_back(FeatureDummyNode(tagName, nodeName));
		}

	private:
		std::vector<FeatureArtPiece> m_aFeatureArtPieces;
		std::vector<FeatureDummyNode> m_aFeatureDummyNodes;
		CvString m_szVarietyButton;

		friend CvArtInfoFeature;
	};

	DllExport const FeatureVariety &getVariety(int index) const;
	DllExport int getNumVarieties() const;
	DllExport std::string getFeatureDummyNodeName(int variety, std::string tagName);

protected:

	int getConnectionMaskFromString(const CvString &connectionString);
	int getRotatedConnectionMask(int connectionMask, RotationTypes rotation);

	bool m_bAnimated;
	bool m_bRiverArt;
	TileArtTypes m_eTileArtType;
	LightTypes m_eLightType;
	std::vector<FeatureVariety> m_aFeatureVarieties;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEmphasizeInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEmphasizeInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvEmphasizeInfo();
	virtual ~CvEmphasizeInfo();

	bool isAvoidGrowth() const;				// Exposed to Python
	bool isGreatPeople() const;				// Exposed to Python

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int getCommerceChange(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	bool m_bAvoidGrowth;
	bool m_bGreatPeople;

	// Arrays

	int* m_piYieldModifiers;
	int* m_piCommerceModifiers;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUpkeepInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUpkeepInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvUpkeepInfo();
	virtual ~CvUpkeepInfo();

	int getPopulationPercent() const;			//	Exposed to Python
	int getCityPercent() const;						//	Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iPopulationPercent;
	int m_iCityPercent;			

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCultureLevelInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCultureLevelInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCultureLevelInfo();
	virtual ~CvCultureLevelInfo();

	int getCityDefenseModifier() const;		//	Exposed to Python

	int getSpeedThreshold(int i) const;		//	Exposed to Python

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCityDefenseModifier;

	int* m_paiSpeedThreshold;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEraInfo
//
//  DESC:   Used to manage different types of Art Styles
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEraInfo : 
	public CvInfoBase
{
public:

	CvEraInfo();
	virtual ~CvEraInfo();

	int getStartingUnitMultiplier() const;		//	Exposed to Python
	int getStartingDefenseUnits() const;			//	Exposed to Python
	int getStartingWorkerUnits() const;				//	Exposed to Python
	int getStartingExploreUnits() const;			//	Exposed to Python
	int getAdvancedStartPoints() const;					//	Exposed to Python
	int getStartingGold() const;					//	Exposed to Python
	int getFreePopulation() const;				//	Exposed to Python
	int getStartPercent() const;					//	Exposed to Python
	int getGrowthPercent() const;					//	Exposed to Python
	int getTrainPercent() const;					//	Exposed to Python
	int getConstructPercent() const;			//	Exposed to Python
	int getCreatePercent() const;					//	Exposed to Python
	int getResearchPercent() const;				//	Exposed to Python
	int getBuildPercent() const;					//	Exposed to Python
	int getImprovementPercent() const;		//	Exposed to Python
	int getGreatPeoplePercent() const;		//	Exposed to Python
	int getAnarchyPercent() const;				//	Exposed to Python
	int getEventChancePerTurn() const;				//	Exposed to Python
	int getSoundtrackSpace() const;				//	Exposed to Python
	int getNumSoundtracks() const;				//	Exposed to Python
	const TCHAR* getAudioUnitVictoryScript() const;				//	Exposed to Python
	const TCHAR* getAudioUnitDefeatScript() const;				//	Exposed to Python

	bool isNoGoodies() const;					//	Exposed to Python
	bool isNoAnimals() const;					//	Exposed to Python
	bool isNoBarbUnits() const;				//	Exposed to Python
	bool isNoBarbCities() const;			//	Exposed to Python
	bool isFirstSoundtrackFirst() const;			//	Exposed to Python

	// Arrays

	int getSoundtracks(int i) const;			
	int getCitySoundscapeSciptId(int i) const;			

	bool read(CvXMLLoadUtility* pXML);

protected:

	int m_iStartingUnitMultiplier;
	int m_iStartingDefenseUnits;
	int m_iStartingWorkerUnits;
	int m_iStartingExploreUnits;
	int m_iAdvancedStartPoints;
	int m_iStartingGold;
	int m_iFreePopulation;
	int m_iStartPercent;
	int m_iGrowthPercent;
	int m_iTrainPercent;
	int m_iConstructPercent;
	int m_iCreatePercent;
	int m_iResearchPercent;
	int m_iBuildPercent;
	int m_iImprovementPercent;
	int m_iGreatPeoplePercent;
	int m_iAnarchyPercent;
	int m_iEventChancePerTurn;
	int m_iSoundtrackSpace;
	int m_iNumSoundtracks;
	CvString m_szAudioUnitVictoryScript;
	CvString m_szAudioUnitDefeatScript;

	bool m_bNoGoodies;
	bool m_bNoAnimals;
	bool m_bNoBarbUnits;
	bool m_bNoBarbCities;
	bool m_bFirstSoundtrackFirst;

	// Arrays

	int* m_paiSoundtracks;
	int* m_paiCitySoundscapeSciptIds;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvColorInfo
//
//  DESC:   Used to manage different types of Art Styles
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvColorInfo : 
	public CvInfoBase
{
public:

	DllExport CvColorInfo();
	DllExport virtual ~CvColorInfo();

	DllExport const NiColorA& getColor() const;			
	
	bool read(CvXMLLoadUtility* pXML);

protected:

	NiColorA m_Color;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPlayerColorInfo (ADD to Python)
//
//  DESC:   Used to manage different types of Art Styles
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlayerColorInfo : 
	public CvInfoBase
{
public:

	DllExport CvPlayerColorInfo();
	DllExport virtual ~CvPlayerColorInfo();

	DllExport int getColorTypePrimary() const;			
	DllExport int getColorTypeSecondary() const;			
	DllExport int getTextColorType() const;			

	bool read(CvXMLLoadUtility* pXML);

protected:

	int m_iColorTypePrimary;
	int m_iColorTypeSecondary;
	int m_iTextColorType;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvLandscapeInfo
//
//  Purpose:	This info acts as the Civ4Terrain.ini and is initialize in CvXmlLoadUtility with the infos in
//					XML/Terrain/TerrainSettings.xml
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvLandscapeInfo :
	public CvInfoBase
{
	public:

		DllExport CvLandscapeInfo();
		DllExport virtual ~CvLandscapeInfo() {}

		DllExport int getFogR() const;
		DllExport int getFogG() const;
		DllExport int getFogB() const;
		DllExport int getHorizontalGameCell() const;
		DllExport int getVerticalGameCell() const;
		DllExport int getPlotsPerCellX() const;
		DllExport int getPlotsPerCellY() const;
		DllExport int getHorizontalVertCnt() const;
		DllExport int getVerticalVertCnt() const;
		DllExport int getWaterHeight() const;

		DllExport float getTextureScaleX() const;			
		DllExport float getTextureScaleY() const;			
		DllExport float getZScale() const;			

		DllExport bool isUseTerrainShader() const;			
		DllExport bool isUseLightmap() const;			
		DllExport bool isRandomMap() const;		
		DllExport float getPeakScale() const;
		DllExport float getHillScale() const;

		DllExport const TCHAR* getSkyArt();			
		DllExport void setSkyArt(const TCHAR* szPath);			
		DllExport const TCHAR* getHeightMap();			
		DllExport void setHeightMap(const TCHAR* szPath);			
		DllExport const TCHAR* getTerrainMap();			
		DllExport void setTerrainMap(const TCHAR* szPath);			
		DllExport const TCHAR* getNormalMap();			
		DllExport void setNormalMap(const TCHAR* szPath);			
		DllExport const TCHAR* getBlendMap();			
		DllExport void setBlendMap(const TCHAR* szPath);			

		bool read(CvXMLLoadUtility* pXML);

	protected:

		int m_iFogR;
		int m_iFogG;
		int m_iFogB;
		int m_iHorizontalGameCell;
		int m_iVerticalGameCell;
		int m_iPlotsPerCellX;
		int m_iPlotsPerCellY;
		int m_iHorizontalVertCnt;
		int m_iVerticalVertCnt;
		int m_iWaterHeight;

		float m_fTextureScaleX;
		float m_fTextureScaleY;
		float m_fZScale;

		float m_fPeakScale;
		float m_fHillScale;

		bool m_bUseTerrainShader;
		bool m_bUseLightmap;
		bool m_bRandomMap;

		CvString m_szSkyArt;
		CvString m_szHeightMap;
		CvString m_szTerrainMap;
		CvString m_szNormalMap;
		CvString m_szBlendMap;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGameText
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameText : public CvInfoBase
{
public:
	DllExport CvGameText();

	const wchar* getText() const;
	void setText(const wchar* szText);

	// for Python
	std::wstring pyGetText() const { return getText(); }

	void setGender(const wchar* szGender) { m_szGender = szGender;	}
	const wchar* getGender() const { return m_szGender; }

	void setPlural(const wchar* szPlural) { m_szPlural = szPlural; }
	const wchar* getPlural() const { return m_szPlural; }

	DllExport int getNumLanguages() const; // not static for Python access
	DllExport void setNumLanguages(int iNum); // not static for Python access

	bool read(CvXMLLoadUtility* pXML);

protected:

	CvWString m_szText;
	CvWString m_szGender;
	CvWString m_szPlural;

	static int NUM_LANGUAGES;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvDiplomacyTextInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyTextInfo :	public CvInfoBase
{
	friend class CvXMLLoadUtility;		// so it can access private vars to initialize the class
public:
	struct Response 
	{
		DllExport Response() : 
			m_iNumDiplomacyText(0), 
			m_pbCivilizationTypes(NULL), 
			m_pbLeaderHeadTypes(NULL), 
			m_pbAttitudeTypes(NULL), 
			m_pbDiplomacyPowerTypes(NULL), 
			m_paszDiplomacyText(NULL)
		{
		}

		DllExport virtual ~Response ()
		{
			SAFE_DELETE_ARRAY(m_pbCivilizationTypes);
			SAFE_DELETE_ARRAY(m_pbLeaderHeadTypes);
			SAFE_DELETE_ARRAY(m_pbAttitudeTypes);
			SAFE_DELETE_ARRAY(m_pbDiplomacyPowerTypes);
			SAFE_DELETE_ARRAY(m_paszDiplomacyText);
		}
		
		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);
		
		int m_iNumDiplomacyText;
		bool* m_pbCivilizationTypes;
		bool* m_pbLeaderHeadTypes;
		bool* m_pbAttitudeTypes;
		bool* m_pbDiplomacyPowerTypes;
		CvString* m_paszDiplomacyText;	// needs to be public for xml load assignment
	};

	DllExport CvDiplomacyTextInfo();
	DllExport virtual ~CvDiplomacyTextInfo() { uninit(); }	// free memory - MT

	// note - Response member vars allocated by CvXmlLoadUtility  
	DllExport void init(int iNum);			
	DllExport void uninit();			

	DllExport const Response& getResponse(int iNum) const { return m_pResponses[iNum]; }	// Exposed to Python
	DllExport int getNumResponses() const;															// Exposed to Python

	DllExport bool getCivilizationTypes(int i, int j) const;						// Exposed to Python
	DllExport bool getLeaderHeadTypes(int i, int j) const;							// Exposed to Python
	DllExport bool getAttitudeTypes(int i, int j) const;								// Exposed to Python
	DllExport bool getDiplomacyPowerTypes(int i, int j) const;					// Exposed to Python

	DllExport int getNumDiplomacyText(int i) const;											// Exposed to Python

	DllExport const TCHAR* getDiplomacyText(int i, int j) const;				// Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);

private:

	int m_iNumResponses;			// set by init
	Response* m_pResponses;

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEffectInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEffectInfo : 
	public CvInfoBase,
	public CvScalableInfo
{
public:

	DllExport CvEffectInfo();
	DllExport virtual ~CvEffectInfo();

	DllExport const TCHAR* getPath() const { return m_szPath; }
	DllExport void setPath(const TCHAR* szVal) { m_szPath = szVal; }
	DllExport float getUpdateRate( ) const { return m_fUpdateRate; };
	DllExport void setUpdateRate( float fUpdateRate ) { m_fUpdateRate = fUpdateRate; }
	DllExport bool isProjectile() const { return m_bProjectile; };
	DllExport float getProjectileSpeed() const { return m_fProjectileSpeed; };
	DllExport float getProjectileArc() const { return m_fProjectileArc; };
	DllExport bool isSticky() const { return m_bSticky; };
	bool read(CvXMLLoadUtility* pXML);

private:
	CvString m_szPath;
	float m_fUpdateRate;
	bool m_bProjectile;
	bool m_bSticky;
	float m_fProjectileSpeed;
	float m_fProjectileArc;
};



//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAttachableInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAttachableInfo : 
	public CvInfoBase,
	public CvScalableInfo
{
public:

	DllExport CvAttachableInfo();
	DllExport virtual ~CvAttachableInfo();

	DllExport const TCHAR* getPath() const { return m_szPath; }
	DllExport void setPath(const TCHAR* szVal) { m_szPath = szVal; }

	bool read(CvXMLLoadUtility* pXML);

private:
	CvString m_szPath;
	float m_fUpdateRate;
};



//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCameraInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCameraInfo : 
	public CvInfoBase
{
public:

	DllExport CvCameraInfo() {}
	DllExport virtual ~CvCameraInfo() {}

	DllExport const TCHAR* getPath() const { return m_szPath; }
	DllExport void setPath(const TCHAR* szVal) { m_szPath = szVal; }

	bool read(CvXMLLoadUtility* pXML);

private:
	CvString m_szPath;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvQuestInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvQuestInfo :
	public CvInfoBase
{
public:
	struct QuestLink 
	{
		// Stores the QuestLinks Type and Name
		DllExport QuestLink() :
		m_szQuestLinkType("No Type"),
		m_szQuestLinkName("No Name")
		{
		}

	CvString m_szQuestLinkType;
	CvString m_szQuestLinkName;
	};

	DllExport CvQuestInfo();
	DllExport virtual ~CvQuestInfo();

	DllExport void reset();
	DllExport bool initQuestLinks(int iNum);

	DllExport int getNumQuestMessages() const;
	DllExport int getNumQuestLinks() const;
	DllExport int getNumQuestSounds() const;
	DllExport const TCHAR* getQuestObjective() const;
	DllExport const TCHAR* getQuestBodyText() const;
	DllExport const TCHAR* getQuestMessages(int iIndex) const;
	DllExport const TCHAR* getQuestLinkType(int iIndex) const;
	DllExport const TCHAR* getQuestLinkName(int iIndex) const;
	DllExport const TCHAR* getQuestSounds(int iIndex) const;
	DllExport const TCHAR* getQuestScript() const;
	
	DllExport void setNumQuestMessages(int iNum);
	DllExport void setNumQuestSounds(int iNum);
	DllExport void setQuestObjective(const TCHAR* szText);
	DllExport void setQuestBodyText(const TCHAR* szText);
	DllExport void setQuestMessages(int iIndex, const TCHAR* szText);
	DllExport void setQuestSounds(int iIndex, const TCHAR* szText);
	DllExport void setQuestScript(const TCHAR* szText);

	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iNumQuestMessages;
	int m_iNumQuestLinks;
	int m_iNumQuestSounds;

	CvString m_szQuestObjective;
	CvString m_szQuestBodyText;
	CvString m_szQuestScript;

	CvString* m_paszQuestMessages;
	QuestLink* m_pQuestLinks;
	CvString* m_paszQuestSounds;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTutorialInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTutorialMessage
{
public:
	DllExport CvTutorialMessage();
	DllExport virtual ~CvTutorialMessage();

	DllExport const TCHAR* getText() const;
	DllExport const TCHAR* getImage() const;
	DllExport const TCHAR* getSound() const;

	DllExport void setText(const TCHAR* szText);
	DllExport void setImage(const TCHAR* szText);
	DllExport void setSound(const TCHAR* szText);
	DllExport void setScript(int iIndex, const TCHAR* szText);

	DllExport int getNumTutorialScripts() const;
	DllExport const TCHAR* getTutorialScriptByIndex(int i) const;
	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iNumTutorialScripts;
	CvString m_szTutorialMessageText;
	CvString m_szTutorialMessageImage;
	CvString m_szTutorialMessageSound;
	CvString* m_paszTutorialScripts;
};

class CvTutorialMessage;
class CvTutorialInfo :
	public CvInfoBase
{
public:
	DllExport CvTutorialInfo();
	DllExport virtual ~CvTutorialInfo();

	DllExport const TCHAR* getNextTutorialInfoType();
	DllExport void setNextTutorialInfoType(const TCHAR* szVal);

	DllExport bool initTutorialMessages(int iNum);
	DllExport void resetMessages();

	DllExport int getNumTutorialMessages() const;
	DllExport const CvTutorialMessage* getTutorialMessage(int iIndex) const;

	bool read(CvXMLLoadUtility* pXML);

private:
	CvString m_szNextTutorialInfoType;
	int m_iNumTutorialMessages;
	CvTutorialMessage* m_paTutorialMessages;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGameOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvGameOptionInfo();
	DllExport virtual ~CvGameOptionInfo();

	DllExport bool getDefault() const;
	DllExport bool getVisible() const;

	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;
	bool m_bVisible;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvMPOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMPOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvMPOptionInfo();
	DllExport virtual ~CvMPOptionInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvForceControlInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvForceControlInfo :
	public CvInfoBase
{
public:
	DllExport CvForceControlInfo();
	DllExport virtual ~CvForceControlInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPlayerOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlayerOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvPlayerOptionInfo();
	DllExport virtual ~CvPlayerOptionInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGraphicOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGraphicOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvGraphicOptionInfo();
	DllExport virtual ~CvGraphicOptionInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEventTriggerInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEventTriggerInfo : public CvInfoBase
{
	friend class CvXMLLoadUtility;

public:
	CvEventTriggerInfo();
	virtual ~CvEventTriggerInfo();

	int getPercentGamesActive() const;		// Exposed to Python
	int getProbability() const;				// Exposed to Python
	int getNumUnits() const;					// Exposed to Python
	int getNumBuildings() const;				// Exposed to Python
	int getNumUnitsGlobal() const;			// Exposed to Python
	int getNumBuildingsGlobal() const;		// Exposed to Python
	int getNumPlotsRequired() const;			// Exposed to Python
	int getPlotType() const;					// Exposed to Python
	int getNumReligions() const;				// Exposed to Python
	int getNumCorporations() const;			// Exposed to Python
	int getOtherPlayerShareBorders() const;	// Exposed to Python
	int getOtherPlayerHasTech() const;		// Exposed to Python
	int getCityFoodWeight() const;			// Exposed to Python
	int getCivic() const;						// Exposed to Python
	int getMinPopulation() const;				// Exposed to Python
	int getMaxPopulation() const;				// Exposed to Python
	int getMinMapLandmass() const;			// Exposed to Python
	int getMinOurLandmass() const;			// Exposed to Python
	int getMaxOurLandmass() const;			// Exposed to Python
	int getMinDifficulty() const;				// Exposed to Python
	int getAngry() const;						// Exposed to Python
	int getUnhealthy() const;					// Exposed to Python
	int getUnitDamagedWeight() const;			// Exposed to Python
	int getUnitDistanceWeight() const;		// Exposed to Python
	int getUnitExperienceWeight() const;		// Exposed to Python
	int getMinTreasury() const;				// Exposed to Python

	int getBuildingRequired(int i) const;		// Exposed to Python
	int getNumBuildingsRequired() const;		// Exposed to Python
	int getUnitRequired(int i) const;			// Exposed to Python
	int getNumUnitsRequired() const;			// Exposed to Python
	int getPrereqOrTechs(int i) const;		// Exposed to Python
	int getNumPrereqOrTechs() const;			// Exposed to Python
	int getPrereqAndTechs(int i) const;		// Exposed to Python
	int getNumPrereqAndTechs() const;			// Exposed to Python
	int getObsoleteTech(int i) const;				// Exposed to Python
	int getNumObsoleteTechs() const;				// Exposed to Python
	int getEvent(int i) const;				// Exposed to Python
	int getNumEvents() const;					// Exposed to Python
	int getPrereqEvent(int i) const;			// Exposed to Python
	int getNumPrereqEvents() const;			// Exposed to Python
	int getFeatureRequired(int i) const;		// Exposed to Python
	int getNumFeaturesRequired() const;		// Exposed to Python
	int getTerrainRequired(int i) const;		// Exposed to Python
	int getNumTerrainsRequired() const;		// Exposed to Python
	int getImprovementRequired(int i) const;	// Exposed to Python
	int getNumImprovementsRequired() const;	// Exposed to Python
	int getBonusRequired(int i) const;		// Exposed to Python
	int getNumBonusesRequired() const;		// Exposed to Python
	int getRouteRequired(int i) const;		// Exposed to Python
	int getNumRoutesRequired() const;			// Exposed to Python
	int getReligionRequired(int i) const;		// Exposed to Python
	int getNumReligionsRequired() const;		// Exposed to Python
	int getCorporationRequired(int i) const;	// Exposed to Python
	int getNumCorporationsRequired() const;	// Exposed to Python

	const CvWString& getText(int i) const;
	int getTextEra(int i) const;
	int getNumTexts() const;
	const CvWString& getWorldNews(int i) const;
	int getNumWorldNews() const;

	bool isSinglePlayer() const;				// Exposed to Python
	bool isTeam() const;						// Exposed to Python
	bool isRecurring() const;					// Exposed to Python
	bool isGlobal() const;					// Exposed to Python
	bool isPickPlayer() const;				// Exposed to Python
	bool isOtherPlayerWar() const;			// Exposed to Python
	bool isOtherPlayerHasReligion() const;	// Exposed to Python
	bool isOtherPlayerHasOtherReligion() const;	// Exposed to Python
	bool isOtherPlayerAI() const;				// Exposed to Python
	bool isPickCity() const;					// Exposed to Python
	bool isPickOtherPlayerCity() const;		// Exposed to Python
	bool isShowPlot() const;					// Exposed to Python
	bool isUnitsOnPlot() const;				// Exposed to Python
	bool isOwnPlot() const;					// Exposed to Python
	bool isPickReligion() const;				// Exposed to Python
	bool isStateReligion() const;				// Exposed to Python
	bool isHolyCity() const;					// Exposed to Python
	bool isPickCorporation() const;			// Exposed to Python
	bool isHeadquarters() const;				// Exposed to Python
	bool isProbabilityUnitMultiply() const;	// Exposed to Python
	bool isProbabilityBuildingMultiply() const;	// Exposed to Python
	bool isPrereqEventCity() const;			// Exposed to Python

	const char* getPythonCallback() const;
	const char* getPythonCanDo() const;
	const char* getPythonCanDoCity() const;
	const char* getPythonCanDoUnit() const;

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iPercentGamesActive;
	int m_iProbability;
	int m_iNumUnits;
	int m_iNumBuildings;
	int m_iNumUnitsGlobal;
	int m_iNumBuildingsGlobal;
	int m_iNumPlotsRequired;
	int m_iPlotType;
	int m_iNumReligions;
	int m_iNumCorporations;
	int m_iOtherPlayerShareBorders;
	int m_iOtherPlayerHasTech;
	int m_iCityFoodWeight;
	int m_iCivic;
	int m_iMinPopulation;
	int m_iMaxPopulation;
	int m_iMinMapLandmass;
	int m_iMinOurLandmass;
	int m_iMaxOurLandmass;
	int m_iMinDifficulty;
	int m_iAngry;
	int m_iUnhealthy;
	int m_iUnitDamagedWeight;
	int m_iUnitDistanceWeight;
	int m_iUnitExperienceWeight;
	int m_iMinTreasury;
	
	std::vector<int> m_aiUnitsRequired;
	std::vector<int> m_aiBuildingsRequired;
	std::vector<int> m_aiPrereqOrTechs;
	std::vector<int> m_aiPrereqAndTechs;
	std::vector<int> m_aiObsoleteTechs;
	std::vector<int> m_aiEvents;
	std::vector<int> m_aiPrereqEvents;
	std::vector<int> m_aiFeaturesRequired;
	std::vector<int> m_aiTerrainsRequired;
	std::vector<int> m_aiImprovementsRequired;
	std::vector<int> m_aiBonusesRequired;
	std::vector<int> m_aiRoutesRequired;
	std::vector<int> m_aiReligionsRequired;
	std::vector<int> m_aiCorporationsRequired;

	std::vector<int> m_aiTextEra;
	std::vector<CvWString> m_aszText;
	std::vector<CvWString> m_aszWorldNews;

	bool m_bSinglePlayer;
	bool m_bTeam;
	bool m_bRecurring;
	bool m_bGlobal;
	bool m_bPickPlayer;
	bool m_bOtherPlayerWar;
	bool m_bOtherPlayerHasReligion;
	bool m_bOtherPlayerHasOtherReligion;
	bool m_bOtherPlayerAI;
	bool m_bPickCity;
	bool m_bPickOtherPlayerCity;
	bool m_bShowPlot;
	bool m_bUnitsOnPlot;
	bool m_bOwnPlot;
	bool m_bPickReligion;
	bool m_bStateReligion;
	bool m_bHolyCity;
	bool m_bPickCorporation;
	bool m_bHeadquarters;
	bool m_bProbabilityUnitMultiply;
	bool m_bProbabilityBuildingMultiply;
	bool m_bPrereqEventCity;

	CvString m_szPythonCallback;
	CvString m_szPythonCanDo;
	CvString m_szPythonCanDoCity;
	CvString m_szPythonCanDoUnit;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEventInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEventInfo : public CvInfoBase
{
	friend class CvXMLLoadUtility;

public:
	CvEventInfo();
	virtual ~CvEventInfo();

	bool isQuest() const;						// Exposed to Python
	bool isGlobal() const;					// Exposed to Python
	bool isTeam() const;						// Exposed to Python
	bool isCityEffect() const;				// Exposed to Python
	bool isOtherPlayerCityEffect() const;		// Exposed to Python
	bool isGoldToPlayer() const;				// Exposed to Python
	bool isGoldenAge() const;					// Exposed to Python
	bool isDeclareWar() const;				// Exposed to Python
	bool isDisbandUnit() const;				// Exposed to Python

	int getGold() const;						// Exposed to Python
	int getRandomGold() const;				// Exposed to Python
	int getEspionagePoints() const;			// Exposed to Python
	int getCulture() const;					// Exposed to Python
	int getTech() const;						// Exposed to Python
	int getTechPercent() const;				// Exposed to Python
	int getTechCostPercent() const;			// Exposed to Python
	int getTechMinTurnsLeft() const;			// Exposed to Python
	int getPrereqTech() const;				// Exposed to Python
	int getUnitClass() const;					// Exposed to Python
	int getNumUnits() const;					// Exposed to Python
	int getBuildingClass() const;				// Exposed to Python
	int getBuildingChange() const;			// Exposed to Python
	int getHappy() const;						// Exposed to Python
	int getHealth() const;					// Exposed to Python
	int getHurryAnger() const;				// Exposed to Python
	int getHappyTurns() const;				// Exposed to Python
	int getFood() const;						// Exposed to Python
	int getFoodPercent() const;				// Exposed to Python
	int getFeature() const;					// Exposed to Python
	int getFeatureChange() const;				// Exposed to Python
	int getImprovement() const;				// Exposed to Python
	int getImprovementChange() const;			// Exposed to Python
	int getBonus() const;						// Exposed to Python
	int getBonusChange() const;				// Exposed to Python
	int getRoute() const;						// Exposed to Python
	int getRouteChange() const;				// Exposed to Python
	int getBonusRevealed() const;				// Exposed to Python
	int getBonusGift() const;					// Exposed to Python
	int getUnitExperience() const;			// Exposed to Python
	int getUnitImmobileTurns() const;			// Exposed to Python
	int getConvertOwnCities() const;			// Exposed to Python
	int getConvertOtherCities() const;		// Exposed to Python
	int getMaxNumReligions() const;			// Exposed to Python
	int getOurAttitudeModifier() const;		// Exposed to Python
	int getAttitudeModifier() const;			// Exposed to Python
	int getTheirEnemyAttitudeModifier() const;// Exposed to Python
	int getPopulationChange() const;			// Exposed to Python
	int getRevoltTurns() const;				// Exposed to Python
	int getMinPillage() const;				// Exposed to Python
	int getMaxPillage() const;				// Exposed to Python
	int getUnitPromotion() const;				// Exposed to Python
	int getFreeUnitSupport() const;			// Exposed to Python
	int getInflationModifier() const;			// Exposed to Python
	int getSpaceProductionModifier() const;	// Exposed to Python
	int getAIValue() const;	// Exposed to Python

	int getAdditionalEventChance(int i) const;// Exposed to Python
	int getAdditionalEventTime(int i) const;	// Exposed to Python
	int getClearEventChance(int i) const;		// Exposed to Python
	int getTechFlavorValue(int i) const;		// Exposed to Python
	int getPlotExtraYield(int i) const;		// Exposed to Python
	int getFreeSpecialistCount(int i) const;	// Exposed to Python
	int getUnitCombatPromotion(int i) const;	// Exposed to Python
	int getUnitClassPromotion(int i) const;	// Exposed to Python
	const CvWString& getWorldNews(int i) const;
	int getNumWorldNews() const;

	int getBuildingYieldChange(int iBuildingClass, int iYield) const;
	int getNumBuildingYieldChanges() const;
	int getBuildingCommerceChange(int iBuildingClass, int iCommerce) const;
	int getNumBuildingCommerceChanges() const;
	int getBuildingHappyChange(int iBuildingClass) const;
	int getNumBuildingHappyChanges() const;
	int getBuildingHealthChange(int iBuildingClass) const;
	int getNumBuildingHealthChanges() const;

	const char* getPythonCallback() const;
	const char* getPythonExpireCheck() const;
	const char* getPythonCanDo() const;
	const char* getPythonHelp() const;
	const wchar* getUnitNameKey() const;
	const wchar* getQuestFailTextKey() const;
	const wchar* getOtherPlayerPopup() const;
	const wchar* getLocalInfoTextKey() const;

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);

private:
	bool m_bQuest;
	bool m_bGlobal;
	bool m_bTeam;
	bool m_bCityEffect;
	bool m_bOtherPlayerCityEffect;
	bool m_bGoldToPlayer;
	bool m_bGoldenAge;
	bool m_bDeclareWar;
	bool m_bDisbandUnit;

	int m_iGold;
	int m_iRandomGold;
	int m_iCulture;
	int m_iEspionagePoints;
	int m_iTech;
	int m_iTechPercent;
	int m_iTechCostPercent;
	int m_iTechMinTurnsLeft;
	int m_iPrereqTech;
	int m_iUnitClass;
	int m_iNumUnits;
	int m_iBuildingClass;
	int m_iBuildingChange;
	int m_iHappy;
	int m_iHealth;
	int m_iHurryAnger;
	int m_iHappyTurns;
	int m_iFood;
	int m_iFoodPercent;
	int m_iFeature;
	int m_iFeatureChange;
	int m_iImprovement;
	int m_iImprovementChange;
	int m_iBonus;
	int m_iBonusChange;
	int m_iRoute;
	int m_iRouteChange;
	int m_iBonusRevealed;
	int m_iBonusGift;
	int m_iUnitExperience;
	int m_iUnitImmobileTurns;
	int m_iConvertOwnCities;
	int m_iConvertOtherCities;
	int m_iMaxNumReligions;
	int m_iOurAttitudeModifier;
	int m_iAttitudeModifier;
	int m_iTheirEnemyAttitudeModifier;
	int m_iPopulationChange;
	int m_iRevoltTurns;
	int m_iMinPillage;
	int m_iMaxPillage;
	int m_iUnitPromotion;
	int m_iFreeUnitSupport;
	int m_iInflationModifier;
	int m_iSpaceProductionModifier;
	int m_iAIValue;

	int* m_piTechFlavorValue;
	int* m_piPlotExtraYields;
	int* m_piFreeSpecialistCount;
	int* m_piAdditionalEventChance;
	int* m_piAdditionalEventTime;
	int* m_piClearEventChance;
	int* m_piUnitCombatPromotions;
	int* m_piUnitClassPromotions;

	std::vector<BuildingYieldChange> m_aBuildingYieldChanges;
	std::vector<BuildingCommerceChange> m_aBuildingCommerceChanges;
	BuildingChangeArray m_aBuildingHappyChanges;
	BuildingChangeArray m_aBuildingHealthChanges;

	CvString m_szPythonCallback;
	CvString m_szPythonExpireCheck;
	CvString m_szPythonCanDo;
	CvString m_szPythonHelp;
	CvWString m_szUnitName;
	CvWString m_szOtherPlayerPopup;
	CvWString m_szQuestFailText;
	CvWString m_szLocalInfoText;
	std::vector<CvWString> m_aszWorldNews;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEspionageMissionInfo
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEspionageMissionInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvEspionageMissionInfo();
	virtual ~CvEspionageMissionInfo();
	
	int getCost() const;
	bool isPassive() const;
	bool isTwoPhases() const;
	bool isTargetsCity() const;
	bool isSelectPlot() const;
	
	int getTechPrereq() const;
	int getVisibilityLevel() const;
	bool isInvestigateCity() const;
	bool isSeeDemographics() const;
	bool isNoActiveMissions() const;
	bool isSeeResearch() const;

	bool isDestroyImprovement() const;
	int getDestroyBuildingCostFactor() const;
	int getDestroyUnitCostFactor() const;
	int getDestroyProjectCostFactor() const;
	int getDestroyProductionCostFactor() const;
	int getBuyUnitCostFactor() const;
	int getBuyCityCostFactor() const;
	int getStealTreasuryTypes() const;
	int getCityInsertCultureAmountFactor() const;
	int getCityInsertCultureCostFactor() const;
	int getCityPoisonWaterCounter() const;
	int getCityUnhappinessCounter() const;
	int getCityRevoltCounter() const;
	int getBuyTechCostFactor() const;
	int getSwitchCivicCostFactor() const;
	int getSwitchReligionCostFactor() const;
	int getPlayerAnarchyCounter() const;
	int getCounterespionageNumTurns() const;
	int getCounterespionageMod() const;
	int getDifficultyMod() const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCost;
	bool m_bIsPassive;
	bool m_bIsTwoPhases;
	bool m_bTargetsCity;
	bool m_bSelectPlot;

	int m_iTechPrereq;
	int m_iVisibilityLevel;
	bool m_bInvestigateCity;
	bool m_bSeeDemographics;
	bool m_bNoActiveMissions;
	bool m_bSeeResearch;

	bool m_bDestroyImprovement;
	int m_iDestroyBuildingCostFactor;
	int m_iDestroyUnitCostFactor;
	int m_iDestroyProjectCostFactor;
	int m_iDestroyProductionCostFactor;
	int m_iBuyUnitCostFactor;
	int m_iBuyCityCostFactor;
	int m_iStealTreasuryTypes;
	int m_iCityInsertCultureAmountFactor;
	int m_iCityInsertCultureCostFactor;
	int m_iCityPoisonWaterCounter;
	int m_iCityUnhappinessCounter;
	int m_iCityRevoltCounter;
	int m_iBuyTechCostFactor;
	int m_iSwitchCivicCostFactor;
	int m_iSwitchReligionCostFactor;
	int m_iPlayerAnarchyCounter;
	int m_iCounterespionageNumTurns;
	int m_iCounterespionageMod;
	int m_iDifficultyMod;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUnitArtStyleTypeInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUnitArtStyleTypeInfo : public CvInfoBase
{
public:

	CvUnitArtStyleTypeInfo();
	virtual ~CvUnitArtStyleTypeInfo();

    const TCHAR* getEarlyArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j) const;
	void setEarlyArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, const TCHAR* szVal);
	const TCHAR* getLateArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j) const;
	void setLateArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, const TCHAR* szVal);
	const TCHAR* getMiddleArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j) const;
	void setMiddleArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);

protected:

	struct ArtDefneTag
	{
		int iMeshIndex;
		int iUnitType;
		CvString szTag;
	};
	typedef std::vector<ArtDefneTag> ArtDefineArray;
    ArtDefineArray m_azEarlyArtDefineTags;
	ArtDefineArray m_azLateArtDefineTags;
	ArtDefineArray m_azMiddleArtDefineTags;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvVoteSourceInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVoteSourceInfo : public CvInfoBase
{
public:

	CvVoteSourceInfo();
	virtual ~CvVoteSourceInfo();

	int getVoteInterval() const;					// Exposed to Python
	int getFreeSpecialist() const;					// Exposed to Python
	int getCivic() const;					// Exposed to Python
	const CvWString getPopupText() const;
	const CvWString getSecretaryGeneralText() const;

	std::wstring pyGetSecretaryGeneralText() { return getSecretaryGeneralText(); }						// Exposed to Python

	int getReligionYield(int i) const;					// Exposed to Python
	int getReligionCommerce(int i) const;					// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

protected:
	int m_iVoteInterval;
	int m_iFreeSpecialist;
	int m_iCivic;

	int* m_aiReligionYields;
	int* m_aiReligionCommerces;

	CvString m_szPopupText;
	CvString m_szSecretaryGeneralText;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvMainMenuInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMainMenuInfo : public CvInfoBase
{
public:

	DllExport CvMainMenuInfo();
	DllExport virtual ~CvMainMenuInfo();

	DllExport std::string getScene() const;
	DllExport std::string getSceneNoShader() const;
	DllExport std::string getSoundtrack() const;
	DllExport std::string getLoading() const;
	DllExport std::string getLoadingSlideshow() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	std::string m_szScene;
	std::string m_szSceneNoShader;
	std::string m_szSoundtrack;
	std::string m_szLoading;
	std::string m_szLoadingSlideshow;
};
#endif
