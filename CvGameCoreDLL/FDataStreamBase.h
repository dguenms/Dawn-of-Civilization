#pragma once

//	$Revision: #4 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.

/*
* FILE:    FDataStreamBase.h
* DATE:    7/15/2004
* AUTHOR: Mustafa Thamer
* PURPOSE: Base Classe of Stream classes for file, null and mem streams.
*
*		Easily read and write data to those kinds of streams using the same baseclass interface.
*		FStrings not used since this is a public dll header.
*/

#ifndef FDATASTREAMBASE_H
#define FDATASTREAMBASE_H

#include "ReproTest.h" // advc.repro
// Stream abstract base class
class FDataStreamBase
{
public:
	virtual void			Rewind() = 0;
	virtual bool			AtEnd() = 0;
	virtual void			FastFwd() = 0;
	virtual unsigned int	GetPosition() const =  0;
	virtual void			SetPosition(unsigned int position) = 0;
	virtual void			Truncate() = 0;
	virtual void			Flush() = 0;
	virtual unsigned int	GetEOF() const = 0;
	virtual unsigned int	GetSizeLeft() const = 0;
	virtual void			CopyToMem(void* mem) = 0;

	virtual unsigned int	WriteString(const wchar *szName) = 0;
	virtual unsigned int	WriteString(const char *szName) = 0;
	virtual unsigned int	WriteString(const std::string& szName) = 0;
	virtual unsigned int	WriteString(const std::wstring& szName) = 0;
	virtual unsigned int	WriteString(int count, std::string values[]) = 0;
	virtual unsigned int	WriteString(int count, std::wstring values[]) = 0;

	virtual unsigned int	ReadString(char *szName) = 0;
	virtual unsigned int	ReadString(wchar *szName) = 0;
	virtual unsigned int	ReadString(std::string& szName) = 0;
	virtual unsigned int	ReadString(std::wstring& szName) = 0;
	virtual unsigned int	ReadString(int count, std::string values[]) = 0;
	virtual unsigned int	ReadString(int count, std::wstring values[]) = 0;

	virtual char*			ReadString() = 0;		// allocates memory
	virtual wchar*			ReadWideString() = 0;	// allocates memory

	virtual void		Read(char *) = 0;
	virtual void		Read(byte *) = 0;
	virtual void		Read(int count, char values[]) = 0;
	virtual void		Read(int count, byte values[]) = 0;
	virtual void		Read(bool *) = 0;
	virtual void		Read(int count, bool values[]) = 0;
	virtual void		Read(short	*s) = 0;
	virtual void		Read(unsigned short	*s)  = 0;
	virtual void		Read(int count, short values[]) = 0;
	virtual void		Read(int count, unsigned short values[]) = 0;
	virtual void		Read(int* i) = 0;
	virtual void		Read(unsigned int* i) = 0;
	virtual void 		Read(int count, int values[]) = 0;
	virtual void 		Read(int count, unsigned int values[]) = 0;

	virtual void		Read(long* l) = 0;
	virtual void		Read(unsigned long* l)  = 0;
	virtual void 		Read(int count, long values[]) = 0;
	virtual void 		Read(int count, unsigned long values[])  = 0;

	virtual void		Read(float* value) = 0;
	virtual void		Read(int count, float values[]) = 0;

	virtual void		Read(double* value) = 0;
	virtual void		Read(int count, double values[]) = 0;

	virtual void		WriteExternal(char value) = 0;
	virtual void		WriteExternal(byte value) = 0;
	virtual void		WriteExternal(int count, const char values[]) = 0;
	virtual void		WriteExternal(int count, const byte values[]) = 0;

	virtual void		WriteExternal(bool value) = 0;
	virtual void		WriteExternal(int count, const bool values[]) = 0;

	virtual void		WriteExternal(short value) = 0;
	virtual void		WriteExternal(unsigned short value) = 0;
	virtual void		WriteExternal(int count, const short values[]) = 0;
	virtual void		WriteExternal(int count, const unsigned short values[])  = 0;

	virtual void		WriteExternal(int value) = 0;
	virtual void		WriteExternal(unsigned int value)  = 0;
	virtual void 		WriteExternal(int count, const int values[]) = 0;
	virtual void		WriteExternal(int count, const unsigned int values[])  = 0;

	virtual void		WriteExternal(long value) = 0;
	virtual void		WriteExternal(unsigned long value) = 0;
	virtual void 		WriteExternal(int count, const long values[]) = 0;
	virtual void		WriteExternal(int count, const unsigned long values[])  = 0;

	virtual void		WriteExternal(float value) = 0;
	virtual void		WriteExternal(int count, const float values[]) = 0;

	virtual void		WriteExternal(double value) = 0;
	virtual void		WriteExternal(int count, const double values[]) = 0;

