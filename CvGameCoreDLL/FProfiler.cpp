#include "CvGameCoreDLL.h"

// advc.003o: New implementation file. Contents cut from CvGameCoreDLL.cpp.

#ifdef USE_INTERNAL_PROFILER

//	Uncomment the following line to provide (very) detailed tracing to
//	the debug stream (view with DbgView or a debugger)
#define DETAILED_TRACE

#define MAX_SAMPLES 900
static ProfileSample* _currentSample = NULL;
static int numSamples = 0;
static ProfileSample* sampleList[MAX_SAMPLES];
static ProfileSample* sampleStack[MAX_SAMPLES];
static int depth = -1;

#ifdef DETAILED_TRACE
static ProfileSample* lastExit = NULL;
static int exitCount = 0;
static bool detailedTraceEnabled = false;

#include "CvDLLPythonIFaceBase.h" // advc.003o

static void GenerateTabString(char* buffer,int n)
{
	while(n-- > 0)
	{
		*buffer++ = '\t';
	}

	*buffer = '\0';
}
#endif

void EnableDetailedTrace(bool enable)
{
#ifdef DETAILED_TRACE
	detailedTraceEnabled = enable;
#endif
}

void IFPBeginSample(ProfileSample* sample)
{
	if ( sample->Id == -1 )
	{
		if ( numSamples == MAX_SAMPLES )
		{
			dumpProfileStack();
			::MessageBox(NULL,"Profile sample limit exceeded","CvGameCore",MB_OK);
			return;
		}
		sample->Id = numSamples;
		sample->OpenProfiles = 0;
		sample->ProfileInstances = 0;
		sample->Accumulator.QuadPart = 0;
		sample->ChildrenSampleTime.QuadPart = 0;
		sampleList[numSamples++] = sample;
	}

	if ( ++depth == MAX_SAMPLES )
	{
		::MessageBox(NULL,"Sample stack overflow","CvGameCore",MB_OK);
	}
	else
	{
		sampleStack[depth] = sample;
	}

	sample->ProfileInstances++;
	sample->OpenProfiles++;

	if ( sample->OpenProfiles == 1 )
	{
		if ( _currentSample == NULL )
		{
			sample->Parent = -1;
		}
		else
		{
			sample->Parent = _currentSample->Id;
		}

		QueryPerformanceCounter(&sample->StartTime);
	}

	_currentSample = sample;

#ifdef DETAILED_TRACE
	if ( detailedTraceEnabled && lastExit != sample )
	{
		char buffer[300];

		if ( exitCount != 0 )
		{
			GenerateTabString(buffer, depth);
			sprintf(buffer+depth, "[%d]\n", exitCount);
			OutputDebugString(buffer);

			exitCount = 0;
		}

		GenerateTabString(buffer, depth);
		sprintf(buffer+depth, "-->%s\n", sample->Name);

		OutputDebugString(buffer);
	}
#endif
}

void IFPEndSample(ProfileSample* sample)
{
	if ( _currentSample != sample )
	{
		MessageBox(NULL,"Sample closure not matched","CvGameCore",MB_OK);
	}

	if ( depth < 0 )
	{
		MessageBox(NULL,"Too many end-samples","CvGameCore",MB_OK);
	}
	else if ( depth == 0 )
	{
		_currentSample = NULL;
		depth = -1;
	}
	else
	{
		_currentSample = sampleStack[--depth];
	}

	if ( sample->OpenProfiles-- == 1 )
	{
		LARGE_INTEGER now;
		LONGLONG ellapsed;

		QueryPerformanceCounter(&now);

		ellapsed = (now.QuadPart - sample->StartTime.QuadPart);
		sample->Accumulator.QuadPart += ellapsed;

		if ( _currentSample != NULL )
		{
			_currentSample->ChildrenSampleTime.QuadPart += ellapsed;
		}
	}

#ifdef DETAILED_TRACE
	if ( detailedTraceEnabled && lastExit != sample )
	{
		char buffer[300];

		GenerateTabString(buffer, depth+1);
		strcpy(buffer+depth+1, "...\n");

		OutputDebugString(buffer);
		exitCount = 1;
	}
	else
	{
		exitCount++;
	}

	lastExit = sample;
#endif
}

void IFPBegin(void)
{
	for(int i = 0; i < numSamples; i++ )
	{
		sampleList[i]->Accumulator.QuadPart = 0;
		sampleList[i]->ChildrenSampleTime.QuadPart = 0;
		sampleList[i]->ProfileInstances = sampleList[i]->OpenProfiles;
	}
}

