/**********************************************************************

File:		CvBugOptions.cpp
Author:		EmperorFool
Created:	2009-01-21

		Copyright (c) 2009 The BUG Mod. All rights reserved.

**********************************************************************/

// This file has been edited for K-Mod

#include "CvGameCoreDLL.h"
#include "CyArgsList.h"
#include "CvDLLPythonIFaceBase.h"
#include "FVariableSystem.h"

#include "CvBugOptions.h"

bool g_bIsBug = false;


void logMsg(const char* format, ...)
{
	static char buf[2048];
	_vsnprintf(buf, 2048 - 4, format, (char*)(&format + 1));
	gDLL->logMsg("bull.log", buf);
}


bool isBug()
{
	return g_bIsBug;
}

void setIsBug(bool bIsBug)
{
	logMsg("isBug: %s", bIsBug ? "true" : "false");
	g_bIsBug = bIsBug;
}


bool getDefineBOOL(const char* xmlKey, bool bDefault)
{
	int iResult = 0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, iResult))
	{
		return iResult != 0;
	}
	else
	{
		return bDefault;
	}
}

int getDefineINT(const char* xmlKey, int iDefault)
{
	int iResult = 0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, iResult))
	{
		return iResult;
	}
	else
	{
		return iDefault;
	}
}


bool getBugOptionBOOL(const char* id, bool bDefault, const char* xmlKey)
{
	if (isBug())
	{
		CyArgsList argsList;
		long lResult = 0;

		argsList.add(id);
		argsList.add(bDefault);

		//logMsg("debug - getOptionBOOL(%s)", id);
		gDLL->getPythonIFace()->callFunction(PYBugOptionsModule, "getOptionBOOL", argsList.makeFunctionArgs(), &lResult);
		//logMsg("debug - got value %ld", lResult);

		return lResult != 0;
	}
	else
	{
		CvString tmp;
		if (!xmlKey)
		{
			tmp.append(OPTION_XML_PREFIX);
			tmp.append(id);
			xmlKey = tmp.c_str();
		}
		//logMsg("debug - getBugOptionBOOL %s", xmlKey);
		return getDefineBOOL(xmlKey, bDefault);
	}
}

int getBugOptionINT(const char* id, int iDefault, const char* xmlKey)
{
	if (isBug())
	{
		CyArgsList argsList;
		long lResult = 0;

		argsList.add(id);
		argsList.add(iDefault);

		//logMsg("debug - getOptionBOOL(%s)", id);
		gDLL->getPythonIFace()->callFunction(PYBugOptionsModule, "getOptionINT", argsList.makeFunctionArgs(), &lResult);
		//logMsg("debug - got value %ld", lResult);

		return lResult;
	}
	else
	{
		CvString tmp;
		if (!xmlKey)
		{
			tmp.append(OPTION_XML_PREFIX);
			tmp.append(id);
			xmlKey = tmp.c_str();
		}
		//logMsg("debug - getBugOptionINT %s", xmlKey);
		return getDefineINT(xmlKey, iDefault);
	}
}
