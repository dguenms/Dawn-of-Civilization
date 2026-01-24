//  FILE:    CvXMLLoadUtility.cpp
//  AUTHOR:  Eric MacDonald  --  8/2003
//			 Mustafa Thamer
//  PURPOSE: Group of functions to load in the xml files for Civilization 4
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"
#include "CvInfo_Misc.h"

static const int kBufSize = 2048;

/*	advc.006g: Prefer a failed assertion over a message box when debugging.
	I've redirected all MessageBox calls to this function. */
void CvXMLLoadUtility::errorMessage(char const* szMessage, XMLErrorTypes eErrType)
{
	#ifdef _DEBUG
		FErrorMsg(szMessage);
	#else
		gDLL->MessageBox(szMessage, eErrType == XML_LOAD_ERROR ?
				"XML Load Error" : "XML Error");
	#endif
}

void CvXMLLoadUtility::logMsg(char* format, ...)
{
	static char buf[kBufSize];
	_vsnprintf(buf, kBufSize-4, format, (char*)(&format+1));
	gDLL->logMsg("xml.log", buf);
}

bool CvXMLLoadUtility::CreateFXml()
{
	PROFILE("CreateFXML");
	try
	{
		m_pFXml = gDLL->getXMLIFace()->CreateFXml(m_pSchemaCache);
	}
	catch(...)
	{
		char	szMessage[512];
		sprintf( szMessage, "Caught unhandled exception creating XML parser object \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		errorMessage(szMessage, XML_LOAD_ERROR);
		return false;
	}
	return true;
}

void CvXMLLoadUtility::DestroyFXml()
{
	PROFILE("DestroyFXML");
	gDLL->getXMLIFace()->DestroyFXml(m_pFXml);
}


CvXMLLoadUtility::CvXMLLoadUtility() :
//m_iCurProgressStep(0), m_pCBFxn(NULL)
m_pDummy(NULL), // advc.003k
m_pFXml(NULL)
{
	m = new Data(); // advc.003k
	m->bAssertMandatory = true; // advc.006b
	m->bEventsLoaded = m->bThroneRoomLoaded = false; // advc.003v
	m->bTrueStartsDataLoaded = false; // advc.tsl
	m_pSchemaCache = gDLL->getXMLIFace()->CreateFXmlSchemaCache();
}


CvXMLLoadUtility::~CvXMLLoadUtility()
{
	/*	advc (note): The EXE only seems to call this when exiting from the opening menu.
		But possibly deleting it twice seems worse than never, so I'm not going to
		delete CvGlobals::m_pXMLLoadUtility in CvDLLButtonPopup::OnOkClicked . */
	gDLL->getXMLIFace()->DestroyFXmlSchemaCache(m_pSchemaCache);
	SAFE_DELETE(m); // advc.003k
}

// Clean up items for in-game reloading
void CvXMLLoadUtility::ResetLandscapeInfo()
{
	CvGlobals& kGlobals = CvGlobals::getInstance(); // advc.003t: non-const globals
	for (int i = 0; i < GC.getNumLandscapeInfos(); ++i)
		SAFE_DELETE(kGlobals.m_paLandscapeInfo[i]);
	kGlobals.m_paLandscapeInfo.clear();
	SetupGlobalLandscapeInfo();
}

// Clean up items for in-game reloading
void CvXMLLoadUtility::ResetGlobalEffectInfo()
{
	CvGlobals& kGlobals = CvGlobals::getInstance(); // advc.003t: non-const globals
	for (int i = 0; i < kGlobals.getNumEffectInfos(); ++i)
		SAFE_DELETE(kGlobals.m_paEffectInfo[i]);
	kGlobals.m_paEffectInfo.clear();
	LoadGlobalClassInfo(kGlobals.m_paEffectInfo, "CIV4EffectInfos", "Misc", "Civ4EffectInfos/EffectInfos/EffectInfo", false, false);
}

// advc.003j: Unused (always was, apparently)
// Takes a string of hex digits, 0-f and converts it into an unsigned integer mask value
#if 0
void CvXMLLoadUtility::MakeMaskFromString(unsigned int *puiMask, char* szMask)
{
	int iLength = (int)strlen(szMask); // kmodx: compute strlen only once
	// loop through each character in the szMask parameter
	for (int i=0;i<iLength;i++) // kmodx: see above
	{	// if the current character in the string is a zero
		if (szMask[i] == '0')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// making the last 4 bits of the mask 0000
		}
		// if the current character in the string is a zero
		else if (szMask[i] == '1')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 1 to the adjusted value of the mask
			// making the last 4 bits of the mask 0001
			*puiMask += 1;
		}
		// if the current character in the string is a two
		else if (szMask[i] == '2')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 2 to the adjusted value of the mask
			// making the last 4 bits of the mask 0010
			*puiMask += 2;
		}
		// if the current character in the string is a three
		else if (szMask[i] == '3')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 3 to the adjusted value of the mask
			// making the last 4 bits of the mask 0011
			*puiMask += 3;
		}
		// if the current character in the string is a four
		else if (szMask[i] == '4')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 4 to the adjusted value of the mask
			// making the last 4 bits of the mask 0100
			*puiMask += 4;
		}
		// if the current character in the string is a five
		else if (szMask[i] == '5')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 5 to the adjusted value of the mask
			// making the last 4 bits of the mask 0101
			*puiMask += 5;
		}
		// if the current character in the string is a six
		else if (szMask[i] == '6')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 6 to the adjusted value of the mask
			// making the last 4 bits of the mask 0110
			*puiMask += 6;
		}
		// if the current character in the string is a seven
		else if (szMask[i] == '7')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 7 to the adjusted value of the mask
			// making the last 4 bits of the mask 0111
			*puiMask += 7;
		}
		// if the current character in the string is a eight
		else if (szMask[i] == '8')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 8 to the adjusted value of the mask
			// making the last 4 bits of the mask 1000
			*puiMask += 8;
		}
		// if the current character in the string is a nine
		else if (szMask[i] == '9')
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 9 to the adjusted value of the mask
			// making the last 4 bits of the mask 1001
			*puiMask += 9;
		}
		// if the current character in the string is a A, 10
		else if ((szMask[i] == 'a') || (szMask[i] == 'A'))
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 10 to the adjusted value of the mask
			// making the last 4 bits of the mask 1010
			*puiMask += 10;
		}
		// if the current character in the string is a B, 11
		else if ((szMask[i] == 'b') || (szMask[i] == 'B'))
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 11 to the adjusted value of the mask
			// making the last 4 bits of the mask 1011
			*puiMask += 11;
		}
		// if the current character in the string is a C, 12
		else if ((szMask[i] == 'c') || (szMask[i] == 'C'))
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 12 to the adjusted value of the mask
			// making the last 4 bits of the mask 1100
			*puiMask += 12;
		}
		// if the current character in the string is a D, 13
		else if ((szMask[i] == 'd') || (szMask[i] == 'D'))
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 13 to the adjusted value of the mask
			// making the last 4 bits of the mask 1101
			*puiMask += 13;
		}
		// if the current character in the string is a E, 14
		else if ((szMask[i] == 'e') || (szMask[i] == 'E')) // advc.001: first one was 'd'
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 14 to the adjusted value of the mask
			// making the last 4 bits of the mask 1110
			*puiMask += 14;
		}
		// if the current character in the string is a F, 15
		else if ((szMask[i] == 'f') || (szMask[i] == 'F'))
		{
			// shift the current value of the mask to the left by 4 bits
			*puiMask <<= 4;
			// add 15 to the adjusted value of the mask
			// making the last 4 bits of the mask 1111
			*puiMask += 15;
		}
	}
}
#endif

