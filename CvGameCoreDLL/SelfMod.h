// advc.092b: Let's put all self-modifying code in a single place
#pragma once
#ifndef SELF_MOD_H
#define SELF_MOD_H

// Runtime modifications to the native code of Civ4BeyondSword.exe (v3.19)
class Civ4BeyondSwordPatches
{
public:
	void patchPlotIndicatorSize(); // (exposed to Python via CyGameCoreUtils) 
	bool isPlotIndicatorSizePatched() const { return m_bPlotIndicatorSizePatched; }
	Civ4BeyondSwordPatches()
	:	m_bPlotIndicatorSizePatched(false)
	{}

private:
	bool m_bPlotIndicatorSizePatched;
	void showErrorMsgToPlayer(CvWString szMsg);
};

namespace smc
{
	extern Civ4BeyondSwordPatches BtS_EXE;
}

#endif
