#pragma once

#ifndef CVSTRUCTS_H
#define CVSTRUCTS_H

// structs.h

// <advc.071>
class CvPlot;
class CvUnit;
// </advc.071>

// XXX these should not be in the DLL per se (if the user changes them, we are screwed...)

struct XYCoords
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

struct IDInfo
{
	/*	advc.opt: Default owner changed from NO_PLAYER to Barbarians so that
		the owner doesn't need to be checked before calling FFreeListTrashArray::getAt. */
	IDInfo(PlayerTypes eOwner = BARBARIAN_PLAYER, int iID = FFreeList::INVALID_INDEX) :
		eOwner(eOwner), iID(iID)
	{	/*	advc: Not worth slowing down assert builds I think. I've had it enabled
			for quite some time. It's fine currently and not likely to break I think. */
		//FAssert(iID != FFreeList::INVALID_INDEX || eOwner == BARBARIAN_PLAYER);
	}
	void validateOwner(); // advc.opt
	bool isIDSet() const { return iID != FFreeList::INVALID_INDEX; } // advc

	PlayerTypes eOwner;
	int iID;

	bool operator== (const IDInfo& info) const
	{
		return (eOwner == info.eOwner && iID == info.iID);
	}
	// K-Mod
	bool operator!= (const IDInfo& info) const { return !(*this==info); }
	bool operator< (const IDInfo& a) const
	{
		return eOwner < a.eOwner || (eOwner == a.eOwner && iID < a.iID);
	} // K-Mod end

	void reset()
	{
		//eOwner = NO_PLAYER;
		eOwner = BARBARIAN_PLAYER; // advc.opt
		iID = FFreeList::INVALID_INDEX;
	}
};

struct GameTurnInfo				// Exposed to Python
{
	int iMonthIncrement;
	int iNumGameTurnsPerIncrement;
};

struct OrderData					// Exposed to Python
{
	INIT_STRUCT_PADDING(OrderData);
	OrderTypes eOrderType;
	int iData1;
	int iData2;
	bool bSave;
};

struct MissionData				// Exposed to Python
{
	INIT_STRUCT_PADDING(MissionData);
	MissionTypes eMissionType;
	int iData1;
	int iData2;
	MovementFlags eFlags;
	int iPushTurn;
	bool bModified; // advc.011b
};
// <advc.011b> Needed for savegame compatibility
struct MissionDataLegacy { MissionTypes eMissionType; int iData1; int iData2;
	MovementFlags eFlags; int iPushTurn; }; // </advc.011b>

struct TradeData					// Exposed to Python
{
	// <advc> To replace global setTradeItem (CvGameCoreUtils)
	TradeData(TradeableItems eItem = NO_TRADE_ITEM, int iData = -1,
		bool bOffering = false, bool bHidden = false)
	{
		INIT_STRUCT_PADDING_INL();
		m_eItemType = eItem;
		m_iData = iData;
		m_bOffering = bOffering;
		m_bHidden = bHidden;
	} // </advc>
	TradeableItems m_eItemType;	//	What type of item is this
	int m_iData;				//	Any additional data?
	bool m_bOffering;			//	Is this item up for grabs?
	bool m_bHidden;				//	Are we hidden?
};
/*	advc.003k: Memory layout probably mustn't change b/c CLinkList<TradeData>
	occurs in the parameter lists of some exported functions */
BOOST_STATIC_ASSERT(sizeof(TradeData) == 12);

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
	VoteSelectionSubData(VoteTypes eVote = NO_VOTE) // advc: Ensure initialization
	:	eVote(eVote), ePlayer(NO_PLAYER),
		iCityId(FFreeList::INVALID_INDEX), eOtherPlayer(NO_PLAYER)
	{}
	VoteTypes eVote;
	PlayerTypes ePlayer;
	int iCityId;
	PlayerTypes eOtherPlayer;
	CvWString szText;
};

struct VoteSelectionData
{	// advc:
	VoteSelectionData(VoteSourceTypes eVS = NO_VOTESOURCE)
	:	eVoteSource(eVS), iId(FFreeList::INVALID_INDEX) {}
	int iId;
	VoteSourceTypes eVoteSource;
	std::vector<VoteSelectionSubData> aVoteOptions;

