#pragma once

// gameAI.h

#ifndef CIV4_GAME_AI_H
#define CIV4_GAME_AI_H

#include "CvGame.h"

class CvGameAI : public CvGame
{

public:

  CvGameAI();
  virtual ~CvGameAI();

  void AI_init();
  void AI_uninit();
	void AI_reset();

	void AI_makeAssignWorkDirty();
	void AI_updateAssignWork();

	int AI_combatValue(UnitTypes eUnit);

	int AI_turnsPercent(int iTurns, int iPercent);

	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

protected:

  int m_iPad;

};

#endif
