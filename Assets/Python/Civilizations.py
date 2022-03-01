from RFCUtils import *
from Core import *

from Events import events, handler


### Unit spawn functions ###

def getStartingUnits(iPlayer):
	lStartingUnits = [(iRole, iAmount) for iRole, iAmount in dStartingUnits[iPlayer].items() if iRole != iWork]
	
	if not player(iPlayer).isHuman():
		lStartingUnits += dExtraAIUnits[iPlayer].items()
	
	return lStartingUnits
	
def getAdditionalUnits(iPlayer):
	return dAdditionalUnits[iPlayer].items()

### Tech preference functions ###

def getTechPreferences(iPlayer):
	dPreferences = defaultdict({}, 0)
	iCivilization = civ(iPlayer)
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = infos.tech(iTech).getPrereqOrTechs(i)
			iAndPrereq = infos.tech(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = dPreferences[iPrereqTech]
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	player(iPlayer).resetTechPreferences()

	for iTech, iValue in dPreferences.items():
		player(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	pPlayer.resetBuildingClassPreferences()
	
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingClassPreference(infos.building(iBuilding).getBuildingClassType(), iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingClassPreference(infos.building(iWonder).getBuildingClassType(), iDefaultPreference)
	
### General functions ###
		
def initBirthYear(iPlayer):
	player(iPlayer).setInitialBirthTurn(year(dBirth[iPlayer]))

@handler("GameStart")
def init():
	for iPlayer in players.major():
		initBirthYear(iPlayer)
		initPlayerTechPreferences(iPlayer)
		initBuildingPreferences(iPlayer)
		
@handler("playerCivAssigned")
def onActivate(iPlayer):
	initPlayerTechPreferences(iPlayer)
	initBuildingPreferences(iPlayer)
	

### Civilization starting attributes ###

class Civilization(object):

	def __init__(self, iCiv, **kwargs):
		self.iCiv = iCiv
	
		self.iLeader = kwargs.get("iLeader")
		self.iGold = kwargs.get("iGold")
		self.iStateReligion = kwargs.get("iStateReligion")
		self.iAdvancedStartPoints = kwargs.get("iAdvancedStartPoints")
		
		self.lCivics = kwargs.get("lCivics", [])
		
		self.dAttitudes = kwargs.get("dAttitudes", {})
		
		self.sLeaderName = kwargs.get("sLeaderName")
		
		self.techs = kwargs.get("techs", techs.none())
	
	@property
	def player(self):
		return player(self.iCiv)
	
	@property
	def team(self):
		return team(self.player.getTeam())
	
	@property
	def info(self):
		return infos.civ(self.iCiv)
	
	def isPlayable(self):
		return self.info.getStartingYear() != 0
	
	def apply(self):
		if self.iLeader is not None:
			self.player.setLeader(self.iLeader)
		
		if self.sLeaderName is not None:
			self.player.setLeaderName(text(self.sLeaderName))
		
		if self.iGold is not None:
			self.player.changeGold(scale(self.iGold))
		
		if self.iStateReligion is not None:
			self.player.setLastStateReligion(self.iStateReligion)
		
		for iCivic in self.lCivics:
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
		
		if self.techs:
			for iTech in self.techs:
				self.team.setHasTech(iTech, True, self.player.getID(), False, False)
			
			self.player.setStartingEra(self.player.getCurrentEra())
		
		for iCiv, iAttitude in self.dAttitudes.items():
			self.player.AI_changeAttitudeExtra(slot(iCiv), iAttitude)
	
	def advancedStart(self):
		if self.iAdvancedStartPoints is not None:
			self.player.setAdvancedStartPoints(scale(self.iAdvancedStartPoints))
			
			if not self.player.isHuman():
				self.player.AI_doAdvancedStart()

lCivilizations = [
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
	Civilization(
		iBabylonia,
		techs=techs.of(iPottery, iPastoralism, iAgriculture)
	),
	Civilization(
		iHarappa,
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
	Civilization(
		iChina,
		techs=techs.of(iTanning, iMining, iAgriculture, iPastoralism, iPottery, iMythology, iSmelting, iLeverage)
	),
	Civilization(
		iGreece,
		iGold=100,
		lCivics=[iRepublic, iSlavery, iDeification],
		techs=techs.column(2).including(iAlloys, iArithmetics, iWriting)
	),
	Civilization(
		iIndia,
		iGold=80,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iDeification],
		techs=techs.column(2).including(iAlloys, iWriting, iCalendar).without(iSeafaring)
	),
	Civilization(
		iPhoenicia,
		iGold=200,
		iAdvancedStartPoints=50,
		lCivics=[iRepublic, iSlavery],
		techs=techs.column(2).including(iAlloys, iWriting, iShipbuilding)
	),
	Civilization(
		iPolynesia,
		techs=techs.of(iTanning, iMythology, iSailing, iSeafaring)
	),
	Civilization(
		iPersia,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iZoroastrianism,
		lCivics=[iMonarchy, iManorialism, iRedistribution, iClergy],
		techs=techs.column(3).including(iBloomery, iPriesthood).without(iSeafaring, iShipbuilding)
	),
	Civilization(
		iRome,
		iGold=100,
		iAdvancedStartPoints=150,
		lCivics=[iRepublic, iSlavery, iRedistribution],
		techs=techs.column(3).including(iBloomery, iCement, iMathematics, iLiterature).without(iRiding, iCalendar, iShipbuilding)
	),
	Civilization(
		iMaya,
		iGold=200,
		lCivics=[iDespotism, iSlavery],
		techs=techs.column(1).including(iProperty, iMasonry, iSmelting, iCeremony).without(iSailing)
	),
	Civilization(
		iTamils,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iClergy],
		techs=techs.column(3).including(iBloomery, iMathematics, iContract, iPriesthood)
	),
	Civilization(
		iEthiopia,
		iGold=100,
		lCivics=[iMonarchy, iSlavery, iClergy],
		techs=techs.column(2).including(iAlloys, iWriting, iCalendar, iPriesthood)
	),
	Civilization(
		iKorea,
		iGold=200,
		iStateReligion=iBuddhism,
		lCivics=[iDespotism, iCasteSystem, iRedistribution],
		techs=techs.column(5).without(iGeneralship, iEngineering, iCurrency)
	),
	Civilization(
		iByzantium,
		iGold=400,
		iAdvancedStartPoints=100,
		iStateReligion=iOrthodoxy,
		lCivics=[iDespotism, iCitizenship, iSlavery, iMerchantTrade, iClergy],
		techs=techs.column(5).including(iArchitecture, iPolitics, iEthics)
	),
	Civilization(
		iJapan,
		iGold=100,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRedistribution, iDeification],
		techs=techs.column(5).including(iNobility, iSteel, iArtisanry, iPolitics)
	),
	Civilization(
		iVikings,
		iGold=150,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iConquest],
		techs=techs.column(6).without(iScholarship, iEthics)
	),
	Civilization(
		iTurks,
		iGold=100,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iConquest],
		techs=techs.column(5).including(iNobility, iSteel).column(5).without(iNavigation, iMedicine, iPhilosophy)
	),
	Civilization(
		iArabia,
		iGold=300,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iCitizenship, iSlavery, iMerchantTrade, iClergy, iConquest],
		techs=techs.column(6).including(iAlchemy, iTheology).without(iPolitics)
	),
	Civilization(
		iTibet,
		iGold=50,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iMerchantTrade, iClergy, iConquest],
		techs=techs.column(5).including(iNobility, iScholarship, iEthics)
	),
	Civilization(
		iIndonesia,
		iGold=300,
		iAdvancedStartPoints=50,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iCasteSystem, iMerchantTrade, iDeification],
		techs=techs.column(5).including(iEthics).without(iGeneralship)
	),
	Civilization(
		iMoors,
		iGold=200,
		iAdvancedStartPoints=100,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iMachinery, iAlchemy, iTheology).without(iPolitics)
	),
	Civilization(
		iSpain,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iFeudalism, iAlchemy, iGuilds)
	),
	Civilization(
		iFrance,
		iGold=150,
		iAdvancedStartPoints=50,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy, iTributaries],
		techs=techs.column(6).including(iFeudalism, iTheology)
	),
	Civilization(
		iKhmer,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iHinduism,
		lCivics=[iMonarchy, iCasteSystem, iRedistribution, iDeification],
		techs=techs.column(6).including(iNobility, iArchitecture, iArtisanry, iScholarship, iEthics)
	),
	Civilization(
		iEngland,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iFeudalism, iTheology)
	),
	Civilization(
		iHolyRome,
		iGold=150,
		iAdvancedStartPoints=50,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade, iClergy, iTributaries],
		techs=techs.column(6).including(iFeudalism, iTheology)
	),
	Civilization(
		iRussia,
		iGold=200,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade],
		techs=techs.column(6).including(iFeudalism).without(iScholarship)
	),
	Civilization(
		iMali,
		iGold=600,
		iAdvancedStartPoints=50,
		iStateReligion=iIslam,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iTheology)
	),
	Civilization(
		iPoland,
		iGold=100,
		iStateReligion=iCatholicism,
		lCivics=[iElective, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(6).including(iFeudalism, iFortification, iCivilService, iTheology)
	),
	Civilization(
		iPortugal,
		iGold=200,
		iAdvancedStartPoints=50,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iVassalage, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(7).including(iPatronage)
	),
	Civilization(
		iInca,
		iGold=700,
		lCivics=[iMonarchy, iSlavery, iRedistribution, iDeification],
		techs=techs.column(3).including(iMathematics, iContract, iLiterature, iPriesthood).without(iSeafaring, iAlloys, iRiding, iShipbuilding)
	),
	Civilization(
		iItaly,
		iGold=350,
		iAdvancedStartPoints=250,
		iStateReligion=iCatholicism,
		lCivics=[iRepublic, iCitizenship, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(7).including(iCommune, iPaper, iCompass, iDoctrine)
	),
	Civilization(
		iMongols,
		iGold=250,
		iAdvancedStartPoints=50,
		lCivics=[iElective, iVassalage, iSlavery, iMerchantTrade, iConquest],
		techs=techs.column(7).including(iPaper, iCompass).without(iTheology)
	),
	Civilization(
		iAztecs,
		iGold=600,
		lCivics=[iDespotism, iCitizenship, iSlavery, iRedistribution, iDeification],
		techs=techs.column(3).including(iMathematics, iContract, iLiterature, iPriesthood, iGeneralship, iAesthetics, iCurrency, iLaw).without(iSeafaring, iAlloys, iRiding, iShipbuilding)
	),
	Civilization(
		iMughals,
		iGold=400,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iRegulatedTrade, iTheocracy, iConquest],
		techs=techs.column(7).including(iCommune, iCropRotation, iDoctrine, iGunpowder)
	),
	Civilization(
		iOttomans,
		iGold=300,
		iAdvancedStartPoints=200,
		iStateReligion=iIslam,
		lCivics=[iDespotism, iVassalage, iSlavery, iRegulatedTrade, iClergy, iConquest],
		techs=techs.column(7).including(iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder)
	),
	Civilization(
		iThailand,
		iGold=800,
		iStateReligion=iBuddhism,
		lCivics=[iMonarchy, iVassalage, iCasteSystem, iRegulatedTrade, iMonasticism],
		techs=techs.column(8).without(iCompass, iDoctrine, iCommune, iPatronage)
	),
	Civilization(
		iCongo,
		iGold=300,
		lCivics=[iElective, iVassalage, iSlavery, iRedistribution],
		techs=techs.column(6).including(iMachinery, iCivilService, iGuilds, iTheology)
	),
	Civilization(
		iIran,
		iGold=600,
		iAdvancedStartPoints=250,
		iStateReligion=iIslam,
		lCivics=[iMonarchy, iVassalage, iSlavery, iMerchantTrade, iTheocracy],
		techs=techs.column(9).including(iHeritage, iFirearms)
	),
	Civilization(
		iNetherlands,
		iGold=600,
		iAdvancedStartPoints=300,
		iStateReligion=iProtestantism,
		lCivics=[iRepublic, iCentralism, iManorialism, iMerchantTrade, iClergy],
		techs=techs.column(10)
	),
	Civilization(
		iGermany,
		iGold=800,
		iAdvancedStartPoints=250,
		iStateReligion=iProtestantism,
		lCivics=[iMonarchy, iCentralism, iManorialism, iRegulatedTrade, iClergy, iConquest],
		techs=techs.column(11).without(iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning)
	),
	Civilization(
		iAmerica,
		iGold=1500,
		iAdvancedStartPoints=500,
		iStateReligion=iProtestantism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iTolerance, iIsolationism],
		techs=techs.column(12).including(iRepresentation, iChemistry)
	),
	Civilization(
		iArgentina,
		iGold=1200,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iTolerance, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism)
	),
	Civilization(
		iMexico,
		iGold=500,
		iAdvancedStartPoints=100,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism)
	),
	Civilization(
		iColombia,
		iGold=750,
		iAdvancedStartPoints=150,
		iStateReligion=iCatholicism,
		lCivics=[iDespotism, iConstitution, iIndividualism, iRegulatedTrade, iClergy, iNationhood],
		techs=techs.column(12).including(iRepresentation, iNationalism)
	),
	Civilization(
		iBrazil,
		iGold=1600,
		iAdvancedStartPoints=200,
		iStateReligion=iCatholicism,
		lCivics=[iMonarchy, iConstitution, iSlavery, iFreeEnterprise, iClergy, iColonialism],
		techs=techs.column(12).including(iRepresentation, iNationalism, iBiology)
	),
	Civilization(
		iCanada,
		iGold=1000,
		iAdvancedStartPoints=250,
		iStateReligion=iCatholicism,
		lCivics=[iDemocracy, iConstitution, iIndividualism, iFreeEnterprise, iTolerance, iNationhood],
		techs=techs.column(13).including(iBallistics, iEngine, iRailroad, iJournalism)
	),
]

