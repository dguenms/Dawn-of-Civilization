#include "CvGameCoreDLL.h"

//#define _TEST_ENUM_MAP // advc: Uncomment to enable the tests

/*	For testing read and write functions. Not important that the data is stored
	in the same way that FDataStream in the EXE stores it. Just need the
	write functions to store data in the format that the read functions expect. */
#ifdef _TEST_ENUM_MAP
class TestStream : public FDataStreamBase
{
private:
	std::vector<byte> m_data;
	int m_iPos;
	template<class T>
	void readCount(int iCount, T values[])
	{
		for (int i = 0; i < iCount; i++)
			Read(&values[i]);
	}
	template<class T>
	void writeCount(int iCount, T const values[])
	{
		for (int i = 0; i < iCount; i++)
			Write(values[i]);
	}
	template<class T>
	void readPtr(T* pValue)
	{
		for (int i = 0; i < sizeof(T); i++)
		{
			FAssert(m_iPos < (int)m_data.size());
			((byte*)pValue)[i] = m_data.at(m_iPos);
			m_iPos++;
		}
	}
	template<class T>
	void writeBytes(T value)
	{
		byte* aBytes = (byte*)&value;
		for (int i = 0; i < sizeof(T); i++)
		{
			m_data.push_back(aBytes[i]);
		}
	}
public:
	TestStream() : m_iPos(0) {}
	bool AtEnd() { return (m_iPos == (int)m_data.size()); }
	~TestStream() { FAssert(AtEnd()); }

	// (These are probably supposed to return the number of bytes written)
	unsigned int WriteString(wchar const* szName)
	{
		std::wstring tmp(szName);
		return WriteString(tmp);
	}
	unsigned int WriteString(char const* szName)
	{
		std::string tmp(szName);
		return WriteString(tmp);
	}
	unsigned int WriteString(std::string const& szName)
	{
		WriteExternal((int)szName.length());
		for (size_t i = 0; i < szName.length(); i++)
			WriteExternal(szName.at(i));
		return 0;
	}
	unsigned int WriteString(std::wstring const& szName)
	{
		Write((int)szName.length());
		for (size_t i = 0; i < szName.length(); i++)
			Write(szName.at(i));
		return 0;
	}
	unsigned int WriteString(int iCount, std::string values[])
	{
		for (int i = 0; i < iCount; i++)
			WriteString(values[i]);
		return 0;
	}
	unsigned int WriteString(int iCount, std::wstring values[])
	{
		for (int i = 0; i < iCount; i++)
			WriteString(values[i]);
		return 0;
	}
	unsigned int ReadString(char *szName)
	{
		szName = ReadString();
		return 0;
	}
	unsigned int ReadString(wchar* szName)
	{
		szName = ReadWideString();
		return 0;
	}
	char* ReadString()
	{
		std::string tmp;
		ReadString(tmp);
		// Not going to allocate memory here ...
		return NULL;
	}
	wchar* ReadWideString()
	{
		std::wstring tmp;
		ReadString(tmp);
		return NULL;
	}
	unsigned int ReadString(std::string& szName)
	{
		int iLength;
		Read(&iLength);
		for (int i = 0; i < iLength; i++)
		{
			char c;
			Read(&c);
			szName += c;
		}
		return 0;
	}
	unsigned int ReadString(std::wstring& szName)
	{
		int iLength;
		Read(&iLength);
		for (int i = 0; i < iLength; i++)
		{
			char c;
			Read(&c);
			szName += c;
		}
		return 0;
	}
	unsigned int ReadString(int iCount, std::string values[])
	{
		for (int i = 0; i < iCount; i++)
			ReadString(values[i]);
		return 0;
	}
	unsigned int ReadString(int iCount, std::wstring values[])
	{
		for (int i = 0; i < iCount; i++)
			ReadString(values[i]);
		return 0;
	}
	void Read(char* pValue)
	{
		readPtr(pValue);
	}
	void Read(byte* pValue)
	{
		readPtr(pValue);
	}
	void Read(bool* pValue)
	{
		readPtr(pValue);
	}
	void Read(short* pValue)
	{
		readPtr(pValue);
	}
	void Read(word* pValue)
	{
		readPtr(pValue);
	}
	void Read(int* pValue)
	{
		readPtr(pValue);
	}
	void Read(uint* pValue)
	{
		readPtr(pValue);
	}
	void Read(long* pValue)
	{
		readPtr(pValue);
	}
	void Read(unsigned long* pValue)
	{
		readPtr(pValue);
	}
	void Read(float* pValue)
	{
		readPtr(pValue);
	}
	void Read(double* pValue)
	{
		readPtr(pValue);
	}
	void Read(int iCount, char values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, byte values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, bool values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, short values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, unsigned short values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, int values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, unsigned int values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, long values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, unsigned long values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, float values[])
	{
		readCount(iCount, values);
	}
	void Read(int iCount, double values[])
	{
		readCount(iCount, values);
	}
	template<class T>
	void Write(T value)
	{
		WriteExternal(value);
	}
	void WriteExternal(char value)
	{
		writeBytes(value);
	}
	void WriteExternal(byte value)
	{
		writeBytes(value);
	}
	void WriteExternal(bool value)
	{
		writeBytes(value);
	}
	void WriteExternal(short value)
	{
		writeBytes(value);
	}
	void WriteExternal(word value)
	{
		writeBytes(value);
	}
	void WriteExternal(int value)
	{
		writeBytes(value);
	}
	void WriteExternal(uint value)
	{
		writeBytes(value);
	}
	void WriteExternal(long value)
	{
		writeBytes(value);
	}
	void WriteExternal(unsigned long value)
	{
		writeBytes(value);
	}
	void WriteExternal(float value)
	{
		writeBytes(value);
	}
	void WriteExternal(double value)
	{
		writeBytes(value);
	}
	template<class T>
	void Write(int iCount, T const values[])
	{
		WriteExternal(iCount, values);
	}
	void WriteExternal(int iCount, char const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, byte const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, bool const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, short const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, word const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, int const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, uint const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, long const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, unsigned long const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, float const values[])
	{
		writeCount(iCount, values);
	}
	void WriteExternal(int iCount, double const values[])
	{
		writeCount(iCount, values);
	}
	void Rewind() { FErrorMsg("not implemented"); }
	void FastFwd() { FErrorMsg("not implemented"); }
	unsigned int GetPosition() const { FErrorMsg("not implemented"); return 0; }
	void SetPosition(unsigned int position) { FErrorMsg("not implemented"); }
	void Truncate() { FErrorMsg("not implemented"); }
	void Flush() { FErrorMsg("not implemented"); }
	unsigned int GetEOF() const { FErrorMsg("not implemented"); return 0; }
	unsigned int GetSizeLeft() const { FErrorMsg("not implemented"); return 0; }
	void CopyToMem(void* mem) { FErrorMsg("not implemented"); }
};

