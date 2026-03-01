#include "CvGameCoreDLL.h"
#include "MilitaryBranch.h"
#include "UWAIAgent.h"
#include "CoreAI.h"
#include "CvCity.h"

using std::ostream;
using std::vector;

// static factory
MilitaryBranch* MilitaryBranch::create(MilitaryBranchTypes eBranch, PlayerTypes eOwner)
{
	switch(eBranch)
	{
	case HOME_GUARD: return new MilitaryBranch::HomeGuard(eOwner);
	case ARMY: return new MilitaryBranch::Army(eOwner);
	case FLEET: return new MilitaryBranch::Fleet(eOwner);
	case LOGISTICS: return new MilitaryBranch::Logistics(eOwner);
	case CAVALRY: return new MilitaryBranch::Cavalry(eOwner);
	case NUCLEAR: return new MilitaryBranch::NuclearArsenal(eOwner);
	default: FErrorMsg("Unknown military branch type"); return NULL;
	}
}


MilitaryBranch::MilitaryBranch(PlayerTypes eOwner)
:	m_eOwner(eOwner), m_eTypicalUnit(NO_UNIT), m_iUnits(0),
	m_bCanBombard(false), m_bCanSoften(false)
{}


void MilitaryBranch::write(FDataStreamBase* pStream) const
{
	int iSaveVersion;
	//iSaveVersion = 0;
	iSaveVersion = 1; // scaled instead of double
	/*	I hadn't thought of a version number in the initial release. Need
		to fold it into m_eTypicalUnit now to avoid breaking compatibility.
		Add 1 b/c the typical unit can be -1. */
	pStream->Write(m_eTypicalUnit + 1 + 1000 * iSaveVersion);
	m_rTypicalPower.write(pStream);
	m_rTotalPower.write(pStream);
	pStream->Write(m_iUnits);
	pStream->Write(m_bCanBombard);
	pStream->Write(m_bCanSoften);
}


void MilitaryBranch::read(FDataStreamBase* pStream)
{
	int iSaveVersion;
	{
		int iTmp;
		pStream->Read(&iTmp);
		iSaveVersion = iTmp / 1000;
		if (iSaveVersion <= 0)
			m_eTypicalUnit = (UnitTypes)iTmp;
		else m_eTypicalUnit = (UnitTypes)((iTmp % 1000) - 1);
	}
	if (iSaveVersion < 1)
	{
		double dTypicalPower, dTotalPower;
		pStream->Read(&dTypicalPower);
		pStream->Read(&dTotalPower);
		m_rTypicalPower = scaled::fromDouble(dTypicalPower);
		m_rTotalPower = scaled::fromDouble(dTotalPower);
	}
	else
	{
		m_rTypicalPower.read(pStream);
		m_rTotalPower.read(pStream);
	}
	pStream->Read(&m_iUnits);
	pStream->Read(&m_bCanBombard);
	pStream->Read(&m_bCanSoften);
}


void MilitaryBranch::updateTypicalUnit()
{
	PROFILE_FUNC();

	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	scaled rBestValue;
	CvCivilization const& kCiv = kOwner.getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes const eUnit = kCiv.unitAt(i);
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);
		// Siege and air units count for power but aren't typical
		if (kUnit.getCombat() <= 0 || kUnit.getCombatLimit() < 100 ||
			!isValidDomain(eUnit) || kUnit.getDomainType() == DOMAIN_AIR ||
			kUnit.getDomainType() == DOMAIN_IMMOBILE)
		{
			continue;
		}
		UnitClassTypes const eUnitClass = CvCivilization::unitClass(eUnit);
		/*	I may want to give some combat unit (e.g. War Elephant) a national limit
			or an instance cost modifier at some point */
		CvUnitClassInfo const& kUnitClass = GC.getInfo(eUnitClass);
		{
			int iNationalLimit = kUnitClass.getMaxPlayerInstances();
			if (iNationalLimit >= 0 &&
				iNationalLimit < (GC.AI_getGame().AI_getCurrEraFactor() + 1) * 4)
			{
				continue;
			}
		}
		if (kUnitClass.getInstanceCostModifier() >= 20)
			continue;
		/*	Could call this for land units as well, but relying on the capital for
			those is faster, and perhaps more accurate as well. */
		if (kUnit.getDomainType() == DOMAIN_SEA)
		{
			if (!GET_TEAM(kOwner.getTeam()).AI_isExpectingToTrain(kOwner.getID(), eUnit))
				continue;
		}
		else
		{
			if (!kOwner.hasCapital() ||
				!kOwner.getCapital()->canTrain(eUnit, false, false, false, false,
				true)) // Ignore air unit cap
			{
				continue;
			}
		}
		/*	Normally apply situational modifiers only in simulation steps;
			use them here only in order to determine the most suitable unit
			for a given job. */
		scaled const rUnitPow = unitPower(eUnit, true);
		if (rUnitPow <= 0)
			continue;
		scaled rUtility = unitUtility(eUnit, rUnitPow);
		scaled rProductionCost = estimateProductionCost(eUnit);
		if (rProductionCost <= 0)
			continue;
		scaled rLoopValue = rUtility / rProductionCost;
		if (rLoopValue > rBestValue)
		{
			rBestValue = rLoopValue;
			m_rTypicalPower = unitPower(eUnit, false);
			m_eTypicalUnit = eUnit;
		}
	}
}