/*  Goes through the XML tree until reaching a non-comment node.
	Returns false if it can't find one. */
bool CvXMLLoadUtility::SkipToNextVal()
{
	// we will loop through and skip over any comment nodes
	while (gDLL->getXMLIFace()->IsLastLocatedNodeCommentNode(m_pFXml))
	{
		// if we cannot set the current xml node to it's next sibling then we will break out of the for loop
		// otherwise we will continue looping
		if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
			return false; // couldn't find any non-comment nodes
	}
	return true;
}

/*	advc: Looks up szType in the global list of info enum types.
	Misleading comments deleted. Just think of this as a wrapper for
	CvGlobals::getInfoTypeForString with additional error output.) */
int CvXMLLoadUtility::FindInInfoClass(const TCHAR* szType, bool hideAssert)
{
	int iR = GC.getInfoTypeForString(szType, hideAssert);
	if (iR >= 0)
		return iR;
	if (!hideAssert)
		handleUnknownTypeString(szType); // advc: Moved into subroutine
	return iR;
}

/*	advc: Info enum, global type or even a non-enum id associated with a
	CvInfo object. To simplify SetVariableListTagPair. */
int CvXMLLoadUtility::getGlobalEnumFromString(TCHAR const* szType)
{
	int iR = GC.getTypesEnum(szType, true);
	if (iR < 0)
		iR = GC.getInfoTypeForString(szType, true);
	if (iR < 0)
		handleUnknownTypeString(szType);
	return iR;
}

