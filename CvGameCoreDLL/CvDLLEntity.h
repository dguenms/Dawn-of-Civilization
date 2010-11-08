#pragma once

#ifndef CvDLLEntity_h
#define CvDLLEntity_h

//
// Class which represents an entity object in the DLL.
// Implements common entity functions by making calls to CvDLLEntityIFaceBase
//
// To expose new entity functions:
// 1. Add the pure virtual function prototype to CvDLLEntityIFaceBase.h
// 2. Add the function prototype and implementation to CvDLLEntityIFace.[cpp,h]
// 3. Add a wrapper function (for convenience) to this file and implement it in the corresponding cpp
//

//#include "CvEnums.h"

class CvCityEntity;
class CvEntity;
class CvUnitEntity;
class CvCity;
class CvUnit;
class CvPlot;

class DllExport CvDLLEntity
{
public:
	CvDLLEntity();
	virtual ~CvDLLEntity();

	CvEntity* getEntity() { return m_pEntity;	}
	const CvEntity* getEntity() const { return m_pEntity;	}
	CvUnitEntity* getUnitEntity() { return (CvUnitEntity*)m_pEntity;	}
	CvCityEntity* getCityEntity() { return (CvCityEntity*)m_pEntity;	}
	const CvUnitEntity* getUnitEntity() const { return (CvUnitEntity*)m_pEntity;	}
	const CvCityEntity* getCityEntity() const { return (CvCityEntity*)m_pEntity;	}

	void setEntity(CvEntity* pG) { m_pEntity = pG;	}

	void removeEntity();
	virtual void setup();
	void setVisible(bool);
	void createCityEntity(CvCity*);
	void createUnitEntity(CvUnit*);
	void destroyEntity();

	bool IsSelected() const;
	void PlayAnimation(AnimationTypes eAnim, float fSpeed = 1.0f, bool bQueue = false, int iLayer = 0, 
		float fStartPct = 0.0f, float fEndPct = 1.0f);
	void StopAnimation(AnimationTypes eAnim);
	void MoveTo( const CvPlot * pkPlot );
	void QueueMove( const CvPlot * pkPlot );
	void ExecuteMove( float fTimeToExecute, bool bCombat );
	void SetPosition( const CvPlot * pkPlot );
	void NotifyEntity( MissionTypes eMission );
	void SetSiegeTower(bool show);
	bool GetSiegeTower();

protected:
	CvEntity* m_pEntity;
};

#endif	// CvDLLEntity_h
