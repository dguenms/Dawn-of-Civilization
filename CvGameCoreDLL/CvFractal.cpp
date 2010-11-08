// fractal.cpp

#include "CvGameCoreDLL.h"
#include "CvFractal.h"
#include "CvRandom.h"
#include "CvGameCoreUtils.h"
#include "CvGameCoreUtils.h"
#include "FProfiler.h"


#define FLOAT_PRECISION		(1000)


// Public Functions...

CvFractal::CvFractal()
{
	reset();
}

CvFractal::~CvFractal()
{
	uninit();
}

void CvFractal::uninit()
{
	if (m_aaiFrac != NULL)
	{
		for (int iX = 0; iX < m_iFracX + 1; iX++)
		{
			SAFE_DELETE_ARRAY(m_aaiFrac[iX]);
		}
		SAFE_DELETE_ARRAY(m_aaiFrac);
	}
}

void CvFractal::reset()
{
	m_aaiFrac = NULL;
	m_iFracXExp = -1;
	m_iFracYExp = -1;
	m_iXs = -1;
	m_iYs = -1;
	m_iFlags = 0;
	m_iFracX = -1;
	m_iFracY = -1;
}

void CvFractal::fracInit(int iNewXs, int iNewYs, int iGrain, CvRandom& random, int iFlags, CvFractal* pRifts, int iFracXExp/*=7*/, int iFracYExp/*=6*/)
{
	fracInitInternal(iNewXs, iNewYs, iGrain, random, NULL, -1, iFlags, pRifts, iFracXExp, iFracYExp);
}

// pbyHints should be a 1d array of bytes representing a 2d array 
//	with width = 2^(iFracXExp - minExp + iGrain) + (GC.getMapINLINE().isWrapXINLINE() ? 0 : 1)
//	and height = 2^(iFracYExp - minExp + iGrain) + (GC.getMapINLINE().isWrapYINLINE() ? 0 : 1)
// where minExp = std::min(iFracXExp, iFracYExp)
// Note above that an extra value is required in a dimension in which the map does not wrap.

void CvFractal::fracInitHinted(int iNewXs, int iNewYs, int iGrain, CvRandom& random, byte* pbyHints, int iHintsLength, int iFlags, CvFractal* pRifts, int iFracXExp/*=7*/, int iFracYExp/*=6*/)
{
	int iFlagsNonPolar = iFlags & (~FRAC_POLAR);
	fracInitInternal(iNewXs, iNewYs, iGrain, random, pbyHints, iHintsLength, iFlagsNonPolar, pRifts, iFracXExp, iFracYExp);
}

