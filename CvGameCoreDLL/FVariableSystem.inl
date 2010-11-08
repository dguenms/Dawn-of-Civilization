//	$Revision: #4 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//------------------------------------------------------------------------------------------------
//
//  *****************   FIRAXIS GAME ENGINE   ********************
//
//!  \file		FVariableSystem.inl
//!  \author	Bart Muzzin - 11/22/2004
//!	 \brief		Implementation of a runtime modifiable set of variables (inlines).
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2002-2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

typedef stdext::hash_map< std::string, FVariable *>::const_iterator VSIteratorC;
typedef stdext::hash_map< std::string, FVariable *>::iterator VSIterator;

//---------------------------------------------------------------------------------------
// inline FVariable::~FVariable()
//---------------------------------------------------------------------------------------
//! \brief Destructor. If the object is string type, the memory is destroyed.
//---------------------------------------------------------------------------------------
inline FVariable::~FVariable()
{
	if ( m_eType == FVARTYPE_STRING )
	{
		delete [] m_szValue ;
	}
	else
	if ( m_eType == FVARTYPE_WSTRING )
	{
		delete [] m_wszValue ;
	}
}

//---------------------------------------------------------------------------------------
// inline FVariable::CopyFrom(const FTranslatorText& varSrc)
//---------------------------------------------------------------------------------------
//! \brief Copy Function. 
//---------------------------------------------------------------------------------------
inline void FVariable::CopyFrom(const FVariable& varSrc)
{
	if (varSrc.m_eType == FVARTYPE_STRING && varSrc.m_szValue)
	{
		// copy string to new allocation
		m_szValue = new char[strlen(varSrc.m_szValue)+1];
		strcpy(m_szValue, varSrc.m_szValue);
	}
	else
	if (varSrc.m_eType == FVARTYPE_WSTRING && varSrc.m_wszValue)
	{
		// copy string to new allocation
		m_wszValue = new wchar[wcslen(varSrc.m_wszValue)+1];
		wcscpy(m_wszValue, varSrc.m_wszValue);
	}
	else
	{
		// this should copy the contents of the union
		memcpy((void*)&m_dValue, (void*)&varSrc.m_dValue, sizeof(m_dValue));
	}

	m_eType = varSrc.m_eType;	
}

inline void FVariable::Read(FDataStreamBase *pStream)
{
	int iType;
	pStream->Read(&iType);
	m_eType = (eVariableType)iType;

	if (m_eType==FVARTYPE_STRING)
		m_szValue = pStream->ReadString();
	else
	if (m_eType==FVARTYPE_WSTRING)
		m_wszValue = pStream->ReadWideString();
	else
		pStream->Read(8, (byte*)&m_dValue);		// read the maximum size of the union
}

inline void FVariable::Write(FDataStreamBase *pStream) const
{
	pStream->Write((int)m_eType);
	if (m_eType==FVARTYPE_STRING)
		pStream->WriteString(m_szValue);
	else
	if (m_eType==FVARTYPE_WSTRING)
		pStream->WriteString(m_wszValue);
	else
		pStream->Write(8, (byte*)&m_dValue);		// write the maximum size of the union
}

//////////////////////////////////////////////////////////////////////////

inline FVariableSystem::FVariableSystem( )
{
}

//---------------------------------------------------------------------------------------
// inline FVariableSystem::~FVariableSystem( )
//---------------------------------------------------------------------------------------
//! \brief Destructor. Calls the destructor on all managed FVariable objects.
//---------------------------------------------------------------------------------------
inline FVariableSystem::~FVariableSystem( )
{
	UnInit();
}

inline void FVariableSystem::UnInit()
{
	VSIteratorC iIterator = m_mapVariableMap.begin();
	FVariable * pkVariable;
	while ( iIterator != m_mapVariableMap.end())
	{
		pkVariable = (FVariable*)iIterator->second;
		if ( pkVariable != NULL ) delete pkVariable;
		iIterator++;
	}
	m_mapVariableMap.clear ();
}

//---------------------------------------------------------------------------------------
// inline uint FVariableSystem::GetSize() const
//---------------------------------------------------------------------------------------
//! \brief Gets the number of variables stored by the system
//! \retval Returns the number of variables stored by the system
//---------------------------------------------------------------------------------------
inline uint FVariableSystem::GetSize() const
{
	return (uint)m_mapVariableMap.size();
}

