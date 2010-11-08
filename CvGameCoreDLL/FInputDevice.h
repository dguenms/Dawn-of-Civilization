#pragma once

//	$Revision: #4 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//------------------------------------------------------------------------------------------------
//
//  *****************   FIRAXIS GAME ENGINE   ********************
//
//  FILE:    FInputDevice.h
//
//  AUTHOR:  Mustafa Thamer  --  09/10/2003
//
//  PURPOSE: Contains abstract class which samples an input device.
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

#ifndef		FINPUTDEVICE_H
#define		FINPUTDEVICE_H
#pragma		once

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  CLASS:      FInputDevice
//
//  PURPOSE:    Samples input device and sets mapping to indicate what input events
//		happened since the last update call.  Expected derivations include keyboard and mouse devices 
//			for specific hardware platforms.
//		Also provides immediate (stateless) mode functionality for queries like
//			isKeyDownNow().
//		Currently only keyboard events are supported.
//		HotKey mappings can be set which will map input1 to input2.  When input1 happens, input2 
//			will be reported.
//
//+++++++++++++++++++++++++

class FInputDevice
{
public:
	enum Modifiers		// bit flags
	{
		CTRL	= 0x1,
		ALT		= 0x2,
		SHIFT	= 0x4
	};
	enum State
	{
		UNINIT		= -1,
		UP,
		DOWN,
		DBL_CLICK
	};
	enum InitFlags		// init options, based on DirectInput functionality
	{
		INP_EXCLUSIVE	= 0x1,
		INP_FOREGROUND	= 0x2,
		INP_BUFFERED	= 0x4,

#if 0
		INP_DEFAULT_FLAGS = (INP_EXCLUSIVE | INP_BUFFERED)	// allow background access for debugger
#else
		INP_DEFAULT_FLAGS = (INP_EXCLUSIVE | INP_FOREGROUND | INP_BUFFERED)
#endif
	};

	// these input events are added to the input map (if appropriate) whenever the input device is sampled.
	// currently only uses keyboard input events.
	enum InputType		
	{
		NONE	= 0	  ,
		KB_NONE = NONE  ,
		KB_ESCAPE     ,
		KB_0          ,
		KB_1          ,
		KB_2          ,
		KB_3          ,
		KB_4          ,
		KB_5          ,
		KB_6          ,
		KB_7          ,
		KB_8          ,
		KB_9          ,
		KB_MINUS      ,	    /* - on main keyboard */		
		KB_A          ,
		KB_B         ,
		KB_C          ,
		KB_D          ,
		KB_E          ,
		KB_F          ,
		KB_G          ,
		KB_H          ,
		KB_I          ,
		KB_J          ,
		KB_K          ,
		KB_L          ,
		KB_M          ,
		KB_N          ,
		KB_O          ,
		KB_P          ,
		KB_Q          ,
		KB_R          ,
		KB_S          ,
		KB_T          ,
		KB_U          ,
		KB_V          ,
		KB_W          ,
		KB_X          ,
		KB_Y          ,
		KB_Z          ,
		KB_EQUALS     ,
		KB_BACKSPACE  ,
		KB_TAB        ,
		KB_LBRACKET   ,
		KB_RBRACKET   ,
		KB_RETURN     ,		/* Enter on main keyboard */
		KB_LCONTROL   ,
		KB_SEMICOLON  ,
		KB_APOSTROPHE ,
		KB_GRAVE      ,		/* accent grave */
		KB_LSHIFT     ,
		KB_BACKSLASH  ,
		KB_COMMA      ,
		KB_PERIOD     ,
		KB_SLASH      ,
		KB_RSHIFT     ,
		KB_NUMPADSTAR   ,
		KB_LALT      ,	
		KB_SPACE      ,
		KB_CAPSLOCK    ,
		KB_F1         ,
		KB_F2         ,
		KB_F3         ,
		KB_F4         ,
		KB_F5         ,
		KB_F6         ,
		KB_F7         ,
		KB_F8         ,
		KB_F9         ,
		KB_F10        ,
		KB_F11        ,
		KB_F12        ,
		KB_NUMLOCK    ,
		KB_SCROLL     ,
		KB_NUMPAD0    ,
		KB_NUMPAD1    ,
		KB_NUMPAD2    ,
		KB_NUMPAD3    ,
		KB_NUMPAD4    ,
		KB_NUMPAD5    ,
		KB_NUMPAD6    ,
		KB_NUMPAD7    ,
		KB_NUMPAD8    ,
		KB_NUMPAD9    ,
		KB_NUMPADMINUS   ,
		KB_NUMPADPLUS        ,
		KB_NUMPADPERIOD    , 
		KB_NUMPADEQUALS,
		KB_AT,
		KB_UNDERLINE,
		KB_COLON,
		KB_NUMPADENTER,
		KB_RCONTROL   ,
		KB_VOLUMEDOWN ,
		KB_VOLUMEUP   ,
		KB_NUMPADCOMMA,
		KB_NUMPADSLASH     ,
		KB_SYSRQ      ,
		KB_RALT      ,
		KB_PAUSE      ,
		KB_HOME       ,
		KB_UP         ,
		KB_PGUP      ,
		KB_LEFT       ,
		KB_RIGHT      ,
		KB_END        ,
		KB_DOWN       ,
		KB_PGDN       ,
		KB_INSERT     ,
		KB_DELETE,     

