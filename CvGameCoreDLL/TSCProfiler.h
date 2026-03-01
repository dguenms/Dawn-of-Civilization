#pragma once

#ifndef TSC_PROFILER_H
#define TSC_PROFILER_H

/*  advc.003o: Profiler based on Time Stamp Counter. From the "We the People" mod
	for Civ 4 Colonization. Original code by Nightinggale (3 Nov 2019). */

#ifdef USE_TSC_PROFILER
#define TSC_PROFILE( x ) TSCSample sample( x );
#else
// advc.006c: void(0) in order to force semicolon
#define TSC_PROFILE( x ) (void)0
#endif


class TSCSample // advc: Renamed from "Profiler"
{
public:
	TSCSample(const char* szName);
	~TSCSample();

private:
	const char* m_szName;
	unsigned __int64 m_iStartTime;
};


class TSCProfiler // advc: Renamed from "ProfilerManager"
{
public:
	// advc.003o: Instead of an instance at CvGlobals
	static TSCProfiler& getInstance();
	void addSample(unsigned __int64 iTime, const char* szName);
	void writeFile() const;

private:
	typedef std::pair<unsigned __int64, unsigned __int64> storage;
	typedef stdext::hash_map< std::string, storage > SampleStorageTypes;

	SampleStorageTypes m_Samples;
};

#endif
