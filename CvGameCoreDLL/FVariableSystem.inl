// Copyright (c) 2002-2004 Firaxis Games, Inc. All rights reserved.
// See FVariableSystem.h

/*	advc.006: assert calls replaced with FAssert. However, apparently, this file
	has been compiled into the EXE, so assert will still get called from there. */

typedef stdext::hash_map<std::string, FVariable*>::const_iterator VSIteratorC;
typedef stdext::hash_map<std::string, FVariable*>::iterator VSIterator;


inline FVariable::~FVariable()
{
	if (m_eType == FVARTYPE_STRING)
		delete [] m_szValue ;
	else if (m_eType == FVARTYPE_WSTRING)
		delete [] m_wszValue ;
}


inline void FVariable::CopyFrom(FVariable const& varSrc)
{
	if (varSrc.m_eType == FVARTYPE_STRING && varSrc.m_szValue != 0)
	{
		// copy string to new allocation
		m_szValue = new char[strlen(varSrc.m_szValue) + 1];
		strcpy(m_szValue, varSrc.m_szValue);
	}
	else if (varSrc.m_eType == FVARTYPE_WSTRING && varSrc.m_wszValue != 0)
	{
		// copy string to new allocation
		m_wszValue = new wchar[wcslen(varSrc.m_wszValue) + 1];
		wcscpy(m_wszValue, varSrc.m_wszValue);
	}
	else
	{
		// this should copy the contents of the union
		memcpy((void*)&m_dValue, (void*)&varSrc.m_dValue, sizeof(m_dValue));
	}
	m_eType = varSrc.m_eType;
}


inline void FVariable::Read(FDataStreamBase* pStream)
{
	pStream->Read((int*)&m_eType);
	if (m_eType == FVARTYPE_STRING)
		m_szValue = pStream->ReadString();
	else if (m_eType == FVARTYPE_WSTRING)
		m_wszValue = pStream->ReadWideString();
	// read the maximum size of the union
	else pStream->Read(sizeof(m_dValue), (byte*)&m_dValue);
}


inline void FVariable::Write(FDataStreamBase *pStream) const
{
	pStream->Write((int)m_eType);
	if (m_eType == FVARTYPE_STRING)
		pStream->WriteString(m_szValue);
	else if (m_eType == FVARTYPE_WSTRING)
		pStream->WriteString(m_wszValue);
	// write the maximum size of the union
	else pStream->Write(sizeof(m_dValue), (byte*)&m_dValue);
}

// Calls the destructor on all managed FVariable objects
inline FVariableSystem::~FVariableSystem()
{
	UnInit();
}


inline void FVariableSystem::UnInit()
{
	VSIteratorC iterator = m_mapVariableMap.begin();
	while (iterator != m_mapVariableMap.end())
	{
		FVariable* pVariable = iterator->second;
		if (pVariable != NULL)
			delete pVariable;
		++iterator;
	}
	m_mapVariableMap.clear ();
}


inline uint FVariableSystem::GetSize() const
{
	return m_mapVariableMap.size();
}


inline void FVariableSystem::Read(FDataStreamBase* pStream)
{
	UnInit(); // clear

	int iSize;
	pStream->Read(&iSize); // read num

	for (int i = 0; i < iSize; i++) // read and add vars
	{
		// read key
		std::string szKey;
		pStream->ReadString(szKey);

		// read var
		FVariable* pVariable = new FVariable;
		pVariable->Read(pStream);

		// insert
		m_mapVariableMap[szKey] = pVariable;
	}
	m_iterator = m_mapVariableMap.begin();
}


inline void FVariableSystem::Write(FDataStreamBase* pStream) const
{
	int iSize = GetSize();
	pStream->Write(iSize); // write num

	// write vars/keys
	#ifdef FASSERT_ENABLE // advc
	int iNumWritten = 0;
	#endif
	VSIteratorC iterator = m_mapVariableMap.begin();
	while (iterator != m_mapVariableMap.end())
	{
		// write key
		std::string szKey = iterator->first;
		pStream->WriteString(szKey);

		// write vars
		FVariable* pVariable = iterator->second;
		pVariable->Write(pStream);
		#ifdef FASSERT_ENABLE
		iNumWritten++;
		#endif
		++iterator;
	}
	FAssert(iNumWritten == iSize);
}