	int getID() const;
	void setID(int iID);
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};

struct VoteTriggeredData
{	// advc:
	VoteTriggeredData(VoteSourceTypes eVS = NO_VOTESOURCE)
	:	eVoteSource(eVS), iId(FFreeList::INVALID_INDEX) {}
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

// advc.enum: obsolete
/*struct PlotExtraYield
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
struct BuildingYieldChange {
	BuildingClassTypes eBuildingClass;
	YieldTypes eYield;
	int iChange;
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};
struct BuildingCommerceChange {
	BuildingClassTypes eBuildingClass;
	CommerceTypes eCommerce;
	int iChange;
	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);
};*/


struct FOWVis
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
class CvBattleRound
{
public:
	CvBattleRound();
	bool isValid() const;

	DllExport bool isRangedRound() const;
	void setRangedRound(bool value);

	DllExport int getWaveSize() const;
	DllExport void setWaveSize(int size);

	DllExport int getNumKilled(BattleUnitTypes unitType) const;
	DllExport void setNumKilled(BattleUnitTypes unitType, int value);
	void addNumKilled(BattleUnitTypes unitType, int increment);

	DllExport int getNumAlive(BattleUnitTypes unitType) const;
	DllExport void setNumAlive(BattleUnitTypes unitType, int value);

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
class CvMissionDefinition
{
public:
	CvMissionDefinition();

	DllExport MissionTypes getMissionType() const;
	void setMissionType(MissionTypes missionType);

	DllExport float getMissionTime() const;
	void setMissionTime(float time);

	DllExport CvUnit *getUnit(BattleUnitTypes unitType) const;
	void setUnit(BattleUnitTypes unitType, CvUnit *unit);

