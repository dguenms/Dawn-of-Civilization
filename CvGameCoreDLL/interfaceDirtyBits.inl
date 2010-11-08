// Dirty bits for various items in the interface (stored in a single bit vector) XXX put in enums.h???
enum DirtyBits
{
	SelectionCamera_DIRTY_BIT,
	SelectionList_DIRTY_BIT,
	SavedSelectionList_DIRTY_BIT,
	TestEndTurn_DIRTY_BIT,
	Fog_DIRTY_BIT,
	Waypoints_DIRTY_BIT,
	PercentButtons_DIRTY_BIT,
	MiscButtons_DIRTY_BIT,
	PlotListButtons_DIRTY_BIT,
	SelectionListButtons_DIRTY_BIT,
	SelectionButtons_DIRTY_BIT,
	CitizenButtons_DIRTY_BIT,
	ResearchButtons_DIRTY_BIT,
	ReplayButtons_DIRTY_BIT	,
	Event_DIRTY_BIT,
	Center_DIRTY_BIT,
	GameData_DIRTY_BIT,
	SelectionData_DIRTY_BIT,
	Info_DIRTY_BIT,
	TurnTimer_DIRTY_BIT,
	Help_DIRTY_BIT,
	MinimapSection_DIRTY_BIT,
	SelectionSound_DIRTY_BIT,
	ChatEdit_DIRTY_BIT,
	CityInfo_DIRTY_BIT,
	UnitInfo_DIRTY_BIT,

	NUM_DIRTY_BITS
};