### Starting units ###

dStartingUnits = CivDict({
	iChina: {
		iSettle: 1,
		iWork: 1,
		iBase: 1,
		iDefend: 1,
	},
	iIndia: {
		iSettle: 1,
		iWork: 2,
		iDefend: 1,
		iCounter: 1,
		iAttack: 1,
		iHarass: 1,
	},
	iGreece: {
		iSettle: 1,
		iWork: 2,
		iSettleSea: 1,
		iBase: 2,
		iAttack: 2,
		iCityAttack: 1,
		iWorkerSea: 1,
	},
	iPhoenicia: {
		iSettle: 1,
		iWork: 2,
		iDefend: 1,
		iCounter: 1,
		iSettleSea: 1,
		iTransport: 1,
		iEscort: 1,
	},
	iPolynesia: {
		iSettle: 1,
		iSettleSea: 1,
		iWorkerSea: 1,
	},
	iPersia: {
		iSettle: 3,
		iWork: 3,
		iDefend: 3,
		iAttack: 4,
		iShock: 2,
		# 1 War Elephant
	},
	iRome: {
		iSettle: 4,
		iWork: 2,
		iDefend: 3,
		iAttack: 4,
		iWorkerSea: 1,
		iTransport: 2,
	},
	iMaya: {
		iSettle: 1,
		iWork: 1,
		iSkirmish: 2,
	},
	iTamils: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 2,
		iDefend: 1,
		iShock: 1,
		iAttack: 2,
		iMissionary: 1,
		iWorkerSea: 1,
		iEscort: 1,
	},
	iEthiopia: {
		iSettle: 2,
		iWork: 3,
		iDefend: 2,
		iAttack: 1,
		iWorkerSea: 1,
		iEscort: 1,
		# 1 Shotelai
	},
	iKorea: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iAttack: 1,
		iShock: 1,
		iMissionary: 1,
	},
	iByzantium: {
		iSettle: 4,
		iWork: 3,
		iAttack: 4,
		iCounter: 2,
		iDefend: 2,
		iMissionary: 1,
		iTransport: 2,
		iEscort: 2,
	},
	iJapan: {
		iSettle: 3,
		iWork: 2,
		iDefend: 2,
		iAttack: 2,
		iMissionary: 1,
		iWorkerSea: 2,
	},
	iVikings: {
		iSettle: 2,
		iWork: 3,
		iSettleSea: 1,
		iDefend: 4,
		iExplore: 1,
		iAttack: 3,
		iWorkerSea: 1,
		iExploreSea: 2,
	},
	iTurks: {
		iSettle: 6,
		iWork: 3,
		iDefend: 3,
		iHarass: 6,
		iExplore: 1,
	},
	iArabia: {
		iSettle: 2,
		iWork: 3,
		iDefend: 1,
		iShock: 2,
		iAttack: 2,
		iWork: 1,
		iWorkerSea: 1,
	},
	iTibet: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iHarass: 2,
		iMissionary: 1,
	},
	iKhmer: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 3,
		iDefend: 1,
		iShockCity: 3,
		iMissionary: 1,
		iWorkerSea: 1,
		# 1 Buddhist Missionary
	},
	iIndonesia: {
		iSettle: 1,
		iSettleSea: 2,
		iWork: 3,
		iDefend: 1,
		iMissionary: 1,
		iEscort: 1,
	},
	iMoors: {
		iSettle: 2,
		iWork: 2,
		iDefend: 1,
		iAttack: 2,
		iCounter: 2,
		iHarass: 2,
		iMissionary: 2,
		iWorkerSea: 1,
		iTransport: 1,
		iEscort: 1,
		# if human Spain or Moors: 1 Crossbowman
	},
	iSpain: {
		iSettle: 2,
		iWork: 3,
		iDefend: 2,
		iAttack: 4,
		iMissionary: 1,
	},
	iFrance: {
		iSettle: 3,
		iWork: 3,
		iDefend: 3,
		iCounter: 2,
		iAttack: 3,
		iMissionary: 1,
	},
	iEngland: {
		iSettle: 2,
		iSettleSea: 1,
		iWork: 3,
		iDefend: 3,
		iMissionary: 1,
		iWorkerSea: 2,
		iTransport: 1,
	},
	iHolyRome: {
		iSettle: 3,
		iWork: 3,
		iDefend: 3,
		iCityAttack: 3,
		iShockCity: 3,
		iCitySiege: 4,
		iMissionary: 1,
	},
	iRussia: {
		iSettle: 4,
		iWork: 3,
		iDefend: 2,
		iHarass: 4,
	},
	iMali: {
		iSettle: 3,
		iWork: 3,
		iSkirmish: 5,
		iMissionary: 2,
	},
	iPoland: {
		iSettle: 1,
		iWork: 3,
		iDefend: 1,
		iAttack: 2,
		iShock: 2,
		iMissionary: 1,
		# if human: 1 Settler (to account for scripted AI spawn)
	},
	iPortugal: {
		iSettle: 1,
		iSettleSea: 1,
		iWork: 3,
		iDefend: 4,
		iCounter: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iEscort: 2,
	},
	iInca: {
		iSettle: 1,
		iWork: 4,
		iAttack: 4,
		iDefend: 2,
		# if not human: 1 Settler
	},
	iItaly: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iCounter: 2,
		iSiege: 3,
		iMissionary: 1,
		iWorkerSea: 2,
		iTransport: 1,
		iEscort: 1,
	},
	iMongols: {
		iSettle: 3,
		iWork: 4,
		iDefend: 3,
		iAttack: 2,
		iHarass: 2,
		iShock: 6,
		iSiege: 3,
	},
	iAztecs: {
		iSettle: 2,
		iWork: 3,
		iAttack: 4,
		iDefend: 2,
	},
	iMughals: {
		iSettle: 3,
		iWork: 3,
		iSiege: 3,
		iAttack: 4,
		iHarass: 2,
		iMissionary: 4,
	},
	iOttomans: {
		iSettle: 3,
		iWork: 4,
		iAttack: 4,
		iDefend: 2,
		iShock: 3,
		iSiege: 4,
		iMissionary: 2,
	},
	iThailand: {
		iSettle: 1,
		iWork: 2,
		iCounter: 3,
		iShock: 2,
		iMissionary: 1,
	},
	iCongo: {
		iSettle: 1,
		iWork: 2,
		iDefend: 2,
		iAttack: 2,
	},
	iIran: {
		iSettle: 1,
		iWork: 3,
		iDefend: 3,
		iAttack: 3,
		iSiege: 3,
		iMissionary: 3,
	},
	iNetherlands: {
		iSettle: 2,
		iSettleSea: 2,
		iWork: 2,
		iAttack: 6,
		iCounter: 2,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iExploreSea: 2,
	},
	iGermany: {
		iSettle: 4,
		iWork: 3,
		iAttack: 3,
		iDefend: 2,
		iSiege: 3,
		iMissionary: 2,
	},
	iAmerica: {
		iSettle: 8,
		iWork: 5,
		iSkirmish: 2,
		iAttack: 4,
		iSiege: 2,
		iWorkerSea: 2,
		iTransport: 2,
		iEscort: 1,
	},
	iArgentina: {
		iSettle: 2,
		iWork: 2,
		iAttack: 1,
		iDefend: 2,
		iSiege: 2,
		iMissionary: 1,
		iTransport: 1,
		iEscort: 2,
	},
	iMexico: {
		iSettle: 1,
		iWork: 2,
		iShock: 4,
		iDefend: 3,
		iAttack: 2,
		iCounter: 2,
		iMissionary: 1,
	},
	iColombia: {
		iSettle: 1,
		iWork: 3,
		iDefend: 2,
		iAttack: 3,
		iCounter: 5,
		iMissionary: 1,
		iTransport: 1,
		iAttackSea: 1,
	},
	iBrazil: {
		iSettle: 5,
		iWork: 3,
		iSkirmish: 3,
		iDefend: 3,
		iSiege: 2,
		iMissionary: 1,
		iWorkerSea: 2,
		iTransport: 2,
		iEscort: 3,
	},
	iCanada: {
		iSettle: 5,
		iWork: 3,
		iShock: 3,
		iDefend: 5,
		iMissionary: 1,
		iTransport: 2,
		iEscort: 1,
		iLightEscort: 1,
	}
}, {})

