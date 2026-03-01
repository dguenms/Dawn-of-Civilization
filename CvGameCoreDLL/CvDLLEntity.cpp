#include "CvGameCoreDLL.h"
#include "CvDLLEntity.h"


void CvDLLEntity::setup()
{
	gDLL->getEntityIFace()->setup(getGenericEntity());
}

void CvDLLEntity::destroyEntity()
{
	gDLL->getEntityIFace()->destroyEntity(m_pEntity);
}

void CvDLLEntity::removeEntity()
{
	gDLL->getEntityIFace()->removeEntity(getGenericEntity());
}

void CvDLLEntity::setVisible(bool b)
{
	gDLL->getEntityIFace()->setVisible(getGenericEntity(), b);
}

void CvDLLEntity::setEntity(CvEntity* pEntity)
{
	m_pEntity = pEntity;
}

void CvDLLEntity::PlayAnimation(AnimationTypes eAnim, float fSpeed, bool bQueue,
	int iLayer, float fStartPct, float fEndPct)
{
	gDLL->getEntityIFace()->PlayAnimation(getGenericEntity(), eAnim, fSpeed, bQueue,
			iLayer, fStartPct, fEndPct);
}

void CvDLLEntity::StopAnimation(AnimationTypes eAnim)
{
	gDLL->getEntityIFace()->StopAnimation(getGenericEntity(), eAnim);
}

void CvDLLCityEntity::createEntity(CvCity* pCity)
{
	gDLL->getEntityIFace()->createCityEntity(pCity);
}

void CvDLLUnitEntity::createEntity(CvUnit* pUnit)
{
	gDLL->getEntityIFace()->createUnitEntity(pUnit);
}

void CvDLLUnitEntity::MoveTo(CvPlot const* pPlot)
{
	gDLL->getEntityIFace()->MoveTo(getEntity(), pPlot);
}

void CvDLLUnitEntity::QueueMove(CvPlot const* pPlot)
{
	gDLL->getEntityIFace()->QueueMove(getEntity(), pPlot);
}

void CvDLLUnitEntity::ExecuteMove(float fTimeToExecute, bool bCombat)
{
	gDLL->getEntityIFace()->ExecuteMove(getEntity(), fTimeToExecute, bCombat);
}

void CvDLLUnitEntity::SetPosition(CvPlot const* pPlot)
{
	gDLL->getEntityIFace()->SetPosition(getEntity(), pPlot);
}

void CvDLLUnitEntity::NotifyEntity(MissionTypes eMission)
{
	gDLL->getEntityIFace()->NotifyEntity(getEntity(), eMission);
}

void CvDLLUnitEntity::SetSiegeTower(bool bShow)
{
	gDLL->getEntityIFace()->SetSiegeTower(getEntity(), bShow);
}

bool CvDLLUnitEntity::GetSiegeTower()
{
	return gDLL->getEntityIFace()->GetSiegeTower(getEntity());
}
