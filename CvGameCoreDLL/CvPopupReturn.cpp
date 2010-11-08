#include "CvGameCoreDLL.h"
#include "CvPopupReturn.h"

#define CvPopup_SetAtGrow(kArray, iIdx, kValue)\
	if((int)kArray.size() <= iIdx) kArray.resize(iIdx+1);\
	kArray[iIdx] = kValue;

PopupReturn::PopupReturn(const PopupReturn &popupReturn)
{
	int iI;

	for (iI = 0; iI < popupReturn.getRadioButtonSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSelectedRadioButton, iI, popupReturn.getSelectedRadioButton( iI ));
	}

	for (iI = 0; iI < popupReturn.getCheckboxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiBitField, iI, popupReturn.getCheckboxBitfield( iI ));
	}

	for (iI = 0; iI < popupReturn.getEditboxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aszEditBoxString, iI, popupReturn.getEditBoxString( iI ));
	}

	for (iI = 0; iI < popupReturn.getSpinnerWidsize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, iI, popupReturn.getSpinnerWidgetValue( iI ));
	}

	for (iI = 0; iI < popupReturn.getPulldownSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiPulldownID, iI, popupReturn.getSelectedPullDownValue( iI ));
	}

	for (iI = 0; iI < popupReturn.getListBoxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiListBoxID, iI, popupReturn.getSelectedListBoxValue( iI ));
	}

	for (iI = 0; iI < popupReturn.getSpinBoxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSpinBoxID, iI, popupReturn.getSpinnerWidgetValue( iI ));
	}

	for (iI = 0; iI < popupReturn.getButtonSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiButtonID, iI, popupReturn.getButtonClicked( iI ));
	}
}

// Assignment operator
PopupReturn &PopupReturn::operator=(const PopupReturn &source)
{
	int iI;

	for (iI = 0; iI < source.getRadioButtonSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSelectedRadioButton, iI, source.getSelectedRadioButton( iI ));
	}

	for (iI = 0; iI < source.getCheckboxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiBitField, iI, source.getCheckboxBitfield( iI ));
	}

	for (iI = 0; iI < source.getEditboxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aszEditBoxString, iI, source.getEditBoxString( iI ));
	}

	for (iI = 0; iI < source.getSpinnerWidsize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, iI, source.getSpinnerWidgetValue( iI ));
	}

	for (iI = 0; iI < source.getPulldownSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiPulldownID, iI, source.getSelectedPullDownValue( iI ));
	}

	for (iI = 0; iI < source.getListBoxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiListBoxID, iI, source.getSelectedListBoxValue( iI ));
	}

	for (iI = 0; iI < source.getSpinBoxSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiSpinBoxID, iI, source.getSpinnerWidgetValue( iI ));
	}

	for (iI = 0; iI < source.getButtonSize(); iI++)
	{
		CvPopup_SetAtGrow(m_aiButtonID, iI, source.getButtonClicked( iI ));
	}

	return ( *this );
}

//
// read object from a stream
// 
void PopupReturn::read(FDataStreamBase* pStream)
{
	int iSize;
	int iValue;
	int i;
	wchar szValue[1024];

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiSelectedRadioButton, i, iValue );
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiBitField, i, iValue );
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->ReadString( szValue );
		CvPopup_SetAtGrow(m_aszEditBoxString, i, szValue );
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiSpinnerWidgetValues, i, iValue );
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiPulldownID, i, iValue );
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiListBoxID, i, iValue );
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiSpinBoxID, i, iValue);
	}

	pStream->Read( &iSize );
	for (i = 0; i < iSize; i++)
	{
		pStream->Read( &iValue );
		CvPopup_SetAtGrow(m_aiButtonID, i, iValue );
	}
}

//
// write object to a stream
// 
void PopupReturn::write(FDataStreamBase* pStream) const
{
	unsigned int iI;
	//char szString[1024];
	
	pStream->Write( m_aiSelectedRadioButton.size() );
	for (iI = 0; iI < m_aiSelectedRadioButton.size(); iI++)
	{
		pStream->Write( m_aiSelectedRadioButton[iI] );
	}

	pStream->Write( m_aiBitField.size() );
	for (iI = 0; iI < m_aiBitField.size(); iI++)
	{
		pStream->Write( m_aiBitField[iI] );
	}

	pStream->Write( m_aszEditBoxString.size() );
	for (iI = 0; iI < m_aszEditBoxString.size(); iI++)
	{
		CvWString ws(m_aszEditBoxString[iI]);
		pStream->WriteString( ws.c_str() );
	}

	pStream->Write( m_aiSpinnerWidgetValues.size() );
	for (iI = 0; iI < m_aiSpinnerWidgetValues.size(); iI++)
	{
		pStream->Write( m_aiSpinnerWidgetValues[iI] );
	}

	pStream->Write( m_aiPulldownID.size() );
	for (iI = 0; iI < m_aiPulldownID.size(); iI++)
	{
		pStream->Write( m_aiPulldownID[iI] );
	}

	pStream->Write( m_aiListBoxID.size() );
	for (iI = 0; iI < m_aiListBoxID.size(); iI++)
	{
		pStream->Write( m_aiListBoxID[iI] );
	}

	pStream->Write( m_aiSpinBoxID.size() );
	for (iI = 0; iI < m_aiSpinBoxID.size(); iI++)
	{
		pStream->Write( m_aiSpinBoxID[iI] );
	}

	pStream->Write( m_aiButtonID.size() );
	for (iI = 0; iI < m_aiButtonID.size(); iI++)
	{
		pStream->Write( m_aiButtonID[iI] );
	}
}