dExtraAIUnits = CivDict({
	iJapan: {
		iDefend: 2,
		iAttack: 3,
	},
	iTamils: {
		iShock: 1,
		iMissionary: 1,
	},
	iKorea: {
		iCounter: 2,
		iDefend: 2,
	},
	iEngland: {
		iAttack: 2,
	},
	iPoland: {
		iCounter: 2,
	},
	iMongols: {
		iDefend: 2,
		iAttack: 2,
		iShock: 10,
		iSiege: 5,
		iExplore: 2,
	},
	iIran: {
		iAttack: 6,
		iSiege: 3,
	},
	iGermany: {
		iAttack: 10,
		iSiege: 5,
	},
	iAmerica: {
		iDefend: 1,
	},
	iArgentina: {
		iDefend: 3,
		iShock: 2,
		iSiege: 2,
	},
	iBrazil: {
		iDefend: 1,
	}
}, {})

dAdditionalUnits = CivDict({
	iIndia: {
		iDefend: 2,
		iAttack: 1,
	},
	iGreece: {
		iAttack: 4,
	},
	iPersia: {
		iAttack: 4,
	},
	iPhoenicia: {
		iHarass: 1,
		iShock: 1
	},
	iPolynesia: {
		iBase: 2,
	},
	iRome: {
		iAttack: 4,
	},
	iJapan: {
		iDefend: 2,
		iAttack: 2,
	},
	iTamils: {
		iAttack: 2,
		iShock: 1,
	},
	iEthiopia: {
		iDefend: 2,
		# 2 Shotelai
	},
	iKorea: {
		iHarass: 2,
		# 2 Crossbowmen
	},
	iMaya: {
		iDefend: 2,
		iAttack: 2,
	},
	iByzantium: {
		iShock: 2,
		iHarass: 2,
	},
	iVikings: {
		# 3 Huscarls
	},
	iTurks: {
		iHarass: 4,
	},
	iArabia: {
		iAttack: 2,
		iShock: 4,
	},
	iTibet: {
		iHarass: 2,
	},
	iKhmer: {
		iAttack: 3,
		iShockCity: 2,
	},
	iMoors: {
		# 2 Camel Archers
	},
	iSpain: {
		iDefend: 3,
		iAttack: 3,
	},
	iFrance: {
		iDefend: 3,
		iAttack: 3,
	},
	iEngland: {
		iDefend: 3,
		iAttack: 3,
	},
	iHolyRome: {
		iDefend: 3,
		iAttack: 3,
	},
	iRussia: {
		iAttack: 2,
		iDefend: 2,
		iHarass: 2,
	},
	iMali: {
		iSkirmish: 4,
		iAttack: 3,
	},
	iPoland: {
		iDefend: 2,
		iShock: 2,
	},
	iPortugal: {
		iDefend: 3,
		iCounter: 3,
	},
	iInca: {
		iAttack: 5,
		iDefend: 3,
	},
	iItaly: {
		iShock: 2,
	},
	iMongols: {
		iDefend: 2,
		iHarass: 2,
		iShock: 4,
	},
	iAztecs: {
		iAttack: 5,
		iDefend: 3,
	},
	iMughals: {
		iShockCity: 2,
		iHarass: 4,
	},
	iOttomans: {
		iDefend: 3,
		iHarass: 3,
	},
	iThailand: {
		iCounter: 2,
		iShock: 2,
	},
	iCongo: {
		iAttack: 3,
	},
	iIran: {
		iAttack: 2,
		iHarass: 1,
		iSiege: 1,
	},
	iNetherlands: {
		iAttack: 3,
		iCounter: 3,
	},
	iGermany: {
		iAttack: 5,
		iSiege: 3,
	},
	iAmerica: {
		iAttack: 3,
		iSkirmish: 3,
		iSiege: 3,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 4,
	},
	iMexico: {
		iShock: 4,
		iSiege: 2,
	},
	iColombia: {
		iAttack: 4,
		iSkirmish: 4,
		iSiege: 2,
	},
	iBrazil: {
		iAttack: 3,
		iSkirmish: 2,
		iSiege: 2,
	},
	iCanada: {
		iAttack: 4,
		iShock: 2,
		iSiege: 2,
	},
}, {})

