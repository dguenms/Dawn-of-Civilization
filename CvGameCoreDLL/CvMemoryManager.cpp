#include "CvGameCoreDLL.h"
#include "CvGameCoreDLLUndefNew.h"
#include <new>

// advc.003o: New implementation file. Contents cut from CvGameCoreDLL.cpp.

#ifdef MEMORY_TRACKING
// <advc.003o> Include only conditionally
#include "CvDLLPythonIFaceBase.h"
#include <psapi.h>
#pragma comment(lib, "psapi.lib") // Help the linker find psapi
// </advc.003o>
void	ProfileTrackAlloc(void* ptr);

void	ProfileTrackDeAlloc(void* ptr);

void DumpMemUsage(const char* fn, int line)
{
	PROCESS_MEMORY_COUNTERS pmc;

	if ( GetProcessMemoryInfo( GetCurrentProcess(), &pmc, sizeof(pmc)) )
	{
		char buffer[200];

		sprintf(buffer, "memory (%s,%d): %d Kbytes, peak %d\n", fn, line, (int)(pmc.WorkingSetSize/1024), (int)(pmc.PeakWorkingSetSize/1024));
		OutputDebugString(buffer);
	}
}

#define	PROFILE_TRACK_ALLOC(x)		ProfileTrackAlloc(x);
#define	PROFILE_TRACK_DEALLOC(x)	ProfileTrackDeAlloc(x);
#else
#define	PROFILE_TRACK_ALLOC(x)
#define	PROFILE_TRACK_DEALLOC(x)
#endif

/*  advc.make: For debugging with Visual Leak Detector (if installed). It doesn't
	matter which file includes it. I've put it here with the other memory tracking code.
	Requires a debug build without optimizations (don't know which optimization option
	exactly causes vld to turn itself off). */
//#include <vld.h> 

#ifdef USE_MEMMANAGER // K-Mod. There is a similar #ifdef in the header file, so I assume it's meant to be here as well...
//
// operator global new and delete override for gamecore DLL
//
void *__cdecl operator new(size_t size)
{
	if (gDLL != NULL)
	{
		void* result = NULL;

		try
		{
			result = gDLL->newMem(size, __FILE__, __LINE__);
			/*  advc.make: Don't obscure uninitialized memory by setting _Val=0.
				Adopted from C2C (billw2015). */
			memset(result, 0xDA, size);
			PROFILE_TRACK_ALLOC(result);
		}
		catch(std::exception const&) // advc: Better to catch it by reference
		{
			printToConsole("Allocation failure\n");
		}

		return result;
	}

	//::MessageBoxA(NULL,"Unsafe alloc","CvGameCore",MB_OK); // disabled by K-Mod, for now.
	//printToConsole("Alloc [unsafe]"); // advc.make: Don't need this either, do we?
	return malloc(size);
}

void __cdecl operator delete (void *p)
{
	if (gDLL != NULL)
	{
		PROFILE_TRACK_DEALLOC(p);
		gDLL->delMem(p, __FILE__, __LINE__);
	}
	else free(p);
}

void* operator new[](size_t size)
{
	if (gDLL != NULL)
	{
		//printToConsole("Alloc [safe]");
		void* result = gDLL->newMemArray(size, __FILE__, __LINE__);
		memset(result, 0xDA, size); // advc.make
		return result;
	}

	printToConsole("Alloc [unsafe]");
	::MessageBoxA(NULL,"Unsafe alloc","CvGameCore",MB_OK);
	return malloc(size);
}

void operator delete[](void* pvMem)
{
	if (gDLL != NULL)
		gDLL->delMemArray(pvMem, __FILE__, __LINE__);
	else free(pvMem);
}

void *__cdecl operator new(size_t size, char* pcFile, int iLine)
{
	void* result = gDLL->newMem(size, pcFile, iLine);
	memset(result, 0xDA, size); // advc.make
	return result;
}

void *__cdecl operator new[](size_t size, char* pcFile, int iLine)
{
	FErrorMsg("To check if operator new[](size_t*,char*,int) is ever used"); // advc.test
	//void* result = gDLL->newMem(size, pcFile, iLine);
	// advc.001: Looks like a copy-paste error
	void* result = gDLL->newMemArray(size, pcFile, iLine);
	memset(result, 0xDA, size); // advc.make
	return result;
}