//---------------------------------------------------------------------------------------
//! \brief Writes the system to a stream
//! \retval none
//---------------------------------------------------------------------------------------
inline void FVariableSystem::Read(FDataStreamBase *pStream)
{
	// clear
	UnInit();

	// read num
	int i, iSize;
	pStream->Read(&iSize);

	// read and add vars
	for(i=0;i<iSize;i++)
	{
		// read key
		std::string szKey;
		pStream->ReadString(szKey);

		// read var
		FVariable * pkVariable = new FVariable;
		pkVariable->Read(pStream);

		// insert
		m_mapVariableMap[szKey] = pkVariable;
	}
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
//! \brief Writes the system to a stream
//! \retval none
//---------------------------------------------------------------------------------------
inline void FVariableSystem::Write(FDataStreamBase *pStream) const
{
	// write num
	int iSize = GetSize();
	pStream->Write(iSize);

	// write vars/keys
	int iNumWritten=0;
	VSIteratorC iIterator = m_mapVariableMap.begin();
	FVariable * pkVariable;
	while ( iIterator != m_mapVariableMap.end())
	{
		// write key
		std::string szKey = iIterator->first;
		pStream->WriteString(szKey);

		// write vars
		pkVariable = (FVariable*)iIterator->second;
		pkVariable->Write(pStream);
		
		iNumWritten++;
		iIterator++;
	}

	assert(iNumWritten==iSize);
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, bool & bValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param bValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, bool & bValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_BOOL );
	bValue = pkVariable->m_bValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, char & cValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param cValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, char & cValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_CHAR );
	cValue = pkVariable->m_cValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, byte & ucValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param ucValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, byte & ucValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_UCHAR );
	ucValue = pkVariable->m_ucValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, short & wValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param wValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, short & wValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_SHORT );
	wValue = pkVariable->m_wValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, word & uwValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param uwValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, word & uwValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_USHORT );
	uwValue = pkVariable->m_uwValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, int & iValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param iValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, int & iValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_INT );
	iValue = pkVariable->m_iValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, uint & uiValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param uiValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, uint & uiValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_UINT );
	uiValue = pkVariable->m_uiValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, float & fValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param fValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, float & fValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;

	switch (pkVariable->m_eType)
	{
	case FVARTYPE_FLOAT:
		fValue = pkVariable->m_fValue;
		break;
	case FVARTYPE_DOUBLE:
		fValue = (float)pkVariable->m_dValue;
		break;
	case FVARTYPE_STRING:
		{
			const char* szValue;
			if (!GetValue(szVariable, szValue))
			{
				return false;
			}
			fValue = (float)atof(szValue);
		}
		break;
	case FVARTYPE_WSTRING:
		{
			const wchar* szValue;
			if (!GetValue(szVariable, szValue))
			{
				return false;
			}
			fValue = (float)_wtof(szValue);
		}
		break;
	default:
		assert(false);
		break;
	}

	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, double & dValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param dValue Contains the value of the variable if the function succeeds
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, double & dValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;

	switch (pkVariable->m_eType)
	{
	case FVARTYPE_FLOAT:
		dValue = pkVariable->m_fValue;
		break;
	case FVARTYPE_DOUBLE:
		dValue = pkVariable->m_dValue;
		break;
	case FVARTYPE_STRING:
		{
			const char* szValue;
			if (!GetValue(szVariable, szValue))
			{
				return false;
			}
			dValue = atof(szValue);
		}
		break;
	case FVARTYPE_WSTRING:
		{
			const wchar* szValue;
			if (!GetValue(szVariable, szValue))
			{
				return false;
			}
			dValue = _wtof(szValue);
		}
		break;
	default:
		assert(false);
		break;
	}

	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, const char * & pszValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param pszValue Contains the value of the variable if the function succeeds (do not modify the return value).
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, const char * & pszValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_STRING );
	pszValue = pkVariable->m_szValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::GetValue( const char * szVariable, const wchar * & pwszValue ) const
//---------------------------------------------------------------------------------------
//! \brief Gets the value of the given variable
//! \param szVariable The name of the variable containing the value to query
//! \param pwszValue Contains the value of the variable if the function succeeds (do not modify the return value).
//! \retval true if the variable value was retrieved, false otherwise (value will be unchanged from input).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::GetValue( const char * szVariable, const wchar * & pwszValue ) const
{
	FVariable * pkVariable;
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end())
	{
		return false;
	}
	pkVariable = iIterator->second;
	assert( pkVariable->m_eType == FVARTYPE_WSTRING );
	pwszValue = pkVariable->m_wszValue;
	return true;
}

//---------------------------------------------------------------------------------------
// inline const FVariable * FVariableSystem::GetVariable( const char * szVariable ) const
//---------------------------------------------------------------------------------------
//! \brief Gets a pointer to the variable object that contains the given variable
//! \param szVariable The name of the variable to obtain
//! \retval Pointer to the requested FVariable, or NULL if the variable does not exist
//---------------------------------------------------------------------------------------
inline const FVariable * FVariableSystem::GetVariable( const char * szVariable ) const
{
	VSIteratorC iIterator;
	iIterator = m_mapVariableMap.find ( szVariable );
	if ( iIterator == m_mapVariableMap.end()) return NULL;
	return iIterator->second;
}

