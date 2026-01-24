// advc.repro: New file; see comment in header.

#include "CvGameCoreDLL.h"
#include "ReproTest.h"
#include "CvGame.h"
#include "BBAILog.h"

ReproTest* ReproTest::m_pReproTest = NULL;

void ReproTest::startTest(int iTurns)
{
	SAFE_DELETE(m_pReproTest);
	ReproTest::m_pReproTest = new ReproTest(iTurns);
}

ReproTest::ReproTest(int iTurns)
{
	m_iAutoPlayTurns = iTurns;
	m_bQuickLoadDone = false;
	m_iPos = 0;
	CvGame& kGame = GC.getGame();
	if (!kGame.canDoControl(CONTROL_QUICK_SAVE))
	{
		FErrorMsg("Open widget blocks quick-save. Repro test canceled.");
		return;
	}
	kGame.doControl(CONTROL_QUICK_SAVE);
	/*	For comparing logs, one will have to copy the part in between
		"start" and "reloading" to a new file and the part between
		"reloading" and "end"; then get a diff. */
	#ifdef LOG_AI
		logBBAI("ReproTest: start\n");
	#endif
	if (GC.isLogging())
		gDLL->messageControlLog("ReproTest: start");
	kGame.setAIAutoPlay(m_iAutoPlayTurns, true);
}

void ReproTest::recordData(int iBytes, byte const aBytes[])
{
	// NULL possible despite iBytes > 0 when aBytes points to the 0th element of an empty vector
	if (iBytes <= 0 || aBytes == NULL || GC.getGame().getAIAutoPlay() > 0)
		return;
	for (int i = 0; i < iBytes; i++)
	{
		m_aBytes.push_back(aBytes[i]);
		/*	For pinpointing the cause of "byte %d differs" assertions.
			(examples; only helpful w/ debugger): */
		//FAssert(m_aBytes.size()!=220||m_aObjectIDs.back()!="Game pt1");
		//FAssert(m_aBytes.size()!=568||m_aObjectIDs.back()!="PlayerPt1(1)");
	}
}

void ReproTest::beginWrite(CvString szObjectId)
{
	m_aBytes.clear();
	if (GC.getGame().getAIAutoPlay() <= 0 && !m_bQuickLoadDone)
		m_aObjectIDs.push_back(szObjectId);
}

void ReproTest::endWrite(bool bFinal)
{
	CvGame& kGame = GC.getGame();
	if (kGame.getAIAutoPlay() > 0)
		return;
	FAssert(!m_aBytes.empty());
	if (!m_bQuickLoadDone)
	{
		m_aaSaveData.push_back(m_aBytes);
		if (bFinal)
		{
			if (!kGame.canDoControl(CONTROL_QUICK_LOAD))
			{
				FErrorMsg("Open widget blocks quick-load. Repro test canceled.");
				SAFE_DELETE(m_pReproTest);
				return;
			}
			bool bDebugMode = kGame.isDebugMode();
			m_bQuickLoadDone = true;
			kGame.doControl(CONTROL_QUICK_LOAD);
			#ifdef LOG_AI
				logBBAI("ReproTest: reloading");
			#endif
			if (GC.isLogging())
				gDLL->messageControlLog("ReproTest: reloading\n");
			/*	Debug mode gets turned off after reload. Needs to be consistent
				because, otherwise, CvPlayer::m_listGameMessages won't be reproducible. */
			if (bDebugMode)
				kGame.toggleDebugMode();
			kGame.setAIAutoPlay(m_iAutoPlayTurns, true);
		}
		return;
	}
	CvString szMsg = CvString::format("Non reproducible state of %s "
			"%d turns after quicksave",
			m_aObjectIDs[m_iPos].GetCString(), m_iAutoPlayTurns);
	size_t iOldLen = m_aaSaveData[m_iPos].size();
	size_t iLen = m_aBytes.size();
	if (iLen != iOldLen)
	{
		CvString szLenMsg = szMsg + CvString::format(
				". iLen is %d, iOldLen is %d", iLen, iOldLen);
		FAssertMsg(iLen == iOldLen, szLenMsg.GetCString());
		// Actually, let's still step through the data.
		/*SAFE_DELETE(m_pReproTest);
		return;*/
	}
	bool const bCancelAfterFirstDifference = true;
	bool bSame = true;
	for (size_t i = 0; i < std::min(iLen, iOldLen); i++)
	{
		CvString szLoopMsg;
		if (m_aBytes[i] != m_aaSaveData[m_iPos][i])
		{
			szLoopMsg = szMsg + CvString::format(": byte %d differs: m_aBytes[%d] is %d,"
					" m_aaSaveData[m_iPos][%d] is %d.", i, i, m_aBytes[i], i,
					m_aaSaveData[m_iPos][i]);
			if (i < 80 && i > 0)
			{
				szLoopMsg += " m_aBytes:\n";
				for (size_t j = 0; j < i; j++)
					szLoopMsg += CvString::format("%d.", m_aBytes[j]);
				szLoopMsg += "\nm_aaSaveData[m_iPos]:\n";
				for (size_t j = 0; j < i; j++)
					szLoopMsg += CvString::format("%d.", m_aaSaveData[m_iPos][j]);
			}
			FErrorMsg(szLoopMsg.GetCString());
			bSame = false;
			if (bCancelAfterFirstDifference)
				break;
		}
	}
	m_iPos++;
	if (m_iPos == m_aObjectIDs.size() || (bCancelAfterFirstDifference && !bSame))
	{
		SAFE_DELETE(m_pReproTest);
		#ifdef LOG_AI
			logBBAI("ReproTest: done");
		#endif
		if (GC.isLogging())
			gDLL->messageControlLog("ReproTest: done\n");
	}
}