void CvFractal::fracInitInternal(int iNewXs, int iNewYs, int iGrain, CvRandom& random, byte* pbyHints, int iHintsLength, int iFlags, CvFractal* pRifts, int iFracXExp, int iFracYExp)
{
	PROFILE("CvFractal::fracInit()");
	int iSmooth;
	int iScreen;  // This screens out already marked spots in m_aaiFrac[][];
	int iPass;
	int iSum;
	int iX, iY;
	int iI;

	reset();

	if (iFracXExp < 0)
	{
		iFracXExp = DEFAULT_FRAC_X_EXP;
	}
	if (iFracYExp < 0)
	{
		iFracYExp = DEFAULT_FRAC_Y_EXP;
	}

	m_iFracXExp = iFracXExp;
	m_iFracYExp = iFracYExp;
	m_iFracX = 1 << iFracXExp;
	m_iFracY = 1 << iFracYExp;

	// Init m_aaiFrac to all zeroes:
	m_aaiFrac = new int*[m_iFracX + 1];
	for (iX = 0; iX < m_iFracX + 1; iX++)
	{
		m_aaiFrac[iX] = new int[m_iFracY + 1];
		for (iY = 0; iY < m_iFracY + 1; iY++)
		{
			m_aaiFrac[iX][iY] = 0;
		}
	}

	m_iXs = iNewXs;
	m_iYs = iNewYs;
	m_iFlags = iFlags;
	m_iXInc = ((m_iFracX * FLOAT_PRECISION) / m_iXs);
	m_iYInc = ((m_iFracY * FLOAT_PRECISION) / m_iYs);

	int iMinExp = std::min(m_iFracXExp, m_iFracYExp);
	iSmooth = range(iMinExp - iGrain, 0, iMinExp);

	int iHintsWidth = (1 << (m_iFracXExp - iSmooth)) + ((m_iFlags & FRAC_WRAP_X) ? 0 : 1);
	int iHintsHeight = (1 << (m_iFracYExp - iSmooth)) + ((m_iFlags & FRAC_WRAP_Y) ? 0 : 1);
	if (pbyHints != NULL)
	{
		FAssertMsg(iHintsLength == iHintsWidth*iHintsHeight, "pbyHints is the wrong size!")
	}

	for (iPass = iSmooth; iPass >= 0; iPass--)
	{
		iScreen = 0;

		for (iI = 0; iI <= iPass; iI++)
		{
			iScreen |= (1 << iI);
		}

		if (m_iFlags & FRAC_WRAP_Y)
		{
			for (iX = 0; iX < m_iFracX + 1; iX++)
			{
				m_aaiFrac[iX][m_iFracY] = m_aaiFrac[iX][0];
			}
		}
		else if (m_iFlags & FRAC_POLAR)
		{
			for (iX = 0; iX < m_iFracX + 1; iX++)
			{
				m_aaiFrac[iX][   0    ] = 0;
				m_aaiFrac[iX][m_iFracY] = 0;
			}
		}

		if (m_iFlags & FRAC_WRAP_X)
		{
			for (iY = 0; iY < m_iFracY + 1; iY++)
			{
				m_aaiFrac[m_iFracX][iY] = m_aaiFrac[0][iY];
			}
		}
		else if (m_iFlags & FRAC_POLAR)
		{
			for (iY = 0; iY < m_iFracY + 1; iY++)
			{
				m_aaiFrac[   0    ][iY] = 0;
				m_aaiFrac[m_iFracX][iY] = 0;
			}
		}

		if (m_iFlags & FRAC_CENTER_RIFT)
		{
			if (m_iFlags & FRAC_WRAP_Y)
			{
				for (iX = 0; iX < m_iFracX + 1; iX++)
				{
					for (iY = 0; iY < (m_iFracY / 6); iY++)
					{
						m_aaiFrac[iX][        iY         ] /= (abs((m_iFracY / 12) - iY) + 1);
						m_aaiFrac[iX][(m_iFracY / 2) + iY] /= (abs((m_iFracY / 12) - iY) + 1);
					}
				}
			}

			if (m_iFlags & FRAC_WRAP_X)
			{
				for (iY = 0; iY < m_iFracY + 1; iY++)
				{
					for (iX = 0; iX < (m_iFracX / 6); iX++)
					{
						m_aaiFrac[        iX         ][iY] /= (abs((m_iFracX / 12) - iX) + 1);
						m_aaiFrac[(m_iFracX / 2) + iX][iY] /= (abs((m_iFracX / 12) - iX) + 1);
					}
				}
			}
		}

		for (iX = 0; iX < (m_iFracX >> iPass) + ((m_iFlags & FRAC_WRAP_X) ? 0 : 1); iX++)
		{
			gDLL->callUpdater();
			for (iY = 0; iY < (m_iFracY >> iPass) + ((m_iFlags & FRAC_WRAP_Y) ? 0 : 1); iY++)
			{
				if ((iPass == iSmooth))// If this is the first, pass, set the initial random spots
				{  
					if (pbyHints == NULL)
					{
						m_aaiFrac[iX << iPass][iY << iPass] = random.get(256, "Fractal Gen");
					}
					else
					{
						int iXX = iX % iHintsWidth;  // wrap
						int iYY = iY % iHintsHeight; // wrap
						int iHintsI = iYY*iHintsWidth + iXX;
						FAssertMsg(iHintsI < iHintsLength, "iHintsI out of range");
						m_aaiFrac[iX << iPass][iY << iPass] = pbyHints[iHintsI];
					}
				}
				else  // Interpolate
				{
					iSum = 0;
					if ((iX << iPass) & iScreen)
					{
						if ((iY << iPass) & iScreen)  // (center)
						{
							iSum += m_aaiFrac[(iX-1) << iPass][(iY-1) << iPass];
							iSum += m_aaiFrac[(iX+1) << iPass][(iY-1) << iPass];
							iSum += m_aaiFrac[(iX-1) << iPass][(iY+1) << iPass];
							iSum += m_aaiFrac[(iX+1) << iPass][(iY+1) << iPass];
							iSum >>= 2;
							iSum += random.get(1 << (8 - iSmooth + iPass), "Fractal Gen 2");
							iSum -= 1 << (7 - iSmooth + iPass);
							iSum = range(iSum, 0, 255);
							m_aaiFrac[iX << iPass][iY << iPass] = iSum;
						}
						else  // (horizontal)
						{
							iSum += m_aaiFrac[(iX-1) << iPass][iY << iPass];
							iSum += m_aaiFrac[(iX+1) << iPass][iY << iPass];
							iSum >>= 1;
							iSum += random.get (1 << (8 - iSmooth + iPass), "Fractal Gen 3");
							iSum -= 1 << (7 - iSmooth + iPass);
							iSum = range (iSum, 0, 255);
							m_aaiFrac[iX << iPass][iY << iPass] = iSum;
						}
					}
					else
					{
						if ((iY << iPass) & iScreen)  // (vertical)
						{
							iSum += m_aaiFrac[iX << iPass][(iY-1) << iPass];
							iSum += m_aaiFrac[iX << iPass][(iY+1) << iPass];
							iSum >>= 1;
							iSum += random.get (1 << (8 - iSmooth + iPass), "Fractal Gen 4");
							iSum -= 1 << (7 - iSmooth + iPass);
							iSum = range (iSum, 0, 255);
							m_aaiFrac[iX << iPass][iY << iPass] = (BYTE) iSum;
						}
						else
						{
							continue;  // (corner) This was already set in an earlier iPass.
						}
					}
				}
			}
		}
	}

	if (pRifts)
	{
		tectonicAction(pRifts);  //  Assumes FRAC_WRAP_X is on.
	}

	if (m_iFlags & FRAC_INVERT_HEIGHTS)
	{
		for (iX = 0; iX < m_iFracX; iX++)
		{
			for (iY = 0; iY < m_iFracY; iY++)
			{
				m_aaiFrac[iX][iY] = (255 - m_aaiFrac[iX][iY]);
			}
		}
	}
}


