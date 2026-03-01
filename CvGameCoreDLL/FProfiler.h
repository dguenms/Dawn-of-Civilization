// ---------------------------------------------------------------------------------------------------
// FProfiler - DLL wrapper to FireEngine/FProfiler.cpp
//
// Author: tomw
//---------------------------------------------------------------------------------------------------------------------

#pragma once

#ifndef	__PROFILE_H__
#define __PROFILE_H__

// <advc.003o> Cut from CvGameCoreDLL.h
void startProfilingDLL(bool longLived);
void stopProfilingDLL(bool longLived);

#ifdef USE_INTERNAL_PROFILER
struct ProfileSample;
void IFPBeginSample(ProfileSample* sample);
void IFPEndSample(ProfileSample* sample);
void dumpProfileStack(void);
void EnableDetailedTrace(bool enable);
#endif // </advc.003o>


#include "CvDLLUtilityIFaceBase.h"
#include "CvGlobals.h"	// for gDLL

// <advc.make> I don't think the internal profiler can work w/o the standard profiler
#ifdef USE_INTERNAL_PROFILER
#define FP_PROFILE_ENABLE
#endif
// </advc.make>

//NOTE: This struct must be identical ot the same struct in  FireEngine/FProfiler.h if the
//standard profiler is being used (USE_INTERNAL_PROFILER not defined)
//---------------------------------------------------------------------------------------------------------------------
struct ProfileSample
{
	ProfileSample(char *name)
	{
		strcpy(Name, name);
		Added=false;
		Parent=-1;
#ifdef USE_INTERNAL_PROFILER
		Id = -1;
#endif
	}

	char	Name[256];						// Name of sample;

	unsigned int	ProfileInstances;		// # of times ProfileBegin Called
	int				OpenProfiles;			// # of time ProfileBegin called w/o ProfileEnd
#ifdef USE_INTERNAL_PROFILER
	LARGE_INTEGER	StartTime;				// The current open profile start time
	LARGE_INTEGER	Accumulator;			// All samples this frame added together

	LARGE_INTEGER	ChildrenSampleTime;		// Time taken by all children
#else
	double			StartTime;				// The current open profile start time
	double			Accumulator;			// All samples this frame added together

	double			ChildrenSampleTime;		// Time taken by all children
#endif
	unsigned int	NumParents;				// Number of profile Parents
	bool			Added;					// true when added to the list
	int				Parent;
#ifdef USE_INTERNAL_PROFILER
	int				Id;
#endif
};

//---------------------------------------------------------------------------------------------------------------------
// Allows us to Profile based on Scope, to limit intrusion into code.
// Simply use PROFLE("funcname") instead having to insert begin()/end() pairing
class CProfileScope
{
public:
	CProfileScope() { bValid= false;};
	CProfileScope(ProfileSample *pSample)
	{
		m_pSample = pSample;
		/*bValid = false;
		if (!giProfilerDisabled)*/
		{
			bValid = true;
#ifdef USE_INTERNAL_PROFILER
			IFPBeginSample(m_pSample);
#else
			gDLL->BeginSample(m_pSample);
#endif
		}
	};
	~CProfileScope()
	{
		if(bValid)
		{
#ifdef USE_INTERNAL_PROFILER
			IFPEndSample(m_pSample);
#else
			gDLL->EndSample(m_pSample);
#endif
			bValid = false;
		}
	};

private:
	bool bValid;
	ProfileSample *m_pSample;
};

//---------------------------------------------------------------------------------------------------------------------

// Main Interface for Profile
#ifdef FP_PROFILE_ENABLE				// Turn Profiling On or Off ..
#ifdef USE_INTERNAL_PROFILER
#define PROFILE(name)\
	static ProfileSample sample(name);\
	CProfileScope ProfileScope(&sample);

//BEGIN & END macros:		Only needed if you don't want to use the scope macro above.
// Macros must be in the same scope
#define PROFILE_BEGIN(name)\
	static ProfileSample sample__(name);\
	IFPBeginSample(&sample__);
#define PROFILE_END()\
	IFPEndSample(&sample__);

#define PROFILE_FUNC()\
	static ProfileSample sample(__FUNCTION__);\
	CProfileScope ProfileScope(&sample);

#define PROFILE_STACK_DUMP	dumpProfileStack();
#else
#define PROFILE(name)\
	static ProfileSample sample(name);\
	CProfileScope ProfileScope(&sample);

//BEGIN & END macros:		Only needed if you don't want to use the scope macro above.
// Macros must be in the same scope
#define PROFILE_BEGIN(name)\
	static ProfileSample sample__(name);\
	gDLL->BeginSample(&sample__);
#define PROFILE_END()\
	gDLL->EndSample(&sample__);

#define PROFILE_FUNC()\
	static ProfileSample sample(__FUNCTION__);\
	CProfileScope ProfileScope(&sample);

#define PROFILE_STACK_DUMP ;
#endif
#else // Remove profiling code		advc.006c: void(0) added
#define PROFILE(name) (void)0
#define PROFILE_BEGIN(name) (void)0
#define PROFILE_END() (void)0
#define PROFILE_FUNC() (void)0
#define PROFILE_STACK_DUMP (void)0
#endif


#endif //__PROFILE_H__