dStartingExperience = CivDict({
	iMughals: {
		iAttack: 2,
	},
	iGermany: {
		iAttack: 2,
		iDefend: 2,
		iSiege: 2,
	},
	iArgentina: {
		iAttack: 2,
		iShock: 2,
		iDefend: 2,
		iSiege: 2,
	},
	iMexico: {
		iShock: 2,
		iDefend: 2,
		iAttack: 2,
		iCounter: 2,
	},
}, {})

dAlwaysTrain = CivDict({
	iGreece: [iHoplite, iCatapult],
	iByzantium: [iLegion],
	iArabia: [iMobileGuard, iGhazi],
	iOttomans: [iJanissary, iGreatBombard],
}, [])

dNeverTrain = CivDict({
	iCongo: [iCrossbowman],
}, [])

def createSpecificUnits(iPlayer, tile):
	iCiv = civ(iPlayer)
	bHuman = player(iPlayer).isHuman()
	
	if iCiv == iPersia:
		makeUnit(iPlayer, iWarElephant, tile)
	elif iCiv == iEthiopia:
		makeUnit(iPlayer, iShotelai, tile)
	elif iCiv == iKhmer:
		makeUnit(iPlayer, iBuddhistMissionary, tile)
	elif iCiv == iMoors:
		if civ() in [iSpain, iMoors]:
			makeUnit(iPlayer, iCrossbowman, tile)
	elif iCiv == iSpain:
		if not bHuman:
			makeUnit(iPlayer, iSettler, tile)
			makeUnits(iPlayer, iLancer, tile, 2)
	elif iCiv == iPoland:
		if bHuman:
			# to account for scripted AI settler spawn
			makeUnit(iPlayer, iSettler, tile)
	elif iCiv == iInca:
		if not bHuman:
			makeUnit(iPlayer, iSettler, tile)

