#pragma once

#ifndef CvDLLIniParserIFaceBase_h
#define CvDLLIniParserIFaceBase_h

//
// abstract interface for FIniParser functions used by DLL
//
class FIniParser;
class CvDLLIniParserIFaceBase
{
public:
	virtual FIniParser* create(const char* szFile) = 0;
	virtual void destroy(FIniParser*& pParser, bool bSafeDelete=true) = 0;
	virtual bool SetGroupKey(FIniParser* pParser, const LPCTSTR pGroupKey) = 0;
	virtual bool GetKeyValue(FIniParser* pParser, const LPCTSTR szKey, bool  *iValue) = 0;
	virtual bool GetKeyValue(FIniParser* pParser, const LPCTSTR szKey, short *iValue) = 0;
	virtual bool GetKeyValue(FIniParser* pParser, const LPCTSTR szKey, int   *iValue) = 0;
	virtual bool GetKeyValue(FIniParser* pParser, const LPCTSTR szKey, float *fValue) = 0;
	virtual bool GetKeyValue(FIniParser* pParser, const LPCTSTR szKey, LPTSTR szValue) = 0;

};

#endif	// CvDLLIniParserIFaceBase_h
