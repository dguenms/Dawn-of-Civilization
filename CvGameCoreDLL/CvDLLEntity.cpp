#include "CvGameCoreDLL.h"
#include "CvDLLEntity.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvGlobals.h"

CvDLLEntity::CvDLLEntity() : m_pEntity(NULL)
{

}

CvDLLEntity::~CvDLLEntity()
{

}

void CvDLLEntity::removeEntity()
{
	gDLL->getEntityIFace()->removeEntity(getEntity());
}

void CvDLLEntity::setup()
{
	gDLL->getEntityIFace()->setup(getEntity());
}

void CvDLLEntity::setVisible(bool bVis)
{
	gDLL->getEntityIFace()->setVisible(getEntity(), bVis);
}

void CvDLLEntity::createCityEntity(CvCity* pCity)
{
	gDLL->getEntityIFace()->createCityEntity(pCity);
}

void CvDLLEntity::createUnitEntity(CvUnit* pUnit)
{
	gDLL->getEntityIFace()->createUnitEntity(pUnit);
}

void CvDLLEntity::destroyEntity()
{
	gDLL->getEntityIFace()->destroyEntity(m_pEntity);
}

bool CvDLLEntity::IsSelected() const
{
	return gDLL->getEntityIFace()->IsSelected(getEntity());
}

void CvDLLEntity::PlayAnimation(AnimationTypes eAnim, float fSpeed, bool bQueue, int iLayer, float fStartPct, float fEndPct)
{
	gDLL->getEntityIFace()->PlayAnimation(getEntity(), eAnim, fSpeed, bQueue, iLayer, fStartPct, fEndPct);
}

void CvDLLEntity::StopAnimation(AnimationTypes eAnim)
{
	gDLL->getEntityIFace()->StopAnimation(getEntity(), eAnim);
}

void CvDLLEntity::MoveTo( const CvPlot * pkPlot )
{
	gDLL->getEntityIFace()->MoveTo(getUnitEntity(), pkPlot );
}

void CvDLLEntity::QueueMove( const CvPlot * pkPlot )
{
	gDLL->getEntityIFace()->QueueMove(getUnitEntity(), pkPlot );
}

void CvDLLEntity::ExecuteMove( float fTimeToExecute, bool bCombat )
{
	gDLL->getEntityIFace()->ExecuteMove(getUnitEntity(), fTimeToExecute, bCombat );
}

void CvDLLEntity::SetPosition( const CvPlot * pkPlot )
{
	gDLL->getEntityIFace()->SetPosition(getUnitEntity(), pkPlot );
}

void CvDLLEntity::NotifyEntity( MissionTypes eMission )
{
	gDLL->getEntityIFace()->NotifyEntity( getUnitEntity(), eMission );
}

void CvDLLEntity::SetSiegeTower(bool show)
{
	gDLL->getEntityIFace()->SetSiegeTower( getUnitEntity(), show );
}

bool CvDLLEntity::GetSiegeTower()
{
	return gDLL->getEntityIFace()->GetSiegeTower(getUnitEntity());
}
