#pragma once

// fractal.h

#ifndef CIV4_FRACTAL_H
#define CIV4_FRACTAL_H

class CvRandom;
class CvFractal
{

public:

	enum DllExport FracVals		// Exposed to Python
	{
		FRAC_WRAP_X					= (0x0001),
		FRAC_WRAP_Y					= (0x0002),
		FRAC_PERCENT				= (0x0004),  //  Returns raw data as a percent.
		FRAC_POLAR					= (0x0008),  //  Sets polar regions to zero.
		FRAC_CENTER_RIFT		= (0x0010),  //  Draws rift in center of world, too.
		FRAC_INVERT_HEIGHTS	= (0x0020),  //  Draws inverts the heights
		DEFAULT_FRAC_X_EXP = 7,
		DEFAULT_FRAC_Y_EXP = 6
	};

	//  Smoothness varies with 2^grain.
	//  Totally random is grain = min (iFracXExp, iFracYExp).
	//  As smooth as possible is grain = 0;

	// iFracXExp should be 8 or less
	// iFracYExp should be one less than iFracXExp for Civ3 worlds

	DllExport void fracInit(int iNewXs, int iNewYs, int iGrain, CvRandom& random, int iFlags, CvFractal* pRifts=NULL, int iFracXExp=DEFAULT_FRAC_X_EXP, int iFracYExp=DEFAULT_FRAC_Y_EXP);	// Exposed to Python
	DllExport void fracInitHinted(int iNewXs, int iNewYs, int iGrain, CvRandom& random, byte* pbyHints, int iHintsLength, int iFlags, CvFractal* pRifts, int iFracXExp=DEFAULT_FRAC_X_EXP, int iFracYExp=DEFAULT_FRAC_Y_EXP); // Exposed to Python

	DllExport int getHeight(int x, int y);																					// Exposed to Python
	DllExport int getHeightFromPercent(int iPercent);																			// Exposed to Python

	DllExport void reset();
	DllExport CvFractal();
	DllExport virtual ~CvFractal();
	DllExport void uninit();
	
protected:

	int m_iXs;
	int m_iYs;
	int m_iFlags;

	int m_iFracX;
	int m_iFracY;
	int m_iFracXExp;
	int m_iFracYExp;

	int m_iXInc;
	int m_iYInc;

	int **m_aaiFrac; //[FRAC_X + 1][FRAC_Y + 1];
	void fracInitInternal(int iNewXs, int iNewYs, int iGrain, CvRandom& random, byte* pbyHints, int iHintsLength, int iFlags, CvFractal* pRifts, int iFracXExp, int iFracYExp);
	void tectonicAction(CvFractal* pRifts);
	int yieldX(int iBadX);

};

#endif
