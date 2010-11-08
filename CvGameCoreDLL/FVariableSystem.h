#pragma once

//	$Revision: #4 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//------------------------------------------------------------------------------------------------
//
//  *****************   FIRAXIS GAME ENGINE   ********************
//
//!  \file		FVariableSystem.h
//!  \author	Bart Muzzin - 11/22/2004
//!	 \brief		Implementation of a runtime modifiable set of variables (header).
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2002-2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

#ifndef		FVARIABLESYSTEM_H
#define		FVARIABLESYSTEM_H
#pragma		once

//! Represents the different types of data an FVariable can represent.
enum eVariableType
{
	FVARTYPE_BOOL,		//!< Boolean value.
	FVARTYPE_CHAR,		//!< One byte integer (signed).
	FVARTYPE_UCHAR,		//!< One byte integer (unsigned).
	FVARTYPE_SHORT,		//!< Two byte integer (signed).
	FVARTYPE_USHORT,	//!< Two byte integer (unsigned).
	FVARTYPE_INT,		//!< Four byte integer (signed).
	FVARTYPE_UINT,		//!< Four byte integer (unsigned).
	FVARTYPE_FLOAT,		//!< Four byte floating point number.
	FVARTYPE_DOUBLE,	//!< Eight byte floating point number.
	FVARTYPE_STRING,	//!< String data (uses FString).
	FVARTYPE_WSTRING,	//!< String data (uses FStringW).
	FVARTYPE_COUNT
};

class FVariable;

typedef stdext::hash_map< std::string, FVariable * > FVariableHash;

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// CLASS:	FVariable
//
//! \brief Used with FVariableSystem to create a set of run-time variables.
//!
//! Note that there are no constructors or methods for this class, and all data is public.
//! This is done intentionally to reduce overhead, and this class should rarely be accessed
//! outside of FVariableSystem code. There is a destructor however, because the data contained
//! inside may need to be freed, such as in the case of string data.
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FDataStreamBase;
class FVariable
{
	public:
		FVariable() : m_dValue(0) {}
		FVariable(const FVariable& src) { CopyFrom(src); }
		virtual ~FVariable();

		const FVariable& operator=( const FVariable& varSrc ) { CopyFrom(varSrc); return *this; }
		void CopyFrom(const FVariable& varSrc);
		void Read(FDataStreamBase *);
		void Write(FDataStreamBase *) const;

		union
		{
			bool		m_bValue;		//!< Boolean data
			char		m_cValue;		//!< One byte integer (signed) data.
			byte		m_ucValue;		//!< One byte integer (unsigned) data.
			short		m_wValue;		//!< Two byte integer (signed) data.
			word		m_uwValue;		//!< Two byte integer (unsigned) data.
			int			m_iValue;		//!< Four byte integer (signed) data.
			uint		m_uiValue;		//!< Four byte integer (unsigned) data.
			float		m_fValue;		//!< Four byte floating point data.
			double		m_dValue;		//!< Eight byte floating point data.
			char *		m_szValue;		//!< String data.
			wchar_t *		m_wszValue;		//!< Wide string data.
		};

		eVariableType	m_eType;		//!< The type of data contained in this variable.

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// CLASS:	FVariable
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//! \brief Creates a system in which variables can be added/removed/queried/modified at runtime.
//!
//! This should be used when the application is managing variable data obtained from/exposed to an external source.
//! For example, if variables are read from an XML file, and the variable names are not known beforehand, this system
//! can manage them.
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FVariableSystem
{
	public:

		// Constructor/Destructor
		FVariableSystem( );
		virtual ~FVariableSystem( );

		void UnInit();

		// Number of variables in the system
		uint GetSize() const;

		// Variable accessors
		bool GetValue( const char * szVariable, bool & bValue ) const;
		bool GetValue( const char * szVariable, char & cValue ) const;
		bool GetValue( const char * szVariable, byte & ucValue ) const;
		bool GetValue( const char * szVariable, short & wValue ) const;
		bool GetValue( const char * szVariable, word & uwValue ) const;
		bool GetValue( const char * szVariable, int & iValue ) const;
		bool GetValue( const char * szVariable, uint & uiValue ) const;
		bool GetValue( const char * szVariable, float & fValue ) const;
		bool GetValue( const char * szVariable, double & dValue ) const;
		bool GetValue( const char * szVariable, const char * & pszValue ) const;
		bool GetValue( const char * szVariable, const wchar * & pszValue ) const;
		const FVariable * GetVariable( const char * szVariable ) const;

		// Variable additions/modifiers. If a variable does not exist, it will be added.
		void SetValue( const char * szVariable, bool bValue );
		void SetValue( const char * szVariable, char cValue );
		void SetValue( const char * szVariable, byte ucValue );
		void SetValue( const char * szVariable, short wValue );
		void SetValue( const char * szVariable, word uwValue );
		void SetValue( const char * szVariable, int iValue );
		void SetValue( const char * szVariable, uint uiValue );
		void SetValue( const char * szVariable, float fValue );
		void SetValue( const char * szVariable, double dValue );
		void SetValue( const char * szVariable, const char * szValue );
		void SetValue( const char * szVariable, const wchar * wszValue );

		// Variable removal
		bool RemValue( const char * szVariable );

		// Iteration
		std::string GetFirstVariableName( );
		std::string GetNextVariableName( );

		void Read(FDataStreamBase *);
		void Write(FDataStreamBase *) const;

protected:

		FVariableHash				m_mapVariableMap;		//!< Hash map of variable types
		FVariableHash::iterator		m_iVariableIterator;	//!< Current iterator used with GetFirst/NextVariableName


};

#include "FVariableSystem.inl"

#endif	//FVARIABLESYSTEM_H
