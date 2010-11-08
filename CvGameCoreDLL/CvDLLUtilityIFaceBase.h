#pragma once

#ifndef CvDLLUtilityIFaceBase_h
#define CvDLLUtilityIFaceBase_h

//#include "CvEnums.h"
#include "LinkedList.h"

//
// abstract interface for utility functions used by DLL
// Creator- Mustafa Thamer
// Copyright 2005 Firaxis Games
//
class CvDLLEntityIFaceBase;
class CvDLLInterfaceIFaceBase;
class CvDLLEngineIFaceBase;
class CvDLLIniParserIFaceBase;
class CvDLLPlotBuilderIFaceBase;
class CvDLLSymbolIFaceBase;
class CvDLLFeatureIFaceBase;
class CvDLLRouteIFaceBase;
class CvDLLRiverIFaceBase;
class CvDLLFAStarIFaceBase;
class CvDLLEventReporterIFaceBase;
class CvDLLXmlIFaceBase;
class CvDLLFlagEntityIFaceBase;
class CvDLLPythonIFaceBase;

class CvSymbol;
class CvPlot;
class CvUnit;
class CvCity;
class CvCacheObject;
class CvFont;
class CvDiploParameters;
class CvAudioGame;
struct ProfileSample;
class CvReplayInfo;
class CvPopupInfo;
class CvMessageData;

class CvDLLUtilityIFaceBase
{
public:
	// accessors for other abstract interfaces
	virtual CvDLLEntityIFaceBase* getEntityIFace() = 0;
	virtual CvDLLInterfaceIFaceBase* getInterfaceIFace() = 0;
	virtual CvDLLEngineIFaceBase* getEngineIFace() = 0;
	virtual CvDLLIniParserIFaceBase* getIniParserIFace() = 0;
	virtual CvDLLSymbolIFaceBase* getSymbolIFace() = 0;
	virtual CvDLLFeatureIFaceBase* getFeatureIFace() = 0;
	virtual CvDLLRouteIFaceBase* getRouteIFace() = 0;
	virtual CvDLLPlotBuilderIFaceBase* getPlotBuilderIFace() = 0;
	virtual CvDLLRiverIFaceBase* getRiverIFace() = 0;
	virtual CvDLLFAStarIFaceBase* getFAStarIFace() = 0;
	virtual CvDLLXmlIFaceBase* getXMLIFace() = 0;
	virtual CvDLLFlagEntityIFaceBase* getFlagEntityIFace() = 0;
	virtual CvDLLPythonIFaceBase* getPythonIFace() = 0;

	virtual void delMem(void *p) = 0;
	virtual void* newMem(size_t size) = 0;

	virtual void delMem(void *p, const char* pcFile, int iLine) = 0;
	virtual void* newMem(size_t size, const char* pcFile, int iLine) = 0;
 
	virtual void delMemArray(void *p, const char* pcFile, int iLine) = 0;
	virtual void* newMemArray(size_t size, const char* pcFile, int iLine) = 0;

	virtual void* reallocMem(void* a, unsigned int uiBytes, const char* pcFile, int iLine) = 0; 
	virtual unsigned int memSize(void* a) = 0;

	virtual void clearVector(std::vector<int>& vec) = 0;
	virtual void clearVector(std::vector<byte>& vec) = 0;
	virtual void clearVector(std::vector<float>& vec) = 0;

	virtual int getAssignedNetworkID(int iPlayerID) = 0;
	virtual bool isConnected(int iNetID) = 0;
	virtual bool isGameActive() = 0;
	virtual int GetLocalNetworkID() = 0;
	virtual int GetSyncOOS(int iNetID) = 0;
	virtual int GetOptionsOOS(int iNetID) = 0;
	virtual int GetLastPing(int iNetID) = 0;

	virtual bool IsModem() = 0;
	virtual void SetModem(bool bModem) = 0;

	virtual void AcceptBuddy(const char * szName, int iRequestID) = 0;
	virtual void RejectBuddy(const char * szName, int iRequestID) = 0;

	virtual void messageControlLog(char* s) = 0;
	virtual int getChtLvl() = 0;
	virtual void setChtLvl(int iLevel) = 0;
	virtual bool GetWorldBuilderMode() = 0;
	virtual int getCurrentLanguage() const = 0;
	virtual void setCurrentLanguage(int iNewLanguage) = 0;
	virtual bool isModularXMLLoading() const = 0;

