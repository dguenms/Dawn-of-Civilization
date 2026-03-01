// advc.fract: Test code for the ScaledNum class

#include "CvGameCoreDLL.h"
#include "ScaledNum.h"

//#define SCALED_NUM_TEST
#ifdef SCALED_NUM_TEST
#include "TSCProfiler.h"
#include "CvInfo_GameOption.h"

// Can't define these in a function body (need to have linkage)
TYPEDEF_SCALED_ENUM(166320,int,MovementPts) // Divisible by most numbers between 1 and 30
TYPEDEF_SCALED_ENUM(1024,int,CurrCombatStr)
#endif

/*  To be called once XML data has been loaded. (Need some test data that is unknown
	at compile time.) */
void TestScaledNum()
{
#ifndef SCALED_NUM_TEST
	return;
#else
	// These numbers match the running example commented on in pow.
	//FAssert(scaled(fixp(5.2)).pow(scaled(fixp(2.1))).round() == 32);
	// The example assumes scale 1024, hence the explicit calls. */
	FAssert(ScaledNum<1024>(
			ScaledNum<1024>::fromRational<(int)(5.2 * 10000 + 0.5), 10000>()).
			pow(ScaledNum<1024>(
			ScaledNum<1024>::fromRational<(int)(2.1 * 10000 + 0.5), 10000>())).
			round() == 32);

	// Spotty unit test (tbd.: improve coverage; especially: IntType short, char)
	FAssert((fixp(4/3.) * 1000).round() == 1333);
	FAssert(scaled(0) == per100(0));
	FAssert(fixp(-0.3125) * 1024 == -320);
	FAssert(per1000(2254u).getPercent() == 225);
	FAssert(per10000(22547u).getPermille() == 2255);
	int iSuccesses = 0;
	CvRandom& kRand = GC.getASyncRand();
	for(int i = 0; i < 1000; i++)
		if(fixp(0.4).randSuccess(kRand, ""))
			iSuccesses++;
	FAssertBounds(355, 445, iSuccesses);
	scaled rSum;
	for (int i = 0; i < 20; i++)
		rSum += scaled::hash(i);
	FAssert(rSum.approxEquals(10, fixp(3.5)));
	FAssert(scaled(2).pow(10) == 1024);
	FAssert(scaled(10).pow(-2) == per100(1));
	FAssert((scaled(2).sqrt() * 100).round() == 141);
	FAssert((fixp(0.3).pow(fixp(1.7))*100).round() == 13);
	FAssert(scaled(24).pow(0) == 1);
	FAssert(scaled(0).pow(24) == 0);
	FAssert(scaled(-2).pow(3) == -8);
	scaled rTest = fixp(2.4);
	rTest.increaseTo(3);
	FAssert(rTest == 3);
	// The exact result would be 4.5/1024
	FAssert(ScaledNum<100>(30,100) * ScaledNum<1024>(15,1024) == ScaledNum<1024>(5,1024));
	// If multiplication was performed like this, we'd get 4/1024:
	FAssert(ScaledNum<1024>(ScaledNum<100>(30,100)) *
			ScaledNum<1024>(15,1024) == ScaledNum<1024>(4,1024));
	// Now force a result on the smaller scale:
	ScaledNum<100> rTestPerc = fixp(0.3);
	rTestPerc *= ScaledNum<1024>(15,1024);
	FAssert(rTestPerc == 0);
	rTest.decreaseTo(scaled(1, 2));
	FAssert(rTest == fixp(0.5));
	rTest.clamp(1, 2);
	FAssert(rTest == 1);
	FAssert(rTest >= 1);
	FAssert(rTest <= 1);
	FAssert(rTest * fixp(0.93) < 1);
	FAssert(rTest < fixp(1.01));
	FAssert(rTest > fixp(0.999));
	FAssert(rTest.approxEquals(fixp(1.01), fixp(0.05)));
	rTest -= fixp(2.5);
	FAssert(rTest.approxEquals(fixp(-1.5), fixp(0.01)));
	rTest = per100(250u);
	rTest.mulDiv(4, 5);
	FAssert(rTest == 2);
	FAssert(std::strcmp(scaled(2).str(100), "200 percent") == 0);
	FAssert(std::strcmp(ScaledNum<1024>(2).str(), "2048/1024") == 0);
	FAssert(std::strcmp(scaled(2).str(1), "2") == 0);
	FAssert(std::strcmp(fixp(2.2).str(1), "ca. 2") == 0);
	FAssert(scaled(42).roundToMultiple(5) == 40);
	FAssert(scaled(-43).roundToMultiple(5) == -45);
	FAssert(scaled().ceil() == 0);
	FAssert(scaled(1).ceil() == 1);
	FAssert(scaled(-2).ceil() == -2);
	FAssert(fixp(2.001).ceil() == 3);
	FAssert(fixp(2.5).ceil() == 3);
	FAssert(fixp(2.75).ceil() == 3);
	FAssert(fixp(-9.2).ceil() == -9);
	FAssert(fixp(-9.99).ceil() == -9);

	// Allowed: operations that mix the default EnumType (int) with a non-default EnumType
	MovementPts rMoves = fixp(1.5); // Construction from other
	FAssert(scaled(rMoves).ceil() == 2);
	FAssert(rMoves == scaled(3, 2));  // comparisons
	FAssert(scaled(1) < rMoves);
	FAssert(rMoves - 1 == MovementPts(1, 2)); // global arithmetic operators
	rTest = rMoves + 1;
	FAssert(rTest + rMoves == 2 * rMoves + 1);
	rMoves = MovementPts(1) + MovementPts(2);
	rMoves *= scaled(3, 2); // arithmetic assignment operators
	rTest /= rMoves;
	CurrCombatStr rCombat = fixp(4.9);
	// Will fail static assertions: Mixing different non-default EnumTypes
	//rMoves = rCombat; // !
	//rMoves = rCombat + scaled(1); // ! (global operators preserve EnumType)
	//rMoves == rCombat; // !
	//CurrCombatStr(rMoves).ceil(); // !
	//rMoves *= rCombat; // !
	//rCombat + rMoves; // !
	rMoves = rCombat.convert(); // Explicit cast
	/*	rMoves can't represent rCombat's value exactly b/c of different scales,
		but comparisons are exact. */
	FAssert(rMoves.approxEquals(rCombat.convert(), fixp(0.001)));
	// Types smaller than int (tbd.: more tests)
	ScaledNum<128,short> rTestShort = fixp(1/3.);
	FAssert((rTestShort * 30).round() == 10);
	rTestShort = 1;
	rTest = rTestShort;
	FAssert(rTest == rTestShort);
	ScaledNum<100,unsigned char> rTestUChar;
	rTestUChar = rTestShort;
	rTest -= rTestUChar;
	/*	Almost works, but there really is no point in using an enum as the IntType.
		What doesn't work is the initialization of MAXÌNT and MININT. */
	//ScaledNum<1024,PlayerTypes> rEnum;
	//rEnum = rTest;
	//rEnum *= 3; // ! Failed runtime assertion due to MAXINT==0

	/*	Will do something "non-const" at the end based on the value of iDummy.
		To prevent the compiler from discarding code, results of test computations
		can be added to iDummy. */
	int iDummy = scaled(1, 2).round();

	// This should use only 32-bit numbers and no int divisions
	ScaledNum<4096,unsigned short> rFastPow(423, 1000);
	rFastPow.exponentiate(3);
	FAssert(rFastPow.approxEquals(fixp(0.075686), fixp(0.0005)));
	iDummy += rFastPow.round();

	// Ensure that even extremely high scale factors don't overflow on mulDiv
	uscaled rAlmostSqrtOfTwo = scaled(2).sqrt() - scaled::epsilon();
	ScaledNum<MAX_INT,uint> r1 = rAlmostSqrtOfTwo;
	ScaledNum<MAX_INT - 1,uint> r2 = rAlmostSqrtOfTwo;
	FAssert(r2.MAX == 2);
	r2 *= r1;
	// (But an approxEquals check isn't possible so close to r2.MAX)
	FAssert(r2 > fixp(1.99));
	FAssert(r2 < 2);

	// Speed measurements
	// (CPU cycles noted in comments can be out of date)
	// Exponentiation speed measurements
	{
		scaled rSum = 0;
		for (int i = 0; i < 10; i++)
		{
			// Result (average over 10 samples): 7384 cycles on the first launch
			// after compilation. Then 4568 on the next launch, 4688, 4975.
			// Due to cache? But std::pow shows a similar pattern ...
			//TSC_PROFILE("POW_SCALED");
			for (int j = i; j < 10; j++)
			{
				scaled b = per100(GC.getInfo((TechTypes)0).getResearchCost() + j);
				rSum += b.pow(fixp(1.24));
			}
		}
		iDummy += rSum.round();
		double dSum = 0;
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("POW_DOUBLE"); // Results (averages): 9357, 5423, 4915, 4989 cycles
			for (int j = i; j < 10; j++)
			{
				double b = (GC.getInfo((TechTypes)0).getResearchCost() + j) / 100.0;
				dSum += std::pow(b, 1.24);
			}
		}
		iDummy += fmath::round(dSum);
	}

	// Addition speed measurements
	{
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("ADDITION_INT"); // Result: 180 cycles on average
			int x = GC.getInfo((TechTypes)0).getResearchCost();
			int y = GC.getInfo((TechTypes)1).getResearchCost();
			int z = 0;
			for (int j = i; j < 10; j++)
			{
				z += x + j;
				z -= y - j;
			}
			iDummy += z;
		}
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("ADDITION_SCALED"); // Result: 272 cycles on average
			scaled x = GC.getInfo((TechTypes)0).getResearchCost();
			int y = GC.getInfo((TechTypes)1).getResearchCost(); // Mix it up a bit
			scaled z = 0;
			for (int j = i; j < 10; j++)
			{
				z += x + j;
				z -= y - j;
			}
			iDummy += z.round();
		}
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("ADDITION_DOUBLE"); // Result: 406 cycles on average
			double x = GC.getInfo((TechTypes)0).getResearchCost();
			int y = GC.getInfo((TechTypes)1).getResearchCost();
			double z = 0;
			for (int j = i; j < 10; j++)
			{
				z += x + j;
				z -= y - j;
			}
			iDummy += fmath::round(z);
		}
	}

	// Modifier speed measurements; inspired by CvTeam::getResearchCost.
	{
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("MODIFIERS_BTS_STYLE"); // Result: 927 cycles on average
			int iCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				iCost += j;
				iCost *= GC.getInfo((HandicapTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= GC.getInfo((HandicapTypes)0).getAIResearchPercent();
				iCost /= 100;
				EraTypes eTechEra = (EraTypes)GC.getInfo((TechTypes)0).getEra();
				iCost *= (100 + GC.getInfo(eTechEra).getTechCostModifier());
				iCost /= 100;
				iCost *= GC.getInfo((WorldSizeTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= GC.getInfo((SeaLevelTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= 105;
				iCost /= 100;
				iCost *= GC.getInfo((GameSpeedTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= GC.getInfo((EraTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= (GC.getDefineINT(CvGlobals::TECH_COST_EXTRA_TEAM_MEMBER_MODIFIER) + 100);
				iCost /= 100;
				iCost -= iCost % 5;
				iCost = range(iCost, 10, 2000);
			}
			iDummy += iCost;
		}
	}
	{
		for (int i = 0; i < 10; i++)
		{
			//	Result: 2855 cycles on average with MulDiv. 3932 with cast to __int64.
			//	1584 for scaled_uint, 1045 for scaled_uint w/o overflow handling.
			//	892 if the per100 arguments are also cast to uint.
			//TSC_PROFILE("MODIFIERS_SCALED");
			uscaled rCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				rCost += j;
				rCost *= per100(GC.getInfo((HandicapTypes)0).getResearchPercent());
				rCost *= per100(GC.getInfo((HandicapTypes)0).getAIResearchPercent());
				EraTypes eTechEra = (EraTypes)GC.getInfo((TechTypes)0).getEra();
				rCost *= per100((100 + GC.getInfo(eTechEra).getTechCostModifier()));
				rCost *= per100(GC.getInfo((WorldSizeTypes)0).getResearchPercent());
				rCost *= per100(GC.getInfo((SeaLevelTypes)0).getResearchPercent());
				rCost *= fixp(1.05);
				rCost *= per100(GC.getInfo((GameSpeedTypes)0).getResearchPercent());
				rCost *= per100(GC.getInfo((EraTypes)0).getResearchPercent());
				rCost *= per100((GC.getDefineINT(
						CvGlobals::TECH_COST_EXTRA_TEAM_MEMBER_MODIFIER) + 100));
				int iCost = rCost.roundToMultiple(5);
				rCost = range(iCost, 10, 2000);
			}
			iDummy += rCost.round();
		}
	}
	{
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("MODIFIERS_DOUBLE"); // Result: 659 cycles on average
			double dCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				dCost += j;
				dCost *= GC.getInfo((HandicapTypes)0).getResearchPercent() / 100.;
				dCost *= GC.getInfo((HandicapTypes)0).getAIResearchPercent() / 100.;
				EraTypes eTechEra = (EraTypes)GC.getInfo((TechTypes)0).getEra();
				dCost *= (100 + GC.getInfo(eTechEra).getTechCostModifier()) / 100.;
				dCost *= GC.getInfo((WorldSizeTypes)0).getResearchPercent() / 100.;
				dCost *= GC.getInfo((SeaLevelTypes)0).getResearchPercent() / 100.;
				dCost *= 1.05;
				dCost *= GC.getInfo((GameSpeedTypes)0).getResearchPercent() / 100.;
				dCost *= GC.getInfo((EraTypes)0).getResearchPercent() / 100.;
				dCost *= (GC.getDefineINT(
						CvGlobals::TECH_COST_EXTRA_TEAM_MEMBER_MODIFIER) + 100) / 100.;
				int iCost = fmath::round(dCost) % 5;
				dCost = range(iCost, 10, 2000);
			}
			iDummy += (int)dCost;
		}
	}
	{
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("MODIFIERS_FLOAT"); // Result: 641 cycles on average
			double fCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				fCost += j;
				fCost *= GC.getInfo((HandicapTypes)0).getResearchPercent() / 100.f;
				fCost *= GC.getInfo((HandicapTypes)0).getAIResearchPercent() / 100.f;
				EraTypes eTechEra = (EraTypes)GC.getInfo((TechTypes)0).getEra();
				fCost *= (100 + GC.getInfo(eTechEra).getTechCostModifier()) / 100.f;
				fCost *= GC.getInfo((WorldSizeTypes)0).getResearchPercent() / 100.f;
				fCost *= GC.getInfo((SeaLevelTypes)0).getResearchPercent() / 100.f;
				fCost *= 1.05f;
				fCost *= GC.getInfo((GameSpeedTypes)0).getResearchPercent() / 100.f;
				fCost *= GC.getInfo((EraTypes)0).getResearchPercent() / 100.f;
				fCost *= (GC.getDefineINT(
						CvGlobals::TECH_COST_EXTRA_TEAM_MEMBER_MODIFIER) + 100) / 100.f;
				int iCost = fmath::round(fCost) % 5;
				fCost = range(iCost, 10, 2000);
			}
			iDummy += (int)fCost;
		}
	}

	// More modifier measurements; mostly compile-time constants this time.
	{
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("CONST_MODIFIERS_BTS_STYLE"); // Result: 647 cycles on average
			int iCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				iCost += j;
				iCost *= 125;
				iCost /= 100;
				iCost *= GC.getInfo((HandicapTypes)0).getAIResearchPercent();
				iCost /= 100;
				iCost *= 75;
				iCost /= 100;
				iCost *= 200;
				iCost /= 100;
				iCost *= GC.getInfo((SeaLevelTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= 67;
				iCost /= 100;
				iCost *= GC.getInfo((GameSpeedTypes)0).getResearchPercent();
				iCost /= 100;
				iCost *= 80;
				iCost /= 100;
				iCost = range(iCost, 10, 2000);
			}
			iDummy += iCost;
		}
	}
	{
		for (int i = 0; i < 10; i++)
		{
			//	Result: 2087 cycles on average (scaled w/ MulDiv).
			//	672 for scaled_uint, 579 for scaled_uint w/o overflow handling.
			//	394 if the per100 arguments are also cast to uint.
			//TSC_PROFILE("CONST_MODIFIERS_SCALED");
			scaled rCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				rCost += j;
				rCost *= per100(125);
				rCost *= per100(GC.getInfo((HandicapTypes)0).getAIResearchPercent());
				rCost *= per100(75);
				rCost *= per100(200);
				rCost *= per100(GC.getInfo((SeaLevelTypes)0).getResearchPercent());
				rCost *= fixp(2/3.);
				rCost *= per100(GC.getInfo((GameSpeedTypes)0).getResearchPercent());
				rCost *= per100(80);
				rCost.clamp(10, 2000);
			}
			iDummy += rCost.round();
		}
	}
	{
		for (int i = 0; i < 10; i++)
		{
			//TSC_PROFILE("CONST_MODIFIERS_DOUBLE"); // Result: 491 cycles on average
			double dCost = GC.getInfo((TechTypes)0).getResearchCost();
			for (int j = i; j < 10; j++)
			{
				dCost += j;
				dCost *= 1.25;
				dCost *= GC.getInfo((HandicapTypes)0).getAIResearchPercent() / 100.;
				dCost *= 0.75;
				dCost *= 2.;
				dCost *= GC.getInfo((SeaLevelTypes)0).getResearchPercent() / 100.;
				dCost *= 2/3.;
				dCost *= GC.getInfo((GameSpeedTypes)0).getResearchPercent() / 100.;
				dCost *= 0.8;
				dCost = dRange(dCost, 10, 2000);
			}
			iDummy += (int)dCost;
		}
	}
	/*	This will always be false, but the compiler can't tell.
		See comment near the definition of iDummy. */
	if (iDummy == -7)
	{
		FAssert(false);
		CvGlobals::getInstance().getLogging() = true;
	}
#endif // SCALED_NUM_TEST
}
