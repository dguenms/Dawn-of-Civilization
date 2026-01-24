#pragma once

#ifndef TIGONOMETRY_H
#define TIGONOMETRY_H

// advc.make: Moved out of PCH

//#define SQR(x) ( (x) * (x) ) // advc: Already defined in CvGameCoreUtils.h
// advc: Unused; there's range (CvGameCoreUtils), which is similar enough.
//#define LIMIT_RANGE(low, value, high) value = (value < low ? low : (value > high ? high : value));
#define M_PI		3.14159265358979323846
#define fM_PI		3.141592654f		//!< Pi (float)
//#define DEGTORAD(x) ( (float)( (x) * (M_PI / 180) )) // advc: unused

// Moved from CvGameCoreUtils. Only called externally.
DllExport float directionAngle(DirectionTypes eDirection)
{
	switch (eDirection)
	{
	case DIRECTION_NORTHEAST:	return fM_PI * 0.25f;
	case DIRECTION_EAST:			return fM_PI * 0.5f;
	case DIRECTION_SOUTHEAST:	return fM_PI * 0.75f;
	case DIRECTION_SOUTH:			return fM_PI * 1.0f;
	case DIRECTION_SOUTHWEST:	return fM_PI * 1.25f;
	case DIRECTION_WEST:			return fM_PI * 1.5f;
	case DIRECTION_NORTHWEST:	return fM_PI * 1.75f;
	default:
	case DIRECTION_NORTH:			return 0.0f;
	}
}

#endif
