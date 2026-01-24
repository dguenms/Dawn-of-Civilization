#include "CvGameCoreDLL.h"
#include "CvString.h"

/*	advc: New implementation file for function definitions moved from CvString.h.
	Note, however, that these definitions were compiled into th EXE along with
	the rest of the header. */

void CvWString::Copy(const char* s)
{
	// <advc.001> (from C2C)
	if (s == NULL || s[0] == '\0')
	{
		clear();
		return;
	} // </advc.001>
	wchar *w = new wchar[strlen(s) + 1];
	swprintf(w, L"%S", s); // convert
	assign(w);
	delete [] w;
}


void CvWStringBuffer::append(const wchar *szCharacters)
{
	if(szCharacters == NULL)
		return;

	int inputLength = wcslen(szCharacters);
	int newLength = m_iLength + inputLength;
	ensureCapacity(newLength + 1);

	//append data
	memcpy(m_pBuffer + m_iLength, szCharacters, sizeof(wchar) * (inputLength + 1)); //null character
	m_iLength = newLength;
}


void CvWStringBuffer::ensureCapacity(int newCapacity)
{
	if(newCapacity <= m_iCapacity)
		return;

	m_iCapacity = 2 * newCapacity; //grow by %100
	wchar *newBuffer = new wchar [m_iCapacity];

	//copy data
	if(m_pBuffer != NULL)
	{
		memcpy(newBuffer, m_pBuffer, sizeof(wchar) * (m_iLength + 1)); //null character
		//erase old memory
		SAFE_DELETE_ARRAY(m_pBuffer);
	}
	else newBuffer[0] = 0; //null character
	m_pBuffer = newBuffer;
}


void CvString::Copy(const wchar* w)
{	// <advc.001> (from C2C)
	if (w == NULL || w[0] == '\0')
	{
		clear();
		return;
	} // </advc.001>
	char *s = new char[wcslen(w) + 1];
	sprintf(s, "%S", w); // convert
	assign(s);
	delete [] s;
}


int CvString::Replace(char chOld, char chNew)
{
	int iCnt = 0;
	for(int i = 0; i < (int)size(); i++)
	{
		if ((*this)[i] == chOld)
		{
			replace(i, 1, std::string(1, chNew));
			iCnt++;
		}
	}
	return iCnt;
}


void CvString::getTokens(const CvString& delimiters, std::vector<CvString>& tokensOut) const
{
	//tokenizer code taken from http://www.digitalpeer.com/id/simple

	// skip delimiters at beginning.
	size_type lastPos = find_first_not_of(delimiters, 0);

	// find first "non-delimiter".
	size_type pos = find_first_of(delimiters, lastPos);

	while (CvString::npos != pos || CvString::npos != lastPos)
	{
		// found a token, parse it.
		CvString token = substr(lastPos, pos - lastPos);
		tokensOut.push_back(token);

		// skip delimiters.  Note the "not_of"
		lastPos = find_first_not_of(delimiters, pos);

		// find next "non-delimiter"
		pos = find_first_of(delimiters, lastPos);
	}
}


bool CvString::formatv(std::string & out, const char * fmt, va_list args)
{
	char buf[2048];
	char* pbuf = buf;
	int attempts = 0;
	bool success = false;
	const int kMaxAttempts = 40;

	do
	{
		int maxlen = 2047+2048*attempts;
		int len = _vsnprintf(pbuf,maxlen,fmt,args);
		attempts++;
		success = (len>=0 && len<=maxlen);
		if (!success)
		{
			if (pbuf!=buf)
				delete [] pbuf;
			pbuf = new char[2048+2048*attempts];
		}
	}
	while (!success && attempts<kMaxAttempts);

	if (attempts==kMaxAttempts)
	{
		// dxPrintNL("CvString::formatv - Max reallocs occurred while formatting string. Result is likely truncated!", 0);
	}

	if (success)
		out = pbuf;
	else
		out.clear(); // K-Mod

	if (pbuf!=buf)
		delete [] pbuf;

	return success;
}


bool CvWString::formatv(std::wstring & out, const wchar * fmt, va_list args)
{
	wchar buf[2048];
	wchar * pbuf = buf;
	int attempts = 0;
	bool success = false;
	const int kMaxAttempts = 40;

	do
	{
		int maxlen = 2047+2048*attempts;
		int len = _vsnwprintf(pbuf,maxlen,fmt,args);
		attempts++;
		success = (len>=0 && len<=maxlen);
		if (!success)
		{
			if (pbuf!=buf)
				delete [] pbuf;
			pbuf = new wchar[2048+2048*attempts];
		}
	}
	while (!success && attempts<kMaxAttempts);

	if (attempts==kMaxAttempts)
	{
		// dxPrintNL("CvString::formatv - Max reallocs occurred while formatting string. Result is likely truncated!", 0);
	}

	if (success)
		out = pbuf;
	else
		out.clear(); // K-Mod

	if (pbuf!=buf)
		delete [] pbuf;

	return success;
}


std::wstring CvWString::formatv(const wchar * fmt, va_list args)
{
	std::wstring result;
	formatv(result, fmt, args);
	return result;
}


CvWString CvWString::format(const wchar * fmt, ...)
{
	std::wstring result;
	va_list args;
	va_start(args,fmt);
	formatv(result,fmt,args);
	va_end(args);
	return CvWString(result);
}


bool CvWString::format(std::wstring & out, const wchar * fmt, ...)
{
	va_list args;
	va_start(args,fmt);
	bool r = formatv(out,fmt,args);
	va_end(args);
	return r;
}


void CvWString::Format( LPCWSTR lpszFormat, ...)
{
	std::wstring result;
	va_list args;
	va_start(args,lpszFormat);
	formatv(result,lpszFormat,args);
	va_end(args);
	*this = result;
}


std::string CvString::formatv(const char * fmt, va_list args)
{
	std::string result;
	formatv(result, fmt, args);
	return result;
}


CvString CvString::format(const char * fmt, ...)
{
	std::string result;
	va_list args;
	va_start(args,fmt);
	formatv(result,fmt,args);
	va_end(args);
	return CvString(result);
}


bool CvString::format(std::string & out, const char * fmt, ...)
{
	va_list args;
	va_start(args,fmt);
	bool r = formatv(out,fmt,args);
	va_end(args);
	return r;
}


void CvString::Format( LPCSTR lpszFormat, ...)
{
	std::string result;
	va_list args;
	va_start(args,lpszFormat);
	formatv(result,lpszFormat,args);
	va_end(args);
	*this = result;
}
