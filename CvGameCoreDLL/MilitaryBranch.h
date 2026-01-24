#pragma once

#ifndef MILITARY_BRANCH_H
#define MILITARY_BRANCH_H

/*	advc.104: New class hierarchy. Breaking military power values down into
	branches such as Army and Fleet helps the AI analyze its military prospects. */


/*	Containers of military branches should be laid out in this order.
	Can then access a specific branch using these enumerators. */
enum MilitaryBranchTypes
{
	HOME_GUARD = 0,
	ARMY,
	FLEET,
	LOGISTICS,
	CAVALRY,
	NUCLEAR,
	NUM_BRANCHES
};

class MilitaryBranch
{
public:
	// Factory; caller will own the instance.
	static MilitaryBranch* create(MilitaryBranchTypes eBranch, PlayerTypes eOwner);
	MilitaryBranch(PlayerTypes eOwner);
	virtual ~MilitaryBranch() {}
	// Can't do this in the constructor b/c virtual functions need to be called
	virtual void updateTypicalUnit();

	// Debug output. Derived classes override the (polymorphic) getID function.
	friend std::ostream& operator<<(std::ostream& os, MilitaryBranch const& kBranch);
	virtual char const* str() const;
	virtual MilitaryBranchTypes getID() const;
	// Debug string from enum type
	static char const* str(MilitaryBranchTypes eBranch);

	// Replacing CvPlayer::getTypicalUnitValue
	UnitTypes getTypicalUnit(TeamTypes eOberserver = NO_TEAM) const
	{
		return m_eTypicalUnit;
	}
	scaled getTypicalPower(TeamTypes eOberserver = NO_TEAM) const;
	scaled getTypicalCost(TeamTypes eOberserver = NO_TEAM) const;
	// Total military power of units in this branch
	scaled power() const { return m_rTotalPower; }
	void changePower(scaled rChange) { m_rTotalPower += rChange; }
	/*	True iff eUnit belongs in this branch (at all).
		The template implementation is based on unitPower. */
	bool canEmploy(UnitTypes eUnit) const;
	/*	To be called when a unit is created or destroyed. For tracking the
		total power of trained units. */
	void reportUnit(UnitTypes eUnit, int iChange);
	int numUnits() const { return m_iUnits; }
	/*  Whether a unit can be trained in this branch that is able to bombard city defenses.
		(To be computed in updateTypicalUnit.) */
	bool canBombard() const { return m_bCanBombard; }
	/*  Whether a unit can be trained in this branch that deals collateral damage
		(or has some other way of softening defenders).
		(To be computed in updateTypicalUnit.) */
	bool canSoftenCityDefenders() const { return m_bCanSoften; }
	/*  Not virtual; all persistent data should be at the base class.
		The copy constructors also assume this. */
	void write(FDataStreamBase* pStream) const;
	void read(FDataStreamBase* pStream);

protected:
	// Caveat: This class relies on its implicitly declared copy ctor
	PlayerTypes m_eOwner;
	UnitTypes m_eTypicalUnit;
	scaled m_rTypicalPower;
	scaled m_rTotalPower;
	int m_iUnits;
	bool m_bCanBombard;
	bool m_bCanSoften;

	/*	Used for selecting a typical unit. The military power of eUnit when employed
		within this branch. Should return -1 if eUnit doesn't fit the branch at all.
		A valid domain and positive combat strength need to be ensured by the caller. */
	virtual scaled unitPower(UnitTypes eUnit, bool bModify) const=0;
	/*	Helper function for the unitPower function above.
		If a non-negative rBasePower is given, then that value replaces
		the iPower value defined for eUnit in XML. */
	scaled unitPower(UnitTypes eUnit, scaled rBasePower = -1) const;
	virtual scaled unitUtility(UnitTypes eUnit, scaled rPower) const;
	// Can any unit in this branch have eDomain?
	virtual bool isValidDomain(DomainTypes eDomain) const;
	// Is eUnit's domain valid for this branch? (Wrapper function.)
	bool isValidDomain(UnitTypes eUnit) const;
	bool canKnowTypicalUnit(TeamTypes eObserver) const;
	scaled estimateProductionCost(UnitTypes eUnit);
	/*	Vague expectation of how many extra instances will have been produced
		when halfway through with the military buildup that this class helps predict.
		(Could get the era from m_eOwner, but don't want to include CvPlayer.h.) */
	scaled estimateExtraInstances(scaled rEraFactor) const
	{
		return fixp(1.75) + fixp(1.25) * rEraFactor;
	}

private:
	std::ostream& out(std::ostream& os) const;
	static char const* m_aszDebugStrings[];

public: // Concrete classes nested
	class Army; class HomeGuard; class Fleet; class Logistics;
	class Cavalry; class NuclearArsenal;
};