	// <advc.repro> (And renamed the original functions to WriteExternal)
	void Write(char value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(byte value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(int iCount, char const values[])
	{
		REPRO_TEST_REPORT(sizeof(char) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(int iCount, byte const values[])
	{
		REPRO_TEST_REPORT(sizeof(byte) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(bool value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(int iCount, const bool values[])
	{
		REPRO_TEST_REPORT(sizeof(bool) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(short value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(unsigned short value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(int iCount, const short values[])
	{
		REPRO_TEST_REPORT(sizeof(short) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(int iCount, const unsigned short values[])
	{
		REPRO_TEST_REPORT(sizeof(unsigned short) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(int value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(unsigned int value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(int iCount, int const values[])
	{
		REPRO_TEST_REPORT(sizeof(int) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(int iCount, unsigned int const values[])
	{
		REPRO_TEST_REPORT(sizeof(uint) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(long value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(unsigned long value)
	{
		REPRO_TEST_REPORT(sizeof(value), &value);
		WriteExternal(value);
	}
	void Write(int iCount, long const values[])
	{
		REPRO_TEST_REPORT(sizeof(long) * iCount, values);
		WriteExternal(iCount, values);
	}
	void Write(int iCount, unsigned long const values[])
	{
		REPRO_TEST_REPORT(sizeof(unsigned long) * iCount, values);
		WriteExternal(iCount, values);
	}
	// <advc.enum> long long
	void Write(__int64 lValue)
	{
		__int32* iiPair = reinterpret_cast<__int32*>(&lValue);
		Write(iiPair[0]);
		Write(iiPair[1]);
	}
	void Write(unsigned __int64 lValue)
	{
		unsigned __int32* iiPair = reinterpret_cast<unsigned __int32*>(&lValue);
		Write(iiPair[0]);
		Write(iiPair[1]);
	}
	void Write(int iCount, __int64 const aValues[])
	{
		for (int i = 0; i < iCount; i++)
			Write(aValues[i]);
	}
	void Write(int iCount, unsigned __int64 const aValues[])
	{
		for (int i = 0; i < iCount; i++)
			Write(aValues[i]);
	} // </advc.enum>
	// <advc.fract>
	template<int iSCALE, typename IntType, typename EnumType>
	void Write(ScaledNum<iSCALE,IntType,EnumType> rValue) const
	{
		REPRO_TEST_REPORT(sizeof(rValue), &rValue);
		rValue.write(this);
	}
	template<int iSCALE, typename IntType, typename EnumType>
	void Write(int iCount, ScaledNum<iSCALE,IntType,EnumType> const arValues[])
	{
		REPRO_TEST_REPORT(sizeof(ScaledNum<iSCALE,IntType,EnumType>) * iCount, arValues);
		for (int i = 0; i < iCount; i++)
			arValues[i].write(this);
	} // </advc.fract>
	/*	Floating-point data isn't normally part of the synchronized game state.
		So these wrappers aren't needed, but, somehow, if I remove them and
		rename the respective virtual functions back to "Write", I get a crash
		when calling Write(bool). */
	void Write(float value)
	{
		WriteExternal(value);
	}
	void Write(int count, const float values[])
	{
		WriteExternal(count, values);
	}
	void Write(double value)
	{
		WriteExternal(value);
	}
	void Write(int count, const double values[])
	{
		WriteExternal(count, values);
	} // <advc.repro>
	// <advc.fract>
	template<int iSCALE, typename IntType, typename EnumType>
	void Read(ScaledNum<iSCALE,IntType,EnumType>* arValues)
	{
		arValues->read(this);
	}
	template<int iSCALE, typename IntType, typename EnumType>
	void Read(int iCount, ScaledNum<iSCALE,IntType,EnumType> arValues[])
	{
		for (int i = 0; i < iCount; i++)
			arValues[i].read(this);
	} // </advc.fract>
	// <advc.enum>
	void Read(__int64* lValue)
	{
		__int32 iiPair[2];
		Read(&iiPair[0]);
		Read(&iiPair[1]);
		*lValue = reinterpret_cast<__int64*>(iiPair)[0];
	}
	void Read(unsigned __int64* lValue)
	{
		unsigned __int32 iiPair[2];
		Read(&iiPair[0]);
		Read(&iiPair[1]);
		*lValue = reinterpret_cast<unsigned __int64*>(iiPair)[0];
	}
	void Read(int iCount, __int64 aValues[])
	{
		for (int i = 0; i < iCount; i++)
			Read(&aValues[i]);
	}
	void Read(int iCount, unsigned __int64 aValues[])
	{
		for (int i = 0; i < iCount; i++)
			Read(&aValues[i]);
	} // </advc.enum>
};

#endif
