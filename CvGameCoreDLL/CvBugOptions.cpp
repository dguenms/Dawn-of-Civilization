/*	Author:		EmperorFool
	Created:	2009-01-21
	Copyright (c) 2009 The BUG Mod. All rights reserved. */
// This file has been edited for K-Mod

#include "CvGameCoreDLL.h"
#include "CvBugOptions.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvGame.h"
#include "FVariableSystem.h"

// advc.003t: Replaced by functions in CvGlobals
/*bool getDefineBOOL(const char* xmlKey, bool bDefault) {
	int iResult = 0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, iResult))
		return iResult != 0;
	else return bDefault;
}

int getDefineINT(const char* xmlKey, int iDefault) {
	int iResult = 0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, iResult))
		return iResult;
	else return iDefault;
}*/

// advc:
bool checkBUGStatus(const char* optionKey, bool bWarn)
{	// Once we've received the screen height, BUG should be good to go.
	if(GC.getGame().getScreenHeight() <= 0 &&
		(!GC.IsGraphicsInitialized() || GC.getGame().getActivePlayer() == NO_PLAYER))
	{
		if(!bWarn)
			return false;
		CvString szMsg = "BUG option ";
		szMsg.append(optionKey);
		szMsg.append(" accessed before BUG initialization");
		FAssertMsg(GC.IsGraphicsInitialized(), szMsg.c_str());
		FAssertMsg(GC.getGame().getActivePlayer() != NO_PLAYER, szMsg.c_str());
		return false;
	}
	return true;
}


bool BUGOption::isEnabled(const char* id, bool bDefault, bool bWarn)
{	// <advc>
	PROFILE_FUNC();
	if(!checkBUGStatus(id, bWarn))
		return bDefault;
	// </advc>
	CyArgsList argsList;
	long lResult = 0;
	argsList.add(id);
	argsList.add(bDefault);
	gDLL->getPythonIFace()->callFunction(PYBugOptionsModule, "getOptionBOOL", argsList.makeFunctionArgs(), &lResult);
	return lResult != 0;
}

int BUGOption::getValue(const char* id, int iDefault, bool bWarn)
{	// <advc>
	if(!checkBUGStatus(id, bWarn))
		return iDefault;
	// </advc>
	CyArgsList argsList;
	long lResult = 0;
	argsList.add(id);
	argsList.add(iDefault);
	gDLL->getPythonIFace()->callFunction(PYBugOptionsModule, "getOptionINT", argsList.makeFunctionArgs(), &lResult);
	return lResult;
}
// advc.003d:
CvString BUGOption::userDirPath()
{
	CvString r;
	gDLL->getPythonIFace()->callFunction(PYBugOptionsModule, "getUserDirStr", NULL, &r);
	return r;
}
