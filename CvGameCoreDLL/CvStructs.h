#pragma once

#ifndef CVSTRUCTS_H
#define CVSTRUCTS_H

// structs.h

//#include "CvEnums.h"
#include "CvString.h"

// XXX these should not be in the DLL per se (if the user changes them, we are screwed...)

struct DllExport XYCoords
{
	XYCoords(int x=0, int y=0) : iX(x), iY(y) {}
	int iX;
	int iY;

	bool operator<  (const XYCoords xy) const { return ((iY < xy.iY) || (iY == xy.iY && iX < xy.iX)); }
	bool operator<= (const XYCoords xy) const { return ((iY < xy.iY) || (iY == xy.iY && iX <= xy.iX)); }
	bool operator!= (const XYCoords xy) const { return (iY != xy.iY || iX != xy.iX); }
	bool operator== (const XYCoords xy) const { return (!(iY != xy.iY || iX != xy.iX)); }
	bool operator>= (const XYCoords xy) const { return ((iY > xy.iY) || (iY == xy.iY && iX >= xy.iX)); }
	bool operator>  (const XYCoords xy) const { return ((iY > xy.iY) || (iY == xy.iY && iX > xy.iX)); }
};

struct DllExport IDInfo
{

	IDInfo(PlayerTypes eOwner=NO_PLAYER, int iID=FFreeList::INVALID_INDEX) : eOwner(eOwner), iID(iID) {}
	PlayerTypes eOwner;
	int iID;

	bool operator== (const IDInfo& info) const
	{
		return (eOwner == info.eOwner && iID == info.iID);
	}

	void reset()
	{
		eOwner = NO_PLAYER;
		iID = FFreeList::INVALID_INDEX;
	}
};

struct DllExport GameTurnInfo				// Exposed to Python
{
	int iMonthIncrement;
	int iNumGameTurnsPerIncrement;
};

struct DllExport OrderData					// Exposed to Python
{
	OrderTypes eOrderType;
	int iData1;
	int iData2;
	bool bSave;
};

struct DllExport MissionData				// Exposed to Python
{
	MissionTypes eMissionType;
	int iData1;
	int iData2;
	int iFlags;
	int iPushTurn;
};

struct DllExport TradeData					// Exposed to Python
{
	TradeableItems m_eItemType;				//	What type of item is this
	int m_iData;											//	Any additional data?
	bool m_bOffering;									//	Is this item up for grabs?
	bool m_bHidden;										//	Are we hidden?
};

struct EventTriggeredData
{
	int m_iId;
	EventTriggerTypes m_eTrigger;
	int m_iTurn;
	PlayerTypes m_ePlayer;
	int m_iCityId;
	int m_iPlotX;
	int m_iPlotY;
	int m_iUnitId;
	PlayerTypes m_eOtherPlayer;
	int m_iOtherPlayerCityId;
	ReligionTypes m_eReligion;
	CorporationTypes m_eCorporation;
	BuildingTypes m_eBuilding;
	CvWString m_szText;
	CvWString m_szGlobalText;

	int getID() const;
	void setID(int iID);
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

struct VoteSelectionSubData
{
	VoteTypes eVote;
	PlayerTypes ePlayer;
	int iCityId;
	PlayerTypes eOtherPlayer;
	CvWString szText;
};

struct VoteSelectionData
{
	int iId;
	VoteSourceTypes eVoteSource;
	std::vector<VoteSelectionSubData> aVoteOptions;

	int getID() const;
	void setID(int iID);
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

struct VoteTriggeredData
{
	int iId;
	VoteSourceTypes eVoteSource;
	VoteSelectionSubData kVoteOption;

	int getID() const;
	void setID(int iID);
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

struct EventMessage
{
	CvWString szDescription;
	int iExpirationTurn;
	int iX;
	int iY;

	// python friendly accessors
	std::wstring getDescription() const { return szDescription;	}
};

struct PlotExtraYield
{
	int m_iX;
	int m_iY;
	std::vector<int> m_aeExtraYield;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

struct PlotExtraCost
{
	int m_iX;
	int m_iY;
	int m_iCost;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

typedef std::vector< std::pair<BuildingClassTypes, int> > BuildingChangeArray;

struct BuildingYieldChange
{
	BuildingClassTypes eBuildingClass;
	YieldTypes eYield;
	int iChange;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

struct BuildingCommerceChange
{
	BuildingClassTypes eBuildingClass;
	CommerceTypes eCommerce;
	int iChange;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};


struct DllExport FOWVis
{
	uint uiCount;
	POINT* pOffsets;  // array of "Offset" points

	// python friendly accessors
	POINT getOffsets(int i) const { return pOffsets[i]; }
};

struct DllExport PBGameSetupData
{
	PBGameSetupData();

	int iSize;
	int iClimate;
	int iSeaLevel;
	int iSpeed;
	int iEra;

	int iMaxTurns;
	int iCityElimination;
	int iAdvancedStartPoints;
	int iTurnTime;