	virtual bool IsPitbossHost() const = 0;
	virtual CvString GetPitbossSmtpHost() const = 0;
	virtual CvWString GetPitbossSmtpLogin() const = 0;
	virtual CvWString GetPitbossSmtpPassword() const = 0;
	virtual CvString GetPitbossEmail() const = 0;

	virtual void sendMessageData(CvMessageData* pData) = 0;
	virtual void sendPlayerInfo(PlayerTypes eActivePlayer) = 0;
	virtual void sendGameInfo(const CvWString& szGameName, const CvWString& szAdminPassword) = 0;
	virtual void sendPlayerOption(PlayerOptionTypes eOption, bool bValue) = 0;
	virtual void sendChat(const CvWString& szChatString, ChatTargetTypes eTarget) = 0;
	virtual void sendPause(int iPauseID = -1) = 0;
	virtual void sendMPRetire() = 0;
	virtual void sendToggleTradeMessage(PlayerTypes eWho, TradeableItems eItemType, int iData, int iOtherWho, bool bAIOffer, bool bSendToAll = false) = 0;
	virtual void sendClearTableMessage(PlayerTypes eWhoTradingWith) = 0;
	virtual void sendImplementDealMessage(PlayerTypes eOtherWho, CLinkList<TradeData>* pOurList, CLinkList<TradeData>* pTheirList) = 0;
	virtual void sendContactCiv(NetContactTypes eContactType, PlayerTypes eWho) = 0;
	virtual void sendOffer() = 0;
	virtual void sendDiploEvent(PlayerTypes eWhoTradingWith, DiploEventTypes eDiploEvent, int iData1, int iData2) = 0;
	virtual void sendRenegotiate(PlayerTypes eWhoTradingWith) = 0;
	virtual void sendRenegotiateThisItem(PlayerTypes ePlayer2, TradeableItems eItemType, int iData) = 0;
	virtual void sendExitTrade() = 0;
	virtual void sendKillDeal(int iDealID, bool bFromDiplomacy) = 0;
	virtual void sendDiplomacy(PlayerTypes ePlayer, CvDiploParameters* pParams) = 0;
	virtual void sendPopup(PlayerTypes ePlayer, CvPopupInfo* pInfo) = 0;

	virtual int getMillisecsPerTurn() = 0;
	virtual float getSecsPerTurn() = 0;
	virtual int getTurnsPerSecond() = 0;
	virtual int getTurnsPerMinute() = 0;

	virtual void openSlot(PlayerTypes eID) = 0;
	virtual void closeSlot(PlayerTypes eID) = 0;

	virtual CvWString getMapScriptName() = 0;
	virtual bool getTransferredMap() = 0;
	virtual bool isDescFileName(const char * szFileName) = 0;
	virtual bool isWBMapScript() = 0;
	virtual bool isWBMapNoPlayers() = 0;
	virtual bool pythonMapExists(const char * szMapName) = 0;

	virtual void stripSpecialCharacters(CvWString& szName) = 0;

	virtual void initGlobals() = 0;
	virtual void uninitGlobals() = 0;

	virtual void callUpdater() = 0;

	virtual bool Uncompress(byte** bufIn, unsigned long* bufLenIn, unsigned long maxBufLenOut, int offset=0) = 0;
	virtual bool Compress(byte** bufIn, unsigned long* bufLenIn, int offset=0) = 0;

	virtual void NiTextOut(const TCHAR* szText) = 0;
	virtual void MessageBox(const TCHAR* szText, const TCHAR* szCaption) = 0;
	virtual void SetDone(bool bDone) = 0;
	virtual bool GetDone() = 0;
	virtual bool GetAutorun() = 0;

	virtual void beginDiplomacy(CvDiploParameters* pDiploParams, PlayerTypes ePlayer) = 0;
	virtual void endDiplomacy() = 0;
	virtual bool isDiplomacy() = 0;
	virtual int getDiplomacyPlayer() = 0;
	virtual void updateDiplomacyAttitude(bool bForce = false) = 0;
	virtual bool isMPDiplomacy() = 0;
	virtual bool isMPDiplomacyScreenUp() = 0;
	virtual int getMPDiplomacyPlayer() = 0;
	virtual void beginMPDiplomacy( PlayerTypes eWhoTalkingTo, bool bRenegotiate = false, bool bSimultaneous = true) = 0;
	virtual void endMPDiplomacy() = 0;