def createSpecificAdditionalUnits(iPlayer, tile):
	iCiv = civ(iPlayer)
	
	if iCiv == iEthiopia:
		makeUnits(iPlayer, iShotelai, tile, 2)
	elif iCiv == iKorea:
		makeUnits(iPlayer, iCrossbow, tile, 2)
	elif iCiv == iVikings:
		makeUnits(iPlayer, iHuscarl, tile, 3)
	elif iCiv == iMoors:
		makeUnits(iPlayer, iCamelArcher, tile, 2)


### Tech Preferences ###

dTechPreferences = {
	iEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		
		iAlloys: -20,
		iBloomery: -50,
	},
	iBabylonia : {
		iWriting: 30,
		iContract: 30,
		iCalendar: 30,
		iMasonry: 20,
		iProperty: 20,
		iDivination: 20,
		iConstruction: 20,
	
		iPriesthood: -50,
		iMathematics: -30,
		iAlloys: -30,
		iBloomery: -30,
		iSteel: -30,
	},
	iHarappa : {
		iMasonry: 20,
		iPastoralism: 20,
		iPottery: 20,
		
		iMythology: -50,
		iDivination: -50,
		iCeremony: -50,
	},
	iChina : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,	
	},
	iGreece : {
		iPhilosophy: 50,
		iPriesthood: 40,
		iLiterature: 40,
		iMathematics: 40,
		iNavigation: 40,
		iBloomery: 40,
		iMathematics: 30,
		iCalendar: 20,
		iWriting: 20,
		iShipbuilding: 20,
		iMedicine: 20,
		iAesthetics: 20,
		
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
	},
	iIndia : {
		iCeremony: 200,
		iPriesthood: 200,
		iPhilosophy: 50,
		
		iEngineering: -20,
		iTheology: -20,
		iCivilService: -20,
	},
	iCarthage : {
		iNavigation: 40,
		iRiding: 30,
		iCurrency: 30,
		iCompass: 20,
	},
	iPolynesia : {
		iCompass: 20,
		iDivination: 20,
		iMasonry: 20,
		
		iAlloys: -30,
		iBloomery: -30,
	},
	iPersia : {
		iFission: 15,
	
		iTheology: -40,
	},
	iRome : {
		iTheology: 30,
		iCurrency: 20,
		iLaw: 20,
		iPolitics: 20,
		iConstruction: 15,
		iEngineering: 15,
		
		iCalendar: -20,
	},
	iMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iTamils : {
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iByzantium : {
		iFinance: -50,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
	},
	iJapan : {
		iFeudalism: 40,
		iFortification: 40,
		iRobotics: 40,
	
		iOptics: -40,
		iExploration: -40,
		iFirearms: -30,
		iMachinery: -20,
		iGuilds: -20,
		iGeography: -20,
		iReplaceableParts: -20,
		iScientificMethod: -20,
	},
	iVikings : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iArabia : {
		iScholarship: 30,
		iAlchemy: 30,
		
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
	},
	iTibet : {
		iPhilosophy: 30,
		iEngineering: 20,
		iPaper: 20,
		iTheology: 20,
		iDoctrine: 20,
	},
	iIndonesia : {
		iAesthetics: 30,
		iArtisanry: 30,
		iExploration: -20,
	},
	iMoors : {
		iCivilService: 20,
	
		iExploration: -40,
		iGuilds: -40,
	},
	iSpain : {
		iCartography: 100,
		iExploration: 100,
		iCompass: 100,
		iFirearms: 100,
		iPatronage: 50,
		iReplaceableParts: 30,
		iGuilds: 15,
		iGunpowder: 15,
		iChemistry: 15,
	},
	iFrance : {
		iReplaceableParts: 30,
		iFirearms: 20,
		iExploration: 20,
		iGeography: 20,
		iLogistics: 20,
		iPatronage: 20,
		iMeasurement: 20,
		iAcademia: 20,
		iEducation: 15,
		iFeudalism: 15,
		iChemistry: 15,
		iSociology: 15,
		iFission: 12,
	},
	iKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iEngland : {
		iExploration: 40,
		iGeography: 40,
		iFirearms: 40,
		iReplaceableParts: 30,
		iLogistics: 30,
		iCivilLiberties: 20,
		iEducation: 15,
		iGuilds: 15,
		iChemistry: 15,
	},
	iHolyRome : {
		iAcademia: 50,
		iPrinting: 50,
		iFirearms: 20,
		iReplaceableParts: 20,
		iEducation: 15,
		iGuilds: 15,
		iOptics: 15,
		iFission: 12,
	},
	iRussia : {
		iMacroeconomics: 30,
		iCombinedArms: 30,
		iReplaceableParts: 30,
		iHeritage: 15,
		iPatronage: 15,
		iUrbanPlanning: 15,
		iFission: 12,
		
		iPhilosophy: -20,
		iPrinting: -20,
		iCivilLiberties: -20,
		iSocialContract: -20,
		iRepresentation: -20,
	},
	iMali : {
		iEducation: 30,
	},
	iMughals : {
		iHumanities: 30,
		iPhilosophy: 20,
		iEducation: 20,
		iPaper: 20,
		iPatronage: 20,
		iEngineering: 15,
	
		iReplaceableParts: -30,
		iScientificMethod: -30,
		iCombinedArms: -30,
		iExploration: -30,
	},
	iPoland : {
		iCombinedArms: 30,
		iCivilLiberties: 30,
		iSocialContract: 20,
		iOptics: 20,
	},
	iPortugal : {
		iCartography: 100,
		iExploration: 100,
		iGeography: 100,
		iCompass: 100,
		iFirearms: 100,
		iCompanies: 50,
		iPatronage: 50,
		iReplaceableParts: 20,
	},
	iInca : {
		iConstruction: 40,
		iCalendar: 40,
		
		iFeudalism: -40,
		iMachinery: -20,
		iGunpowder: -20,
		iGuilds: -20,
	},
	iItaly : {
		iRadio: 20,
		iPsychology: 20,
		iFinance: 20,
		iOptics: 20,
		iPatronage: 20,
		iReplaceableParts: 20,
		iHumanities: 20,
		iAcademia: 20,
		iFission: 12,
	},
	iMongols : {
		iPaper: 15,
		
		iFirearms: -40,
		iCombinedArms: -40,
	},
	iAztecs : {
		iConstruction: 40,
		iLiterature: 20,
		
		iGuilds: -40,
		iFeudalism: -20,
		iMachinery: -20,
		iGunpowder: -20,
	},
	iOttomans : {
		iGunpowder: 30,
		iFirearms: 30,
		iCombinedArms: 30,
		iJudiciary: 20,
	},
	iThailand : {
		iCartography: -50,
		iExploration: -50,
	},
	iNetherlands : {
		iExploration: 20,
		iFirearms: 20,
		iOptics: 20,
		iGeography: 20,
		iReplaceableParts: 20,
		iLogistics: 20,
		iEconomics: 20,
		iCivilLiberties: 20,
		iHumanities: 20,
		iAcademia: 20,
		iChemistry: 15,
	},
	iGermany : {
		iEngine: 20,
		iInfrastructure: 20,
		iChemistry: 20,
		iAssemblyLine: 20,
		iPsychology: 20,
		iSociology: 20,
		iSynthetics: 20,
		iFission: 12,
	},
	iAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iEgypt: -15,
	iBabylonia: -40,
	iGreece: -15,
	iIndia: -15,
	iRome: -20,
	iArabia: -15,
	iIndonesia: -15,
	iFrance: -12,
	iKhmer: -15,
	iEngland: -12,
	iRussia: -12,
	iThailand: -15,
	iCongo: -20,
	iNetherlands: -12,
	iAmerica: -12,
}

