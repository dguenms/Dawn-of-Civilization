#pragma once
#ifndef SCALED_NUM_FWD_H
#define SCALED_NUM_FWD_H

/*	advc.fract: Header for ScaledNum forward declarations.
	Shouldn't be needed when porting ScaledNum to another mod; necessary in AdvCiv
	for enum_traits and serialization of enum maps (change id advc.enum). */

template<int iSCALE, typename IntType, typename EnumType>
class ScaledNum;

template<class T>
struct is_scaled_num
{
	static bool const value = false;
};
template<int iSCALE, typename IntType, typename EnumType>
struct is_scaled_num<ScaledNum<iSCALE,IntType,EnumType> >
{
	static bool const value = true;
};

#endif