template<class IntEncMap, class OuterMap>
void testEnum2IntEncMap()
{
	Enum2IntEncMap<OuterMap,IntEncMap> test;
	PlayerTypes eOuterKey = (PlayerTypes)3;
	FAssert(test.get(eOuterKey) == 0);
	FAssert(test.get(eOuterKey, YIELD_PRODUCTION) == 0);
	FAssert(!test.isAnyNonDefault());
	test.add(eOuterKey, YIELD_PRODUCTION, 1);
	FAssert(test.isAnyNonDefault());
	FAssert(test.get(eOuterKey) != 0);
	FAssert(test.get(eOuterKey, YIELD_PRODUCTION) == 1);
	test.resetVal(eOuterKey, YIELD_PRODUCTION);
	FAssert(test.get(eOuterKey, YIELD_PRODUCTION) == 0);
	FAssert(!test.isAnyNonDefault());
	test.set(eOuterKey, YIELD_PRODUCTION, 2);
	FAssert(test.get(eOuterKey, YIELD_PRODUCTION) == 2);
	FAssert(test.get(eOuterKey) != 0);
	test.resetVal(eOuterKey);
	FAssert(test.get(eOuterKey) == 0);
	FAssert(!test.isAnyNonDefault());
	test.add(eOuterKey, YIELD_PRODUCTION, 2);
	test.multiply(eOuterKey, YIELD_PRODUCTION, 3);
	FAssert(test.get(eOuterKey, YIELD_PRODUCTION) == 6);
	test.reset();
	FAssert(test.get(eOuterKey, YIELD_PRODUCTION) == 0);
	test.set(eOuterKey, YIELD_PRODUCTION, 1);
	PlayerTypes eOtherOuterKey = (PlayerTypes)9;
	test.set(eOtherOuterKey, YIELD_PRODUCTION, -3);
	test.set(eOtherOuterKey, YIELD_FOOD, -3);
	FAssert(test.numNonDefault() == 3);
	Enum2IntEncMap<OuterMap,IntEncMap> other = test;
	FAssert(other.numNonDefault() == 3);
	{
		TestStream stream;
		other.write(&stream);
		other.reset();
		other.read(&stream);
		FAssert(other.numNonDefault() == 3);
		FAssert(other.get(eOtherOuterKey, YIELD_FOOD) == -3);
	}
	FOR_EACH_NON_DEFAULT_PAIR(test, Player, IntEncMap)
	{
		if (perPlayerVal.first == eOuterKey)
			FAssert(perPlayerVal.second[YIELD_PRODUCTION] == 1);
		FAssert(perPlayerVal.first == eOuterKey || perPlayerVal.first == eOtherOuterKey);
	}
	FOR_EACH_NON_DEFAULT_KEY(/* this is the copy of test */ other, Player)
	{
		FAssert(eLoopPlayer == eOuterKey || eLoopPlayer == eOtherOuterKey);
	}
	test.set(eOuterKey, YIELD_PRODUCTION, 0);
	test.resetVal(eOtherOuterKey);
	FAssert(!test.isAnyNonDefault());
	int iIterations = 0;
	FOR_EACH_NON_DEFAULT_PAIR(test, Player, IntEncMap)
	{
		iIterations++;
	}
	FAssert(iIterations == 0);
}
#endif

