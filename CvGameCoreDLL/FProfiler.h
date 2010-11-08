// ---------------------------------------------------------------------------------------------------
// FProfiler - DLL wrapper to FireEngine/FProfiler.cpp
//
// Author: tomw
//---------------------------------------------------------------------------------------------------------------------

#ifndef	__PROFILE_H__
#define __PROFILE_H__
#pragma once


#include "CvDLLEntityIFaceBase.h"
#include "CvDLLUtilityIFaceBase.h"
#include "CvGlobals.h"	// for gDLL

#ifndef FINAL_RELEASE
#ifndef FP_PROFILE_ENABLE 
	#define FP_PROFILE_ENABLE 
#endif
#endif

//NOTE: This struct must be identical ot the same struct in  FireEngine/FProfiler.h
//---------------------------------------------------------------------------------------------------------------------
struct ProfileSample
{
	ProfileSample(char *name)					{ strcpy(Name, name); Added=false; Parent=-1; }

	char	Name[256];						// Name of sample;

	unsigned int	ProfileInstances;		// # of times ProfileBegin Called
	int				OpenProfiles;			// # of time ProfileBegin called w/o ProfileEnd
	double			StartTime;				// The current open profile start time
	double			Accumulator;			// All samples this frame added together

	double			ChildrenSampleTime;		// Time taken by all children
	unsigned int	NumParents;				// Number of profile Parents
	bool			Added;					// true when added to the list
	int				Parent;
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
		bValid = true;
		gDLL->BeginSample(m_pSample);
	};
	~CProfileScope()
	{
		if(bValid )
		{
			gDLL->EndSample(m_pSample);
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

#else
#define PROFILE(name)				// Remove profiling code
#define PROFILE_BEGIN(name)
#define PROFILE_END()
#define PROFILE_FUNC()
#endif


#endif //__PROFILE_H__


