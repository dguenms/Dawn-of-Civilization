#pragma once

#ifndef CV_INFO_ORGANIZATION_H
#define CV_INFO_ORGANIZATION_H

/*  advc.003x: Cut from CvInfos.h; CvReligionInfo and CvCorporationInfo. To be
	precompiled. (Changes are very rare, in fact, no changes by mods at all so far.) */

/*  advc.003x: Common base class to reduce code duplication. Just the stuff that
	was exactly the same in CvReligionInfo and CvCorporationInfo. */
class CvOrganizationInfo : public CvHotkeyInfo
{
	typedef CvHotkeyInfo base_t;
public: // All the const functions are exposed to Python
	CvOrganizationInfo();

	wchar getChar() const; // advc: return wchar (not int)
	void setChar(/* advc: */ wchar wc);
	TechTypes getTechPrereq() const { return m_eTechPrereq; }
	UnitClassTypes getFreeUnitClass() const { return m_eFreeUnitClass; }
	int getSpreadFactor() const { return m_iSpreadFactor; }
	MissionTypes getMissionType() const { return m_eMissionType; }
	void setMissionType(int iNewType);

	const TCHAR* getMovieFile() const;
	const TCHAR* getMovieSound() const;
	const TCHAR* getSound() const;

	bool read(CvXMLLoadUtility* pXML);

protected:
	wchar m_wcSymbol; // advc
	TechTypes m_eTechPrereq;
	UnitClassTypes m_eFreeUnitClass;
	MissionTypes m_eMissionType;
	int m_iSpreadFactor;

	CvString m_szMovieFile;
	CvString m_szMovieSound;
	CvString m_szSound;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvReligionInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvReligionInfo : public CvOrganizationInfo
{
public: // All the const functions are exposed to Python
	CvReligionInfo();
	~CvReligionInfo();

	wchar getHolyCityChar() const;
	void setHolyCityChar(wchar c);
	int getNumFreeUnits() const;

	const TCHAR* getTechButton() const;
	const TCHAR* getGenericTechButton() const;
	const TCHAR* getButtonDisabled() const;

	const wchar* getAdjectiveKey() const;
	std::wstring pyGetAdjectiveKey() { return getAdjectiveKey(); }

	// Array access:

	int getGlobalReligionCommerce(int i) const;
	int* getGlobalReligionCommerceArray() const;
	int getHolyCityCommerce(int i) const;
	int* getHolyCityCommerceArray() const;
	int getStateReligionCommerce(int i) const;
	int* getStateReligionCommerceArray() const;

	bool read(CvXMLLoadUtility* pXML);

	static bool isReligionTech(TechTypes eTech); // advc.003w: Moved from CvGameCoreUtils

protected:
	wchar m_cHolyCityChar; // advc: was int
	int m_iNumFreeUnits;

	CvString m_szTechButton;
	CvString m_szGenericTechButton;
	CvWString m_szAdjectiveKey;

	int* m_paiGlobalReligionCommerce;
	int* m_paiHolyCityCommerce;
	int* m_paiStateReligionCommerce;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvCorporationInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCorporationInfo : public CvOrganizationInfo
{
public: // All the const functions are exposed to Python
	CvCorporationInfo();
	virtual ~CvCorporationInfo();

	wchar getHeadquarterChar() const;
	void setHeadquarterChar(wchar c);
	int getSpreadCost() const { return m_iSpreadCost; }
	int getMaintenance() const { return m_iMaintenance; }
	BonusTypes getBonusProduced() const { return m_eBonusProduced; }

	// Array access:
	int getNumPrereqBonuses() const { return m_aePrereqBonuses.size(); }
	BonusTypes getPrereqBonus(int i) const
	{
		FAssertBounds(0, getNumPrereqBonuses(), i);
		return m_aePrereqBonuses[i];
	}
	int py_getPrereqBonus(int i) const;
	// </advc.003t>
	int getHeadquarterCommerce(int i) const;
	int* getHeadquarterCommerceArray() const;
	int getCommerceProduced(int i) const;
	int* getCommerceProducedArray() const;
	int getYieldProduced(int i) const;
	int* getYieldProducedArray() const;

	bool read(CvXMLLoadUtility* pXML);

	static bool isCorporationTech(TechTypes eTech); // advc.003w: Moved from CvGameCoreUtils; unused.

protected:
	wchar m_cHeadquarterChar; // advc: was int
	int m_iSpreadCost;
	int m_iMaintenance;
	BonusTypes m_eBonusProduced;

	std::vector<BonusTypes> m_aePrereqBonuses; // advc.003t: was int*
	int* m_paiHeadquarterCommerce;
	int* m_paiCommerceProduced;
	int* m_paiYieldProduced;
};

#endif
