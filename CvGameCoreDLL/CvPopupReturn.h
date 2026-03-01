#pragma once
//	Purpose:	Return structure for popups
//	Author:		Patrick Dawson
//  Copyright (c) 2002 Firaxis Games, Inc. All rights reserved.
#ifndef CVPOPUPRETURN_h
#define CVPOPUPRETURN_h

class FDataStream;
#define CvPopup_SetAtGrow(kArray, iIdx, kValue)\
	if((int)kArray.size() <= iIdx) kArray.resize(iIdx+1);\
	kArray[iIdx] = kValue;

class PopupReturn
{
	PopupReturn(PopupReturn const&); // advc: Made private (was unused)

public:
	DllExport PopupReturn& operator=(PopupReturn const& source);
	/*	<advc> Implementations moved to CvPopupReturn.cpp.
		Removed most of the uninformative comments. */
	void setSelectedRadioButton(int iValue, int iGroup = 0);
	int getSelectedRadioButton(int iGroup = 0) const;												// Exposed to Python (JS)
	int getRadioButtonSize() const;
	void setCheckboxBitfield(int iValue, int iGroup = 0); // set the bitfield for checkboxes
	int getCheckboxBitfield(int iGroup = 0) const; // get the selected bitfield
	int getCheckboxSize() const;
	void setEditBoxString(CvWString szValue, int iGroup = 0); // set the editbox string
	const wchar *getEditBoxString(int iGroup = 0) const; // get the selected editbox string			// Exposed to Python
	int getEditboxSize() const;
	void setSpinnerWidgetValue(const int iValue, int iGroup = 0); // set the spinner widget value
	int getSpinnerWidgetValue(int iGroup = 0) const;
	int getSpinnerWidsize() const; // get the spinner widget size
	void setSelectedPulldownValue(int iValue, int iGroup = 0); // set the selected pulldown value
	int getSelectedPullDownValue(int iGroup = 0) const;												// Exposed to Python
	int getPulldownSize() const;
	void setSelectedListBoxValue(int iValue, int iGroup = 0); // set the selected listbox value
	int getSelectedListBoxValue(int iGroup = 0) const;												// Exposed to Python
	int getListBoxSize() const;
	void setCurrentSpinBoxValue(int iValue, int iIndex = 0); // set the current spinbox value
	int getCurrentSpinBoxValue(int iIndex = 0) const;												// Exposed to Python
	int getSpinBoxSize() const;
	void setButtonClicked(int iValue, int iGroup = 0); // set the button clicked
	
	int getButtonClicked(int iGroup = 0) const; // get the button ID								// Exposed to Python
	int getButtonSize() const;

	DllExport void read(FDataStreamBase* pStream);
	DllExport void write(FDataStreamBase* pStream) const;

private: // advc.003k (warning): It's not safe to add data members to this class!
	std::vector<int> m_aiSelectedRadioButton;		//	Selected Radio Button
	std::vector<int> m_aiBitField;					//	BitField
	std::vector<CvWString> m_aszEditBoxString;		//	EditBox String
	std::vector<int> m_aiSpinnerWidgetValues;		//	Spinner Widget Values
	std::vector<int> m_aiPulldownID;				//	Pulldown ID
	std::vector<int> m_aiListBoxID;					//	ListBox ID
	std::vector<int> m_aiButtonID;					//	The button clicked on
	std::vector<int> m_aiSpinBoxID;					//	SpinBox ID
};

#undef CvPopup_SetAtGrow

BOOST_STATIC_ASSERT(sizeof(PopupReturn) == 128); // advc.003k

#endif	// CVPOPUPRETURN_h