void MilitaryBranch::NuclearArsenal::updateTypicalUnit()
{
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	if (!kOwner.hasCapital())
		return;
	scaled rBestValue;
	CvCivilization const& kCiv = kOwner.getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		if (!kOwner.getCapitalCity()->canTrain(eUnit))
			continue;
		scaled const rPow = unitPower(eUnit, true);
		if (rPow <= 0)
			continue;
		scaled rUtility = unitUtility(eUnit, rPow);
		scaled rProductionCost = estimateProductionCost(eUnit);
		if (rProductionCost <= 0)
			continue;
		scaled rLoopValue = rUtility / rProductionCost;
		if (rLoopValue > rBestValue)
		{
			rBestValue = rLoopValue;
			m_rTypicalPower = unitPower(eUnit, false);
			m_eTypicalUnit = eUnit;
		}
	}
}


scaled MilitaryBranch::getTypicalPower(TeamTypes eObserver) const
{
	if (canKnowTypicalUnit(eObserver))
		return m_rTypicalPower;
	return m_rTypicalPower * fixp(0.8); // Underestimate power
}


scaled MilitaryBranch::getTypicalCost(TeamTypes eObserver) const
{
	if (m_eTypicalUnit == NO_UNIT)
		return -1;
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	scaled rCost = kOwner.getProductionNeeded(getTypicalUnit(),
			estimateExtraInstances(kOwner.AI_getCurrEraFactor()).uround());
	if (canKnowTypicalUnit(eObserver))
		return rCost;
	return rCost * fixp(0.85); // Underestimate cost
}


bool MilitaryBranch::canKnowTypicalUnit(TeamTypes eObserver) const
{
	if (eObserver == NO_TEAM || TEAMID(m_eOwner) == eObserver ||
		getTypicalUnit() == NO_UNIT)
	{
		return true;
	}
	CvUnitInfo const& kTypicalUnit = GC.getInfo(getTypicalUnit());
	if (kTypicalUnit.getPrereqAndTech() != NO_TECH) // Warrior
		return true;
	/*	Could keep track of seen units (per other player) in CvPlayerAI::
		AI_doEnemyUnitData -- however, in theory, it should be possible to infer
		completed units from changes in the power curve (maybe also techs
		from changes in score), and letting the AI cheat here is actually to
		the advantage of human players that want to deter the AI in the early game. */
	if(GET_PLAYER(m_eOwner).getUnitClassCount(kTypicalUnit.getUnitClassType()) > 0)
		return true; // The unit's in the wild
	for (MemberIter itObs(eObserver); itObs.hasNext(); ++itObs)
	{
		if (itObs->canSeeTech(m_eOwner))
			return true; // Tech visible on Foreign Advisor
	}
	return false;
}


scaled MilitaryBranch::estimateProductionCost(UnitTypes eUnit)
{
	scaled rCost = GC.getInfo(eUnit).getProductionCost();
	UnitClassTypes const eUnitClass = GC.getInfo(eUnit).getUnitClassType();
	/*	CvPlayer::getProductionNeeded would be needlessly slow. Don't need all
		those modifiers, and we need a projection for InstanceCostModifier anyway. */
	int iInstanceCostMod = GC.getInfo(eUnitClass).getInstanceCostModifier();
	if (iInstanceCostMod > 0)
	{
		rCost *= 1 + (per100(iInstanceCostMod) *
				(GET_PLAYER(m_eOwner).getUnitClassCount(eUnitClass) +
				estimateExtraInstances(GET_PLAYER(m_eOwner).AI_getCurrEraFactor())));
	}
	return rCost;
}


