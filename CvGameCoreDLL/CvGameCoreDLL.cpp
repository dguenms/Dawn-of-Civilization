#include "CvGameCoreDLL.h"

/*  advc.003o: Profiling code moved to FProfiler.cpp. Memory tracking/ profiling
	moved to CvMemoryManager.cpp. Changes to CvGameCoreDLL.cpp cause the
	precompiled header to be rebuilt. That may also desirable for the profiling
	and memory management code, but I still don't want it all in one file. */

BOOL APIENTRY DllMain(HANDLE hModule,
					  DWORD  ul_reason_for_call,
					  LPVOID lpReserved)
{
	switch( ul_reason_for_call ) {
	case DLL_PROCESS_ATTACH:
		{
		// The DLL is being loaded into the virtual address space of the current process as a result of the process starting up
		printToConsole("DLL_PROCESS_ATTACH\n");

		// set timer precision
		#ifdef FASSERT_ENABLE // advc.make (avoid warning about unused var)
		MMRESULT iTimeSet =
		#endif
		timeBeginPeriod(1);		// set timeGetTime and sleep resolution to 1 ms, otherwise it's 10-16ms
		FAssertMsg(iTimeSet==TIMERR_NOERROR, "failed setting timer resolution to 1 ms");
		}
		break;
	case DLL_THREAD_ATTACH:
		// printToConsole("DLL_THREAD_ATTACH\n");
		break;
	case DLL_THREAD_DETACH:
		// printToConsole("DLL_THREAD_DETACH\n");
		break;
	case DLL_PROCESS_DETACH:

		printToConsole("DLL_PROCESS_DETACH\n");
		timeEndPeriod(1);
		break;
	}

	return TRUE;	// success
}
