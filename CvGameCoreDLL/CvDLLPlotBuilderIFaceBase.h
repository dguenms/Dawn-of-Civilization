#pragma once

#ifndef CvDLLPlotBuilderIFaceBase_h
#define CvDLLPlotBuilderIFaceBase_h

#include "CvDLLEntityIFaceBase.h"
#include "CvDLLUtilityIFaceBase.h"
#include "CvGlobals.h"	// for gDLL

//
// abstract interface for CvPlotBuilder functions used by DLL
//
class CvPlotBuilder;
class CvDLLPlotBuilderIFaceBase : public CvDLLEntityIFaceBase
{
public:
	virtual void init(CvPlotBuilder*, CvPlot*) = 0;
	virtual CvPlotBuilder* create()  = 0;

	// derived methods
	virtual void destroy(CvPlotBuilder*& pPlotBuilder, bool bSafeDelete=true) {
		gDLL->getEntityIFace()->destroyEntity((CvEntity*&)pPlotBuilder, bSafeDelete);
	}
};

#endif	// CvDLLPlotBuilderIFaceBase_h
