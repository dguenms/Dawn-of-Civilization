#pragma once

#ifndef CvDLLEntityIFaceBase_h
#define CvDLLEntityIFaceBase_h

#pragma warning(disable:4100) 

//#include "CvEnums.h"

//
// abstract class containing entity-related functions that the DLL needs
//
class CvEntity;
class CvUnitEntity;
class CvCity;
class CvUnit;
class CvMissionDefinition;
class CvPlot;
class CvRiver;

class CvDLLEntityIFaceBase
{
public:
	virtual void removeEntity(CvEntity*)  { FAssertMsg(false, "can't get here"); }
	virtual void addEntity(CvEntity*, uint uiEntAddFlags)  { FAssertMsg(false, "can't get here"); }
	virtual void setup(CvEntity*)  { FAssertMsg(false, "can't get here"); }
	virtual void setVisible(CvEntity*, bool)  { FAssertMsg(false, "can't get here"); }
	virtual void createCityEntity(CvCity*)  { FAssertMsg(false, "can't get here"); }
	virtual void createUnitEntity(CvUnit*)  { FAssertMsg(false, "can't get here"); }
	virtual void destroyEntity(CvEntity*&, bool bSafeDelete=true)  { FAssertMsg(false, "can't get here"); }
	virtual void updatePosition(CvEntity *gameEntity)  { FAssertMsg(false, "can't get here"); }
	virtual void setupFloodPlains(CvRiver *river) { FAssertMsg(false, "can't get here"); }

	virtual bool IsSelected(const CvEntity*)  const { return false; }
	virtual void PlayAnimation(CvEntity*, AnimationTypes eAnim, float fSpeed = 1.0f, bool bQueue = false, int iLayer = 0, float fStartPct = 0.0f, float fEndPct = 1.0f)  { FAssertMsg(false, "can't get here"); }
	virtual void StopAnimation(CvEntity*, AnimationTypes eAnim)  { FAssertMsg(false, "can't get here"); }
	virtual void StopAnimation(CvEntity * ) { FAssertMsg(false, "can't get here");}
	virtual void NotifyEntity(CvUnitEntity*, MissionTypes eMission) { FAssertMsg( false, "can't get here"); }
	virtual void MoveTo(CvUnitEntity*, const CvPlot * pkPlot )  { FAssertMsg(false, "can't get here"); }
	virtual void QueueMove(CvUnitEntity*, const CvPlot * pkPlot )  { FAssertMsg(false, "can't get here"); }
	virtual void ExecuteMove(CvUnitEntity*, float fTimeToExecute, bool bCombat )  { FAssertMsg(false, "can't get here"); }
	virtual void SetPosition(CvUnitEntity* pEntity, const CvPlot * pkPlot )  { FAssertMsg(false, "can't get here"); }
	virtual void AddMission(const CvMissionDefinition* pDefinition) { FAssertMsg(false, "can't get here"); };
	virtual void RemoveUnitFromBattle(CvUnit* pUnit) { FAssertMsg(false, "can't get here"); };
	virtual void showPromotionGlow(CvUnitEntity* pEntity, bool show) { FAssertMsg(false, "can't get here"); };
	virtual void updateEnemyGlow(CvUnitEntity* pEntity) { FAssertMsg(false, "can't get here"); };
	virtual void updatePromotionLayers(CvUnitEntity* pEntity) { FAssertMsg(false, "can't get here"); };
	virtual void updateGraphicEra(CvUnitEntity* pEntity, EraTypes eOldEra = NO_ERA) { FAssertMsg(false, "can't get here"); };
	virtual void SetSiegeTower(CvUnitEntity *pEntity, bool show) { FAssertMsg(false, "can't get here"); };
	virtual bool GetSiegeTower(CvUnitEntity *pEntity) { FAssertMsg(false, "can't get here"); return false; };
};

#endif	// CvDLLEntityIFaceBase_h
