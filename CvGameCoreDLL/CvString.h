#pragma once
#ifndef CvString_h
#define CvString_h

#include <string>

// simple string classes, based on stl, but with a few helpers
// Mustafa Thamer
// Firaxis Games, copyright 2005
//
/*	advc (note): There's a revised version of this class by lesslol in the MNAI-U mod;
	could be more efficient. C2C has also made some changes. */

// advc: Let's make this the place for string utility functions (from Taurus mod)
namespace cstring
{
	inline bool empty(char const* szString)
	{
		return (szString[0] == '\0');
	}
	// Uses a C function, so it kind of fits here.
	inline std::string& tolower(std::string& s)
	{
		for (size_t i = 0; i < s.length(); i++)
			s[i] = static_cast<char>(::tolower(s[i]));
		return s;
	}
}

// wide string
class CvWString : public std::wstring
{
public:
	CvWString() {}
	CvWString(const std::string& s) { Copy(s.c_str()); 	}
	CvWString(const CvWString& s) { *this = s; 	}
	CvWString(const char* s) { Copy(s); 	}
	CvWString(const wchar* s) { if (s) *this = s; }
//	CvWString(const __wchar_t* s) { if (s) *this = s; }
	CvWString(const std::wstring& s) { assign(s.c_str()); }
#ifndef _USRDLL
	// FString conversion, if not in the DLL
	CvWString(const FStringA& s) { Copy(s.GetCString()); }
	CvWString(const FStringW& s) { assign(s.GetCString()); }
#endif
	~CvWString() {}

	void Copy(const char* s); // advc: Definition moved into implementation file

	// FString compatibility
	const wchar* GetCString() const 	{ return c_str(); }

	// implicit conversion
	operator const wchar*() const 	{ return c_str(); }

	// operators
	wchar& operator[](int i) { return std::wstring::operator[](i);	}
	wchar& operator[](std::wstring::size_type i) { return std::wstring::operator[](i);	}
	const wchar operator[](int i) const { return std::wstring::operator[](i);	}
	const CvWString& operator=( const wchar* s) { if (s) assign(s); else clear();	return *this; }
	const CvWString& operator=( const std::wstring& s) { assign(s.c_str());	return *this; }
	const CvWString& operator=( const std::string& w) { Copy(w.c_str());	return *this; }
	const CvWString& operator=( const CvWString& w) { assign(w.c_str());	return *this; }
#ifndef _USRDLL
	// FString conversion, if not in the DLL
	const CvWString& operator=( const FStringW& s) { assign(s.GetCString());	return *this; }
	const CvWString& operator=( const FStringA& w) { Copy(w.GetCString());	return *this; }
#endif
	const CvWString& operator=( const char* w) { Copy(w);	return *this; }

	void Format(LPCWSTR lpszFormat, ...);

	// static helpers
	static bool formatv(std::wstring& out, const wchar * fmt, va_list args);
	static bool format(std::wstring & out, const wchar * fmt, ...);
	static CvWString format(const wchar * fmt, ...);
	static std::wstring formatv(const wchar * fmt, va_list args);
};


//#define WIDEPTR(s) (s ? CvWString(s).c_str() : NULL)

inline CvWString operator+( const CvWString& s, const CvWString& t) { return (std::wstring&)s + (std::wstring&)t; }
inline CvWString operator+( const CvWString& s, const wchar* t) { return (std::wstring&)s + std::wstring(t); }
inline CvWString operator+( const wchar* s, const CvWString& t) { return std::wstring(s) + std::wstring(t); }
//CvString operator+( const CvString& s, const CvString& t) { return (std::string&)s + (std::string&)t; }

class CvWStringBuffer
{
public:
	CvWStringBuffer()
	{
		m_pBuffer = NULL;
		m_iLength = 0;
		m_iCapacity = 0;
	}

	~CvWStringBuffer()
	{
		SAFE_DELETE_ARRAY(m_pBuffer);
	}

	void append(wchar character)
	{
		int newLength = m_iLength + 1;
		ensureCapacity(newLength + 1);
		m_pBuffer[m_iLength] = character;
		m_pBuffer[m_iLength + 1] = 0; //null character
		m_iLength = newLength;
	}

	void append(const wchar *szCharacters); // advc: Definition moved into implementation file

	void append(const CvWString &szString)
	{
		append(szString.GetCString());
	}

	void append(const CvWStringBuffer &szStringBuffer)
	{
		append(szStringBuffer.m_pBuffer);
	}

