#include "CvGameCoreDLL.h"
#include "CvPopupReturn.h"

#define CvPopup_SetAtGrow(kArray, iIdx, kValue)\
	if((int)kArray.size() <= iIdx) kArray.resize(iIdx+1);\
	kArray[iIdx] = kValue;

PopupReturn::PopupReturn(const PopupReturn &popupReturn)
{
	// advc: (and original code commented out)
	FErrorMsg("PopupReturn copy-constructor not implemented");
	/*int iI;

	for (iI = 0; iI < popupReturn.getRadioButtonSize(); iI++)
		CvPopup_SetAtGrow(m_aiSelectedRadioButton, iI, popupReturn.getSelectedRadioButton(iI));
	for (iI = 0; iI < popupReturn.getCheckboxSize(); iI++)
		CvPopup_SetAtGrow(m_aiBitField, iI, popupReturn.getCheckboxBitfield(iI));
	for (iI = 0; iI < popupReturn.getEditboxSize(); iI++)
		CvPopup_SetAtGrow(m_aszEditBoxString, iI, popupReturn.getEditBoxString(iI));
	for (iI = 0; iI < popupReturn.getSpinnerWidsize(); iI++)
		CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, iI, popupReturn.getSpinnerWidgetValue(iI));
	for (iI = 0; iI < popupReturn.getPulldownSize(); iI++)
		CvPopup_SetAtGrow(m_aiPulldownID, iI, popupReturn.getSelectedPullDownValue(iI));
	for (iI = 0; iI < popupReturn.getListBoxSize(); iI++)
		CvPopup_SetAtGrow(m_aiListBoxID, iI, popupReturn.getSelectedListBoxValue(iI));
	for (iI = 0; iI < popupReturn.getSpinBoxSize(); iI++)
		CvPopup_SetAtGrow(m_aiSpinBoxID, iI, popupReturn.getSpinnerWidgetValue(iI));
	for (iI = 0; iI < popupReturn.getButtonSize(); iI++)
		CvPopup_SetAtGrow(m_aiButtonID, iI, popupReturn.getButtonClicked(iI));*/
}

// Assignment operator
PopupReturn &PopupReturn::operator=(const PopupReturn &source)
{
	int iI;

	for (iI = 0; iI < source.getRadioButtonSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSelectedRadioButton, iI, source.getSelectedRadioButton(iI));
	}

	for (iI = 0; iI < source.getCheckboxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiBitField, iI, source.getCheckboxBitfield(iI));
	}

	for (iI = 0; iI < source.getEditboxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aszEditBoxString, iI, source.getEditBoxString(iI));
	}

	for (iI = 0; iI < source.getSpinnerWidsize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, iI, source.getSpinnerWidgetValue(iI));
	}

	for (iI = 0; iI < source.getPulldownSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiPulldownID, iI, source.getSelectedPullDownValue(iI));
	}

	for (iI = 0; iI < source.getListBoxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiListBoxID, iI, source.getSelectedListBoxValue(iI));
	}

	for (iI = 0; iI < source.getSpinBoxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSpinBoxID, iI, source.getSpinnerWidgetValue(iI));
	}

	for (iI = 0; iI < source.getButtonSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiButtonID, iI, source.getButtonClicked(iI));
	}

	return *this;
}


void PopupReturn::read(FDataStreamBase* pStream)
{
	int iSize=-1;
	int iValue=-1;
	int i;

	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiSelectedRadioButton, i, iValue);
	}

	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiBitField, i, iValue);
	}
	{
		pStream->Read(&iSize);
		wchar szValue[1024];
		for (i = 0; i < iSize; i++)
		{
			pStream->ReadString(szValue);
			CvPopup_SetAtGrow(m_aszEditBoxString, i, szValue);
		}
	}
	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, i, iValue);
	}

	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiPulldownID, i, iValue);
	}

	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiListBoxID, i, iValue);
	}

	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiSpinBoxID, i, iValue);
	}

	pStream->Read(&iSize);
	for (i = 0; i < iSize; i++)
	{
		pStream->Read(&iValue);
		CvPopup_SetAtGrow(m_aiButtonID, i, iValue);
	}
}