void __cdecl operator delete(void* pvMem, char* pcFile, int iLine)
{
	gDLL->delMem(pvMem, pcFile, iLine);
}

void __cdecl operator delete[](void* pvMem, char* pcFile, int iLine)
{
	FErrorMsg("To check if operator delete[](void*,char*,int) is ever used"); // advc.test
	//gDLL->delMem(pvMem, pcFile, iLine);
	// advc.001: Looks like a copy-paste error
	gDLL->delMemArray(pvMem, pcFile, iLine);
}


void* reallocMem(void* a, unsigned int uiBytes, const char* pcFile, int iLine)
{
	return gDLL->reallocMem(a, uiBytes, pcFile, iLine);
}

unsigned int memSize(void* a)
{
	return gDLL->memSize(a);
}
#endif


#ifdef MEMORY_TRACKING
CMemoryTrack*	CMemoryTrack::trackStack[MAX_TRACK_DEPTH];
int CMemoryTrack::m_trackStackDepth = 0;

CMemoryTrack::CMemoryTrack(const char* name, bool valid)
{
	m_highWater = 0;
	m_name = name;
	m_valid = valid;
	// <advc> Safer to initialize this
	for(int i = 0; i < MAX_TRACKED_ALLOCS; i++)
		m_track[i] = NULL; // </advc>
	if ( m_trackStackDepth < MAX_TRACK_DEPTH )
	{
		trackStack[m_trackStackDepth++] = this;
	}
}

CMemoryTrack::~CMemoryTrack()
{
	if ( m_valid )
	{
		for(int i = 0; i < m_highWater; i++)
		{
			if ( m_track[i] != NULL )
			{
				char buffer[200];

				sprintf(buffer, "Apparent memory leak detected in %s\n", m_name);
				OutputDebugString(buffer);
			}
		}
	}

	if ( trackStack[m_trackStackDepth-1] == this )
	{
		m_trackStackDepth--;
	}
}

void CMemoryTrack::NoteAlloc(void* ptr)
{
	if ( m_valid )
	{
		for(int i = 0; i < m_highWater; i++)
		{
			if ( m_track[i] == NULL )
			{
				break;
			}
		}

		if ( i == m_highWater )
		{
			if ( m_highWater < MAX_TRACKED_ALLOCS )
			{
				m_highWater++;
			}
			else
			{
				m_valid = false;
				return;
			}
		}

		m_track[i] = ptr;
	}
}

void CMemoryTrack::NoteDeAlloc(void* ptr)
{
	if ( m_valid )
	{
		for(int i = 0; i < m_highWater; i++)
		{
			if ( m_track[i] == ptr )
			{
				m_track[i] = NULL;
				break;
			}
		}
	}
}

CMemoryTrack* CMemoryTrack::GetCurrent(void)
{
	if ( 0 < m_trackStackDepth && m_trackStackDepth < MAX_TRACK_DEPTH )
	{
		return trackStack[m_trackStackDepth-1];
	}
	else
	{
		return NULL;
	}
}

CMemoryTrace::CMemoryTrace(const char* name)
{
	PROCESS_MEMORY_COUNTERS pmc;

	GetProcessMemoryInfo( GetCurrentProcess(), &pmc, sizeof(pmc));
	m_name = name;
	m_start = pmc.WorkingSetSize;
}

CMemoryTrace::~CMemoryTrace()
{
	PROCESS_MEMORY_COUNTERS pmc;

	if ( GetProcessMemoryInfo( GetCurrentProcess(), &pmc, sizeof(pmc)) )
	{
		char buffer[200];
		sprintf(buffer, "function %s added %dK bytes, total now %dK\n", m_name, (int)(pmc.WorkingSetSize - m_start)/1024, (int)pmc.WorkingSetSize/1024);
		OutputDebugString(buffer);
	}
}

void ProfileTrackAlloc(void* ptr)
{
	CMemoryTrack* current = CMemoryTrack::GetCurrent();

	if ( current != NULL )
	{
		current->NoteAlloc(ptr);
	}
}

void ProfileTrackDeAlloc(void* ptr)
{
	CMemoryTrack* current = CMemoryTrack::GetCurrent();

	if ( current != NULL )
	{
		current->NoteDeAlloc(ptr);
	}
}

#endif