	void assign(const CvWString &szString)
	{
		assign(szString.GetCString());
	}

	void assign(const wchar *szCharacters)
	{
		clear();
		append(szCharacters);
	}

	void clear()
	{
		if(m_pBuffer != NULL)
		{
			m_iLength = 0;
			m_pBuffer[0] = 0; //null character
		}
	}

	bool isEmpty() const
	{
		return (m_iLength == 0);
	}

	const wchar *getCString()
	{
		ensureCapacity(1);
		return m_pBuffer;
	}

private:
	void ensureCapacity(int newCapacity); // advc: Definition moved into implementation file

	wchar *m_pBuffer;
	int m_iLength;
	int m_iCapacity;
};


class CvString : public std::string
{
public:
	CvString() {}
	CvString(int iLen) { reserve(iLen); }
	CvString(const char* s) { operator=(s); }
	CvString(const std::string& s) { assign(s.c_str()); }
	explicit // don't want accidental conversions down to narrow strings
		/*  advc (note): This conversion breaks when there are any non-ASCII chars
			in the wstring. Should perhaps take into account the locale through
			boost::locale::conv and/ or check for characters that can't be narrowed.
			Many logBBAI calls convert from wide to narrow strings through the %S
			format specifier and _vsnprintf - not sure if that's safer. */
		CvString(const std::wstring& s) { Copy(s.c_str()); }
	~CvString() {}

	void Convert(const std::wstring& w) { Copy(w.c_str());	}
	void Copy(const wchar* w); // advc: Definition moved into implementation file

	// implicit conversion
	operator const char*() const 	{ return c_str(); }
	//	operator const CvWString() const 	{ return CvWString(c_str()); }

	// operators
	char& operator[](int i) { return std::string::operator[](i);	}
	char& operator[](std::string::size_type i) { return std::string::operator[](i);	}
	const char operator[](int i) const { return std::string::operator[](i);	}
	const CvString& operator=( const char* s) { if (s) assign(s); else clear();	return *this; }
	const CvString& operator=( const std::string& s) { assign(s.c_str());	return *this; }
	// don't want accidental conversions down to narrow strings
//	const CvString& operator=( const std::wstring& w) { Copy(w.c_str());	return *this; }
//	const CvString& operator=( const wchar* w) { Copy(w);	return *this; }

	// FString compatibility
	bool IsEmpty() const { return empty();	}
	const char* GetCString() const 	{ return c_str(); }	// convert
	int CompareNoCase(const char* lpsz) const { return stricmp(lpsz, c_str()); }
	int CompareNoCase(const char* lpsz, int iLength) const { return strnicmp(lpsz, c_str(), iLength);  }
	void Format(LPCSTR lpszFormat, ...);
	int GetLength() const { return size(); }
	int Replace(char chOld, char chNew);

	void getTokens(const CvString& delimiters, std::vector<CvString>& tokensOut) const;

	// static helpers
	static bool formatv(std::string& out, const char * fmt, va_list args);
	static bool format(std::string & out, const char * fmt, ...);
	static CvString format(const char * fmt, ...);
	static std::string formatv(const char * fmt, va_list args);
};
// DON'T add any data members or virtual functions to these classes,
// so they stay the same size as their stl counterparts
/*	<advc.003k> This is advisable also b/c this header has been compiled into
	the EXE and its classes are used in the interfaces between EXE and DLL */
BOOST_STATIC_ASSERT(sizeof(CvWString) == sizeof(std::wstring));
BOOST_STATIC_ASSERT(sizeof(CvString) == sizeof(std::string));
BOOST_STATIC_ASSERT(sizeof(CvWStringBuffer) == 12); // </advc.003k>

// INLINES
// Don't move these into a cpp file, since I don't want CvString to be part of the DLL, MT
// advc: I've done just that - since CvString is part of the DLL.


/*	advc (side note): Regarding the FString classes mentioned in Firaxis comments,
	the EXE does use those, and, based on disassembly, the memory layout might be: */
#if 0
struct FString // (Or maybe this is only a component that FString holds a pointer to)
{
	int m_iCapacity;
	int m_iSize;
	char m_cFirstChar;
	char const* GetCString() const { return &m_cFirstChar; }
	/*	I guess growth must involve allocation of raw memory and a reinterpret_cast.
		It's not a static array like MSVC's std::string uses:
		union { Elem _Buf[_BUF_SIZE]; _Elem *_Ptr; ) */
};
#endif

#endif