// advc: Cut from FindInInfoClass
void CvXMLLoadUtility::handleUnknownTypeString(TCHAR const* szType)
{
	if (_tcscmp(szType, "NONE") != 0 && _tcscmp(szType, "") != 0)
	{
		char errorMsg[1024];
		sprintf(errorMsg, "Tag: %s in Info class was incorrect \n Current XML file is: %s", szType, GC.getCurrentXMLFile().GetCString());
		errorMessage(errorMsg);
	}
}

/*  Loads an XML file into the FXml variable. The szFilename parameter has the
	m_szXmlPath member variable pre-pended to it to form the full pathname.
	Gets the full pathname for the XML file from the FileManager.
	If successful, we return true from the function and set pFXml to a
	valid FXml pointer. */ // (advc: Comment from header file merged in)
bool CvXMLLoadUtility::LoadCivXml(FXml* pFXml, const TCHAR* szFilename)
{
	char szLog[256];
	sprintf(szLog, "LoadCivXml (%s)", szFilename);
	PROFILE(szLog);
	OutputDebugString(szLog);
	OutputDebugString("\n");
	// advc.wine: (printToConsole can't handle a char[])
	printf("LoadCivXml (%s)\n", szFilename);

	CvString szPath = szFilename;
	if (!gDLL->fileManagerEnabled())
		szPath = "Assets//" + szPath;
	logMsg("Loading XML file %s\n", szPath.c_str());
	if (!gDLL->getXMLIFace()->LoadXml(pFXml, szPath))
	{
		logMsg("Load XML file %s FAILED\n", szPath.c_str());
		return false;
	}
	logMsg("Load XML file %s SUCCEEDED\n", szPath.c_str());
	CvGlobals::getInstance().setCurrentXMLFile(szFilename);
	return true; // success
}

/*	Sets the number of strings in a list, initializes the string to the correct length,
	and fills it from the current XML file. Assumes that the current node is
	the parent node of the string list children. */
bool CvXMLLoadUtility::SetStringList(CvString** ppszStringArray, int* piSize)
{
	FAssertMsg(*ppszStringArray == NULL, "Possible memory leak");
	*piSize = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
	*ppszStringArray = NULL;
	if (*piSize > 0)
	{
		*ppszStringArray = new CvString[*piSize];
		CvString* pszStringArray = *ppszStringArray;
		if (GetChildXmlVal(pszStringArray[0]))
		{
			for (int i = 1; i < *piSize; i++)
			{
				if (!GetNextXmlVal(pszStringArray[i]))
					break;
			}
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
	}
	return true;
}

// call the progress updater fxn if it exists
void CvXMLLoadUtility::UpdateProgressCB(const char* szMessage)
{
	/*	advc.003k: RegisterProgressCB is never called, so m_pCBFxn is alway NULL.
		The memory previously allocated for m_iCurProgressStep has been repurposed;
		see comments in header. */
	/*if (m_iCurProgressStep > GetNumProgressSteps())
		m_iCurProgressStep = 1; // wrap
	if (m_pCBFxn != NULL) {
		m_pCBFxn(++m_iCurProgressStep, GetNumProgressSteps(), CvString::format(
				"Reading XML %s", szMessage ? szMessage : "").c_str());
	}*/
}

// for fast lookup of children by name
void CvXMLLoadUtility::MapChildren()
{
	gDLL->getXMLIFace()->MapChildren(m_pFXml);
}
