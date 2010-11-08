#include "CvGameCoreDLL.h"
#include ".\cvpopupinfo.h"

CvPopupInfo::CvPopupInfo(ButtonPopupTypes eButtonPopupType, int iData1, int iData2, int iData3, int iFlags, bool bOption1, bool bOption2) :
	m_iData1(iData1),
	m_iData2(iData2),
	m_iData3(iData3),
	m_iFlags(iFlags),
	m_bOption1(bOption1),
	m_bOption2(bOption2),
	m_eButtonPopupType(eButtonPopupType),
	m_bPendingDelete(false)
{
}

CvPopupInfo::~CvPopupInfo()
{
}

const CvPopupInfo& CvPopupInfo::operator=(const CvPopupInfo& other)
{
	setButtonPopupType(other.getButtonPopupType());
	setData1(other.getData1());
	setData2(other.getData2());
	setData3(other.getData3());
	setFlags(other.getFlags());
	setOption1(other.getOption1());
	setOption2(other.getOption2());
	setText(other.getText());
	setPendingDelete(other.getPendingDelete());
	setOnFocusPythonCallback(other.getOnFocusPythonCallback());
	setOnClickedPythonCallback(other.getOnClickedPythonCallback());
	setPythonModule(other.getPythonModule());
	m_aPythonButtons.clear();
	for (int i = 0; i < other.getNumPythonButtons(); i++)
	{
		m_aPythonButtons.push_back(other.m_aPythonButtons[i]);
	}

	return (*this);
}


int CvPopupInfo::getData1() const
{
	return m_iData1;
}

int CvPopupInfo::getData2() const
{
	return m_iData2;
}

int CvPopupInfo::getData3() const
{
	return m_iData3;
}

int CvPopupInfo::getFlags() const
{
	return m_iFlags;
}

bool CvPopupInfo::getOption1() const
{
	return m_bOption1;
}

bool CvPopupInfo::getOption2() const
{
	return m_bOption2;
}

ButtonPopupTypes CvPopupInfo::getButtonPopupType() const
{
	return m_eButtonPopupType;
}

const CvWString& CvPopupInfo::getText() const
{
	return m_szText;
}

const CvString& CvPopupInfo::getOnFocusPythonCallback() const
{
	return m_szOnFocusPythonCallback;
}

const CvString& CvPopupInfo::getOnClickedPythonCallback() const
{
	return m_szOnClickedPythonCallback;
}

const CvString& CvPopupInfo::getPythonModule() const
{
	return m_szPythonModule;
}

const CvWString& CvPopupInfo::getPythonButtonText(int i) const
{
	FAssertMsg(i < (int)m_aPythonButtons.size(), "index out of range");
	return m_aPythonButtons[i].szText;
}

const CvString& CvPopupInfo::getPythonButtonArt(int i) const
{
	FAssertMsg(i < (int)m_aPythonButtons.size(), "index out of range");
	return m_aPythonButtons[i].szArt;
}

void CvPopupInfo::setData1(int iValue)
{
	m_iData1 = iValue;
}

void CvPopupInfo::setData2(int iValue)
{
	m_iData2 = iValue;
}

void CvPopupInfo::setData3(int iValue)
{
	m_iData3 = iValue;
}

void CvPopupInfo::setFlags(int iValue)
{
	m_iFlags = iValue;
}

void CvPopupInfo::setOption1(bool bValue)
{
	m_bOption1 = bValue;
}

void CvPopupInfo::setOption2(bool bValue)
{
	m_bOption2 = bValue;
}

void CvPopupInfo::setButtonPopupType(ButtonPopupTypes eValue)
{
	m_eButtonPopupType = eValue;
}

void CvPopupInfo::setText(const wchar* pszText)
{
	m_szText = pszText;
}

bool CvPopupInfo::getPendingDelete() const
{
	return m_bPendingDelete;
}

void CvPopupInfo::setPendingDelete(bool bDelete)
{
	m_bPendingDelete = bDelete;
}


void CvPopupInfo::setOnFocusPythonCallback(const char* pszCallback)
{
	m_szOnFocusPythonCallback = pszCallback;
}

void CvPopupInfo::setOnClickedPythonCallback(const char* pszCallback)
{
	m_szOnClickedPythonCallback = pszCallback;
}

void CvPopupInfo::setPythonModule(const char* pszModule)
{
	m_szPythonModule = pszModule;
}

void CvPopupInfo::addPythonButton(const wchar* szText, const char* szArt)
{
	CvPopupButtonPython button;
	button.szText = szText;
	button.szArt = szArt;
	m_aPythonButtons.push_back(button);
}

int CvPopupInfo::getNumPythonButtons() const
{
	return (int)m_aPythonButtons.size();
}


void CvPopupInfo::read(FDataStreamBase& stream)
{
	stream.Read(&m_iData1);
	stream.Read(&m_iData2);
	stream.Read(&m_iData3);
	stream.Read(&m_iFlags);
	stream.Read(&m_bOption1);
	stream.Read(&m_bOption2);

	int iType;
	stream.Read(&iType);
	m_eButtonPopupType = (ButtonPopupTypes)iType;
	stream.ReadString(m_szText);

	stream.ReadString(m_szOnFocusPythonCallback);
	stream.ReadString(m_szOnClickedPythonCallback);
	stream.ReadString(m_szPythonModule);
	uint iSize;
	stream.Read(&iSize);
	for (uint i = 0; i < iSize; i++)
	{
		CvPopupButtonPython button;
		stream.ReadString(button.szText);
		stream.ReadString(button.szArt);
		m_aPythonButtons.push_back(button);
	}
}

void CvPopupInfo::write(FDataStreamBase& stream) const
{
	stream.Write(m_iData1);
	stream.Write(m_iData2);
	stream.Write(m_iData3);
	stream.Write(m_iFlags);
	stream.Write(m_bOption1);
	stream.Write(m_bOption2);

	stream.Write(m_eButtonPopupType);
	stream.WriteString(m_szText);

	stream.WriteString(m_szOnFocusPythonCallback);
	stream.WriteString(m_szOnClickedPythonCallback);
	stream.WriteString(m_szPythonModule);
	uint iSize = m_aPythonButtons.size();
	stream.Write(iSize);
	for (uint i = 0; i < iSize; i++)
	{
		stream.WriteString(m_aPythonButtons[i].szText);
		stream.WriteString(m_aPythonButtons[i].szArt);
	}
}