	virtual bool getAudioDisabled() = 0;
	virtual int getAudioTagIndex(const TCHAR* szTag, int iScriptType = -1) = 0;

	virtual void DoSound( int iScriptId ) = 0;
	virtual void Do3DSound( int iScriptId, NiPoint3 vPosition ) = 0;

	virtual FDataStreamBase* createFileStream() = 0;
	virtual void destroyDataStream(FDataStreamBase*& stream) = 0;

	virtual CvCacheObject* createGlobalTextCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createGlobalDefinesCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createTechInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createBuildingInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createUnitInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createLeaderHeadInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createCivilizationInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createPromotionInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createDiplomacyInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createEventInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createEventTriggerInfoCacheObject(const TCHAR* szCacheFileName) = 0;

	virtual CvCacheObject* createCivicInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createHandicapInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createBonusInfoCacheObject(const TCHAR* szCacheFileName) = 0;
	virtual CvCacheObject* createImprovementInfoCacheObject(const TCHAR* szCacheFileName) = 0;

	virtual bool cacheRead(CvCacheObject* pCache, const TCHAR* szSourceFileName=NULL) = 0;
	virtual bool cacheWrite(CvCacheObject* pCache) = 0;
	virtual void destroyCache(CvCacheObject*& pCache) = 0;

	virtual bool fileManagerEnabled() = 0;

	virtual void logMsg(const TCHAR* pLogFileName, const TCHAR* pBuf, bool bWriteToConsole=false, bool bTimeStamp=true) = 0;
	virtual void logMemState(const char* msg) = 0;

	virtual int getSymbolID(int iID) = 0;
	virtual void setSymbolID(int iID, int iValue) = 0;

	virtual CvWString getText(CvWString szIDTag, ...) = 0;
	virtual CvWString getObjectText(CvWString szIDTag, uint uiForm, bool bNoSubs = false) = 0;
	virtual void addText(const TCHAR* szIDTag, const wchar* szString, const wchar* szGender = L"N", const wchar* szPlural = L"false") = 0;		
	virtual uint getNumForms(CvWString szIDTag) = 0;

	virtual WorldSizeTypes getWorldSize() = 0;
	virtual uint getFrameCounter() const = 0;

	virtual bool altKey() = 0;
	virtual bool shiftKey() = 0;
	virtual bool ctrlKey() = 0;
	virtual bool scrollLock() = 0;
	virtual bool capsLock() = 0;
	virtual bool numLock() = 0;

	virtual void ProfilerBegin()=0;
	virtual void ProfilerEnd()=0;
	virtual void BeginSample(ProfileSample *pSample)=0;
	virtual void EndSample(ProfileSample *pSample)=0;
	virtual bool isGameInitializing() = 0;

	virtual void enumerateFiles(std::vector<CvString>& files, const char* szPattern) = 0;
	virtual void enumerateModuleFiles(std::vector<CvString>& aszFiles, const CvString& refcstrRootDirectory,	const CvString&	refcstrModularDirectory, const CvString& refcstrExtension, bool bSearchSubdirectories) = 0;

	virtual void SaveGame(SaveGameTypes eSaveGame) = 0;
	virtual void LoadGame() = 0;
	virtual int loadReplays(std::vector<CvReplayInfo*>& listReplays) = 0;
	virtual void QuickSave() = 0;
	virtual void QuickLoad() = 0;
	virtual void sendPbemTurn(PlayerTypes ePlayer) = 0;
	virtual void getPassword(PlayerTypes ePlayer) = 0;

	virtual bool getGraphicOption(GraphicOptionTypes eGraphicOption) = 0;
	virtual bool getPlayerOption(PlayerOptionTypes ePlayerOption) = 0;
	virtual int getMainMenu() = 0;
	
	virtual bool isFMPMgrHost() = 0;
	virtual bool isFMPMgrPublic() = 0;
	virtual void handleRetirement(PlayerTypes ePlayer) = 0;
	virtual PlayerTypes getFirstBadConnection() = 0;
	virtual int getConnState(PlayerTypes ePlayer) = 0;

	virtual bool ChangeINIKeyValue(const char* szGroupKey, const char* szKeyValue, const char* szOut) = 0;

	virtual char* md5String(char* szString) = 0;

	virtual const char* getModName(bool bFullPath = true) const = 0;
	virtual bool hasSkippedSaveChecksum() const = 0;
	virtual void reportStatistics() = 0;
};

#endif	// CvDLLUtilityIFaceBase_h
