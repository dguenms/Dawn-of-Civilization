/*  <advc.127> Cut and pasted from CvDLLInterfaceIFaceBase.h; this function
	is getting too large for an inline definition. */

#include "CvGameCoreDLL.h"
#include "CvDLLInterfaceIFaceBase.h" // </advc.127>
#include "CvGame.h"
#include "CvPlayer.h"
#include "CvPlot.h"
#include "RiseFall.h" // advc.700

void CvDLLInterfaceIFaceBase::addMessage(PlayerTypes ePlayer, bool bForce,
	int iLength, CvWString szString, LPCTSTR pszSound,
	InterfaceMessageTypes eType, LPCSTR pszIcon, ColorTypes eFlashColor,
	int iFlashX, int iFlashY, bool bShowOffScreenArrows,
	bool bShowOnScreenArrows)
{
	// <advc>
	if (iLength == -1)
		iLength = GC.getEVENT_MESSAGE_TIME();
	// Perhaps the EXE does that anyway; let's make sure.
	if (eFlashColor == NO_COLOR)
		eFlashColor = GC.getColorType("WHITE"); // </advc>
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	// <advc.700>
	bool const bRiseFall = GC.getGame().isOption(GAMEOPTION_RISE_FALL);
	// Adjustments for AI Auto Play
	if (kPlayer.isHumanDisabled()) // Replacing getActivePlayer check
	{
		if (bRiseFall) // Silent AI Auto Play in R&F games
			return; // </advc.700>
		if (eType != MESSAGE_TYPE_MAJOR_EVENT && eType != MESSAGE_TYPE_CHAT && // K-Mod
			eType != MESSAGE_TYPE_MAJOR_EVENT_LOG_ONLY) // advc.106b
		{
			return;
		}
		// <advc.127>
		// Announce immediately; don't wait until the active player's next turn.
		bForce = true;
		// Don't exceed the default display time
		iLength = std::min(iLength, GC.getEVENT_MESSAGE_TIME());
		pszSound = NULL;
		/*	K-Mod had also discarded the "flash" info. That's used for the
			text color and coordinates stored in the Turn Log -- not just
			for the (disabled) icon. */
		// </advc.127>
		pszIcon = NULL;
		bShowOffScreenArrows = bShowOnScreenArrows = false;
	}
	else if (!kPlayer.isHuman() &&
		/*  advc.700: Want message archive to be available when human
			takes over. AI messages expire just like human messages. */
		!(bRiseFall && GC.getGame().getRiseFall().isDeliverMessages(ePlayer)))
	{
		return;
	}
	// <advc.106>
	if (gDLL->getEngineIFace()->isGlobeviewUp())
		bForce = false; // </advc.106>
	addMessageExternal(ePlayer, bForce, iLength, szString,
			pszSound, eType, pszIcon, eFlashColor, iFlashX, iFlashY,
			bShowOffScreenArrows, bShowOnScreenArrows);
}

void CvDLLInterfaceIFaceBase::addMessage(PlayerTypes ePlayer, bool bForce,
	int iLength, CvWString szString, CvPlot const& kPlot,
	LPCTSTR pszSound, InterfaceMessageTypes eType, LPCSTR pszIcon,
	ColorTypes eFlashColor, bool bShowOffScreenArrows, bool bShowOnScreenArrows)
{
	addMessage(ePlayer, bForce, iLength, szString, pszSound, eType, pszIcon,
			eFlashColor, kPlot.getX(), kPlot.getY(),
			bShowOffScreenArrows, bShowOnScreenArrows);
}
