#pragma once

#ifndef CvDLLEntityIFaceBase_h
#define CvDLLEntityIFaceBase_h

//#pragma warning(disable:100) // advc.make: Moved to PragmaWarnings.h


// abstract class containing entity-related functions that the DLL needs

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
	virtual void removeEntity(CvEntity*) { FErrorMsg("can't get here"); }
	virtual void addEntity(CvEntity*, uint uiEntAddFlags) { FErrorMsg("can't get here"); }
	virtual void setup(CvEntity*) { FErrorMsg("can't get here"); }
	virtual void setVisible(CvEntity*, bool) { FErrorMsg("can't get here"); }
	virtual void createCityEntity(CvCity*) { FErrorMsg("can't get here"); }
	virtual void createUnitEntity(CvUnit*) { FErrorMsg("can't get here"); }
	virtual void destroyEntity(CvEntity*&, bool bSafeDelete=true) { FErrorMsg("can't get here"); }
	virtual void updatePosition(CvEntity* pGameEntity) { FErrorMsg("can't get here"); }
	virtual void setupFloodPlains(CvRiver* pRiver) { FErrorMsg("can't get here"); }

	virtual bool IsSelected(const CvEntity*) const { return false; }
	virtual void PlayAnimation(CvEntity*, AnimationTypes eAnim, float fSpeed = 1.0f, bool bQueue = false,
			int iLayer = 0, float fStartPct = 0.0f, float fEndPct = 1.0f) { FErrorMsg("can't get here"); }
	virtual void StopAnimation(CvEntity*, AnimationTypes eAnim) { FErrorMsg("can't get here"); }
	virtual void StopAnimation(CvEntity *) { FErrorMsg("can't get here");}
	virtual void NotifyEntity(CvUnitEntity*, MissionTypes eMission) { FErrorMsg("can't get here"); }
	virtual void MoveTo(CvUnitEntity*, CvPlot const* pkPlot) { FErrorMsg("can't get here"); }
	virtual void QueueMove(CvUnitEntity*, CvPlot const* pkPlot) { FErrorMsg("can't get here"); }
	virtual void ExecuteMove(CvUnitEntity*, float fTimeToExecute, bool bCombat) { FErrorMsg("can't get here"); }
	virtual void SetPosition(CvUnitEntity* pEntity, CvPlot const* pkPlot) { FErrorMsg("can't get here"); }
	virtual void AddMission(CvMissionDefinition const* pDefinition) { FErrorMsg("can't get here"); };
	virtual void RemoveUnitFromBattle(CvUnit* pUnit) { FErrorMsg("can't get here"); };
	virtual void showPromotionGlow(CvUnitEntity* pEntity, bool bShow) { FErrorMsg("can't get here"); };
	virtual void updateEnemyGlow(CvUnitEntity* pEntity) { FErrorMsg("can't get here"); };
	virtual void updatePromotionLayers(CvUnitEntity* pEntity) { FErrorMsg("can't get here"); };
	virtual void updateGraphicEra(CvUnitEntity* pEntity, EraTypes eOldEra = NO_ERA) { FErrorMsg("can't get here"); };
	virtual void SetSiegeTower(CvUnitEntity *pEntity, bool bShow) { FErrorMsg("can't get here"); };
	virtual bool GetSiegeTower(CvUnitEntity *pEntity) { FErrorMsg("can't get here"); return false; };
};

#endif
