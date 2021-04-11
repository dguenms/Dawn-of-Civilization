from VictoryGoals import *
from Locations import *


### CONSTANTS ###

iNumAdditionalVictories = 21
iNumReligiousVictories = iNumReligions + iNumAdditionalVictories
(iPaganism, iSecularism, iAnnunaki, iAsatru, iAtua, iBaalism, iBon, iDruidism, iInti, iMazdaism,
iMugyo, iOlympianism, iPesedjet, iRodnovery, iShendao, iShinto, iTengri, iTeotlMaya, iTeotlAztec, iVedism,
iYoruba) = range(iNumReligions, iNumReligiousVictories)


### GOALS ###

dGoals = {
	iHinduism: (
		DifferentSpecialists(holyCity(iHinduism), 5),
		GoldenAges(3),
		BestPopulationCities(5).religion(iHinduism),
	),
	iZoroastrianism: (
		ResourceCount(iIncense, 6),
		ReligionSpreadPercent(iZoroastrianism, 10),
		CultureLevel(holyCity(iZoroastrianism), iCultureLevelLegendary),
	),
	iJudaism: (
		SpecialistCount(sum(iSpecialistGreatProphet, iSpecialistGreatScientist, iSpecialistGreatStatesman), 15),
		CultureLevel(holyCity(iJudaism), iCultureLevelLegendary),
		AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 6).minority(iJudaism).named("JEWISH_MINORITY_ATTITUDES"),
	),
	iConfucianism: (
		AttitudeCount(AttitudeTypes.ATTITUDE_FRIENDLY, 5).named("FRIENDLY_RELATIONS"),
		CityBuildings(holyCity(iConfucianism), wonders(), 5),
		UnitCombatCount(sum(UnitCombatTypes.UNITCOMBAT_MELEE, UnitCombatTypes.UNITCOMBAT_GUN).join("OR"), 200),
	),
	iTaoism: (
		HealthiestTurns(100),
		ShrineIncome(sum(iConfucianism, iTaoism), 40),
		CultureLevel(holyCity(iTaoism), iCultureLevelLegendary),
	),
	iBuddhism: (
		PeaceTurns(100),
		HappiestTurns(100),
		AllAttitude(AttitudeTypes.ATTITUDE_CAUTIOUS),
	),
	iOrthodoxy: (
		BuildingCount(iOrthodoxCathedral, 4),
		BestCultureCities(5).religion(iOrthodoxy),
		NoStateReligion(iCatholicism),
	),
	iCatholicism: (
		PopeTurns(100),
		All(
			# Orthodox shrine?
			BuildingCount(iCatholicShrine),
			SpecialistCount(iSpecialistGreatProphet, 12).religion(iCatholicism),
		),
		WorldPercent(50).religion(iCatholicism),
	),
	iIslam: (
		ReligionSpreadPercent(iIslam, 40),
		CitySpecialistCount(holyCity(iIslam), great_people(), 7),
		BuildingCount(religious_buildings(shrine).named("SHRINES"), 5),
	),
	iProtestantism: (
		FirstDiscovered(iCivilLiberties, iSocialContract, iEconomics),
		SpecialistCount((iSpecialistGreatMerchant, 5), (iSpecialistGreatEngineer, 5)).religion(iProtestantism),
		StateReligionPercent(iProtestantism, 50).orSecular().named("HALF_PROTESTANT_OR_SECULAR"),
	),
	iPaganism: (
		BuildingCount(iPaganTemple, 15).world(),
		NoReligionPercent(50).named("HALF_NO_RELIGION"),
	),
	iSecularism: (
		BuildingCount(religious_buildings(cathedral).named("CATHEDRALS"), 7).named("ALL_CATHEDRALS"),
		All(
			BuildingCount(iUniversity, 25),
			SpecialistCount(
				(iSpecialistGreatScientist, 10),
				(iSpecialistGreatStatesman, 10),
			),
		).secular(),
		BestTechPlayers(5).secular(),
	),
}

dAdditionalPaganGoal = {
	iAnnunaki: BestWonderCity(capital()),
	iAsatru: UnitLevelCount(5, 5),
	iAtua: All(
		ResourceCount(iPearls, 4),
		TerrainCount(iOcean, 50),
	),
	iBaalism: BestTradeIncomeCity(capital()),
	iBon: PeakCount(50),
	iDruidism: FeatureCount(sum(iForest, iMud), 20),
	iInti: GoldPercent(50).named("HALF_WORLD_GOLD"),
	iMazdaism: ResourceCount(iIncense, 6),
	iMugyo: BestSpecialistCity(capital(), great_people()),
	iOlympianism: BuildingCount(pagan_wonders(), 7),
	iPesedjet: Some(FirstGreatPerson(*lGreatPeople), 3).named("FIRST_GREAT_PEOPLE"),
	iRodnovery: ResourceCount(iFur, 7),
	iShendao: PopulationPercent(25),
	iShinto: CitySpecialistCount(capital(), iSpecialistGreatSpy, 3),
	iTengri: ResourceCount(iHorse, 8),
	iTeotlMaya: CombatFood(50),
	iTeotlAztec: SacrificeHappiness(10),
	iVedism: CelebrateTurns(100),
	iYoruba: ResourceCount((iIvory, 8), (iGems, 6)),
}

for iReligion in range(iNumReligions):
	for i, goal in enumerate(dGoals[iReligion]):
		goal.titled("%s%s" % (infos.religion(iReligion).getText().upper()[:3], i+1))