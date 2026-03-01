#pragma once

//	$Revision: #4 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//  *****************   FIRAXIS GAME ENGINE   ********************
//  author: Bart Muzzin - 11/22/2004
//	Implementation of a runtime modifiable set of variables (header).
//  Copyright (c) 2002-2004 Firaxis Games, Inc. All rights reserved.
// advc: Got rid of some redundant code and comments

#pragma once
#ifndef FVARIABLESYSTEM_H
#define FVARIABLESYSTEM_H


// The types of data an FVariable can represent
enum eVariableType
{
	FVARTYPE_BOOL,		// 1-byte boolean
	FVARTYPE_CHAR,		// 1-byte integer (signed)
	FVARTYPE_UCHAR,		// 1-byte integer (unsigned)
	FVARTYPE_SHORT,		// 2-byte integer (signed)
	FVARTYPE_USHORT,	// 2-byte integer (unsigned)
	FVARTYPE_INT,		// 4-byte integer (signed)
	FVARTYPE_UINT,		// 4-byte integer (unsigned)
	FVARTYPE_FLOAT,		// 4-byte floating point
	FVARTYPE_DOUBLE,	// 8-byte floating point
	FVARTYPE_STRING,	// 0-terminated narrow-character string
	FVARTYPE_WSTRING,	// 0-terminated wide-character string
	FVARTYPE_COUNT
};

class FDataStreamBase;

/*	Used with FVariableSystem to create a set of run-time variables.
	Note that there are no constructors or methods for this class, and all data is public.
	This is done intentionally to reduce overhead, and this class should rarely be accessed
	outside of FVariableSystem code. There is a destructor however, because the data contained
	inside may need to be freed, such as in the case of string data. */
class FVariable
{
public:
	FVariable() : m_dValue(0), /* advc (from C2C): */ m_eType(FVARTYPE_INT) {}
	FVariable(FVariable const& src) { CopyFrom(src); } // Copy Function
	// Destructor. If the object is string type, the memory is destroyed.
	virtual ~FVariable();

	FVariable const& operator=(FVariable const& varSrc)
	{
		CopyFrom(varSrc);
		return *this;
	}
	void CopyFrom(const FVariable& varSrc);
	void Read(FDataStreamBase* pStream);
	void Write(FDataStreamBase* pSTream) const;

	/*	<advc> Not nice, but gets rid of even more clutter in FVariableSystem.
		If we want e.g.
			FVariableSystem varSys; int i;
			varSys.GetValue("MY_VAR", &i);
		to assert that the type of "MY_VAR" is indeed INT and not e.g. SHORT,
		and if we insist on avoiding the overhead of a virtual function call
		within the GetValue functions, then I don't think there is an elegant
		solution involving templates and inheritance. */
	bool getValue(bool) const { return m_bValue; }
	char getValue(char) const { return m_cValue; }
	byte getValue(byte) const { return m_ucValue; }
	short getValue(short) const { return m_wValue; }
	word getValue(word) const { return m_uwValue; }
	int getValue(int) const { return m_iValue; }
	uint getValue(uint) const { return m_uiValue; }
	float getValue(float) const { return m_fValue; }
	double getValue(double) const { return m_dValue; }
	char* getValue(char*) const { return m_szValue; }
	wchar* getValue(wchar*) const { return m_wszValue; }
	char* getValue(char const*) const { return m_szValue; }
	wchar* getValue(wchar const*) const { return m_wszValue; }
	void setValue(bool b) { m_bValue = b; m_eType = FVARTYPE_BOOL; }
	void setValue(char c) { m_cValue = c; m_eType = FVARTYPE_CHAR; }
	void setValue(byte uc) { m_ucValue = uc; m_eType = FVARTYPE_UCHAR; }
	void setValue(short w) { m_wValue = w; m_eType = FVARTYPE_SHORT; }
	void setValue(word uw) { m_uwValue = uw; m_eType = FVARTYPE_USHORT; }
	void setValue(int i) { m_iValue = i; m_eType = FVARTYPE_INT; }
	void setValue(uint ui) { m_uiValue = ui; m_eType = FVARTYPE_UINT; }
	void setValue(float f) { m_fValue = f; m_eType = FVARTYPE_FLOAT; }
	void setValue(double d) { m_dValue = d; m_eType = FVARTYPE_DOUBLE; }
	void setValue(char* sz)
	{
		m_szValue = strcpy(new char[strlen(sz) + 1], sz);
		m_eType = FVARTYPE_STRING;
	}
	void setValue(wchar* wsz)
	{
		m_wszValue = wcscpy(new wchar[wcslen(wsz) + 1], wsz);
		m_eType = FVARTYPE_WSTRING;
	}
	void assertType(bool) const
	{
		FAssert(m_eType == FVARTYPE_BOOL);
	}
	void assertType(char) const
	{
		FAssert(m_eType == FVARTYPE_CHAR);
	}
	void assertType(byte) const
	{
		FAssert(m_eType == FVARTYPE_UCHAR);
	}
	void assertType(short) const
	{
		FAssert(m_eType == FVARTYPE_SHORT);
	}
	void assertType(word) const
	{
		FAssert(m_eType == FVARTYPE_USHORT);
	}
	void assertType(int) const
	{
		FAssert(m_eType == FVARTYPE_INT);
	}
	void assertType(uint) const
	{
		FAssert(m_eType == FVARTYPE_UINT);
	}
	void assertType(char*) const
	{
		FAssert(m_eType == FVARTYPE_STRING);
	}
	void assertType(wchar*) const
	{
		FAssert(m_eType == FVARTYPE_WSTRING);
	}
	void assertType(const char*) const
	{
		FAssert(m_eType == FVARTYPE_STRING);
	}
	void assertType(const wchar*) const
	{
		FAssert(m_eType == FVARTYPE_WSTRING);
	} // </advc>