	int iNumCustomMapOptions;
	int * aiCustomMapOptions;
	int getCustomMapOption(int iOption) {return aiCustomMapOptions[iOption];}

	int iNumVictories;
	bool * abVictories;
	bool getVictory(int iVictory) {return abVictories[iVictory];}

	std::wstring szMapName;
	std::wstring getMapName() {return szMapName;}

	std::vector<bool> abOptions;
	bool getOptionAt(int iOption) {return abOptions[iOption];}

	std::vector<bool> abMPOptions;
	bool getMPOptionAt(int iOption) {return abMPOptions[iOption];}
};

struct DllExport PBPlayerSetupData
{
	int iWho;
	int iCiv;
	int iLeader;
	int iTeam;
	int iDifficulty;

	std::wstring szStatusText;
	std::wstring getStatusText() {return szStatusText;}
};

struct DllExport PBPlayerAdminData
{
	std::wstring szName;
	std::wstring getName() {return szName;}
	std::wstring szPing;
	std::wstring getPing() {return szPing;}
	std::wstring szScore;
	std::wstring getScore() {return szScore;}
	bool bHuman;
	bool bClaimed;
	bool bTurnActive;
};

class CvUnit;
class CvPlot;

//! An enumeration for indexing units within a CvBattleDefinition
enum BattleUnitTypes
{
	BATTLE_UNIT_ATTACKER,	//!< Index referencing the attacking unit
	BATTLE_UNIT_DEFENDER,	//!< Index referencing the defending unit
	BATTLE_UNIT_COUNT		//!< The number of unit index references
};

void checkBattleUnitType(BattleUnitTypes unitType);

//!< An enumeration for indexing times within the CvBattleDefinition
enum BattleTimeTypes
{
	BATTLE_TIME_BEGIN,
	BATTLE_TIME_RANGED,
	BATTLE_TIME_END,
	BATTLE_TIME_COUNT
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  STRUCT:      CvBattleRound
//!  \brief		Represents a single round within a battle.
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DllExport CvBattleRound
{
public:
	CvBattleRound();
	bool isValid() const;

	bool isRangedRound() const;
	void setRangedRound(bool value);

	int getWaveSize() const;
	void setWaveSize(int size);

	int getNumKilled(BattleUnitTypes unitType) const;
	void setNumKilled(BattleUnitTypes unitType, int value);
	void addNumKilled(BattleUnitTypes unitType, int increment);

	int getNumAlive(BattleUnitTypes unitType) const;
	void setNumAlive(BattleUnitTypes unitType, int value);

private:
	int		m_aNumKilled[BATTLE_UNIT_COUNT];		//!< The number of units killed during this round for both sides
	int		m_aNumAlive[BATTLE_UNIT_COUNT];		//!< The number of units alive at the end of this round for both sides
	int		m_iWaveSize;				//!< The number of units that can perform exchanges
	bool	m_bRangedRound;				//!< true if this round is ranged, false otherwise
};

//------------------------------------------------------------------------------------------------

typedef std::vector<CvBattleRound> CvBattleRoundVector;		//!< Type declaration for a collection of battle round definitions

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  CLASS:      CvMissionDefinition
//!  \brief		Base mission definition struct
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DllExport CvMissionDefinition
{
public:
	CvMissionDefinition();

	MissionTypes getMissionType() const;
	void setMissionType(MissionTypes missionType);

	float getMissionTime() const;
	void setMissionTime(float time);

	CvUnit *getUnit(BattleUnitTypes unitType) const;
	void setUnit(BattleUnitTypes unitType, CvUnit *unit);

	const CvPlot *getPlot() const;
	void setPlot(const CvPlot *plot);

protected:
	MissionTypes		m_eMissionType;			//!< The type of event
	CvUnit *			m_aUnits[BATTLE_UNIT_COUNT];		//!< The units involved
	float				m_fMissionTime;			//!< The amount of time that the event will take
	const CvPlot *		m_pPlot;					//!< The plot associated with the event
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  STRUCT:     CvBattleDefinition
//!  \brief		A definition passed to CvBattleManager to start a battle between units
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DllExport CvBattleDefinition : public CvMissionDefinition
{
public:
	CvBattleDefinition();
	CvBattleDefinition( const CvBattleDefinition & kCopy );

	int getDamage(BattleUnitTypes unitType, BattleTimeTypes timeType) const;
	void setDamage(BattleUnitTypes unitType, BattleTimeTypes timeType, int damage);
	void addDamage(BattleUnitTypes unitType, BattleTimeTypes timeType, int increment);
	
	int getFirstStrikes(BattleUnitTypes unitType) const;
	void setFirstStrikes(BattleUnitTypes unitType, int firstStrikes);
	void addFirstStrikes(BattleUnitTypes unitType, int increment);
	
	bool isAdvanceSquare() const;
	void setAdvanceSquare(bool advanceSquare);

	int getNumRangedRounds() const;
	void setNumRangedRounds(int count);
	void addNumRangedRounds(int increment);
	
	int getNumMeleeRounds() const;
	void setNumMeleeRounds(int count);
	void addNumMeleeRounds(int increment);

	int getNumBattleRounds() const;
	void clearBattleRounds();
	CvBattleRound &getBattleRound(int index);
	const CvBattleRound &getBattleRound(int index) const;
	void addBattleRound(const CvBattleRound &round);
	void setBattleRound(int index, const CvBattleRound &round);

private:
	void checkBattleTimeType(BattleTimeTypes timeType) const;
	void checkBattleRound(int index) const;

	int					m_aDamage[BATTLE_UNIT_COUNT][BATTLE_TIME_COUNT];	//!< The beginning damage of the units
	int					m_aFirstStrikes[BATTLE_UNIT_COUNT];		//!< The number of ranged first strikes the units made
	int					m_iNumRangedRounds;				//!< The number of ranged rounds
	int					m_iNumMeleeRounds;				//!< The number of melee rounds
	bool				m_bAdvanceSquare;					//!< true if the attacking unit should move into the new square
	CvBattleRoundVector	m_aBattleRounds;					//!< The rounds that define the battle plan
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  CLASS:      CvAirMissionDefinition
//!  \brief		A definition passed to CvAirMissionManager to start an air mission
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DllExport CvAirMissionDefinition : public CvMissionDefinition
{
public:
	CvAirMissionDefinition();
	CvAirMissionDefinition( const CvAirMissionDefinition & kCopy );

	int getDamage(BattleUnitTypes unitType) const;
	void setDamage(BattleUnitTypes unitType, int damage);
	bool isDead(BattleUnitTypes unitType) const;

private:
	int					m_aDamage[BATTLE_UNIT_COUNT];		//!< The ending damage of the units
};

struct DllExport CvWidgetDataStruct
{
	int m_iData1;										//	The first bit of data
	int m_iData2;										//	The second piece of data

	bool m_bOption;									//	A boolean piece of data

	WidgetTypes m_eWidgetType;			//	What the 'type' of this widget is (for parsing help and executing actions)
};

struct DllExport CvPlotIndicatorData
{
	CvPlotIndicatorData() : m_eVisibility(PLOT_INDICATOR_VISIBLE_ALWAYS), m_bFlashing(false), m_pUnit(NULL), m_bTestEnemyVisibility(false), m_bVisibleOnlyIfSelected(false), m_bPersistentRotation(false)
	{
	}
	CvString m_strIcon;
	CvString m_strLabel;
	NiColor m_kColor;
	CvWString m_strHelpText;
	PlotIndicatorVisibilityFlags m_eVisibility;
	bool m_bFlashing;
	NiPoint2 m_Target;
	const CvUnit* m_pUnit;
	bool m_bTestEnemyVisibility;
	bool m_bVisibleOnlyIfSelected;
	bool m_bPersistentRotation;
};

struct DllExport CvGlobeLayerData
{
	CvGlobeLayerData(GlobeLayerTypes eType) : m_eType(eType), m_bGlobeViewRequired(true), m_bShouldCitiesZoom(false), m_iNumOptions(0) { }
	GlobeLayerTypes m_eType;
	CvString m_strName;
	CvString m_strButtonHelpTag;
	CvString m_strButtonStyle;
	bool m_bGlobeViewRequired;
	bool m_bShouldCitiesZoom;
	int m_iNumOptions;
};

struct DllExport CvFlyoutMenuData
{
	CvFlyoutMenuData(FlyoutTypes eType, int iId, int iX, int iY, const wchar* strTitle) : m_eFlyout(eType), m_iID(iId), m_iX(iX), m_iY(iY), m_strTitle(strTitle) { }
	FlyoutTypes m_eFlyout;
	int m_iID;
	int m_iX;
	int m_iY;
	CvWString m_strTitle;
};

struct DllExport CvStatBase
{
	CvStatBase(const char* strKey) : m_strKey(strKey) { }
	virtual ~CvStatBase() { }
	CvString m_strKey;
};

struct DllExport CvStatInt : public CvStatBase
{
	CvStatInt(const char* strKey, int iValue) : CvStatBase(strKey), m_iValue(iValue) { }
	int m_iValue;
};

struct DllExport CvStatString : public CvStatBase
{
	CvStatString(const char* strKey, const char* strValue) : CvStatBase(strKey), m_strValue(strValue) { }
	CvString m_strValue;
};

struct DllExport CvStatFloat : public CvStatBase
{
	CvStatFloat(const char* strKey, float fValue) : CvStatBase(strKey), m_fValue(fValue) { }
	float m_fValue;
};

struct DllExport CvWBData
{
	CvWBData(int iId, const wchar* strHelp, const char* strButton) : m_iId(iId), m_strHelp(strHelp), m_strButton(strButton) { }
	int m_iId;
	CvWString m_strHelp;
	CvString m_strButton;
};


#endif	// CVSTRUCTS_H
