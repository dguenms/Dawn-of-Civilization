#pragma once

#ifndef _CVSTATISTICS_H_
#define _CVSTATISTICS_H_

//#include "CvEnums.h"

class CvCity;
class CvUnit;

//
// game stats record
//
class CvGameRecord
{
	friend class CvStatistics;
public:
	void init();
	void uninit();
	void reset();

	// Map played
	void setMapName( const char * szMapName );
	const CvString& getMapName( void ) const;

	// Era played
	void setEra( EraTypes eEra );
	EraTypes getEra( void ) const;

	// for serialization
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
		
private:
	CvGameRecord();								// no one can create one of these except CvStatistics
	~CvGameRecord();					// no one can destroy one of these except CvStatistics
				
	EraTypes m_eEra;

	CvString m_szMapName;							
};


//
// player stats record
//
class CvPlayerRecord
{
friend class CvStatistics;
public:
	void init();
	void uninit();
	void reset();

	// ID
	void setPlayerID( int iID );
	DllExport int getPlayerID( void ) const;

	// Outcome
	void setVictory(VictoryTypes eVictory);
	DllExport int getVictory() const;

	// Length of time player lasted in game
	void setTimePlayed( int iTime );
	DllExport int getMinutesPlayed() const;

	// Leader/Civ played
	void setLeader( LeaderHeadTypes eLeader );
	DllExport LeaderHeadTypes getLeader() const;

	// Num units built
	void unitBuilt( CvUnit *pUnit );
	DllExport int getNumUnitsBuilt(int iUnitType) const;

	// Num units we killed
	void unitKilled( CvUnit *pUnit );
	DllExport int getNumUnitsKilled( int iUnitType ) const;

	// Num units we had killed
	void unitWasKilled( CvUnit *pUnit );
	DllExport int getNumUnitsWasKilled( int iUnitType ) const;

	// Num cities built
	void cityBuilt();
	DllExport int getNumCitiesBuilt() const;

	// Num cities razed
	void cityRazed();
	DllExport int getNumCitiesRazed() const;

	// Num buildings built
	void buildingBuilt( BuildingTypes eBuilding );
	DllExport int getNumBuildingsBuilt( BuildingTypes eBuilding ) const;

	// Religion founded
	void religionFounded( ReligionTypes eReligion );
	DllExport bool getReligionFounded( ReligionTypes eReligion ) const;

	// Num Golden Ages
	void goldenAge();
	DllExport int getNumGoldenAges() const;

	// for serialization
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);
		
private:
	CvPlayerRecord();								// no one can create one of these except CvStatistics
	~CvPlayerRecord();						// no one can destroy one of these except CvStatistics

	int m_iID;
	int m_iTime;

	VictoryTypes m_eVictory;
	LeaderHeadTypes m_eLeader;

	int * m_piNumUnitsBuilt;				//	# of total units built
	int * m_piNumUnitsKilled;				//  # of total units we killed
	int * m_piNumUnitsWasKilled;			//  # of total units we had killed
	int * m_piNumBuildingsBuilt;			//  # of total buildings we built

	bool * m_pbReligionFounded;				//  which religions we founded

	int m_iNumCitiesBuilt;								//	# of cities we have built
	int m_iNumCitiesRazed;								//	# of cities we have razed
	int m_iNumGoldenAges;									//  # of golden ages we have begun
};

//
// stats manager class
//
class CvStatistics
{
public:
	~CvStatistics();

	void init();
	void uninit();
	void reset();

	// Game stat updates
	void setMapName(const char * szMapName);
	void setEra(EraTypes eEra);

	// Player stat updates
	void setVictory( TeamTypes eWinner, VictoryTypes eVictory );
	void setTimePlayed( PlayerTypes ePlayer, int iTime );
	void setLeader( PlayerTypes ePlayer, LeaderHeadTypes eLeader );

	// Player stat events
	void unitBuilt( CvUnit *pUnit );
	void unitKilled( CvUnit *pUnit, PlayerTypes eAttacker );
	void cityBuilt( CvCity * pCity );
	void cityRazed( CvCity * pCity, PlayerTypes ePlayer );
	void buildingBuilt( CvCity *pCity, BuildingTypes eBuilding );
	void religionFounded( ReligionTypes eReligion, PlayerTypes eFounder );
	void goldenAge( PlayerTypes ePlayer );

	DllExport CvPlayerRecord* getPlayerRecord( int iIndex );

	const char* getMapName() const;
	EraTypes getEra() const;

	// for serialization
	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

private:
	CvGameRecord m_GameRecord;									// The one game record
	std::vector<CvPlayerRecord*> m_PlayerRecords;					//	The player Records
};


#endif
