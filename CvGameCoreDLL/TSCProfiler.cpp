#include "CvGameCoreDLL.h"
#include "TSCProfiler.h"

// advc.003o: Adopted from "We the People"; see comment in header file.

static __declspec(naked)unsigned __int64 __cdecl RDTSC(void)
{
	__asm
	{
		rdtsc
		ret; // return value at EDX : EAX
	}
}

TSCSample::TSCSample(const char* szName)
	: m_szName(szName)
	, m_iStartTime(RDTSC())
{
}

TSCSample::~TSCSample()
{
	unsigned __int64 iTime = RDTSC();
	iTime -= m_iStartTime;
	TSCProfiler::getInstance().addSample(iTime, m_szName);
}

// <advc.003o>
TSCProfiler& TSCProfiler::getInstance()
{
	static TSCProfiler singleton;
	return singleton;
} // </advc.003o>

void TSCProfiler::addSample(unsigned __int64 iTime, const char* szName)
{
	SampleStorageTypes::iterator pIterator;

	// TODO: make thread-safe without slowing down single threaded performance

	pIterator = this->m_Samples.find(szName);
	if (pIterator == m_Samples.end())
		m_Samples.insert(std::pair <std::string, storage>( szName, storage(1, iTime)));
	else
	{
		pIterator->second.first++;
		pIterator->second.second += iTime;
	}
}

void TSCProfiler::writeFile() const
{
	if (m_Samples.empty())
		return;

	// <advc.003o>
	std::ostringstream out;
	out << "Name\t\tAverage clocks\tNumber of calls\tTotal clocks\n";
	for (SampleStorageTypes::const_iterator iterator = m_Samples.begin(); iterator != m_Samples.end(); ++iterator)
	{
		unsigned __int64 iCount = iterator->second.first;
		unsigned __int64 iTime = iterator->second.second;
		out << iterator->first.c_str() << "\t" << (iTime / iCount) << "\t\t"
				<< iCount << "\t" << iTime << "\n";
	}
	out << std::endl;
	gDLL->logMsg("TSCProfile.log", out.str().c_str(), false, false);
	// </advc.003o>

	/*CvString filename = gDLL->getModName();
	filename.append("Profile output.txt");

	// Using C style file writing
	// The reason is that C++ style apparently has a known bug in our compiler and it won't compile in some projects (like ours).
	// The precise cause is unknown, but the recommendation is to use C style file writing.
	FILE *f = fopen(filename.GetCString(), "w");
	if (f != NULL)
	{
		fprintf(f, "Name\tAverage clocks\tNumber of calls\tTotal clocks\n");

		for (SampleStorageTypes::const_iterator iterator = m_Samples.begin(); iterator != m_Samples.end(); ++iterator)
		{
			const char* name = iterator->first.c_str();
			unsigned __int64 iCount = iterator->second.first;
			unsigned __int64 iTime = iterator->second.second;
			unsigned __int64 iAvg = iTime / iCount;

			fprintf(f, "%s", name);
			fprintf(f, "\t%I64u", iAvg);
			fprintf(f, "\t%I64u", iCount);
			fprintf(f, "\t%I64u", iTime);
			fprintf(f, "\n");
		}
		fclose(f);
	}*/
}
