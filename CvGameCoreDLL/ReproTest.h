#pragma once

#ifndef REPRO_TEST_H
#define REPRO_TEST_H

/*	advc.repro: When ENABLE_REPRO_TEST is defined, then contacting an AI leader via
	right click in the Foreign Advisor (see startTest call in CvDLLWidgetData.cpp)
	will start a "reproducibility test": Quick-save; run AI Auto Play for a number
	of turns equal to the id of the contacted player; upon auto-saving after AI Auto Play,
	copy all synchronized savegame data to a place that doesn't get reset upon loading
	(namely to m_pReproTest->m_aaSaveData); quick-load; run AI Auto Play for the
	same number of turns as before; upon auto-saving, compare the synchronized data
	that gets written to the savegame with the data kept in memory and assert that
	they're the same.
	Prerequisites: Assert (or Debug) build, AutoSaveInterval = 1 in CivilizationIV.ini.
	May also want to enable the BBAI log (BBAILog.h) and MessageLog, maybe also RandLog
	in CivilizationIV.ini. (See comment in ReproTest constructor about comparing logs.)
	Caveat: MSVC03 doesn't initialize padding bytes. CLinkList will write those into
	savegames. I've fixed that for a few structs through the INIT_STRUCT_PADDING macro,
	but there might be more. */
//#define ENABLE_REPRO_TEST

#ifdef ENABLE_REPRO_TEST
	#define REPRO_TEST_REPORT(iBytes, aBytes) \
		if (ReproTest::getInstance() != NULL) \
			ReproTest::getInstance()->recordData((iBytes), (byte const*)(aBytes));
	#define REPRO_TEST_BEGIN_WRITE(szObjectID) \
		if (ReproTest::getInstance() != NULL) \
			ReproTest::getInstance()->beginWrite(CvString(szObjectID));
	#define REPRO_TEST_END_WRITE() \
		if (ReproTest::getInstance() != NULL) \
			ReproTest::getInstance()->endWrite(false);
	#define REPRO_TEST_FINAL_WRITE() \
		if (ReproTest::getInstance() != NULL) \
			ReproTest::getInstance()->endWrite(true);
	#define INIT_STRUCT_PADDING_INL() \
		SecureZeroMemory(this, sizeof(*this))
	#define INIT_STRUCT_PADDING(StructName) \
		StructName() { INIT_STRUCT_PADDING_INL(); }
#else
	#define REPRO_TEST_REPORT(iBytes, aBytes)
	#define REPRO_TEST_BEGIN_WRITE(szObjectID)
	#define REPRO_TEST_END_WRITE()
	#define REPRO_TEST_FINAL_WRITE()
	#define INIT_STRUCT_PADDING_INL()
	#define INIT_STRUCT_PADDING(StructName)
#endif


class CvString;

class ReproTest
{
	static ReproTest* m_pReproTest;
public:
	static void startTest(int iTurns);
	static ReproTest* getInstance() { return m_pReproTest; }
	ReproTest(int iTurns);
	void beginWrite(CvString szObjectId);
	void endWrite(bool bFinal);
	void recordData(int iBytes, byte const aBytes[]);

private:
	int m_iAutoPlayTurns;
	bool m_bQuickLoadDone;
	std::vector<byte> m_aBytes;
	std::vector<CvString> m_aObjectIDs;
	std::vector<std::vector<byte> > m_aaSaveData;
	size_t m_iPos;
};

#endif