int CvFractal::getHeight(int iX, int iY)
{
	int iErrX;
	int iErrY;
	int iSum;
	int iHeight;
	int iLowX;
	int iLowY;
	int iI;

	FAssertMsg(0 <= iX && iX < m_iXs, "iX out of range");
	FAssertMsg(0 <= iY && iY < m_iYs, "iY out of range");
	iLowX = ((m_iXInc * iX) / FLOAT_PRECISION);
	if (iLowX > m_iFracX - 1)
	{
		iLowX = m_iFracX - 1;	// clamp so that iLowX+1 doesn't overrun array
	}
	iLowY = ((m_iYInc * iY) / FLOAT_PRECISION);
	if (iLowY > m_iFracY - 1)
	{
		iLowY = m_iFracY - 1;	// clamp so that iLowY+1 doesn't overrun array
	}
	iErrX = ((m_iXInc * iX) - (iLowX * FLOAT_PRECISION));
	iErrY = ((m_iYInc * iY) - (iLowY * FLOAT_PRECISION));

	iSum = 0;
	iSum += ((FLOAT_PRECISION - iErrX) * (FLOAT_PRECISION - iErrY) * m_aaiFrac[iLowX    ][iLowY    ]);
	iSum += ((                  iErrX) * (FLOAT_PRECISION - iErrY) * m_aaiFrac[iLowX + 1][iLowY    ]);
	iSum += ((FLOAT_PRECISION - iErrX) * (                  iErrY) * m_aaiFrac[iLowX    ][iLowY + 1]);
	iSum += ((                  iErrX) * (                  iErrY) * m_aaiFrac[iLowX + 1][iLowY + 1]);

	iSum /= (FLOAT_PRECISION * FLOAT_PRECISION);

	iHeight = range(iSum, 0, 255);

	if (m_iFlags & FRAC_PERCENT)
	{
		iI = ((iHeight * 100) >> 8);

		return iI;
	}
	else
	{
		return iHeight;
	}
}


