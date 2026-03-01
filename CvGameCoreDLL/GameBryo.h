#pragma once

#ifndef GAME_BRYO_H
#define GAME_BRYO_H

// advc: Moved out of CvGameCoreDLL.h for tidiness

class NiColor
{
public:
	NiColor() : r(0), g(0), b(0) {} // advc: Better initialize these
	float r, g, b;
};
class NiColorA
{
public:
	NiColorA(float fr, float fg, float fb, float fa) : r(fr), g(fg), b(fb), a(fa) {}
	NiColorA() /* advc: */ : r(0), g(0), b(0), a(0) {}
	float r, g, b, a;
};
class NiPoint2
{
public:
	NiPoint2() /* advc: */ : x(-1), y(-1) {}
	NiPoint2(float fx, float fy) : x(fx), y(fy) {}

	float x, y;
};
class NiPoint3
{
public:
	NiPoint3() /* advc: */ : x(0), y(0), z(0) {}
	NiPoint3(float fx, float fy, float fz) : x(fx),y(fy),z(fz) {}

	bool NiPoint3::operator== (const NiPoint3& pt) const
	{	return (x == pt.x && y == pt.y && z == pt.z);	}

	NiPoint3 NiPoint3::operator+ (const NiPoint3& pt) const
	{	return NiPoint3(x+pt.x,y+pt.y,z+pt.z);	}

	NiPoint3 NiPoint3::operator- (const NiPoint3& pt) const
	{	return NiPoint3(x-pt.x,y-pt.y,z-pt.z);	}

	float NiPoint3::operator* (const NiPoint3& pt) const
	{	return x*pt.x+y*pt.y+z*pt.z;	}

	NiPoint3 NiPoint3::operator* (float fScalar) const
	{	return NiPoint3(fScalar*x,fScalar*y,fScalar*z);	}

	NiPoint3 NiPoint3::operator/ (float fScalar) const
	{
		float fInvScalar = 1.0f/fScalar;
		return NiPoint3(fInvScalar*x,fInvScalar*y,fInvScalar*z);
	}

	NiPoint3 NiPoint3::operator- () const
	{	return NiPoint3(-x,-y,-z);	}

	float Length() const
	{ return sqrt(x * x + y * y + z * z); }

	float Unitize()
	{
		float length = Length();
		if(length != 0)
		{
			x /= length;
			y /= length;
			z /= length;
		}
		return length;
	}

//	NiPoint3 operator* (float fScalar, const NiPoint3& pt)
//	{	return NiPoint3(fScalar*pt.x,fScalar*pt.y,fScalar*pt.z);	}
	float x, y, z;
};

namespace NiAnimationKey
{
	enum KeyType
	{
		NOINTERP,
		LINKEY,
		BEZKEY,
		TCBKEY,
		EULERKEY,
		STEPKEY,
		NUMKEYTYPES
	};
};

#endif