//---------------------------------------------------------------------------------------
// inline const FVariable * FVariableSystem::GetVariable( const char * szVariable ) const
//---------------------------------------------------------------------------------------
//! \brief Gets a pointer to the variable object that contains the given variable
//! \param szVariable The name of the variable to obtain
//! \retval Pointer to the requested FVariable, or NULL if the variable does not exist
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, bool bValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_BOOL;
	pkVariable->m_bValue = bValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, char cValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param cValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, char cValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_CHAR;
	pkVariable->m_cValue = cValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, byte ucValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param ucValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, byte ucValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_UCHAR;
	pkVariable->m_ucValue = ucValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, short wValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param wValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, short wValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_SHORT;
	pkVariable->m_wValue = wValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, word uwValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param uwValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, word uwValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_USHORT;
	pkVariable->m_uwValue = uwValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, int iValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param iValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, int iValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_INT;
	pkVariable->m_iValue = iValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, uint uiValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param uiValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, uint uiValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_UINT;
	pkVariable->m_uiValue = uiValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, float fValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param uiValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, float fValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_FLOAT;
	pkVariable->m_fValue = fValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, double dValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param uiValue The value that the variable should take on
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, double dValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_DOUBLE;
	pkVariable->m_dValue = dValue;
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, const char * szValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param szValue The value that the variable should take on (string is copied).
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, const char * szValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_STRING;
	pkVariable->m_szValue = strcpy( new char[strlen( szValue ) + 1], szValue ); 
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline void FVariableSystem::SetValue( const char * szVariable, const wchar * wszValue )
//---------------------------------------------------------------------------------------
//! \brief Creates (or modifies) a variable with the given name and sets it value.
//! \param szVariable The name of the variable to create
//! \param wszValue The value that the variable should take on (string is copied).
//---------------------------------------------------------------------------------------
inline void FVariableSystem::SetValue( const char * szVariable, const wchar * wszValue )
{
	FVariable * pkVariable;
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable ); 
	if ( iIterator != m_mapVariableMap.end() )
	{
		delete iIterator->second;
	}
	pkVariable = new FVariable;
	pkVariable->m_eType = FVARTYPE_WSTRING;
	pkVariable->m_wszValue = wcscpy( new wchar[wcslen( wszValue ) + 1], wszValue ); 
	m_mapVariableMap[szVariable] = pkVariable;
	m_iVariableIterator = m_mapVariableMap.begin();
}

//---------------------------------------------------------------------------------------
// inline bool FVariableSystem::RemValue( const char * szVariable )
//---------------------------------------------------------------------------------------
//! \brief Removes a variable from the system.
//! \param szVariable The name of the variable to remove
//! \retval true if the variable was removed, false otherwise (probably DNE).
//---------------------------------------------------------------------------------------
inline bool FVariableSystem::RemValue( const char * szVariable )
{
	VSIteratorC iIterator = m_mapVariableMap.find( szVariable );
	if ( iIterator != m_mapVariableMap.end() ) delete iIterator->second;
	m_mapVariableMap.erase( szVariable );
	m_iVariableIterator = m_mapVariableMap.begin();
	return true;
}

//---------------------------------------------------------------------------------------
// inline std::string FVariableSystem::GetFirstVariableName( )
//---------------------------------------------------------------------------------------
//! \brief Gets the name of the "first" variable in the system
//! \retval The name of the variable or an empty string if there are no variables
//---------------------------------------------------------------------------------------
inline std::string FVariableSystem::GetFirstVariableName( )
{
	m_iVariableIterator = m_mapVariableMap.begin();
	if (m_iVariableIterator != m_mapVariableMap.end())
		return (*m_iVariableIterator).first;
	else
		return "";
}

//---------------------------------------------------------------------------------------
// inline std::string FVariableSystem::GetNextVariableName( )
//---------------------------------------------------------------------------------------
//! \brief Gets the name of the "next" variable in the system (use after GetFirstVariableName)
//! \retval The name of the variable, or an empty string if there are no more variables
//------------------------------------------------------------------------------------------------
inline std::string FVariableSystem::GetNextVariableName( )
{
	if ( m_iVariableIterator != m_mapVariableMap.end())
		m_iVariableIterator++;

	if ( m_iVariableIterator != m_mapVariableMap.end())
		return (*m_iVariableIterator).first;
	else
		return "";
}