void PopupReturn::write(FDataStreamBase* pStream) const
{
	size_t iI;

	pStream->Write(m_aiSelectedRadioButton.size());
	for (iI = 0; iI < m_aiSelectedRadioButton.size(); iI++)
	{
		pStream->Write(m_aiSelectedRadioButton[iI]);
	}

	pStream->Write(m_aiBitField.size());
	for (iI = 0; iI < m_aiBitField.size(); iI++)
	{
		pStream->Write(m_aiBitField[iI]);
	}

	pStream->Write(m_aszEditBoxString.size());
	for (iI = 0; iI < m_aszEditBoxString.size(); iI++)
	{
		CvWString ws(m_aszEditBoxString[iI]);
		pStream->WriteString( ws.c_str() );
	}

	pStream->Write(m_aiSpinnerWidgetValues.size());
	for (iI = 0; iI < m_aiSpinnerWidgetValues.size(); iI++)
	{
		pStream->Write(m_aiSpinnerWidgetValues[iI]);
	}

	pStream->Write(m_aiPulldownID.size());
	for (iI = 0; iI < m_aiPulldownID.size(); iI++)
	{
		pStream->Write(m_aiPulldownID[iI]);
	}

	pStream->Write(m_aiListBoxID.size());
	for (iI = 0; iI < m_aiListBoxID.size(); iI++)
	{
		pStream->Write(m_aiListBoxID[iI]);
	}

	pStream->Write(m_aiSpinBoxID.size());
	for (iI = 0; iI < m_aiSpinBoxID.size(); iI++)
	{
		pStream->Write(m_aiSpinBoxID[iI]);
	}

	pStream->Write(m_aiButtonID.size());
	for (iI = 0; iI < m_aiButtonID.size(); iI++)
	{
		pStream->Write(m_aiButtonID[iI]);
	}
}

/*	<advc> Implementations moved from header. Neater. These don't need to be inlined.
	Replaced some operator[] accesses with vector::at. */
void PopupReturn::setSelectedRadioButton(int iValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aiSelectedRadioButton, iGroup, iValue);
}

int PopupReturn::getSelectedRadioButton(int iGroup) const
{
	return m_aiSelectedRadioButton.at(iGroup);
}

int PopupReturn::getRadioButtonSize() const
{
	return m_aiSelectedRadioButton.size();
}

void PopupReturn::setCheckboxBitfield(int iValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aiBitField, iGroup, iValue);
}

int PopupReturn::getCheckboxBitfield(int iGroup) const
{
	return m_aiBitField.at(iGroup);
}

int PopupReturn::getCheckboxSize() const
{
	return m_aiBitField.size();
}

void PopupReturn::setEditBoxString(CvWString szValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aszEditBoxString, iGroup, szValue);
}

wchar const* PopupReturn::getEditBoxString(int iGroup) const
{
	if (iGroup < (int)m_aszEditBoxString.size())
		return m_aszEditBoxString.at(iGroup);
	return NULL;
}

int PopupReturn::getEditboxSize() const
{
	return m_aszEditBoxString.size();
}

void PopupReturn::setSpinnerWidgetValue(const int iValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, iGroup, iValue);
}

int PopupReturn::getSpinnerWidgetValue(int iGroup) const
{
	return (iGroup < ((int)m_aiSpinBoxID.size()) ? m_aiSpinBoxID.at(iGroup) : -1);
}

int PopupReturn::getSpinnerWidsize() const
{
	return m_aiSpinnerWidgetValues.size();
}

void PopupReturn::setSelectedPulldownValue(int iValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aiPulldownID, iGroup, iValue);
}

int PopupReturn::getSelectedPullDownValue(int iGroup) const
{
	return m_aiPulldownID.at(iGroup);
}

int PopupReturn::getPulldownSize() const
{
	return m_aiPulldownID.size();
}

void PopupReturn::setSelectedListBoxValue(int iValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aiListBoxID, iGroup, iValue);
}

int PopupReturn::getSelectedListBoxValue(int iGroup) const
{
	return (iGroup < ((int)m_aiListBoxID.size()) ? m_aiListBoxID.at(iGroup) : -1);
}

int PopupReturn::getListBoxSize() const
{
	return m_aiListBoxID.size();
}

void PopupReturn::setCurrentSpinBoxValue(int iValue, int iIndex)
{
	CvPopup_SetAtGrow(m_aiSpinBoxID, iIndex, iValue);
}

int PopupReturn::getCurrentSpinBoxValue(int iIndex) const
{
	return (iIndex < ((int)m_aiSpinBoxID.size()) ? m_aiSpinBoxID.at(iIndex) : -1);
}

int PopupReturn::getSpinBoxSize() const
{
	return m_aiSpinBoxID.size();
}

void PopupReturn::setButtonClicked(int iValue, int iGroup)
{
	CvPopup_SetAtGrow(m_aiButtonID, iGroup, iValue);
}

int PopupReturn::getButtonClicked(int iGroup) const
{
	return m_aiButtonID.at(iGroup);
}

int PopupReturn::getButtonSize() const
{
	return m_aiButtonID.size();
}
// </advc> (end of moved implementations)