	DllExport const CvPlot *getPlot() const;
	void setPlot(const CvPlot *plot);

protected:
	MissionTypes		m_eMissionType;					//!< The type of event
	CvUnit *			m_aUnits[BATTLE_UNIT_COUNT];	//!< The units involved
	float				m_fMissionTime;					//!< The amount of time that the event will take
	const CvPlot *		m_pPlot;						//!< The plot associated with the event
};

// advc:
class NukeMissionDef : public CvMissionDefinition
{
public:
	NukeMissionDef(CvPlot const& kPlot, CvUnit& kNuke, bool bIntercept,
			int iBaseTime); // advc.002m
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  STRUCT:     CvBattleDefinition
//!  \brief		A definition passed to CvBattleManager to start a battle between units
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBattleDefinition : public CvMissionDefinition
{
public:
	CvBattleDefinition();
	DllExport CvBattleDefinition(const CvBattleDefinition & kCopy);
	DllExport ~CvBattleDefinition();
	DllExport int getDamage(BattleUnitTypes unitType, BattleTimeTypes timeType) const;
	void setDamage(BattleUnitTypes unitType, BattleTimeTypes timeType, int damage);
	void addDamage(BattleUnitTypes unitType, BattleTimeTypes timeType, int increment);

	DllExport int getFirstStrikes(BattleUnitTypes unitType) const;
	void setFirstStrikes(BattleUnitTypes unitType, int firstStrikes);
	void addFirstStrikes(BattleUnitTypes unitType, int increment);

	DllExport bool isAdvanceSquare() const;
	void setAdvanceSquare(bool advanceSquare);

	int getNumRangedRounds() const;
	void setNumRangedRounds(int count);
	void addNumRangedRounds(int increment);

	int getNumMeleeRounds() const;
	void setNumMeleeRounds(int count);
	void addNumMeleeRounds(int increment);

	DllExport int getNumBattleRounds() const;
	DllExport void clearBattleRounds();
	DllExport CvBattleRound &getBattleRound(int index);
	DllExport const CvBattleRound &getBattleRound(int index) const;
	DllExport void addBattleRound(const CvBattleRound &round);
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
class CvAirMissionDefinition : public CvMissionDefinition
{
public:
	CvAirMissionDefinition();
	DllExport CvAirMissionDefinition(const CvAirMissionDefinition & kCopy);

	DllExport int getDamage(BattleUnitTypes unitType) const;
	void setDamage(BattleUnitTypes unitType, int damage);
	DllExport bool isDead(BattleUnitTypes unitType) const;

private:
	int					m_aDamage[BATTLE_UNIT_COUNT];		//!< The ending damage of the units
};

struct CvWidgetDataStruct
{
	int m_iData1;										//	The first bit of data
	int m_iData2;										//	The second piece of data

	bool m_bOption;									//	A boolean piece of data

	WidgetTypes m_eWidgetType;			//	What the 'type' of this widget is (for parsing help and executing actions)
};

/*	advc (note, fwiw): I've noticed while inspecting disassembly that the EXE
	calls the auto-generated copy ctor of this struct. */
struct DllExport CvPlotIndicatorData
{
	CvPlotIndicatorData()
	:	m_eVisibility(PLOT_INDICATOR_VISIBLE_ALWAYS), m_bFlashing(false), m_pUnit(NULL),
		m_bTestEnemyVisibility(false), m_bVisibleOnlyIfSelected(false),
		m_bPersistentRotation(false)
	{}
	CvString m_szIcon;
	CvString m_szLabel;
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
	CvGlobeLayerData(GlobeLayerTypes eType)
	:	m_eType(eType), m_bGlobeViewRequired(true), m_bShouldCitiesZoom(false),
		m_iNumOptions(0)
	{}
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
	CvFlyoutMenuData(FlyoutTypes eType, int iId, int iX, int iY, wchar const* szTitle)
	:	m_eFlyout(eType), m_iID(iId), m_iX(iX), m_iY(iY), m_strTitle(szTitle)
	{}
	FlyoutTypes m_eFlyout;
	int m_iID;
	int m_iX;
	int m_iY;
	CvWString m_strTitle;
};

struct CvStatBase
{
	CvStatBase(const char* szKey) : m_strKey(szKey) {}
	virtual ~CvStatBase() {}
	CvString m_strKey;
};

struct CvStatInt : public CvStatBase
{
	CvStatInt(char const* szKey, int iValue)
	:	CvStatBase(szKey), m_iValue(iValue)
	{}
	int m_iValue;
};

struct CvStatString : public CvStatBase
{
	CvStatString(char const* szKey, const char* szValue)
	:	CvStatBase(szKey), m_strValue(szValue)
	{}
	CvString m_strValue;
};

struct CvStatFloat : public CvStatBase
{
	CvStatFloat(char const* szKey, float fValue)
	:	CvStatBase(szKey), m_fValue(fValue)
	{}
	float m_fValue;
};

struct DllExport CvWBData
{
	CvWBData(int iId, wchar const* szHelp, char const* szButton)
	:	m_iId(iId), m_strHelp(szHelp), m_strButton(szButton)
	{}
	int m_iId;
	CvWString m_strHelp;
	CvString m_strButton;
};
// advc.071:
struct FirstContactData
{
	FirstContactData(CvPlot const* pAt1, CvPlot const* pAt2 = NULL,
			CvUnit const* pUnit1 = NULL, CvUnit const* pUnit2 = NULL);
	FirstContactData() : u1(), u2(), x1(-1), x2(-1), y1(-1), y2(-1) {}
	IDInfo u1, u2;
	int x1, y1, x2, y2;
};
// advc.072:
struct DealItemData
{
	DealItemData() : eGivePlayer(NO_PLAYER), eReceivePlayer(NO_PLAYER),
			eItemType(TRADE_ITEM_NONE), iData(-1), iDeal(-1) {}
	DealItemData(PlayerTypes eGivePlayer, PlayerTypes eReceivePlayer,
			TradeableItems eItemType, int iData, int iDeal) :
			eGivePlayer(eGivePlayer), eReceivePlayer(eReceivePlayer),
			eItemType(eItemType), iData(iData), iDeal(iDeal) {}
	PlayerTypes eGivePlayer, eReceivePlayer;
	TradeableItems eItemType;
	int iData, iDeal;
};

#endif	// CVSTRUCTS_H