// <advc>
#ifdef FASSERT_ENABLE
	#define ASSERT_VAR_TYPE(kVariable, tValue) kVariable.assertType(tValue)
#else
	#define ASSERT_VAR_TYPE(kVariable, tValue) void(0)
#endif // </advc>


template<typename T> // advc: Replacing some 10 separate functions
inline bool FVariableSystem::GetValue(char const* szVariable, T& tValue) const
{
	VSIteratorC iIterator = m_mapVariableMap.find(szVariable);
	if (iIterator == m_mapVariableMap.end())
		return false;
	FVariable const& kVariable = *iIterator->second;
	ASSERT_VAR_TYPE(kVariable, tValue);
	tValue = kVariable.getValue(tValue);
	return true;
}


inline bool FVariableSystem::GetValue(char const* szVariable, float& fValue) const
{
	VSIteratorC iIterator = m_mapVariableMap.find(szVariable);
	if (iIterator == m_mapVariableMap.end())
		return false;
	FVariable const& kVariable = *iIterator->second;
	switch (kVariable.m_eType)
	{
	case FVARTYPE_FLOAT:
		fValue = kVariable.m_fValue;
		break;
	case FVARTYPE_DOUBLE:
		fValue = (float)kVariable.m_dValue;
		break;
	case FVARTYPE_STRING:
	{
		/*char const* szValue;
		if (!GetValue(szVariable, szValue)) return false;*/
		fValue = (float)atof(/* advc.opt: */ kVariable.m_szValue);
		break;
	}
	case FVARTYPE_WSTRING:
	{
		/*wchar const* szValue;
		if (!GetValue(szVariable, szValue)) return false;*/
		fValue = (float)_wtof(/* advc.opt: */ kVariable.m_wszValue);
		break;
	}
	default: FAssert(false);
	}

	return true;
}


inline bool FVariableSystem::GetValue(char const* szVariable, double& dValue) const
{
	VSIteratorC iIterator = m_mapVariableMap.find(szVariable);
	if (iIterator == m_mapVariableMap.end())
		return false;
	FVariable const& kVariable = *iIterator->second;
	switch (kVariable.m_eType)
	{
	case FVARTYPE_FLOAT:
		dValue = kVariable.m_fValue;
		break;
	case FVARTYPE_DOUBLE:
		dValue = kVariable.m_dValue;
		break;
	case FVARTYPE_STRING:
	{
		/*char const* szValue;
		if (!GetValue(szVariable, szValue)) return false;*/
		dValue = atof(/* advc.opt: */ kVariable.m_szValue);
		break;
	}
	case FVARTYPE_WSTRING:
	{
		/*wchar const* szValue;
		if (!GetValue(szVariable, szValue)) return false;*/
		dValue = _wtof(/* advc.opt: */ kVariable.m_wszValue);
		break;
	}
	default: FAssert(false);
	}

	return true;
}


inline FVariable const* FVariableSystem::GetVariable(char const* szVariable) const
{
	VSIteratorC iIterator = m_mapVariableMap.find(szVariable);
	if (iIterator == m_mapVariableMap.end())
		return NULL;
	return iIterator->second;
}


template<typename T> // advc: Replacing a dozen separate functions
inline void FVariableSystem::SetValue(char const* szVariable, T tValue)
{
	VSIteratorC iIterator = m_mapVariableMap.find(szVariable);
	if (iIterator != m_mapVariableMap.end())
		delete iIterator->second;
	FVariable& kVariable = *new FVariable;
	kVariable.setValue(tValue);
	m_mapVariableMap[szVariable] = &kVariable;
	m_iterator = m_mapVariableMap.begin();
}


inline bool FVariableSystem::RemValue(char const* szVariable)
{
	VSIteratorC iIterator = m_mapVariableMap.find(szVariable);
	if (iIterator != m_mapVariableMap.end())
		delete iIterator->second;
	m_mapVariableMap.erase(szVariable);
	m_iterator = m_mapVariableMap.begin();
	return true;
}


inline std::string FVariableSystem::GetFirstVariableName()
{
	m_iterator = m_mapVariableMap.begin();
	if (m_iterator != m_mapVariableMap.end())
		return m_iterator->first;
	return "";
}


inline std::string FVariableSystem::GetNextVariableName( )
{
	if (m_iterator != m_mapVariableMap.end())
		++m_iterator;
	if (m_iterator != m_mapVariableMap.end())
		return m_iterator->first;
	return "";
}