scaled MilitaryBranch::unitPower(UnitTypes eUnit, scaled rBasePower) const
{
	/*	Perhaps CvPlayerAI::AI_unitValue could be used here
		(and in the derived classes). Would have to be tested, might be slow.
		The main point would be future-proofing. */
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	scaled r = rBasePower;
	if (r < 0)
		r = kUnit.getPowerValue();
	/*	A good start. Power values mostly equal combat strength; the
		BtS developers have manually increased the value of first strikers
		(usually +1 power), and considerably decreased the value of units
		that can only defend.
		Collateral damage and speed seem underappreciated. */
	if (kUnit.getCollateralDamage() > 0 && kUnit.getDomainType() == DOMAIN_LAND ||
		kUnit.getMoves() > 1)
	{
		r *= fixp(1.12);
	}
	// Sea units that can't bombard cities are overrated in Unit XML
	if (kUnit.getDomainType() == DOMAIN_SEA && kUnit.getBombardRate() == 0)
		r *= fixp(2/3.);

	/*	The BtS power value for Tactical Nuke seems low (30, same as Tank),
		but considering that the AI isn't good at using nukes tactically, and that
		the strategic value is captured by the Risk WarUtilityAspect, it seems
		just about right. */
	//if(kUnit.isSuicide()) r *= fixp(4/3.); // all missiles

	/*	Combat odds don't increase linearly with strength. Use a power law
		with an exponent between 1.5 and 2 (configured in XML). */
	r.exponentiate(per100(GC.getDefineINT(CvGlobals::POWER_CORRECTION)));
	return r;
}


bool MilitaryBranch::canEmploy(UnitTypes eUnit) const
{
	return (GC.getInfo(eUnit).getCombat() > 0 && isValidDomain(eUnit) &&
			unitPower(eUnit, false) > 0);
}


void MilitaryBranch::reportUnit(UnitTypes eUnit, int iChange)
{
	// (Calling canEmploy could cause unitPower to be called twice)
	if ((GC.getInfo(eUnit).getCombat() > 0 || GC.getInfo(eUnit).isNuke()) &&
		isValidDomain(eUnit))
	{
		scaled rPowChange = unitPower(eUnit, false);
		if (rPowChange > 0)
		{
			rPowChange *= iChange;
			m_rTotalPower += rPowChange;
			m_iUnits += iChange;
		}
	}
}


bool MilitaryBranch::isValidDomain(DomainTypes eDomain) const
{
	return true; // default implementation
}


scaled MilitaryBranch::HomeGuard::initTotals(int iNonNavalUnits,
	scaled rNonNavalPower)
{
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	// Akin to list in CvUnitAI::AI_isCityAIType
	UnitAITypes guardAITypes[] = {
		UNITAI_CITY_DEFENSE,
		UNITAI_CITY_COUNTER,
		UNITAI_DEFENSE_AIR,
		UNITAI_CITY_SPECIAL,
		UNITAI_RESERVE,
	};
	/*	Humans tends to use few and weak garrisons. (However, when fearing an attack
		by a much stronger AI civ, humans may also turtle ...) */
	if (kOwner.isHuman())
		m_iUnits = (fixp(4/3.) * kOwner.getNumCities()).round();
	else
	{
		m_iUnits = 0;
		for (int i = 0; i < ARRAYSIZE(guardAITypes); i++)
			m_iUnits += kOwner.AI_getNumAIUnits(guardAITypes[i]);
		/*	Units with aggressive AI types can be temporarily tied down
			defending cities. So the count based on AI types isn't reliable. */
		m_iUnits = scaled::max(m_iUnits, fixp(10/7.) * kOwner.getNumCities()).round();
	}
	m_iUnits = std::min(m_iUnits, iNonNavalUnits);
	scaled rGuardPortion;
	/*	Splitting rNonNavalPower up based on counted units tends to overestimate
		the power of garrisons because these tend to be cheaper units. On the
		other hand, the AI doesn't put every single non-garrison into its invasion
		stacks, so this may even out. */
	if (iNonNavalUnits > 0)
		rGuardPortion = scaled(m_iUnits, iNonNavalUnits);
	FAssert(rGuardPortion <= 1);
	m_rTotalPower = rNonNavalPower * rGuardPortion;
	return rGuardPortion;
}


bool MilitaryBranch::isValidDomain(UnitTypes eUnit) const
{
	return isValidDomain(GC.getInfo(eUnit).getDomainType());
}