		M_NONE,
		M_LEFT,
		M_CENTER,
		M_RIGHT,
		M_FORWARD,
		M_BACKWARD,
		M_WHEEL,

		NUM_INPUT_TYPE		// keep at the end
	};

private:
	// comparison class for STL map sorting
	struct compStruct
	{
		bool operator()(const InputType s1, const InputType s2) const	{	return (s1<s2);		}
	};
public:
	// holds the data associated with an input event
	struct InputValue
	{
		int m_iState;		// used for key state, FKBInputDevice::KEY_UP/FKBInputDevice::KEY_DOWN
		POINT m_point;		// used for mouse coords
		InputValue(int iState=UNINIT, int px=-1, int py=-1) : m_iState(iState) {m_point.x=px; m_point.y=py;  }
		bool operator==(const InputValue& in) const		{ return in.m_iState==m_iState && in.m_point.x==m_point.x && in.m_point.y==m_point.y; }
	};

	// holds the input type and data
	struct InputEvent
	{
		uint m_uiModifiers;		// CTRL/ALT/SHIFT
		InputValue m_val;		// state and location
		InputType m_type;		// event type
		InputEvent() : m_uiModifiers(0),m_type(NONE) {}
		InputEvent(InputType it, InputValue iv, uint uiMod=0) : m_type(it), m_val(iv), m_uiModifiers(uiMod) {}
		bool operator==(const InputEvent& in) const
		{ return (in.m_val==m_val && in.m_type==m_type && in.m_uiModifiers==m_uiModifiers); }
	};
	typedef std::vector<InputEvent> InputEventsList;				// list of input events

	FInputDevice();
	virtual ~FInputDevice();

	bool Init(unsigned long flags=INP_DEFAULT_FLAGS);
	bool UnInit();									

	virtual bool ReadInputs() = 0;									// sample input and fill in InputEventList

	unsigned long GetFlags() const { return m_ulFlags; }			// init flags should be passed in to Init()

	// access the map of buffered input events
	const InputEventsList& GetInputEvents() const { return m_InputEvents;	}	// return list of input events
	int GetNumInputEvents() const { return (int)m_InputEvents.size();	}
	const InputEvent& GetInputEvent(int i) { return m_InputEvents[i];	}

	// immediate mode accessors
	virtual InputValue GetInputImmediate(InputType input) const = 0;

	// hot key mappings
	void AddHotKeyMapping(InputType inputFrom, InputType inputTo);	// Will overwrite any existing mapping for that input.
	bool RemoveHotKeyMapping(InputType inputFrom);
	void ClearHotKeyMappings();
	InputType TranslateHotKey(InputType inputFrom) const;			// Call to use hot key mappings
protected:
	typedef std::map<InputType, InputType, compStruct> HotKeyMap;	// map of inputs to inputs (internal use only)

	virtual bool IInit() = 0;
	virtual bool IUnInit() = 0;

	HotKeyMap m_HotKeyMap;
	InputEventsList m_InputEvents;
	bool m_bInitted;
	unsigned long m_ulFlags;
};

#endif	//FINPUTDEVICE_H