void IFPEnd(void)
{
	//	Log the timings
	char buffer[300];
	LARGE_INTEGER freq;

	QueryPerformanceFrequency(&freq);

	gDLL->logMsg("IFP_log.txt","Fn\tTime (mS)\tAvg time\t#calls\tChild time\tParent\n",
			false, false); // advc.003o: Don't timestamp

	for(int i = 0; i < numSamples; i++ )
	{
		if ( sampleList[i]->ProfileInstances != 0 )
		{
			sprintf(buffer,
					"%s\t%d\t%d\t%u\t%d\t%s\n",
					sampleList[i]->Name,
					(int)((1000*sampleList[i]->Accumulator.QuadPart)/freq.QuadPart),
					(int)((1000*sampleList[i]->Accumulator.QuadPart)/(freq.QuadPart*sampleList[i]->ProfileInstances)),
					sampleList[i]->ProfileInstances,
					(int)((1000*sampleList[i]->ChildrenSampleTime.QuadPart)/freq.QuadPart),
					sampleList[i]->Parent == -1 ? "" : sampleList[sampleList[i]->Parent]->Name);
			gDLL->logMsg("IFP_log.txt",buffer, /* advc.003o: */ false, false);
		}
	}
}

static bool isInLongLivedSection = false;
static ProfileSample rootSample__("Root");

//
// dump the current (profile) call stack to debug output
//
void dumpProfileStack(void)
{
	int i = 0;
	int dumpDepth = depth;
	char buffer[200];

	OutputDebugString("Profile stack:\n");

	while(dumpDepth >= 0)
	{
		char* ptr = buffer;

		i++;
		for(int j = 0; j < i; j++)
		{
			*ptr++ = '\t';
		}
		strcpy(ptr,sampleStack[dumpDepth--]->Name);
		strcat(ptr, "\n");
		OutputDebugString(buffer);
	}
}

static int pythonDepth = 0;

bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg)
{
	PROFILE("IFPPythonCall1");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool result = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return result;
}

bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, long* result)
{
	PROFILE("IFPPythonCall2");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool bResult = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, result);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return bResult;
}


bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, CvString* result)
{
	PROFILE("IFPPythonCall3");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool bResult = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, result);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return bResult;
}


bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, CvWString* result)
{
	PROFILE("IFPPythonCall4");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool bResult = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, result);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return bResult;
}


bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, std::vector<byte>* pList)
{
	PROFILE("IFPPythonCall5");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool result = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, pList);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return result;
}


bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, std::vector<int> *pIntList)
{
	PROFILE("IFPPythonCall6");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool result = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, pIntList);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return result;
}


bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, int* pIntList, int* iListSize)
{
	PROFILE("IFPPythonCall7");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool result = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, pIntList, iListSize);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return result;
}


bool IFPPythonCall(const char* callerFn, const char* moduleName, const char* fxnName, void* fxnArg, std::vector<float> *pFloatList)
{
	PROFILE("IFPPythonCall8");

	//OutputDebugString(CvString::format("Python call to %s::%s [%d]\n", moduleName, fxnName, pythonDepth++).c_str());

	bool result = gDLL->getPythonIFace()->callFunction(moduleName, fxnName, fxnArg, pFloatList);

	//OutputDebugString("...complete\n");
	pythonDepth--;

	return result;
}



#endif

//
// enable dll profiler if necessary, clear history
//
void startProfilingDLL(bool longLived)
{
#ifdef USE_INTERNAL_PROFILER
	if ( longLived )
	{
		isInLongLivedSection = true;
	}
	else if (GC.isDLLProfilerEnabled() && !isInLongLivedSection)
	{
		IFPBegin();
		IFPBeginSample(&rootSample__);
	}
#else
	if (GC.isDLLProfilerEnabled())
	{
		gDLL->ProfilerBegin();
	}
#endif
}

//
// dump profile stats on-screen
//
void stopProfilingDLL(bool longLived)
{
#ifdef USE_INTERNAL_PROFILER
	if ( longLived )
	{
		isInLongLivedSection = false;
	}
	else if (GC.isDLLProfilerEnabled() && !isInLongLivedSection)
	{
		IFPEndSample(&rootSample__);
		IFPEnd();
	}
#else
	if (GC.isDLLProfilerEnabled())
	{
		gDLL->ProfilerEnd();
	}
#endif
}
