#pragma once

#ifndef CvDLLSymbolIFaceBase_h
#define CvDLLSymbolIFaceBase_h

// abstract interfaces for CvSymbol functions used by DLL

class CvPlot;
/*	advc (note): These are apparently defined in the EXE,
	CvSymbol being the common base class, and CvRiver derived from CvRoute. */
class CvSymbol;
class CvRoute;
class CvFeature;
class CvRiver;

class CvDLLSymbolIFaceBase
{
public:
	virtual void init(CvSymbol*, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;
	virtual CvSymbol* createSymbol() = 0;
	virtual void destroy(CvSymbol*&, bool bSafeDelete = true) = 0;
	virtual void setAlpha(CvSymbol*, float fAlpha) = 0;
	virtual void setScale(CvSymbol*, float fScale) = 0;
	virtual void Hide(CvSymbol*, bool bHide) = 0;
	virtual bool IsHidden(CvSymbol*) = 0;
	virtual void updatePosition(CvSymbol*) = 0;
	virtual int getID(CvSymbol*) = 0;
	virtual SymbolTypes getSymbol(CvSymbol* pSym) = 0;
	virtual void setTypeYield(CvSymbol *, int iType, int count) = 0;
};

class CvDLLFeatureIFaceBase
{
public:
	virtual CvFeature* createFeature() = 0;
	virtual void init(CvFeature*, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;
	virtual FeatureTypes getFeature(CvFeature* pFeature) = 0;
	virtual void setDummyVisibility(CvFeature* pFeature, char const* szDummyTag, bool bShow) = 0;
	virtual void addDummyModel(CvFeature* pFeature, char const* szDummyTag, char const* szModelTag) = 0;
	virtual void setDummyTexture(CvFeature* pFeature, char const* szDummyTag, char const* textureTag) = 0;
	virtual CvString pickDummyTag(CvFeature* pFeature, int iMouseX, int iMouseY) = 0;
	virtual void resetModel(CvFeature* pFeature) = 0;

	/*	derived methods
		advc (note): I guess they correspond to CvSymbol functions that CvFeature overrides */
	virtual void destroy(CvFeature*& pFeature, bool bSafeDelete = true)
	{
		CvSymbol* pSymbol = base(pFeature); // advc
		gDLL->getSymbolIFace()->destroy(pSymbol, bSafeDelete);
		// <advc> This is apparently the point of the reference to a pointer
		if (pSymbol == NULL)
			pFeature = NULL; // </advc>
	}
	virtual void Hide(CvFeature* pFeature, bool bHide)
	{
		gDLL->getSymbolIFace()->Hide(base(pFeature), bHide);
	}
	virtual bool IsHidden(CvFeature* pFeature)
	{
		return gDLL->getSymbolIFace()->IsHidden(base(pFeature));
	}
	virtual void updatePosition(CvFeature* pFeature)
	{
		gDLL->getSymbolIFace()->updatePosition(base(pFeature));
	}
private:
	// advc: Put the (up-)casts in one place
	static CvSymbol* base(CvFeature* pFeature)
	{
		return reinterpret_cast<CvSymbol*>(pFeature);
	}
};

class CvDLLRouteIFaceBase
{
public:
	virtual CvRoute* createRoute() = 0;
	virtual void init(CvRoute* pRoute, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;
	virtual RouteTypes getRoute(CvRoute* pRoute) = 0;

	// derived methods
	virtual void destroy(CvRoute*& pRoute, bool bSafeDelete = true)
	{
		PROFILE_FUNC(); // advc
		CvSymbol* pSymbol = base(pRoute); // advc
		gDLL->getSymbolIFace()->destroy(pSymbol, bSafeDelete);
		if (pSymbol == NULL) // advc
			pRoute = NULL; // advc>
	}
	virtual void Hide(CvRoute* pRoute, bool bHide)
	{
		gDLL->getSymbolIFace()->Hide(base(pRoute), bHide);
	}
	virtual bool IsHidden(CvRoute* pRoute)
	{
		return gDLL->getSymbolIFace()->IsHidden(base(pRoute));
	}
	virtual void updatePosition(CvRoute* pRoute)
	{
		gDLL->getSymbolIFace()->updatePosition(base(pRoute));
	}
	virtual int getConnectionMask(CvRoute* pRoute) = 0;
	virtual void updateGraphicEra(CvRoute* pRoute) = 0;
	// <advc>
private:
	static CvSymbol* base(CvRoute* pRoute)
	{
		return reinterpret_cast<CvSymbol*>(pRoute);
	} // </advc>
};

class CvDLLRiverIFaceBase
{
public:
	virtual CvRiver* createRiver() = 0;
	virtual void init(CvRiver* pRiver, int iID, int iOffset, int iType, CvPlot* pPlot) = 0;

	// derived methods
	virtual void destroy(CvRiver*& pRiver, bool bSafeDelete=true)
	{
		CvRoute* pRoute = base(pRiver); // advc
		gDLL->getRouteIFace()->destroy(pRoute, bSafeDelete);
		if (pRoute == NULL) // advc
			pRiver = NULL; // advc
	}
	virtual void Hide(CvRiver* pRiver, bool bHide)
	{
		gDLL->getRouteIFace()->Hide(base(pRiver), bHide);
	}
	virtual bool IsHidden(CvRiver* pRiver)
	{
		return gDLL->getRouteIFace()->IsHidden(base(pRiver));
	}
	virtual void updatePosition(CvRiver* pRiver)
	{
		gDLL->getRouteIFace()->updatePosition(base(pRiver));
	}
	// <advc>
private:
	static CvRoute* base(CvRiver* pRiver)
	{
		return reinterpret_cast<CvRoute*>(pRiver);
	} // </advc>
};

#endif
