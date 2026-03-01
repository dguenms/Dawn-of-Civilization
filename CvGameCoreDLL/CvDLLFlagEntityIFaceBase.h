/*	$Header: //depot/main/Civilization4/CvGameCoreDLL/CvDLLFlagEntityIFaceBase.h#3 $
	***************** CIV4 GAME ENGINE   ********************
	author: Bart Muzzin -- 4-12-2005
	DLL Stub interface for CvFlagEntity
	Copyright (c) 2005 Firaxis Games, Inc. All rights reserved. */

#pragma once
#ifndef CvDLLFlagEntityIFaceBase_H
#define CvDLLFlagEntityIFaceBase_H

#include "CvDLLEntityIFaceBase.h"

class CvPlot;
class CvFlagEntity;


// abstract interface for CvFlagEntity functions used by DLL
class CvDLLFlagEntityIFaceBase : public CvDLLEntityIFaceBase
{
	public:

		virtual CvFlagEntity* create(PlayerTypes ePlayer) = 0;

		virtual PlayerTypes getPlayer(CvFlagEntity* pFlag) const = 0;
		virtual CvPlot* getPlot(CvFlagEntity* pFlag) const = 0;
		virtual void setPlot(CvFlagEntity* pkFlag, CvPlot* pPlot, bool bOffset) = 0;
		virtual void updateUnitInfo(CvFlagEntity* pFlag, CvPlot const* pkPlot, bool bOffset) = 0;
		virtual void updateGraphicEra(CvFlagEntity* pFlag) = 0;
		virtual void setVisible(CvFlagEntity* pEnt, bool bVis)
		{	/*	advc (note): Without the CvFlagEntity definition, the compiler can't know
				that it's derived from CvEntity. */
			gDLL->getEntityIFace()->setVisible(reinterpret_cast<CvEntity*>(pEnt), bVis);
		}
		virtual void destroy(CvFlagEntity*& pImp, bool bSafeDelete=true) = 0;
};

#endif