int CvFractal::getHeightFromPercent(int iPercent)
{
	PROFILE("CvFractal::getHeightFromPercent()");
	int iEstimate;
	int iLowerBound;
	int iUpperBound;
	int iSum;
	int iX, iY;

	iLowerBound = 0;
	iUpperBound = 255;

	iPercent = range(iPercent, 0, 100);
	iEstimate = 255 * iPercent / 100;

	while (iEstimate != iLowerBound)
	{
		iSum = 0;

		for (iX = 0; iX < m_iFracX; iX++)
		{
			for (iY = 0; iY < m_iFracY; iY++)
			{
				if (m_aaiFrac[iX][iY] < iEstimate)
				{
					iSum++;
				}
			}
		}
		if ((100 * iSum / m_iFracX / m_iFracY) > iPercent)
		{
			iUpperBound = iEstimate;
			iEstimate = (iUpperBound + iLowerBound) / 2;
		}
		else
		{
			iLowerBound = iEstimate;
			iEstimate = (iUpperBound + iLowerBound) / 2;
		}
	}

	return iEstimate;
}

// Protected Functions...

void CvFractal::tectonicAction(CvFractal* pRifts)  //  Assumes FRAC_WRAP_X is on.
{
	int iRift1x;
	int iRift2x;
	int iDeep;
	int iWidth;
	int iRx, iLx;
	int iX, iY;

	iRift1x = (m_iFracX / 4);
	iRift2x = ((m_iFracX / 4) * 3);

	iWidth = 16;

	for (iY = 0; iY < m_iFracY + 1; iY++)
	{
		for (iX = 0; iX < iWidth; iX++)
		{
			//  Rift along edge of map.
			iDeep = 0;
			iRx = yieldX (((((pRifts->m_aaiFrac[iRift2x][iY] - 128) * m_iFracX) / 128) / 8) + iX);
			iLx = yieldX (((((pRifts->m_aaiFrac[iRift2x][iY] - 128) * m_iFracX) / 128) / 8) - iX);
			m_aaiFrac[iRx][iY] = (((m_aaiFrac[iRx][iY] * iX) + iDeep * (iWidth - iX)) / iWidth);
			m_aaiFrac[iLx][iY] = (((m_aaiFrac[iLx][iY] * iX) + iDeep * (iWidth - iX)) / iWidth);
		}
	}

	for (iY = 0; iY < m_iFracY + 1; iY++)
	{
		m_aaiFrac[m_iFracX][iY] = m_aaiFrac[0][iY];
	}
}


int CvFractal::yieldX(int iBadX)  //  Assumes FRAC_WRAP_X is on.
{
	if (iBadX < 0)
	{
		return (iBadX + m_iFracX);
	}

	if (iBadX >= m_iFracX)
	{
		return (iBadX - m_iFracX);
	}

	return iBadX;
}
