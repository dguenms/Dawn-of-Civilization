#pragma once

#ifndef CvDLLSymbolIFaceBase_h
#define CvDLLSymbolIFaceBase_h

//#include "CvEnums.h"
#include "CvDLLUtilityIFaceBase.h"
#include "CvGlobals.h"	// for gDLL

//
// abstract interface for CvSymbol functions used by DLL
//

class CvSymbol;
class CvPlot;
class CvRoute;
class CvFeature;
class CvRiver;
class CvDLLSymbolIFaceBase
{
public:
	virtual void init(CvSymbol* , int iID, int iOffset, int iType, CvPlot* pPlot) = 0;
	virtual CvSymbol* createSymbol() = 0;
	virtual void destroy(CvSymbol*&, bool bSafeDelete=true ) = 0;
	virtual void setAlpha(CvSymbol*, float fAlpha) = 0;
	virtual void setScale(CvSymbol*, float fScale) = 0;
	virtual void Hide(CvSymbol*, bool bHide) = 0;
	virtual bool IsHidden(CvSymbol*) = 0;
	virtual void updatePosition(CvSymbol*) = 0;
	virtual int getID(CvSymbol*) = 0;	
	virtual SymbolTypes getSymbol(CvSymbol* pSym) = 0;
	virtual void setTypeYield(CvSymbol *, int iType, int count) =0;
};

class CvDLLFeatureIFaceBase
{
public:
	virtual CvFeature* createFeature() = 0;
	virtual void init(CvFeature*, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;
	virtual FeatureTypes getFeature(CvFeature* pObj) = 0;
	virtual void setDummyVisibility(CvFeature *feature, const char *dummyTag, bool show) = 0;
	virtual void addDummyModel(CvFeature *feature, const char *dummyTag, const char *modelTag) = 0;
	virtual void setDummyTexture(CvFeature *feature, const char *dummyTag, const char *textureTag) = 0;
	virtual CvString pickDummyTag(CvFeature *feature, int mouseX, int mouseY) = 0;
	virtual void resetModel(CvFeature *feature) = 0;

	// derived methods
	virtual void destroy(CvFeature*& pObj, bool bSafeDelete=true) { gDLL->getSymbolIFace()->destroy((CvSymbol*&)pObj, bSafeDelete); }
	virtual void Hide(CvFeature* pObj, bool bHide) { gDLL->getSymbolIFace()->Hide((CvSymbol*)pObj, bHide); }
	virtual bool IsHidden(CvFeature* pObj) { return gDLL->getSymbolIFace()->IsHidden((CvSymbol*)pObj); }
	virtual void updatePosition(CvFeature* pObj) { gDLL->getSymbolIFace()->updatePosition((CvSymbol*)pObj); }
};

class CvDLLRouteIFaceBase
{
public:
	virtual CvRoute* createRoute() = 0;
	virtual void init(CvRoute*, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;
	virtual RouteTypes getRoute(CvRoute* pObj) = 0;

	// derived methods
	virtual void destroy(CvRoute*& pObj, bool bSafeDelete=true) { gDLL->getSymbolIFace()->destroy((CvSymbol*&)pObj, bSafeDelete); }
	virtual void Hide(CvRoute* pObj, bool bHide) { gDLL->getSymbolIFace()->Hide((CvSymbol*)pObj, bHide); }
	virtual bool IsHidden(CvRoute* pObj) { return gDLL->getSymbolIFace()->IsHidden((CvSymbol*)pObj); }
	virtual void updatePosition(CvRoute* pObj) { gDLL->getSymbolIFace()->updatePosition((CvSymbol*)pObj); }
	virtual int getConnectionMask(CvRoute* pObj) = 0;
	virtual void updateGraphicEra(CvRoute *pObj) = 0;
};

class CvDLLRiverIFaceBase
{
public:
	virtual CvRiver* createRiver() = 0;
	virtual void init(CvRiver*, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;

	// derived methods
	virtual void destroy(CvRiver*& pObj, bool bSafeDelete=true) { gDLL->getRouteIFace()->destroy((CvRoute*&)pObj, bSafeDelete); }
	virtual void Hide(CvRiver* pObj, bool bHide) { gDLL->getRouteIFace()->Hide((CvRoute*)pObj, bHide); }
	virtual bool IsHidden(CvRiver* pObj) { return gDLL->getRouteIFace()->IsHidden((CvRoute*)pObj); }
	virtual void updatePosition(CvRiver* pObj) { gDLL->getRouteIFace()->updatePosition((CvRoute*)pObj); }
};

#endif	// CvDLLSymbolIFaceBase_h