	union
	{
		bool		m_bValue;
		char		m_cValue;
		byte		m_ucValue;
		short		m_wValue;
		word		m_uwValue;
		int			m_iValue;
		uint		m_uiValue;
		float		m_fValue;
		double		m_dValue;
		char*		m_szValue;
		wchar*		m_wszValue;
	}; // advc.003k: Memory layout mustn't change, i.e. m_eType needs to come last.
	eVariableType	m_eType;		// The type of data contained in this variable
};
BOOST_STATIC_ASSERT(sizeof(FVariable) == 24); // advc.003k
/*	(That's 4 for the vtable, 4 for m_eType and - apparently -
	16 for the union and padding. A little weird, but must stay this way.) */

typedef stdext::hash_map<std::string, FVariable*> FVariableHash;

/*	Creates a system in which variables can be added/removed/queried/modified at runtime.
	This should be used when the application is managing variable data obtained
	from/exposed to an external source. For example, if variables are read from an XML file,
	and the variable names are not known beforehand, this system can manage them. */
class FVariableSystem
{
public:
	FVariableSystem() {}
	virtual ~FVariableSystem();
	void UnInit();
	uint GetSize() const; // Number of variables stored by the system

	/*	Variable accessors. Get the value of the given variable.
		szVariable: The name of the variable containing the value to query.
		tValue: Contains the value of the variable if the function succeeds.
		Returns true if the variable value was retrieved,
		false otherwise (value will be unchanged from input). */
	bool GetValue(char const* szVariable, float& fValue) const;
	bool GetValue(char const* szVariable, double& dValue) const; // (unused)
	template<typename T> // advc (used only for T=int, T=char const*)
	bool GetValue(char const* szVariable, T& tValue) const;
	/*	Gets a pointer to the variable object that contains the given variable.
		szVariable: The name of the variable to obtain.
		Returns a pointer to the requested FVariable, or
		NULL if the variable does not exist. */
	FVariable const* GetVariable(char const* szVariable) const; // (unused)

	/*	Variable additions/modifiers. If a variable does not exist, it will be added.
		Creates (or modifies) a variable with the given name and sets it value.
		szVariable: The name of the variable to create.
		cValue: The value that the variable should take on. */
	template<typename T> // advc
	void SetValue(char const* szVariable, T tValue);

	// advc (note): The rest of the functions are unused ...

	/*	Removes a variable from the system.
		szVariable: The name of the variable to remove.
		Returns true if the variable was removed,
		false otherwise (probably does not exist). */
	bool RemValue(char const* szVariable);

	// Iteration
	/*	Gets the name of the "first" variable in the system.
		Returns the name of the variable or an
		empty string if there are no variables. */
	std::string GetFirstVariableName();
	/*	Gets the name of the "next" variable in the system
		(use after GetFirstVariableName).
		Returns the name of the variable, or an
		empty string if there are no more variables. */
	std::string GetNextVariableName();

	void Read(FDataStreamBase* pStream); // Reads the system from a stream
	void Write(FDataStreamBase* pStream) const; // Writes the system to a stream

private:
	FVariableHash m_mapVariableMap; // Hash map of variable types
	// Current iterator used with GetFirst/NextVariableName
	FVariableHash::iterator m_iterator;
};

#include "FVariableSystem.inl"

#endif
