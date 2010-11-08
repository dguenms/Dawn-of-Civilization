#ifndef CV_DLL_TRANSLATOR_H
#define CV_DLL_TRANSLATOR_H

class CvDllTranslator
{
public:
	DllExport static void initializeTags(CvWString& szTagStartIcon, CvWString& szTagStartOur, CvWString& szTagStartCT, CvWString& szTagStartColor, CvWString& szTagStartLink, CvWString& szTagEndLink, CvWString& szEndLinkReplacement, std::map<std::wstring, CvWString>& aIconMap, std::map<std::wstring, CvWString>& aColorMap);
	DllExport static bool replaceOur(const CvWString& szKey, int iForm, CvWString& szReplacement);
	DllExport static bool replaceCt(const CvWString& szKey, int iForm, CvWString& szReplacement);
};

#endif