void TestEnumMap()
{
#ifdef _TEST_ENUM_MAP
	{	// Typical list enum map
		ListEnumMap<BuildingTypes,short> test;
		BuildingTypes eKey = static_cast<BuildingTypes>(3);
		FAssert(test.get(eKey) == 0);
		FAssert(!test.isAnyNonDefault());
		test.set(eKey, 1);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eKey) == 1);
		test.resetVal(eKey);
		FAssert(test.get(eKey) == 0);
		FAssert(!test.isAnyNonDefault());
		/*	After resetting eKey, it'll still be (explicitly) stored,
			but the loops should skip it. */
		int iCount = 0;
		FOR_EACH_NON_DEFAULT_PAIR(test, Building, int)
			iCount++;
		FAssert(iCount == 0);
		iCount = 0;
		FOR_EACH_NON_DEFAULT_KEY(test, Building)
			iCount++;
		FAssert(iCount == 0);
		test.add(eKey, 2);
		test.multiply(eKey, 3);
		FAssert(test.get(eKey) == 6);
		test.divide(eKey, 4);
		FAssert(test.get(eKey) == 1);
		test.reset();
		FAssert(test.get(eKey) == 0);
		test.set(eKey, 1);
		BuildingTypes eOtherKey = static_cast<BuildingTypes>(9);
		test.set(eOtherKey, -3);
		FAssert(test.numNonDefault() == 2);
		ListEnumMap<BuildingTypes,short> other = test; // copy-ctor
		FAssert(other.numNonDefault() == 2);
		test.set(eKey, 0);
		test.resetVal(eOtherKey);
		FAssert(!test.isAnyNonDefault());
		FOR_EACH_NON_DEFAULT_PAIR(other, Building, int)
		{
			if (perBuildingVal.first == eKey)
				FAssert(perBuildingVal.second == 1);
			FAssert(perBuildingVal.first == eKey || perBuildingVal.first == eOtherKey);
		}
		//FOR_EACH_NON_DEFAULT_PAIR(other, Building, char) {}  // Should fail a static assertion
		FOR_EACH_NON_DEFAULT_KEY(other, Building)
		{
			FAssert(eLoopBuilding == eKey || eLoopBuilding == eOtherKey);
		}
		ListEnumMap<BuildingTypes,short> other2;
		other2 = other; // assignment operator
		FAssert(other2.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_PAIR(other2, Building, int)
		{
			if (perBuildingVal.first == eKey)
				FAssert(perBuildingVal.second == 1);
			FAssert(perBuildingVal.first == eKey || perBuildingVal.first == eOtherKey);
		}
		TestStream stream;
		other2.write(&stream);
		other2.reset();
		other2.read(&stream);
		FAssert(other2.numNonDefault() == 2);
		FAssert(other2.get(eKey) == 1);
	}
	{	// Boolean list enum map, key enum known at compile time.
		ListEnumMap<DirectionTypes,bool> test;
		FAssert(!test.get(DIRECTION_NORTH));
		FAssert(!test.isAnyNonDefault());
		test.set(DIRECTION_WEST, true);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(DIRECTION_WEST));
		test.resetVal(DIRECTION_WEST);
		FAssert(!test.get(DIRECTION_WEST));
		//test.add(DIRECTION_WEST, 1); // Should fail a static assertion
		test.toggle(DIRECTION_WEST);
		FAssert(test.get(DIRECTION_WEST));
		test.set(DIRECTION_NORTH, true);
		FAssert(test.numNonDefault() == 2);
		ListEnumMap<DirectionTypes,bool> other = test;
		FAssert(other.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_PAIR(test, Direction, bool)
		{
			FAssert(perDirectionVal.second);
			FAssert(perDirectionVal.first == DIRECTION_NORTH ||
					perDirectionVal.first == DIRECTION_WEST);
		}
		FOR_EACH_NON_DEFAULT_KEY(test, Direction)
		{
			FAssert(eLoopDirection == DIRECTION_NORTH ||
					eLoopDirection == DIRECTION_WEST);
		}
		TestStream stream;
		other.write(&stream);
		other.reset();
		other.read(&stream);
		FAssert(other.numNonDefault() == 2);
		FAssert(other.get(DIRECTION_NORTH));
	}
	{	// List-based enum-to-enum map, using two unusual enum types.
		ListEnumMap<WorldSizeTypes,CityPlotTypes> test;
		test.set(WORLDSIZE_SMALL, CITY_HOME_PLOT);
		FAssert(test.get(WORLDSIZE_LARGE) == -1);
		FAssert(test.get(WORLDSIZE_SMALL) == CITY_HOME_PLOT);
	}
	{	// List enum map with pointer-type values
		ListEnumMap<PlayerTypes,scaled*> test;
		scaled rNum;
		test.set((PlayerTypes)0, &rNum);
		FAssert(test.get((PlayerTypes)1) == NULL);
		FAssert(test.get((PlayerTypes)0) == &rNum);
	}
	{	// List enum map with float values
		ListEnumMap<TeamTypes,float> test;
		test.set((TeamTypes)0, .5f);
		FAssert(test.get((TeamTypes)1) == 0);
		FAssert(test.get((TeamTypes)0) == .5f);
	}
	{	// List enum map with ScaledNum values
		ListEnumMap<TeamTypes,scaled> test;
		test.set((TeamTypes)0, fixp(0.5));
		FAssert(test.get((TeamTypes)1) == 0);
		FAssert(test.get((TeamTypes)0) == fixp(0.5));
	}
	{	// List enum map with smaller compact value type, unsigned value types.
		ListEnumMap<UnitTypes,uint,byte> test;
		test.set((UnitTypes)3, 5);
		FAssert(test.get((UnitTypes)1) == 0);
		FAssert(test.get((UnitTypes)3) == 5);
	}
	{	// List enum map with nonzero default value
		ListEnumMap<UnitTypes,int,short,100> test;
		test.set((UnitTypes)3, 5);
		FAssert(test.get((UnitTypes)1) == 100);
		FAssert(test.get((UnitTypes)3) == 5);
	}
	{	// List enum map with end marker
		ListEnumMap<UnitTypes,int,char,0,false,true> test;
		test.set((UnitTypes)8, 5);
		FAssert(test.get((UnitTypes)1) == 0);
		FAssert(test.get((UnitTypes)8) == 5);
		test.set((UnitTypes)3, -3);
		FAssert(test.get((UnitTypes)3) == -3);
		FOR_EACH_NON_DEFAULT_PAIR(test, Unit, short)
		{
			FAssert(perUnitVal.second != 0);
			FAssert(perUnitVal.first == 8 ||
					perUnitVal.first == 3);
		}
		test.set((UnitTypes)8, 0);
		FAssert(test.get((UnitTypes)8) == 0);
		FAssert(test.get((UnitTypes)3) == -3);
		FAssert(test.isAnyNonDefault());
		TestStream stream;
		test.write(&stream);
		test.reset();
		FAssert(!test.isAnyNonDefault());
		test.read(&stream);
		FAssert(test.get((UnitTypes)3) == -3);
	}
	{	// Monotone ListEnumMap
		NonDefaultEnumMap<BuildingTypes,short> test;
		BuildingTypes eKey = static_cast<BuildingTypes>(3);
		FAssert(test.get(eKey) == 0);
		FAssert(!test.isAnyNonDefault());
		test.set(eKey, 1);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eKey) == 1);
		//test.resetVal(eKey); // Should fail runtime assertion
		FOR_EACH_NON_DEFAULT_PAIR(test, Building, int)
		{
			FAssert(perBuildingVal.first == eKey && perBuildingVal.second == 1);
		}
	}
	{	// Offline list-based enum set
		OfflineListEnumSet<CivicTypes> test;
		test.set((CivicTypes)5, true);
		FAssert(!test.get((CivicTypes)1));
		FAssert(test.get((CivicTypes)5));
		test.set((CivicTypes)3, true);
		//test.toggle((CivicTypes)2); // private
		//test.add((CivicTypes)2, 1); // should fail static assert
		FOR_EACH_NON_DEFAULT_KEY(test, Civic)
		{
			FAssert(eLoopCivic == 5 || eLoopCivic == 3);
		}
		FAssert(test.isAnyNonDefault());
		TestStream stream;
		test.write(&stream);
		test.reset();
		FAssert(!test.isAnyNonDefault());
		test.read(&stream);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get((CivicTypes)5));
	}
	{	// Typical array enum map, lazy allocation.
		ArrayEnumMap<TerrainTypes,short> test;
		TerrainTypes eKey = static_cast<TerrainTypes>(2);
		FAssert(test.get(eKey) == 0);
		FAssert(!test.isAnyNonDefault());
		test.set(eKey, 1);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eKey) == 1);
		test.resetVal(eKey);
		FAssert(test.get(eKey) == 0);
		FAssert(!test.isAnyNonDefault());
		test.add(eKey, 2);
		test.multiply(eKey, 3);
		FAssert(test.get(eKey) == 6);
		test.divide(eKey, 4);
		FAssert(test.get(eKey) == 1);
		test.reset();
		FAssert(test.get(eKey) == 0);
		test.set(eKey, 1);
		TerrainTypes eOtherKey = static_cast<TerrainTypes>(4);
		test.set(eOtherKey, -3);
		FAssert(test.numNonDefault() == 2);
		ArrayEnumMap<TerrainTypes,short> other = test;
		FAssert(other.numNonDefault() == 2);
		test.set(eKey, 0);
		test.resetVal(eOtherKey);
		FAssert(!test.isAnyNonDefault());
		FOR_EACH_NON_DEFAULT_PAIR(other, Terrain, int)
		{
			if (perTerrainVal.first == eKey)
				FAssert(perTerrainVal.second == 1);
			FAssert(perTerrainVal.first == eKey || perTerrainVal.first == eOtherKey);
		}
		FOR_EACH_NON_DEFAULT_KEY(other, Terrain)
		{
			FAssert(eLoopTerrain == eKey || eLoopTerrain == eOtherKey);
		}
		TestStream stream;
		other.write(&stream);
		other.reset();
		other.read(&stream);
		FAssert(other.get(eKey) == 1);
	}
	{	// Array enum map w/ forced default value and eager allocation
		ArrayEnumMap<TerrainTypes,short,short,-1,true> test;
		TerrainTypes eKey = static_cast<TerrainTypes>(2);
		FAssert(test.get(eKey) == -1);
		FAssert(!test.isAnyNonDefault());
		test.set(eKey, 0);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eKey) == 0);
		test.resetVal(eKey);
		FAssert(test.get(eKey) == -1);
		FAssert(!test.isAnyNonDefault());
		test.add(eKey, 2);
		test.multiply(eKey, 3);
		FAssert(test.get(eKey) == 3);
		test.divide(eKey, 2);
		FAssert(test.get(eKey) == 1);
		test.reset();
		FAssert(test.get(eKey) == -1);
		test.set(eKey, 1);
		TerrainTypes eOtherKey = static_cast<TerrainTypes>(4);
		test.set(eOtherKey, -3);
		FAssert(test.numNonDefault() == 2);
		ArrayEnumMap<TerrainTypes,short,short,-1,true> other = test; // copy-ctor
		FAssert(other.numNonDefault() == 2);
		test.set(eKey, -1);
		test.resetVal(eOtherKey);
		FAssert(!test.isAnyNonDefault());
		FOR_EACH_NON_DEFAULT_PAIR(other, Terrain, int)
		{
			if (perTerrainVal.first == eKey)
				FAssert(perTerrainVal.second == 1);
			FAssert(perTerrainVal.first == eKey || perTerrainVal.first == eOtherKey);
		}
		FOR_EACH_NON_DEFAULT_KEY(other, Terrain)
		{
			FAssert(eLoopTerrain == eKey || eLoopTerrain == eOtherKey);
		}
		ArrayEnumMap<TerrainTypes,short,short,-1,true> other2;
		other2 = other; // assignment operator
		FAssert(other2.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_PAIR(other2, Terrain, int)
		{
			if (perTerrainVal.first == eKey)
				FAssert(perTerrainVal.second == 1);
			FAssert(perTerrainVal.first == eKey || perTerrainVal.first == eOtherKey);
		}
		TestStream stream;
		other2.write(&stream);
		other2.reset();
		other2.read(&stream);
		FAssert(other2.numNonDefault() == 2);
	}
	{	// Boolean array enum map using dynamic memory
		ArrayEnumMap<UnitTypes,bool> test;
		UnitTypes eKey = (UnitTypes)1;
		FAssert(!test.get(eKey));
		FAssert(!test.isAnyNonDefault());
		UnitTypes eOtherKey = (UnitTypes)24;
		test.set(eOtherKey, true);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eOtherKey));
		test.resetVal(eOtherKey);
		FAssert(!test.get(eOtherKey));
		test.toggle(eOtherKey);
		FAssert(test.get(eOtherKey));
		test.set(eKey, true);
		FAssert(test.numNonDefault() == 2);
		ArrayEnumMap<UnitTypes,bool> other = test;
		FAssert(other.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_KEY(test, Unit)
		{
			FAssert(eLoopUnit == eKey || eLoopUnit == eOtherKey);
		}
		TestStream stream;
		test.write(&stream);
		test.reset();
		test.read(&stream);
		FAssert(other.numNonDefault() == 2);
	}
	{	// Boolean array enum map with a single block of static memory
		ArrayEnumMap<DirectionTypes,bool> test;
		FAssert(!test.get(DIRECTION_NORTH));
		FAssert(!test.isAnyNonDefault());
		test.set(DIRECTION_WEST, true);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(DIRECTION_WEST));
		test.resetVal(DIRECTION_WEST);
		FAssert(!test.get(DIRECTION_WEST));
		test.toggle(DIRECTION_WEST);
		FAssert(test.get(DIRECTION_WEST));
		test.set(DIRECTION_NORTH, true);
		FAssert(test.numNonDefault() == 2);
		ArrayEnumMap<DirectionTypes,bool> other = test;
		FAssert(other.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_PAIR(test, Direction, bool)
		{
			FAssert(perDirectionVal.second);
			FAssert(perDirectionVal.first == DIRECTION_NORTH ||
					perDirectionVal.first == DIRECTION_WEST);
		}
		FOR_EACH_NON_DEFAULT_KEY(test, Direction)
		{
			FAssert(eLoopDirection == DIRECTION_NORTH ||
					eLoopDirection == DIRECTION_WEST);
		}
		TestStream stream;
		test.write(&stream);
		test.reset();
		test.read(&stream);
		FAssert(test.numNonDefault() == 2);
	}
	{	// Non-boolean array enum map maxing out static memory
		ArrayEnumMap<DirectionTypes,PlayerTypes> test;
		FAssert(test.get(DIRECTION_NORTH) == NO_PLAYER);
		FAssert(!test.isAnyNonDefault());
		test.set(DIRECTION_WEST, (PlayerTypes)3);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(DIRECTION_WEST) == 3);
		test.resetVal(DIRECTION_WEST);
		FAssert(test.get(DIRECTION_WEST) == NO_PLAYER);
		test.add(DIRECTION_WEST, (PlayerTypes)2);
		FAssert(test.get(DIRECTION_WEST) == 1);
		test.set(DIRECTION_NORTH, (PlayerTypes)0);
		FAssert(test.numNonDefault() == 2);
		ArrayEnumMap<DirectionTypes,PlayerTypes> other = test;
		FAssert(other.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_KEY(test, Direction)
		{
			FAssert(eLoopDirection == DIRECTION_NORTH ||
					eLoopDirection == DIRECTION_WEST);
		}
		TestStream stream;
		test.write(&stream);
		test.reset();
		test.read(&stream);
		FAssert(test.numNonDefault() == 2);
	}
	{	/*	Array enum map with pointer-type values, eager allocation.
			(Like in the inner map of a 2D map.) */
		ArrayEnumMap<PlayerTypes,scaled*,int,NULL,true> test;
		scaled rNum(3);
		test.set((PlayerTypes)0, &rNum);
		FAssert(test.get((PlayerTypes)1) == NULL);
		FAssert(test.get((PlayerTypes)0) == &rNum);
		// Mustn't serialize pointers
		/*TestStream stream;
		test.write(&stream);*/ // Should fail static assertion
	}
	{	// Yield change map (4x char)
		YieldChangeMap test;
		FAssert(test.get(YIELD_PRODUCTION) == 0);
		FAssert(!test.isAnyNonDefault());
		test.set(YIELD_PRODUCTION, 2);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(YIELD_PRODUCTION) == 2);
		test.multiply(YIELD_PRODUCTION, 3);
		FAssert(test.get(YIELD_PRODUCTION) == 6);
		test.set(YIELD_COMMERCE, -2);
		FAssert(test.numNonDefault() == 2);
		YieldChangeMap other = test;
		FAssert(other.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_PAIR(test, Yield, int)
		{
			FAssert(perYieldVal.second != 0);
			FAssert(perYieldVal.first == YIELD_PRODUCTION ||
					perYieldVal.first == YIELD_COMMERCE);
		}
		// Insert and retrieve yield change map
		ArrayEnumMap<FeatureTypes,YieldChangeMap::enc_t> test2d;
		FAssert(test2d.get((FeatureTypes)1) == 0);
		test2d.set((FeatureTypes)1, test.encode());
		YieldChangeMap::enc_t enc = test2d.get((FeatureTypes)1);
		FAssert(enc == test.encode());
		YieldChangeMap restored(enc);
		FAssert(restored.numNonDefault() == 2);
		TestStream stream;
		restored.write(&stream);
		restored.reset();
		restored.read(&stream);
		FAssert(restored.encode() == enc);
	}
	{	// Commerce percent map (4x short)
		CommercePercentMap test;
		FAssert(test.get(COMMERCE_ESPIONAGE) == 0);
		FAssert(!test.isAnyNonDefault());
		test.set(COMMERCE_ESPIONAGE, 2);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(COMMERCE_ESPIONAGE) == 2);
		test.set(COMMERCE_GOLD, -2);
		FAssert(test.numNonDefault() == 2);
		CommercePercentMap other = test;
		FAssert(other.numNonDefault() == 2);
		FOR_EACH_NON_DEFAULT_PAIR(test, Commerce, int)
		{
			FAssert(perCommerceVal.second != 0);
			FAssert(perCommerceVal.first == COMMERCE_ESPIONAGE ||
					perCommerceVal.first == COMMERCE_GOLD);
		}
		// Insert and retrieve commerce percent map
		ArrayEnumMap<FeatureTypes,CommercePercentMap::enc_t> test2d;
		FAssert(test2d.get((FeatureTypes)1) == 0);
		test2d.set((FeatureTypes)1, test.encode());
		CommercePercentMap::enc_t enc = test2d.get((FeatureTypes)1);
		FAssert(enc == test.encode());
		CommercePercentMap restored(enc);
		FAssert(restored.numNonDefault() == 2);
		TestStream stream;
		restored.write(&stream);
		restored.reset();
		restored.read(&stream);
		FAssert(restored.encode() == enc);
	}
	{	// Subsequence enum map
		CivPlayerMap<bool> test;
		FAssert(test.get((PlayerTypes)3) == 0);
		FAssert(!test.isAnyNonDefault());
		test.set((PlayerTypes)3, true);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get((PlayerTypes)3));
		test.set((PlayerTypes)6, true);
		FAssert(test.numNonDefault() == 2);
		CivPlayerMap<bool> other = test;
		FAssert(other.numNonDefault() == 2);
		TestStream stream;
		other.write(&stream);
		other.reset();
		other.read(&stream);
		FAssert(other.numNonDefault() == 2);
	}
	{	// Typical 2D enum map based on arrays
		ArrayEnumMap2D<UnitTypes,UnitAITypes,short> test;
		UnitTypes eOuterKey = (UnitTypes)3;
		FAssert(test.get(eOuterKey) == NULL);
		UnitAITypes eInnerKey = (UnitAITypes)2;
		FAssert(test.get(eOuterKey, eInnerKey) == 0);
		FAssert(!test.isAnyNonDefault());
		test.add(eOuterKey, eInnerKey, 1);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eOuterKey) != NULL);
		FAssert(test.get(eOuterKey, eInnerKey) == 1);
		test.resetVal(eOuterKey, eInnerKey);
		FAssert(test.get(eOuterKey, eInnerKey) == 0);
		FAssert(test.get(eOuterKey) != NULL);
		FAssert(!test.isAnyNonDefault());
		test.resetVal(eOuterKey);
		FAssert(test.get(eOuterKey) == NULL);
		test.add(eOuterKey, eInnerKey, 2);
		test.multiply(eOuterKey, eInnerKey, 3);
		FAssert(test.get(eOuterKey) != NULL);
		FAssert(test.get(eOuterKey, eInnerKey) == 6);
		test.divide(eOuterKey, eInnerKey, 4);
		FAssert(test.get(eOuterKey, eInnerKey) == 1);
		test.reset();
		FAssert(test.get(eOuterKey, eInnerKey) == 0);
		test.set(eOuterKey, eInnerKey, 1);
		UnitTypes eOtherOuterKey = (UnitTypes)9;
		UnitAITypes eOtherInnerKey = (UnitAITypes)4;
		test.set(eOtherOuterKey, eInnerKey, -3);
		test.set(eOtherOuterKey, eOtherInnerKey, -3);
		FAssert(test.numNonDefault() == 3);
		ArrayEnumMap2D<UnitTypes,UnitAITypes,short> other = test;
		FAssert(other.numNonDefault() == 3);
		TestStream stream;
		other.write(&stream);
		other.reset();
		other.read(&stream);
		FAssert(other.numNonDefault() == 3);
		test.set(eOuterKey, eInnerKey, 0);
		test.resetVal(eOtherOuterKey);
		FAssert(!test.isAnyNonDefault());
	}
	{	// Typical 2D enum map based on lists
		ListEnumMap2D<PlayerTypes,CultureLevelTypes,char> test;
		PlayerTypes eOuterKey = (PlayerTypes)3;
		FAssert(test.get(eOuterKey) == NULL);
		CultureLevelTypes eInnerKey = (CultureLevelTypes)2;
		FAssert(test.get(eOuterKey, eInnerKey) == 0);
		FAssert(!test.isAnyNonDefault());
		test.add(eOuterKey, eInnerKey, 1);
		FAssert(test.isAnyNonDefault());
		FAssert(test.get(eOuterKey) != NULL);
		FAssert(test.get(eOuterKey, eInnerKey) == 1);
		test.resetVal(eOuterKey, eInnerKey);
		FAssert(test.get(eOuterKey, eInnerKey) == 0);
		FAssert(test.get(eOuterKey) != NULL);
		FAssert(!test.isAnyNonDefault());
		test.resetVal(eOuterKey);
		FAssert(test.get(eOuterKey) == NULL);
		test.add(eOuterKey, eInnerKey, 2);
		test.multiply(eOuterKey, eInnerKey, 3);
		FAssert(test.get(eOuterKey) != NULL);
		FAssert(test.get(eOuterKey, eInnerKey) == 6);
		test.divide(eOuterKey, eInnerKey, 4);
		FAssert(test.get(eOuterKey, eInnerKey) == 1);
		test.reset();
		FAssert(test.get(eOuterKey, eInnerKey) == 0);
		test.set(eOuterKey, eInnerKey, 1);
		PlayerTypes eOtherOuterKey = (PlayerTypes)9;
		CultureLevelTypes eOtherInnerKey = (CultureLevelTypes)4;
		test.set(eOtherOuterKey, eInnerKey, -3);
		test.set(eOtherOuterKey, eOtherInnerKey, -3);
		FAssert(test.numNonDefault() == 3);
		ListEnumMap2D<PlayerTypes,CultureLevelTypes,char> other = test;
		FAssert(other.numNonDefault() == 3);
		TestStream stream;
		other.write(&stream);
		other.reset();
		other.read(&stream);
		FAssert(other.numNonDefault() == 3);
		FAssert(other.get(eOtherOuterKey, eOtherInnerKey) == -3);
		test.set(eOuterKey, eInnerKey, 0);
		test.resetVal(eOtherOuterKey);
		FAssert(!test.isAnyNonDefault());
	}
	{	// 2D enum map involving yield vectors encoded as integers
		testEnum2IntEncMap<YieldChangeMap, // encoded in 32 bit
				ArrayEnumMap<PlayerTypes,YieldChangeMap::enc_t> >(); // array-based outer map
		testEnum2IntEncMap<YieldPercentMap, // encoded in 64 bit
				ArrayEnumMap<PlayerTypes,YieldPercentMap::enc_t> >(); // array-based outer map
		// Now list-based ...
		testEnum2IntEncMap<YieldChangeMap, ListEnumMap<PlayerTypes,YieldChangeMap::enc_t> >();
		testEnum2IntEncMap<YieldPercentMap, ListEnumMap<PlayerTypes,YieldPercentMap::enc_t> >();
	}
#endif
}