bool MilitaryBranch::HomeGuard::isValidDomain(DomainTypes eDomain) const
{
	return (eDomain == DOMAIN_LAND || eDomain == DOMAIN_AIR);
}


bool MilitaryBranch::Army::isValidDomain(DomainTypes eDomain) const
{
	return (eDomain == DOMAIN_LAND || eDomain == DOMAIN_AIR || eDomain == DOMAIN_IMMOBILE);
}


bool MilitaryBranch::Fleet::isValidDomain(DomainTypes eDomain) const
{
	return (eDomain == DOMAIN_SEA);
}


bool MilitaryBranch::Cavalry::isValidDomain(DomainTypes eDomain) const
{
	return (eDomain == DOMAIN_LAND);
}


scaled MilitaryBranch::HomeGuard::unitPower(UnitTypes eUnit, bool bModify) const
{
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	scaled rBasePow = kUnit.getPowerValue();
	if (bModify)
	{
		if (kUnit.isNoDefensiveBonus())
			rBasePow *= fixp(2/3.);
		scaled rDefMod = 1 + per100(kUnit.getCityDefenseModifier());
		// Prefer potential garrisons
		FOR_EACH_ENUM(Promotion)
		{
			CvPromotionInfo const& kPromo = GC.getInfo(eLoopPromotion);
			if (kPromo.getCityDefensePercent() >= 20 &&
				kPromo.getUnitCombat(kUnit.getUnitCombatType()))
			{
				rDefMod += fixp(0.1);
				break;
			}
		}
		rBasePow *= rDefMod;
	}
	return MilitaryBranch::unitPower(eUnit, rBasePow);
}

// Utility equals power by default
scaled MilitaryBranch::unitUtility(UnitTypes, scaled rPower) const
{
	return rPower;
}


scaled MilitaryBranch::Logistics::unitUtility(UnitTypes eUnit, scaled rPower) const
{
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	return kUnit.getCargoSpace() + kUnit.getCombat() + kUnit.getMoves() +
			(GET_PLAYER(m_eOwner).AI_isAnyImpassable(eUnit) ? 0 : 5);
}


scaled MilitaryBranch::Army::unitPower(UnitTypes eUnit, bool bModify) const
{
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	// (Do include nukes in army)
	/*if (kUnit.isNuke())
		return -1;*/
	scaled rBasePow = kUnit.getPowerValue();
	if (bModify)
	{
		if (kUnit.isMostlyDefensive()) // advc.315
			return -1;
		// Prefer potential city raiders
		FOR_EACH_ENUM(Promotion)
		{
			CvPromotionInfo const& kPromo = GC.getInfo(eLoopPromotion);
			if (kPromo.getCityAttackPercent() >= 20 &&
				kPromo.getUnitCombat(kUnit.getUnitCombatType()))
			{
				rBasePow *= fixp(1.1);
				break;
			}
		}
		/*	Military power is already biased toward aggression.
			No further adjustments needed. */
	}
	return MilitaryBranch::unitPower(eUnit, rBasePow);
}


scaled MilitaryBranch::Cavalry::unitPower(UnitTypes eUnit, bool bModify) const
{
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	if (kUnit.getMoves() <= 1 || kUnit.getProductionCost() >= 150 ||
		kUnit.isMostlyDefensive()) // advc.315
	{
		return -1;
	}
	return MilitaryBranch::unitPower(eUnit);
}


scaled MilitaryBranch::Fleet::unitPower(UnitTypes eUnit, bool bModify) const
{
	scaled rPow = MilitaryBranch::unitPower(eUnit);
	if (bModify && GET_PLAYER(m_eOwner).AI_isAnyImpassable(eUnit))
		rPow /= 2;
	return rPow;
}


scaled MilitaryBranch::Logistics::unitPower(UnitTypes eUnit, bool bModify) const
{
	if (GC.getInfo(eUnit).getSpecialCargo() == NO_SPECIALUNIT)
		/*	This would include carriers and subs in Logistics. But I think
			only proper transport ships should count b/c aircraft can't
			conquer cities. */
		//|| GC.getInfo(eUnit).getDomainCargo() == DOMAIN_AIR)
	{
		return GC.getInfo(eUnit).getCargoSpace();
	}
	return -1;
}


