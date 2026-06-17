#include "CvGameCoreDLL.h"
#include "History.h"
#include "CvPlayer.h"

// advc.004s: New implementation file; see comment in header.

void History::grow(int iSize)
{
	FAssert(iSize >= 0);
	while (iSize >= size())
		m_aiValues.push_back(-1);
}


void History::set(int iTurn, int iValue)
{
	grow(iTurn);
	if (m_iMovingAvgSamples <= 0)
	{
		m_aiValues[iTurn] = iValue;
		return;
	}
	int iOldSamples = std::min(m_iMovingAvgSamples - 1, iTurn - 1);
	int iSamples = iOldSamples;
	int iSum = 0;

	iSum += iValue;
	iSamples++;

	for (int i = iTurn - 1; i >= iTurn - iOldSamples; i--)
		iSum += std::max(m_aiValues[i], 0);
	m_aiValues[iTurn] = intdiv::round(iSum, std::max(1, iSamples));
}


void History::read(FDataStreamBase* pStream)
{
	FAssert(size() == 0);
	int iSize;
	pStream->Read(&iSize);
	if (iSize > 0)
	{
		m_aiValues.resize(iSize);
		pStream->Read(iSize, &m_aiValues[0]);
	}
}


void History::write(FDataStreamBase* pStream)
{
	int iSize = size();
	pStream->Write(iSize);
	if (iSize > 0)
		pStream->Write(iSize, &m_aiValues[0]);
}
