#include "CvGameCoreDLL.h"
#include "CvFractal.h"


#define FLOAT_PRECISION 1024 // advc.opt: was 1000


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
	m_eFlags = NO_FLAGS;
	m_iFracX = -1;
	m_iFracY = -1;
	m_iXInc = m_iYInc = -1; // advc: better initialize
}

void CvFractal::fracInit(int iNewXs, int iNewYs, int iGrain, CvRandom& random,
	int iFlags, CvFractal* pRifts, int iFracXExp/*=7*/, int iFracYExp/*=6*/)
{
	fracInitInternal(iNewXs, iNewYs, iGrain, random, NULL, -1,
			(Flags)iFlags, pRifts, iFracXExp, iFracYExp);
}

/*	pbyHints should be a 1d array of bytes representing a 2d array
	with width = 2^(iFracXExp - minExp + iGrain) + (GC.getMap().isWrapX() ? 0 : 1)
	and height = 2^(iFracYExp - minExp + iGrain) + (GC.getMap().isWrapY() ? 0 : 1)
	where minExp = std::min(iFracXExp, iFracYExp)
	Note above that an extra value is required in a dimension
	in which the map does not wrap. */
void CvFractal::fracInitHinted(int iNewXs, int iNewYs, int iGrain, CvRandom& random,
	byte* pbyHints, int iHintsLength, int iFlags, CvFractal* pRifts,
	int iFracXExp, int iFracYExp)
{
	Flags eFlagsNonPolar = ((Flags)iFlags) & (~FRAC_POLAR);
	fracInitInternal(iNewXs, iNewYs, iGrain, random, pbyHints, iHintsLength,
			eFlagsNonPolar, pRifts, iFracXExp, iFracYExp);
}

