// advc.plotr: New file; see comment in header.

#include "CvGameCoreDLL.h"
#include "PlotRadiusIterator.h"
#include "CvUnit.h"

// Not in the header b/c CvUnit.h isn't included there
template<bool bINCIRCLE>
CvPlot& SpiralPlotIterator<bINCIRCLE>::getUnitPlot(CvUnit const& kUnit) const
{
	return kUnit.getPlot();
}

// Explicit instantiations (for linker)
template class SpiralPlotIterator<true>;
template class SpiralPlotIterator<false>;