scaled MilitaryBranch::NuclearArsenal::unitPower(UnitTypes eUnit, bool bModify) const
{
	CvUnitInfo const& kUnit = GC.getInfo(eUnit);
	if (!kUnit.isNuke())
		return -1; // Disregard non-nuke units
	scaled rBasePow = kUnit.getPowerValue();
	/*	bModify should only be used for picking the typical unit. Make sure
		that ICBM gets chosen over TN despite costing twice as much b/c the
		AI tends to invest more in ICBM than TN. */
	if (bModify && kUnit.getAirRange() == 0)
		rBasePow *= fixp(2.1);
	return MilitaryBranch::unitPower(eUnit, rBasePow);
}


void MilitaryBranch::Army::setTotals(int iUnits, scaled rTotalPow)
{
	m_iUnits = iUnits;
	m_rTotalPower = rTotalPow;
}


void MilitaryBranch::Army::updateTypicalUnit()
{
	MilitaryBranch::updateTypicalUnit();
	updateCanBombard();
	updateCanSoften();
}


void MilitaryBranch::Fleet::updateTypicalUnit()
{
	MilitaryBranch::updateTypicalUnit();
	if (getTypicalUnit() != NO_UNIT)
		m_bCanBombard = (GC.getInfo(getTypicalUnit()).getBombardRate() > 0);
}


void MilitaryBranch::Army::updateCanBombard()
{
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	CvCivilization const& kCiv = kOwner.getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);
		if (((kUnit.getBombardRate() > 0 && kUnit.getDomainType() == DOMAIN_LAND) ||
			(kUnit.getBombardRate() > 0 && kUnit.getDomainType() == DOMAIN_AIR)) &&
			GET_TEAM(kOwner.getTeam()).AI_isExpectingToTrain(kOwner.getID(), eUnit))
		{
			m_bCanBombard = true;
			return;
		}
	}
	m_bCanBombard = false;
}

/*	(Perhaps need such a function for Cavalry as well
	in case that a mod ever gives Cav coll. dmg. or a similar ability). */
void MilitaryBranch::Army::updateCanSoften()
{
	CvPlayerAI const& kOwner = GET_PLAYER(m_eOwner);
	CvCivilization const& kCiv = kOwner.getCivilization();
	for (int i = 0; i < kCiv.getNumUnits(); i++)
	{
		UnitTypes eUnit = kCiv.unitAt(i);
		CvUnitInfo const& kUnit = GC.getInfo(eUnit);
		if (kUnit.getCollateralDamage() > 0 &&
			isValidDomain(kUnit.getDomainType()) &&
			/*	Usually it takes the AI a while to assemble a significant number
				of coll.-dmg. units after discovering the respective tech, so
				let's delay things a bit with this (cheap) extra check. */
			kOwner.getUnitClassCountPlusMaking(kCiv.unitClass(eUnit)) > 1 &&
			GET_TEAM(kOwner.getTeam()).AI_isExpectingToTrain(kOwner.getID(), eUnit))
		{
			m_bCanSoften = true;
			return;
		}
	}
	m_bCanSoften = false;
}


ostream& operator<<(ostream& os, MilitaryBranch const& kBranch)
{
	return kBranch.out(os);
}

ostream& MilitaryBranch::out(ostream& os) const
{
	return os << str();
}

char const* MilitaryBranch::m_aszDebugStrings[] = {
	"Guard", "Army", "Fleet", "Logistics", "Cavalry",
	"Nuclear", "(unknown branch)"
};

char const* MilitaryBranch::str() const
{
	return m_aszDebugStrings[getID()];
}

MilitaryBranchTypes MilitaryBranch::getID() const
{
	return NUM_BRANCHES;
}

MilitaryBranchTypes MilitaryBranch::Army::getID() const
{
	return ARMY;
}

MilitaryBranchTypes MilitaryBranch::HomeGuard::getID() const
{
	return HOME_GUARD;
}

MilitaryBranchTypes MilitaryBranch::Fleet::getID() const
{
	return FLEET;
}

MilitaryBranchTypes MilitaryBranch::Logistics::getID() const
{
	return LOGISTICS;
}

MilitaryBranchTypes MilitaryBranch::Cavalry::getID() const
{
	return CAVALRY;
}

MilitaryBranchTypes MilitaryBranch::NuclearArsenal::getID() const
{
	return NUCLEAR;
}

char const* MilitaryBranch::str(MilitaryBranchTypes eBranch)
{
	if (eBranch < 0 || eBranch > NUM_BRANCHES)
		eBranch = NUM_BRANCHES;
	return m_aszDebugStrings[eBranch];
}