void CvFractal::fracInitInternal(int iNewXs, int iNewYs, int iGrain, CvRandom& random,
	byte* pbyHints, int iHintsLength, Flags eFlags, CvFractal* pRifts,
	int iFracXExp, int iFracYExp)
{
	PROFILE("CvFractal::fracInit()");

	reset();

	bool bDefaultInternalDims = true; // advc.137
	if (iFracXExp < 0 /* advc.137: */ || iFracXExp == DEFAULT_FRAC_X_EXP)
		iFracXExp = DEFAULT_FRAC_X_EXP;
	else bDefaultInternalDims = false; // advc.137
	if (iFracYExp < 0 /* advc.137: */ || iFracYExp == DEFAULT_FRAC_Y_EXP)
		iFracYExp = DEFAULT_FRAC_Y_EXP;
	else bDefaultInternalDims = false; // advc.137
	/*	iFracXExp should be 8 or less
		iFracYExp should be one less than iFracXExp for Civ3 worlds */
	// <advc.137> I think this should depend on the ratio of iNewXs to iNewYs
	if (bDefaultInternalDims && 2 * iNewXs < 3 * iNewYs && pbyHints == NULL)
	{
		iFracYExp++;
		if (2 * iNewXs < iNewYs)
			iFracXExp--;
		// Akin to what RandomScriptMap's R_MultilayeredFractal does
		if (iNewXs >= 90 && iNewYs >= 70)
		{
			iFracXExp++;
			iFracYExp++;
		}
		FAssert(iFracXExp <= 8 && iFracYExp <= 8 && abs(iFracXExp - iFracYExp) <= 1);
	} // </advc.137>
	m_iFracXExp = iFracXExp;
	m_iFracYExp = iFracYExp;
	m_iFracX = 1 << iFracXExp;
	m_iFracY = 1 << iFracYExp;

	// Init m_aaiFrac to all zeroes:
	m_aaiFrac = new int*[m_iFracX + 1];
	for (int iX = 0; iX < m_iFracX + 1; iX++)
	{
		m_aaiFrac[iX] = new int[m_iFracY + 1];
		for (int iY = 0; iY < m_iFracY + 1; iY++)
		{
			m_aaiFrac[iX][iY] = 0;
		}
	}

	m_iXs = iNewXs;
	m_iYs = iNewYs;
	m_eFlags = eFlags;
	m_iXInc = ((m_iFracX * FLOAT_PRECISION) / m_iXs);
	m_iYInc = ((m_iFracY * FLOAT_PRECISION) / m_iYs);

	int iMinExp = std::min(m_iFracXExp, m_iFracYExp);
	int iSmooth = range(iMinExp - iGrain, 0, iMinExp);

	int iHintsWidth = (1 << (m_iFracXExp - iSmooth)) + ((m_eFlags & FRAC_WRAP_X) ? 0 : 1);
	int iHintsHeight = (1 << (m_iFracYExp - iSmooth)) + ((m_eFlags & FRAC_WRAP_Y) ? 0 : 1);

	FAssertMsg(pbyHints == NULL || iHintsLength == iHintsWidth*iHintsHeight, "pbyHints is the wrong size!");

	int const iPolarHeight = polarHeight(); // advc.tsl

	for (int iPass = iSmooth; iPass >= 0; iPass--)
	{
		int iScreen = 0;  // This screens out already marked spots in m_aaiFrac[][];

		for (int i = 0; i <= iPass; i++)
		{
			iScreen |= (1 << i);
		}

		if (m_eFlags & FRAC_WRAP_Y)
		{
			for (int iX = 0; iX < m_iFracX + 1; iX++)
			{
				m_aaiFrac[iX][m_iFracY] = m_aaiFrac[iX][0];
			}
		}
		else if (m_eFlags & FRAC_POLAR)
		{
			for (int iX = 0; iX < m_iFracX + 1; iX++)
			{
				m_aaiFrac[iX][   0    ] = iPolarHeight;
				m_aaiFrac[iX][m_iFracY] = iPolarHeight;
			}
		}

		if (m_eFlags & FRAC_WRAP_X)
		{
			for (int iY = 0; iY < m_iFracY + 1; iY++)
			{
				m_aaiFrac[m_iFracX][iY] = m_aaiFrac[0][iY];
			}
		}
		else if (m_eFlags & FRAC_POLAR)
		{
			for (int iY = 0; iY < m_iFracY + 1; iY++)
			{
				m_aaiFrac[   0    ][iY] = iPolarHeight;
				m_aaiFrac[m_iFracX][iY] = iPolarHeight;
			}
		}

		if (m_eFlags & FRAC_CENTER_RIFT)
		{
			if (m_eFlags & FRAC_WRAP_Y)
			{
				for (int iX = 0; iX < m_iFracX + 1; iX++)
				{
					for (int iY = 0; iY < (m_iFracY / 6); iY++)
					{
						m_aaiFrac[iX][        iY         ] /= (abs((m_iFracY / 12) - iY) + 1);
						m_aaiFrac[iX][(m_iFracY / 2) + iY] /= (abs((m_iFracY / 12) - iY) + 1);
					}
				}
			}
			if (m_eFlags & FRAC_WRAP_X)
			{
				for (int iY = 0; iY < m_iFracY + 1; iY++)
				{
					for (int iX = 0; iX < (m_iFracX / 6); iX++)
					{
						m_aaiFrac[        iX         ][iY] /= (abs((m_iFracX / 12) - iX) + 1);
						m_aaiFrac[(m_iFracX / 2) + iX][iY] /= (abs((m_iFracX / 12) - iX) + 1);
					}
				}
			}
		}

		for (int iX = 0; iX < (m_iFracX >> iPass) +
			((m_eFlags & FRAC_WRAP_X) ? 0 : 1); iX++)
		{
			gDLL->callUpdater();
			for (int iY = 0; iY < (m_iFracY >> iPass) +
				((m_eFlags & FRAC_WRAP_Y) ? 0 : 1); iY++)
			{
				if (iPass == iSmooth)// If this is the first, pass, set the initial random spots
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
					int iSum = 0;
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
		tectonicAction(pRifts);  //  Assumes FRAC_WRAP_X is on.

	if (m_eFlags & FRAC_INVERT_HEIGHTS)
	{
		for (int iX = 0; iX < m_iFracX; iX++)
		{
			for (int iY = 0; iY < m_iFracY; iY++)
			{
				m_aaiFrac[iX][iY] = (255 - m_aaiFrac[iX][iY]);
			}
		}
	}
}


int CvFractal::getHeight(int iX, int iY)
{
	FAssertBounds(0, m_iXs, iX);
	FAssertBounds(0, m_iYs, iY);
	int iLowX = ((m_iXInc * iX) / FLOAT_PRECISION);
	if (iLowX > m_iFracX - 1)
		iLowX = m_iFracX - 1;	// clamp so that iLowX+1 doesn't overrun array
	int iLowY = ((m_iYInc * iY) / FLOAT_PRECISION);
	if (iLowY > m_iFracY - 1)
		iLowY = m_iFracY - 1;	// clamp so that iLowY+1 doesn't overrun array
	int iErrX = ((m_iXInc * iX) - (iLowX * FLOAT_PRECISION));
	int iErrY = ((m_iYInc * iY) - (iLowY * FLOAT_PRECISION));

	int iSum = 0;
	iSum += ((FLOAT_PRECISION - iErrX) * (FLOAT_PRECISION - iErrY) * m_aaiFrac[iLowX    ][iLowY    ]);
	iSum += ((                  iErrX) * (FLOAT_PRECISION - iErrY) * m_aaiFrac[iLowX + 1][iLowY    ]);
	iSum += ((FLOAT_PRECISION - iErrX) * (                  iErrY) * m_aaiFrac[iLowX    ][iLowY + 1]);
	iSum += ((                  iErrX) * (                  iErrY) * m_aaiFrac[iLowX + 1][iLowY + 1]);
	iSum /= (FLOAT_PRECISION * FLOAT_PRECISION);

	int iHeight = range(iSum, 0, 255);
	if (m_eFlags & FRAC_PERCENT)
		return (iHeight * 100) >> 8;
	return iHeight;
}


int CvFractal::getHeightFromPercent(int iPercent)
{
	PROFILE_FUNC();

	iPercent = range(iPercent, 0, 100);

	int iEstimate = 255 * iPercent / 100;
	int iLowerBound = 0;
	int iUpperBound = 255;
	while (iEstimate != iLowerBound)
	{
		int iSum = 0;
		for (int iX = 0; iX < m_iFracX; iX++)
		{
			for (int iY = 0; iY < m_iFracY; iY++)
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


void CvFractal::tectonicAction(CvFractal* pRifts)  //  Assumes FRAC_WRAP_X is on.
{
	int iRift1x = (m_iFracX / 4);
	int iRift2x = ((m_iFracX / 4) * 3);

	int const iWidth = 16;

	for (int iY = 0; iY < m_iFracY + 1; iY++)
	{
		for (int iX = 0; iX < iWidth; iX++)
		{
			//  Rift along edge of map.
			int iRx = yieldX((
					(((pRifts->m_aaiFrac[iRift2x][iY] - 128) * m_iFracX) / 128) / 8)
					+ iX);
			int iLx = yieldX((
					/*  advc.001: Was iRift2x, and iRift1x was unused. I'm not sure
						if it's correct now. The maps look as before to me. */
					(((pRifts->m_aaiFrac[iRift1x][iY] - 128) * m_iFracX) / 128) / 8)
					- iX);
			// <advc> No functional change
			int const iDeep = 0;
			/*  This term was used in the two assignments below. I've called it iShift,
				but I'm not sure what it's for. It's 0. A bug? */
			int iShift = iDeep * (iWidth - iX);
			// </advc>
			m_aaiFrac[iRx][iY] = (((m_aaiFrac[iRx][iY] * iX) +
					iShift)
					/ iWidth);
			m_aaiFrac[iLx][iY] = (((m_aaiFrac[iLx][iY] * iX) +
					iShift)
					/ iWidth);
		}
	}

	for (int iY = 0; iY < m_iFracY + 1; iY++)
	{
		m_aaiFrac[m_iFracX][iY] = m_aaiFrac[0][iY];
	}
}


int CvFractal::yieldX(int iBadX)  //  Assumes FRAC_WRAP_X is on.
{
	/*	<advc> while instead of if. Adopted from Civ4Col.
		Seems like a reasonable precaution if nothing else. */
	while (iBadX < 0)
		iBadX += m_iFracX;
	while (iBadX >= m_iFracX)
		iBadX -= m_iFracX; // </advc>
	return iBadX;
}

// advc.tsl: Wrap this in a protected function so that subclasses can override it
int CvFractal::polarHeight()
{
	/*  No easy way to let map scripts set this because the code that exposes
		CvFractal (and CvFractal::FracVals) is in the EXE. */
	if(GC.getInitCore().getMapScriptName().compare(L"Fractal") == 0)
	{
		/*  A power of 2 probably has no advantage here, but 64 also happens to work
			pretty well. The closer to 0 this is set, the wider the polar water bands. */
		return (1 << 6);
	}
	return 0;
}
