#pragma once

#ifndef CvDLLEntity_h
#define CvDLLEntity_h

// Class which represents an entity object in the DLL.
// Implements common entity functions by making calls to CvDLLEntityIFaceBase

// [advc: These are instructions for devs with access to the full source]
// To expose new entity functions:
// 1. Add the pure virtual function prototype to CvDLLEntityIFaceBase.h
// 2. Add the function prototype and implementation to CvDLLEntityIFace.[cpp,h]
// 3. Add a wrapper function (for convenience) to this file and implement it in the corresponding cpp

/*	advc (note): These three are defined in the EXE.
	CvFlagEntity and CvSymbol are apparently also derived from CvEntity. */
class CvEntity;
class CvCityEntity;
class CvUnitEntity;

class CvCity;
class CvUnit;

class CvPlot;


class CvDLLEntity /* advc.003e: */ : private boost::noncopyable
{
public:
	CvDLLEntity() : m_pEntity(NULL) {}
	virtual ~CvDLLEntity() {}

	virtual void setup();
	
	void destroyEntity();
	void removeEntity();
	void setVisible(bool b);
	void setEntity(CvEntity* pEntity);

	DllExport bool IsSelected() const
	{
		return gDLL->getEntityIFace()->IsSelected(getGenericEntity());
	}

	void PlayAnimation(AnimationTypes eAnim, float fSpeed = 1.0f, bool bQueue = false,
			int iLayer = 0, float fStartPct = 0.0f, float fEndPct = 1.0f);
	void StopAnimation(AnimationTypes eAnim);

protected:
	CvEntity* m_pEntity;
// <advc>
	CvEntity* getGenericEntity() { return m_pEntity; }
	CvEntity const* getGenericEntity() const { return m_pEntity; }
};

/*	Derived classes for more type safety and shorter function names. Without definitions
	of the classes derived from CvEntity (in the EXE), the compiler can't know
	that they're related; so reinterpret casts have to occur at some point. */

class CvDLLCityEntity : public CvDLLEntity
{
public:
	void createEntity(CvCity* pCity);
	CvCityEntity* getEntity() { return reinterpret_cast<CvCityEntity*>(m_pEntity); }
	CvCityEntity const* getEntity() const { return reinterpret_cast<CvCityEntity*>(m_pEntity); }
};

class CvDLLUnitEntity : public CvDLLEntity
{
public:
	void createEntity(CvUnit* pUnit);
	CvUnitEntity* getEntity() { return reinterpret_cast<CvUnitEntity*>(m_pEntity); }
	CvUnitEntity const* getEntity() const { return reinterpret_cast<CvUnitEntity*>(m_pEntity); }

	void MoveTo(CvPlot const* pPlot);
	void QueueMove(CvPlot const* pPlot);
	void ExecuteMove(float fTimeToExecute, bool bCombat);
	void SetPosition(CvPlot const* pPlot);
	void NotifyEntity(MissionTypes eMission);
	void SetSiegeTower(bool bShow);
	bool GetSiegeTower();
}; // </advc>

#endif
