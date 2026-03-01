#pragma once

// fractal.h

#ifndef CIV4_FRACTAL_H
#define CIV4_FRACTAL_H

class CvRandom;
class CvFractal
{

public:

	// Exposed to Python
	/*	advc: ... through the EXE, i.e. the values shouldn't be changed in the DLL
		b/c that wouldn't affect the values in Python.
		Renaming the enum doesn't hurt though. */
	enum /*FracVals*/ Flags
	{
		NO_FLAGS					= 0,
		FRAC_WRAP_X					= (1 << 0),
		FRAC_WRAP_Y					= (1 << 1),
		FRAC_PERCENT				= (1 << 2),  //  Returns raw data as a percent.
		FRAC_POLAR					= (1 << 3),  //  Sets polar regions to zero.
		FRAC_CENTER_RIFT			= (1 << 4),  //  Draws rift in center of world, too.
		FRAC_INVERT_HEIGHTS			= (1 << 5),  //  Draws inverts the heights
		// <avdc.enum> Move ..._EXP out and give the enum bitwise operators (see end of file)
	};
	static int const DEFAULT_FRAC_X_EXP = 7;
	static int const DEFAULT_FRAC_Y_EXP = 6;
	// </advc.enum>

	/*	Smoothness varies with 2^grain.
		Totally random is grain=min{iFracXExp,iFracYExp}.
		As smooth as possible is grain=0. */
	DllExport void fracInit(int iNewXs, int iNewYs, int iGrain, CvRandom& random,		// Exposed to Python
			int iFlags, CvFractal* pRifts=NULL,
			// <advc.137> Let fracInitInternal work this out
			int iFracXExp = /*DEFAULT_FRAC_X_EXP*/-1,
			int iFracYExp = /*DEFAULT_FRAC_Y_EXP*/-1); // </advc.137>
	DllExport void fracInitHinted(int iNewXs, int iNewYs, int iGrain, CvRandom& random,	// Exposed to Python
			byte* pbyHints, int iHintsLength, int iFlags, CvFractal* pRifts,
			// <advc.137>
			int iFracXExp = /*DEFAULT_FRAC_X_EXP*/-1,
			int iFracYExp = /*DEFAULT_FRAC_Y_EXP*/-1); // </advc.137>

	DllExport int getHeight(int x, int y);												// Exposed to Python
	DllExport int getHeightFromPercent(int iPercent);									// Exposed to Python

	void reset();
	DllExport CvFractal();
	virtual ~CvFractal();
	void uninit();

protected:
	// advc.003k (warning): It's not safe to add data members to this class!
	int m_iXs;
	int m_iYs;
	Flags m_eFlags; // advc.enum (was int)

	int m_iFracX;
	int m_iFracY;
	int m_iFracXExp;
	int m_iFracYExp;

	int m_iXInc;
	int m_iYInc;

	int **m_aaiFrac; //[FRAC_X + 1][FRAC_Y + 1];

	void fracInitInternal(int iNewXs, int iNewYs, int iGrain, CvRandom& random,
			byte* pbyHints, int iHintsLength,
			Flags eFlags, // advc.enum
			CvFractal* pRifts, int iFracXExp, int iFracYExp);
	void tectonicAction(CvFractal* pRifts);
	int yieldX(int iBadX);
	int polarHeight(); // advc.tsl
};

BOOST_STATIC_ASSERT(sizeof(CvFractal) == 44); // advc.003k

OVERLOAD_BITWISE_OPERATORS(CvFractal::Flags) // advc.enum

#endif