/*	Includes air and siege units.
	Does not include units guarding cities (HomeGuard), i.e. the Army
	can be fully deployed in an invasion.
	That said, since HomeGuard can't track units trained, Army also tracks
	guard units. HomeGuard::initTotals will determine how those units are
	split between defensive and offensive duties. setTotals can be used to
	tell the army branch how many non-guard units there are. */
class MilitaryBranch::Army : public MilitaryBranch
{
public:
	Army(PlayerTypes eOwner) : MilitaryBranch(eOwner) {}
	Army(MilitaryBranch const& kBase) : MilitaryBranch(kBase) {}
	void setTotals(int iUnits, scaled rTotalPower);
	void updateTypicalUnit(); // override
	MilitaryBranchTypes getID() const; // override
protected:
	scaled unitPower(UnitTypes eUnit, bool bModify) const; // override
	bool isValidDomain(DomainTypes eDomain) const; // override
private:
	void updateCanBombard();
	void updateCanSoften();
};

/*	City garrisons and defensive aircraft. The AI assumes that the
	HomeGuard is not available for invading other civs.
	HomeGuard mustn't be used for tracking trained units. Instead, use
	initTotals to have HomeGuard compute the current number of guard units
	and their power based on the number and power of all non-naval units
	(which is tracked by the Army branch). */
class MilitaryBranch::HomeGuard : public MilitaryBranch
{
public:
	HomeGuard(PlayerTypes eOwner) : MilitaryBranch(eOwner) {}
	HomeGuard(MilitaryBranch const& kBase) : MilitaryBranch(kBase) {}
	// Returns the portion of guard units in the non-naval force
	scaled initTotals(int iNonNavalUnits, scaled rNonNavalPower);
	MilitaryBranchTypes getID() const; // override
protected:
	scaled unitPower(UnitTypes eUnit, bool bModify) const; // override
	bool isValidDomain(DomainTypes eDomain) const; // override
};

// Any ships with combat strength, including transports.
class MilitaryBranch::Fleet : public MilitaryBranch
{
public:
	Fleet(PlayerTypes eOwner) : MilitaryBranch(eOwner) {}
	Fleet(MilitaryBranch const& kBase) : MilitaryBranch(kBase) {}
	void updateTypicalUnit(); // override
	MilitaryBranchTypes getID() const; // override
protected:
	scaled unitPower(UnitTypes eUnit, bool bModify) const; // override
	bool isValidDomain(DomainTypes eDomain) const; // override
};

/*	Ships for transporting Army units. In theory, transports in other domains
	could work similarly, hence the generic name of the class. Ships transporting
	air units are also included in Logistics (since Army units can be land- or
	air-based).
	"Power" refers to cargo capacity in this class. Cargo units are also
	covered by Fleet, but, in that context, their combat strength is counted. */
class MilitaryBranch::Logistics : public MilitaryBranch
{
public:
	Logistics(PlayerTypes eOwner) : MilitaryBranch(eOwner) {}
	Logistics(MilitaryBranch const& kBase) : MilitaryBranch(kBase) {}
	MilitaryBranchTypes getID() const; // override
protected:
	// Cargo capacity
	scaled unitPower(UnitTypes eUnit, bool bModify) const; // override
	// A mix of capacity and strength
	scaled unitUtility(UnitTypes eUnit, scaled rCargo) const; // override
};

/*	Fast early attackers. Don't have to be mounted (e.g. Impi), but most are.
	Tanks aren't Cavalry b/c fast units mostly lose their special role in the
	later eras b/c of railroads and b/c all units classes become motorized
	eventually. This branch really isn't pulling its weight, but might become
	more useful in the future. (Should perhaps still remove it; it adds a lot
	of complexity to the InvasionGraph class.)
	All Cavalry is also included in Army. */
class MilitaryBranch::Cavalry : public MilitaryBranch
{
public:
	Cavalry(PlayerTypes eOwner) : MilitaryBranch(eOwner) {}
	Cavalry(MilitaryBranch const& kBase) : MilitaryBranch(kBase) {}
	MilitaryBranchTypes getID() const; // override
protected:
	scaled unitPower(UnitTypes eUnit, bool bModify) const; // override
	bool isValidDomain(DomainTypes eDomain) const; // override
};

/*	The usefulness of nukes for winning wars is covered by Army.
	This branch is about the strategic (city-wrecking) element that is
	unique to nukes. */
class MilitaryBranch::NuclearArsenal : public MilitaryBranch
{
public:
	NuclearArsenal(PlayerTypes eOwner): MilitaryBranch(eOwner) {}
	NuclearArsenal(MilitaryBranch const& kBase) : MilitaryBranch(kBase) {}
	MilitaryBranchTypes getID() const; // override
	void updateTypicalUnit(); // override
protected:
	scaled unitPower(UnitTypes eUnit, bool bModify) const; // override
};

#endif