dBuildingPreferences = {
	iEgypt : {
		iPyramids: 100,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		iGreatSphinx: 30,
	},
	iBabylonia : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: 0,
		iGreatSphinx: 0,
		
		iOracle: -60,
	},
	iChina : {
		iGreatWall: 80,
		iForbiddenPalace: 40,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 30,
		iTerracottaArmy: 30,
		iPorcelainTower: 30,
		
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iGreece : {
		iColossus: 30,
		iOracle: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iStatueOfZeus: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,
		iGreatLibrary: 15,
		iGreatLighthouse: 15,
		
		iPyramids: -100,
		iGreatCothon: 0,
	},
	iIndia : {
		iKhajuraho: 30,
		iIronPillar: 30,
		iVijayaStambha: 30,
		iNalanda: 30,
		iLotusTemple: 30,
		iTajMahal: 20,
		iWatPreahPisnulok: 20,
		iShwedagonPaya: 20,
		iHarmandirSahib: 20,
		iJetavanaramaya: 20,
		iSalsalBuddha: 20,
		iPotalaPalace: 20,
		iBorobudur: 15,
		iPrambanan: 15,
		
		iParthenon: -30,
		iStatueOfZeus: -20,
	},
	iCarthage : {
		iGreatCothon: 30,
		iGreatLighthouse: 15,
		iColossus: 15,
		
		iPyramids: -50,
	},
	iPolynesia : {
		iMoaiStatues: 30,
	},
	iPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 30,
		iGondeshapur: 30,
		iAlamut: 30,
		iHangingGardens: 15,
		iColossus: 15,
		iOracle: 15,
	},
	iRome : {
		iFlavianAmphitheatre: 30,
		iAquaAppia: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iAlKhazneh: 20,
		
		iGreatWall: -100,
	},
	iMaya : {
		iTempleOfKukulkan: 40,
	},
	iTamils : {
		iJetavanaramaya: 30,
		iKhajuraho: 20,
	},
	iEthiopia : {
		iMonolithicChurch: 40,
	},
	iKorea : {
		iCheomseongdae: 30,
	},
	iByzantium : {
		iHagiaSophia: 40,
		iTheodosianWalls: 30,
		iMountAthos: 30,
		
		iNotreDame: -20,
		iSistineChapel: -20,
	},
	iJapan : {
		iItsukushimaShrine: 30,
		iHimejiCastle: 30,
		iTsukijiFishMarket: 30,
		iSkytree: 30,
	
		iGreatWall: -100,
	},
	iTurks : {
		iGurEAmir: 40,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
	},
	iVikings : {
		iNobelPrize: 30,
		iGlobalSeedVault: 30,
		iCERN: 15,
	},
	iArabia: {
		iSpiralMinaret: 40,
		iDomeOfTheRock: 40,
		iHouseOfWisdom: 40,
		iBurjKhalifa: 40,
		iAlamut: 30,
	
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iTibet : {
		iPotalaPalace: 40,
	},
	iIndonesia : {
		iBorobudur: 40,
		iPrambanan: 40,
		iGardensByTheBay: 40,
		iShwedagonPaya: 20,
		iWatPreahPisnulok: 20,
		iNalanda: 20,
	},
	iMoors : {
		iMezquita: 100,
		
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
	},
	iSpain : {
		iEscorial: 30,
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iSagradaFamilia: 30,
		iCristoRedentor: 20,
		iWembley: 20,
		iIberianTradingCompanyBuilding: 20,
		iTorreDeBelem: 15,
		iNotreDame: 15,
		iMezquita: 15,
	},
	iFrance : {
		iTradingCompanyBuilding: 40,
		iNotreDame: 40,
		iEiffelTower: 30,
		iVersailles: 30,
		iLouvre: 30,
		iTriumphalArch: 30,
		iMetropolitain: 30,
		iCERN: 30,
		iKrakDesChevaliers: 30,
		iChannelTunnel: 30,
		iPalaceOfNations: 20,
		iBerlaymont: 20,
		iLargeHadronCollider: 20,
		iITER: 20,
	},
	iKhmer : {
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iEngland : {
		iTradingCompanyBuilding: 50,
		iOxfordUniversity: 30,
		iWembley: 30,
		iWestminsterPalace: 30,
		iTrafalgarSquare: 30,
		iBellRockLighthouse: 30,
		iCrystalPalace: 30,
		iChannelTunnel: 30,
		iBletchleyPark: 20,
		iAbbeyMills: 20,
		iMetropolitain: 20,
		iNationalGallery: 20,
		iKrakDesChevaliers: 20,
		iHarbourOpera: 20,
	},
	iHolyRome : {
		iSaintThomasChurch: 30,
		iKrakDesChevaliers: 20,
		iNeuschwanstein: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iRussia : {
		iKremlin: 40,
		iSaintBasilsCathedral: 40,
		iLubyanka: 40,
		iHermitage: 40,
		iMotherlandCalls: 30,
		iAmberRoom: 30,
		iSaintSophia: 30,
		iMountAthos: 20,
		iMetropolitain: 20,
	},
	iMali : {
		iUniversityOfSankore: 40,
	},
	iPoland : {
		iSaltCathedral: 30,
		iOldSynagogue: 30,
	},
	iPortugal : {
		iCristoRedentor: 40,
		iTorreDeBelem: 40,
		iIberianTradingCompanyBuilding: 40,
		iWembley: 20,
		iEscorial: 20,
		iNotreDame: 15,
	},
	iInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iItaly : {
		iFlavianAmphitheatre: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iMoleAntonelliana: 30,
	},
	iMongols : {
		iSilverTreeFountain: 40,
	},
	iOttomans : {
		iTopkapiPalace: 60,
		iBlueMosque: 60,
		iHagiaSophia: 20,
		iGurEAmir: 20,
		
		iTajMahal: -40,
		iRedFort: -40,
		iSaintBasilsCathedral: -40,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iMughals : {
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iThailand : {
		iEmeraldBuddha: 40,
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iGreatCothon: 15,
	},
	iIran: {
		iImageOfTheWorldSquare: 30,
		iShalimarGardens: 20,
	},
	iNetherlands : {
		iTradingCompanyBuilding: 60,
		iBourse: 40,
		iDeltaWorks: 40,
		iAtomium: 30,
		iBerlaymont: 30,
		iNationalGallery: 20,
		iWembley: 20,
		iCERN: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iGermany : {
		iBrandenburgGate: 40,
		iAmberRoom: 30,
		iNeuschwanstein: 30,
		iWembley: 20,
		iCERN: 20,
		iIronworks: 15,
	},
	iAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
		iMetropolitain: 20,
	},
	iMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
		iLasLajasSanctuary: 20,
	},
	iArgentina : {
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
		iWembley: 20,
	},
	iColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
		iWembley: 20,
	},
	iCanada : {
		iFrontenac: 30,
		iCNTower: 30,
	}
}