# Dynamic Civs - edead

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
import Victory as vic
from StoredData import sd
import RFCUtils
import CityNameManager
utils = RFCUtils.RFCUtils()
import time

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
localText = CyTranslator()
iNumPlayers = con.iNumPlayers

iEgypt = con.iEgypt
iIndia = con.iIndia
iChina = con.iChina
iBabylonia = con.iBabylonia
iGreece = con.iGreece
iPersia = con.iPersia
iCarthage = con.iCarthage
iPhoenicia = con.iPhoenicia
iRome = con.iRome
iTamils = con.iTamils
iJapan = con.iJapan
iEthiopia = con.iEthiopia
iKorea = con.iKorea
iMaya = con.iMaya
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iTibet = con.iTibet
iKhmer = con.iKhmer
iIndonesia = con.iIndonesia
iMoors = con.iMoors
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iHolyRome = con.iHolyRome
iRussia = con.iRussia
iNetherlands = con.iNetherlands
iHolland = con.iHolland
iMali = con.iMali
iPoland = con.iPoland
iTurkey = con.iTurkey
iPortugal = con.iPortugal
iInca = con.iInca
iItaly = con.iItaly
iMongolia = con.iMongolia
iAztecs = con.iAztecs
iMughals = con.iMughals
iThailand = con.iThailand
iCongo = con.iCongo
iGermany = con.iGermany
iAmerica = con.iAmerica
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iSeljuks = con.iSeljuks
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers


pEgypt = gc.getPlayer(iEgypt)
pIndia = gc.getPlayer(iIndia)
pChina = gc.getPlayer(iChina)
pBabylonia = gc.getPlayer(iBabylonia)
pGreece = gc.getPlayer(iGreece)
pPersia = gc.getPlayer(iPersia)
pCarthage = gc.getPlayer(iCarthage)
pRome = gc.getPlayer(iRome)
pJapan = gc.getPlayer(iJapan)
pTamils = gc.getPlayer(iTamils)
pEthiopia = gc.getPlayer(iEthiopia)
pKorea = gc.getPlayer(iKorea)
pMaya = gc.getPlayer(iMaya)
pByzantium = gc.getPlayer(iByzantium)
pVikings = gc.getPlayer(iVikings)
pArabia = gc.getPlayer(iArabia)
pTibet = gc.getPlayer(iTibet)
pKhmer = gc.getPlayer(iKhmer)
pIndonesia = gc.getPlayer(iIndonesia)
pMoors = gc.getPlayer(iMoors)
pSpain = gc.getPlayer(iSpain)
pFrance = gc.getPlayer(iFrance)
pEngland = gc.getPlayer(iEngland)
pHolyRome = gc.getPlayer(iHolyRome)
pRussia = gc.getPlayer(iRussia)
pNetherlands = gc.getPlayer(iNetherlands)
pHolland = gc.getPlayer(iHolland)
pMali = gc.getPlayer(iMali)
pPoland = gc.getPlayer(iPoland)
pTurkey = gc.getPlayer(iTurkey)
pPortugal = gc.getPlayer(iPortugal)
pInca = gc.getPlayer(iInca)
pItaly = gc.getPlayer(iItaly)
pMongolia = gc.getPlayer(iMongolia)
pAztecs = gc.getPlayer(iAztecs)
pMughals = gc.getPlayer(iMughals)
pThailand = gc.getPlayer(iThailand)
pCongo = gc.getPlayer(iCongo)
pGermany = gc.getPlayer(iGermany)
pAmerica = gc.getPlayer(iAmerica)
pSeljuks = gc.getPlayer(iSeljuks)
pIndependent = gc.getPlayer(iIndependent)
pIndependent2 = gc.getPlayer(iIndependent2)
pNative = gc.getPlayer(iNative)
pCeltia = gc.getPlayer(iCeltia)
pBarbarian = gc.getPlayer(iBarbarian)

teamEgypt = gc.getTeam(pEgypt.getTeam())
teamIndia = gc.getTeam(pIndia.getTeam())
teamChina = gc.getTeam(pChina.getTeam())
teamBabylonia = gc.getTeam(pBabylonia.getTeam())
teamGreece = gc.getTeam(pGreece.getTeam())
teamPersia = gc.getTeam(pPersia.getTeam())
teamCarthage = gc.getTeam(pCarthage.getTeam())
teamRome = gc.getTeam(pRome.getTeam())
teamJapan = gc.getTeam(pJapan.getTeam())
teamTamils = gc.getTeam(pTamils.getTeam())
teamEthiopia = gc.getTeam(pEthiopia.getTeam())
teamKorea = gc.getTeam(pKorea.getTeam())
teamMaya = gc.getTeam(pMaya.getTeam())
teamByzantium = gc.getTeam(pByzantium.getTeam())
teamVikings = gc.getTeam(pVikings.getTeam())
teamArabia = gc.getTeam(pArabia.getTeam())
teamTibet = gc.getTeam(pTibet.getTeam())
teamKhmer = gc.getTeam(pKhmer.getTeam())
teamIndonesia = gc.getTeam(pIndonesia.getTeam())
teamMoors = gc.getTeam(pMoors.getTeam())
teamSpain = gc.getTeam(pSpain.getTeam())
teamFrance = gc.getTeam(pFrance.getTeam())
teamEngland = gc.getTeam(pEngland.getTeam())
teamHolyRome = gc.getTeam(pHolyRome.getTeam())
teamRussia = gc.getTeam(pRussia.getTeam())
teamNetherlands = gc.getTeam(pNetherlands.getTeam())
teamHolland = gc.getTeam(pHolland.getTeam())
teamMali = gc.getTeam(pMali.getTeam())
teamPoland = gc.getTeam(pPoland.getTeam())
teamTurkey = gc.getTeam(pTurkey.getTeam())
teamPortugal = gc.getTeam(pPortugal.getTeam())
teamInca = gc.getTeam(pInca.getTeam())
teamItaly = gc.getTeam(pItaly.getTeam())
teamMongolia = gc.getTeam(pMongolia.getTeam())
teamAztecs = gc.getTeam(pAztecs.getTeam())
teamMughals = gc.getTeam(pMughals.getTeam())
teamThailand = gc.getTeam(pThailand.getTeam())
teamCongo = gc.getTeam(pCongo.getTeam())
teamGermany = gc.getTeam(pGermany.getTeam())
teamAmerica = gc.getTeam(pAmerica.getTeam())
teamSeljuks = gc.getTeam(pSeljuks.getTeam())
teamIndependent = gc.getTeam(pIndependent.getTeam())
teamIndependent2 = gc.getTeam(pIndependent2.getTeam())
teamNative = gc.getTeam(pNative.getTeam())
teamCeltia = gc.getTeam(pCeltia.getTeam())
teamBarbarian = gc.getTeam(pBarbarian.getTeam())

iAncient = con.iAncient
iClassical = con.iClassical
iMedieval = con.iMedieval
iRenaissance = con.iRenaissance
iIndustrial = con.iIndustrial
iModern = con.iModern
iFuture = con.iFuture

tBrazilTL = (32, 14)
tBrazilBR = (43, 30)
tNCAmericaTL = (3, 33)
tNCAmericaBR = (37, 63)

class DynamicCivs:


        def __init__(self):

                self.tTxtKeyNames = ['EGYPT', 'INDIA', 'CHINA', 'BABYLONIA', 'GREECE', 'PERSIA', 'CARTHAGE', 'ROME', 'JAPAN', 'ETHIOPIA',
                                     'KOREA', 'MAYA', 'BYZANTIUM', 'VIKINGS', 'ARABIA', 'KHMER', 'INDONESIA', 'SPAIN', 'FRANCE', 'ENGLAND',
                                     'GERMANY', 'RUSSIA', 'NETHERLANDS', 'MALI', 'PORTUGAL', 'INCA', 'MONGOLIA', 'AZTECS', 'TURKEY', 'AMERICA']
                
                self.defaultNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_DEFAULT",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_DEFAULT",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_DEFAULT",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_DEFAULT",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_DEFAULT",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_DEFAULT",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_DEFAULT",
                        iRome : "TXT_KEY_CIV_ROME_DESC_DEFAULT",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_DEFAULT",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_DEFAULT",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_DEFAULT",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_DEFAULT",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_DEFAULT",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_DEFAULT",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_DEFAULT",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_DEFAULT",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_DEFAULT",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_DEFAULT",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_DEFAULT",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_DEFAULT",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_DEFAULT",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_DEFAULT",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_DEFAULT",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_DEFAULT",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_DEFAULT",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_DEFAULT",
                        iMali : "TXT_KEY_CIV_MALI_DESC_DEFAULT",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_DEFAULT",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_DEFAULT",
                        iInca : "TXT_KEY_CIV_INCA_DESC_DEFAULT",
			iItaly : "TXT_KEY_CIV_ITALY_DESC_DEFAULT",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_DEFAULT",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_DEFAULT",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_DEFAULT",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_DEFAULT",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_DEFAULT",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_DEFAULT",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_DEFAULT",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_DEFAULT",
                }
		
		self.peopleNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_PEOPLES",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_PEOPLES",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_PEOPLES",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_PEOPLES",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_PEOPLES",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_PEOPLES",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_PEOPLES",
                        iRome : "TXT_KEY_CIV_ROME_DESC_PEOPLES",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_PEOPLES",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_PEOPLES",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_PEOPLES",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_PEOPLES",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_PEOPLES",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_PEOPLES",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_PEOPLES",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_PEOPLES",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_PEOPLES",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_PEOPLES",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_PEOPLES",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_PEOPLES",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_PEOPLES",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_PEOPLES",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_PEOPLES",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_PEOPLES",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_PEOPLES",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_PEOPLES",
                        iMali : "TXT_KEY_CIV_MALI_DESC_PEOPLES",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_PEOPLES",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_PEOPLES",
                        iInca : "TXT_KEY_CIV_INCA_DESC_PEOPLES",
			iItaly : "TXT_KEY_CIV_ITALY_DESC_PEOPLES",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_PEOPLES",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_PEOPLES",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_PEOPLES",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_PEOPLES",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_PEOPLES",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_PEOPLES",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_PEOPLES",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_PEOPLES",
                }
				
		self.specificVassalNames = {
			iEgypt : {
				iCarthage : "TXT_KEY_CIV_PHOENICIA_EGYPTIAN_VASSAL",	# Retenu
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_EGYPTIAN_VASSAL"},	# Punt
			#iIndia - none so far
			iChina : {
				iEgypt : "TXT_KEY_CIV_EGYPT_CHINESE_VASSAL",
				iIndia : "TXT_KEY_CIV_INDIA_CHINESE_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_CHINESE_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_CHINESE_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_CHINESE_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_CHINESE_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_CHINESE_VASSAL",
				iJapan : "TXT_KEY_CIV_JAPAN_CHINESE_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_CHINESE_VASSAL",
				iKorea : "TXT_KEY_CIV_KOREA_CHINESE_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_CHINESE_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_CHINESE_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_CHINESE_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_CHINESE_VASSAL",
				iTibet : "TXT_KEY_CIV_TIBET_CHINESE_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_CHINESE_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_CHINESE_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_CHINESE_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_CHINESE_VASSAL",
				iEngland : "TXT_KEY_CIV_ENGLAND_CHINESE_VASSAL",
				iHolyRome : "TXT_KEY_CIV_GERMANY_CHINESE_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_CHINESE_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_CHINESE_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_CHINESE_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_CHINESE_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_CHINESE_VASSAL",
				iItaly : "TXT_KEY_CIV_ROME_CHINESE_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_CHINESE_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_CHINESE_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_CHINESE_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_CHINESE_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_CHINESE_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_CHINESE_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_CHINESE_VASSAL"},
			iBabylonia : {
				iPhoenicia : "TXT_KEY_CIV_PHOENICIA_BABYLONIAN_VASSAL"},	# Babylonian Phoenicia
			iGreece : {
				iIndia : "TXT_KEY_CIV_INDIA_GREEK_VASSAL",	# Greco-Bactrians
				iEgypt : "TXT_KEY_CIV_EGYPT_GREEK_VASSAL",	#  Ptolemaic Egypt
				iPersia : "TXT_KEY_CIV_PERSIA_GREEK_VASSAL"},	# Seleucid Babylonia
			iPersia : {
				iEgypt : "TXT_KEY_CIV_EGYPT_PERSIAN_VASSAL",
				iIndia : "TXT_KEY_CIV_INDIA_PERSIAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_PERSIAN_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_PERSIAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_PERSIAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_PERSIAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_PERSIAN_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_PERSIAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_PERSIAN_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_PERSIAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_PERSIAN_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_PERSIAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_PERSIAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_PERSIAN_VASSAL"},
			#iCarthage - none so far
			iRome : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ROMAN_VASSAL",
				iChina : "TXT_KEY_CIV_CHINA_ROMAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ROMAN_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_ROMAN_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ROMAN_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ROMAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ROMAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ROMAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ROMAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ROMAN_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_ROMAN_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_ROMAN_VASSAL",
				iEngland : "TXT_KEY_CIV_ENGLAND_ROMAN_VASSAL",
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_ROMAN_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_ROMAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ROMAN_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_ROMAN_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_ROMAN_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_ROMAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ROMAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ROMAN_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_ROMAN_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ROMAN_VASSAL",},
			iJapan : {
				iChina : "TXT_KEY_CIV_CHINA_JAPANESE_VASSAL",
				iKorea : "TXT_KEY_CIV_KOREA_JAPANESE_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_JAPANESE_VASSAL",
				iMongolia : "TXT_KEY_CIV_MONGOLIA_JAPANESE_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_JAPANESE_VASSAL",},
			#iTamils - none so far
			#iEthiopia - none so far
			
			#iKorea - none so far
			#iMaya - none so far
			iByzantium : {
				iEgypt : "TXT_KEY_CIV_EGYPT_BYZANTINE_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_BYZANTINE_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_BYZANTINE_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_BYZANTINE_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_BYZANTINE_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_BYZANTINE_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_BYZANTINE_VASSAL"},
			iVikings : {
				iEngland : "TXT_KEY_CIV_ENGLAND_VIKING_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_VIKING_VASSAL"},
			iArabia : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ARABIAN_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ARABIAN_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ARABIAN_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ARABIAN_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_ARABIAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ARABIAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ARABIAN_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ARABIAN_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ARABIAN_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_ARABIAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARABIAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ARABIAN_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ARABIAN_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_ARABIAN_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ARABIAN_VASSAL",},
			#iTibet - none so far
			#iKhmer - none so far
			#iIndonesia - none so far
			#iMoors - none so far
			iSpain : {
				iCarthage : "TXT_KEY_CIV_PHOENICIA_SPANISH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_SPANISH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_SPANISH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_SPANISH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_SPANISH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_SPANISH_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_SPANISH_VASSAL",
				iMoors : "TXT_KEY_CIV_MOORS_SPANISH_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_SPANISH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_SPANISH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_SPANISH_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_SPANISH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_SPANISH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_SPANISH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_SPANISH_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_SPANISH_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_SPANISH_VASSAL"},
			iFrance : {
				iEgypt : "TXT_KEY_CIV_EGYPT_FRENCH_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_FRENCH_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_FRENCH_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_FRENCH_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_FRENCH_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_FRENCH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_FRENCH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_FRENCH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_FRENCH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_FRENCH_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_FRENCH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_FRENCH_VASSAL",
				iSpain : "TXT_KEY_CIV_SPAIN_FRENCH_VASSAL",
				iEngland : "TXT_KEY_CIV_ENGLAND_FRENCH_VASSAL",
				iHolyRome : "TXT_KEY_CIV_GERMANY_FRENCH_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_FRENCH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_FRENCH_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_FRENCH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_FRENCH_VASSAL",
				iPortugal : "TXT_KEY_CIV_PORTUGAL_FRENCH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_FRENCH_VASSAL",
				iItaly : "TXT_KEY_CIV_ROME_FRENCH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_FRENCH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_FRENCH_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_FRENCH_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_FRENCH_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_FRENCH_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_FRENCH_VASSAL"},
			iEngland : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ENGLISH_VASSAL",
				iIndia : "TXT_KEY_CIV_INDIA_ENGLISH_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ENGLISH_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_ENGLISH_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ENGLISH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ENGLISH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_ENGLISH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ENGLISH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_ENGLISH_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_ENGLISH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_ENGLISH_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_ENGLISH_VASSAL",
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_ENGLISH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ENGLISH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_ENGLISH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_ENGLISH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_ENGLISH_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_ENGLISH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_ENGLISH_VASSAL",
				iThailand : "TXT_KEY_CIV_THAILAND_ENGLISH_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_ENGLISH_VASSAL",
				iAmerica : "TXT_KEY_CIV_AMERICA_ENGLISH_VASSAL"},
			iHolyRome : {
				iRome : "TXT_KEY_CIV_ROME_HOLY_ROMAN_VASSAL",
				iFrance : "TXT_KEY_CIV_FRANCE_HOLY_ROMAN_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_HOLY_ROMAN_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_HOLY_ROMAN_VASSAL",
				iItaly : "TXT_KEY_CIV_ITALY_HOLY_ROMAN_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_HOLY_ROMAN_VASSAL"},
			iNetherlands : {
				iIndonesia : "TXT_KEY_CIV_INDONESIA_DUTCH_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_DUTCH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_DUTCH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_DUTCH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_DUTCH_VASSAL"},
			iRussia: {
				iAmerica : "TXT_KEY_CIV_AMERICA_RUSSIAN_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_RUSSIAN_VASSAL"},
			iPortugal : {
				iIndia : "TXT_KEY_CIV_INDIA_PORTUGUESE_VASSAL",
				iIndonesia : "TXT_KEY_CIV_INDONESIA_PORTUGUESE_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_PORTUGUESE_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_PORTUGUESE_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_PORTUGUESE_VASSAL"},
			#iMali - none so far
			#iPoland - none so far
			#iInca - none so far
			iMongolia : {
				iThailand : "TXT_KEY_CIV_THAILAND_MONGOL_VASSAL",
				iEgypt : "TXT_KEY_CIV_EGYPT_MONGOL_VASSAL",
				iChina : "TXT_KEY_CIV_CHINA_MONGOL_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_MONGOL_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_MONGOL_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_MONGOL_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_MONGOL_VASSAL",
				iRome : "TXT_KEY_CIV_ROME_MONGOL_VASSAL",
				iItaly : "TXT_KEY_CIV_ROME_MONGOL_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_MONGOL_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_MONGOL_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_MONGOL_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_MONGOL_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_MONGOL_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_MONGOL_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_MONGOL_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_MONGOL_VASSAL",
				iTurkey : "TXT_KEY_CIV_TURKEY_MONGOL_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_MONGOL_VASSAL"},
			#iAztecs - none so far
			iTurkey : {
				iThailand : "TXT_KEY_CIV_THAILAND_TURKISH_VASSAL",
				iEgypt : "TXT_KEY_CIV_EGYPT_TURKISH_VASSAL",
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_TURKISH_VASSAL",
				iPersia : "TXT_KEY_CIV_PERSIA_TURKISH_VASSAL",
				iGreece : "TXT_KEY_CIV_GREECE_TURKISH_VASSAL",
				iCarthage : "TXT_KEY_CIV_PHOENICIA_TURKISH_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_TURKISH_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_TURKISH_VASSAL",
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_TURKISH_VASSAL",
				iVikings : "TXT_KEY_CIV_VIKINGS_TURKISH_VASSAL",
				iArabia : "TXT_KEY_CIV_ARABIA_TURKISH_VASSAL",
				iKhmer : "TXT_KEY_CIV_KHMER_TURKISH_VASSAL",
				iRussia : "TXT_KEY_CIV_RUSSIA_TURKISH_VASSAL",
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_TURKISH_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_TURKISH_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_TURKISH_VASSAL",
				iMughals : "TXT_KEY_CIV_MUGHALS_TURKISH_VASSAL"},
			iMughals : {
				iIndia : "TXT_KEY_CIV_INDIA_MUGHAL_VASSAL"},
			#iThailand - none so far
			#iCongo - none so far
			iGermany : {
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_GERMAN_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_GERMAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_GERMAN_VASSAL",
				iInca : "TXT_KEY_CIV_INCA_GERMAN_VASSAL",
				iMali : "TXT_KEY_CIV_MALI_GERMAN_VASSAL",
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_GERMAN_VASSAL",
				iPoland : "TXT_KEY_CIV_POLAND_GERMAN_VASSAL"},
			iAmerica : {
				iEngland : "TXT_KEY_CIV_ENGLAND_AMERICAN_VASSAL",
				iJapan : "TXT_KEY_CIV_JAPAN_AMERICAN_VASSAL",
				iGermany : "TXT_KEY_CIV_GERMANY_AMERICAN_VASSAL",
				iMaya : "TXT_KEY_CIV_MAYA_AMERICAN_VASSAL",
				iKorea : "TXT_KEY_CIV_KOREA_AMERICAN_VASSAL",
				iAztecs : "TXT_KEY_CIV_AZTECS_AMERICAN_VASSAL",}
		}
		
		self.genericVassalNames = {
			iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL_GENERIC",
			iRome : "TXT_KEY_CIV_ROMAN_VASSAL_GENERIC",
			iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL_GENERIC",
			iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL_GENERIC",
			iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL_GENERIC",
			iSpain : "TXT_KEY_CIV_SPANISH_VASSAL_GENERIC",
			iFrance : "TXT_KEY_CIV_FRENCH_VASSAL_GENERIC",
			iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL_GENERIC",
			iMongolia : "TXT_KEY_CIV_MONGOL_VASSAL_GENERIC",
			iTurkey : "TXT_KEY_CIV_TURKISH_VASSAL_GENERIC"
		}
				
		self.sovietVassals = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_SOVIET_VASSAL",
                        iIndia : "TXT_KEY_CIV_INDIA_SOVIET_VASSAL",
                        iChina : "TXT_KEY_CIV_CHINA_SOVIET_VASSAL",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_SOVIET_VASSAL",
                        iGreece : "TXT_KEY_CIV_GREECE_SOVIET_VASSAL",
                        iPersia : "TXT_KEY_CIV_PERSIA_SOVIET_VASSAL",
                        iCarthage : "TXT_KEY_CIV_CARTHAGE_SOVIET_VASSAL",
                        iRome : "TXT_KEY_CIV_ROME_SOVIET_VASSAL",
			iItaly : "TXT_KEY_CIV_ROME_SOVIET_VASSAL",
                        iJapan : "TXT_KEY_CIV_JAPAN_SOVIET_VASSAL",
			iTamils : "TXT_KEY_CIV_TAMILS_SOVIET_VASSAL",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_SOVIET_VASSAL",
                        iKorea : "TXT_KEY_CIV_KOREA_SOVIET_VASSAL",
                        iMaya : "TXT_KEY_CIV_MAYA_SOVIET_VASSAL",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_SOVIET_VASSAL",
                        iVikings : "TXT_KEY_CIV_VIKINGS_SOVIET_VASSAL",
                        iArabia : "TXT_KEY_CIV_ARABIA_SOVIET_VASSAL",
                        iKhmer : "TXT_KEY_CIV_KHMER_SOVIET_VASSAL",
			iTibet : "TXT_KEY_CIV_TIBET_SOVIET_VASSAL",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_SOVIET_VASSAL",
			iMoors : "TXT_KEY_CIV_MOORS_SOVIET_VASSAL",
                        iSpain : "TXT_KEY_CIV_SPAIN_SOVIET_VASSAL",
                        iFrance : "TXT_KEY_CIV_FRANCE_SOVIET_VASSAL",
                        iEngland : "TXT_KEY_CIV_ENGLAND_SOVIET_VASSAL",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_SOVIET_VASSAL",
                        iRussia : "TXT_KEY_CIV_RUSSIA_SOVIET_VASSAL",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_SOVIET_VASSAL",
                        iMali : "TXT_KEY_CIV_MALI_SOVIET_VASSAL",
			iPoland : "TXT_KEY_CIV_POLAND_SOVIET_VASSAL",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_SOVIET_VASSAL",
                        iInca : "TXT_KEY_CIV_INCA_SOVIET_VASSAL",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_SOVIET_VASSAL",
                        iAztecs : "TXT_KEY_CIV_AZTECS_SOVIET_VASSAL",
                        iTurkey : "TXT_KEY_CIV_TURKEY_SOVIET_VASSAL",
			iMughals : "TXT_KEY_CIV_MUGHALS_SOVIET_VASSAL",
			iThailand : "TXT_KEY_CIV_THAILAND_SOVIET_VASSAL",
			iCongo : "TXT_KEY_CIV_CONGO_SOVIET_VASSAL",
			iGermany : "TXT_KEY_CIV_GERMANY_SOVIET_VASSAL",
                        iAmerica : "TXT_KEY_CIV_AMERICA_SOVIET_VASSAL",
                }
		
		self.naziVassals = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_NAZI_VASSAL",
                        iIndia : "TXT_KEY_CIV_INDIA_NAZI_VASSAL",
                        iChina : "TXT_KEY_CIV_CHINA_NAZI_VASSAL",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_NAZI_VASSAL",
                        iGreece : "TXT_KEY_CIV_GREECE_NAZI_VASSAL",
                        iPersia : "TXT_KEY_CIV_PERSIA_NAZI_VASSAL",
                        iCarthage : "TXT_KEY_CIV_CARTHAGE_NAZI_VASSAL",
                        iRome : "TXT_KEY_CIV_ROME_NAZI_VASSAL",
			iItaly : "TXT_KEY_CIV_ROME_NAZI_VASSAL",
                        iJapan : "TXT_KEY_CIV_JAPAN_NAZI_VASSAL",
			iTamils : "TXT_KEY_CIV_TAMILS_NAZI_VASSAL",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_NAZI_VASSAL",
                        iKorea : "TXT_KEY_CIV_KOREA_NAZI_VASSAL",
                        iMaya : "TXT_KEY_CIV_MAYA_NAZI_VASSAL",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_NAZI_VASSAL",
                        iVikings : "TXT_KEY_CIV_VIKINGS_NAZI_VASSAL",
                        iArabia : "TXT_KEY_CIV_ARABIA_NAZI_VASSAL",
			iTibet : "TXT_KEY_CIV_TIBET_NAZI_VASSAL",
                        iKhmer : "TXT_KEY_CIV_KHMER_NAZI_VASSAL",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_NAZI_VASSAL",
			iMoors : "TXT_KEY_CIV_MOORS_NAZI_VASSAL",
                        iSpain : "TXT_KEY_CIV_SPAIN_NAZI_VASSAL",
                        iFrance : "TXT_KEY_CIV_FRANCE_NAZI_VASSAL",
                        iEngland : "TXT_KEY_CIV_ENGLAND_NAZI_VASSAL",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_NAZI_VASSAL",
                        iRussia : "TXT_KEY_CIV_RUSSIA_NAZI_VASSAL",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_NAZI_VASSAL",
                        iMali : "TXT_KEY_CIV_MALI_NAZI_VASSAL",
			iPoland : "TXT_KEY_CIV_POLAND_NAZI_VASSAL",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_NAZI_VASSAL",
                        iInca : "TXT_KEY_CIV_INCA_NAZI_VASSAL",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_NAZI_VASSAL",
                        iAztecs : "TXT_KEY_CIV_AZTECS_NAZI_VASSAL",
                        iTurkey : "TXT_KEY_CIV_TURKEY_NAZI_VASSAL",
			iMughals : "TXT_KEY_CIV_MUGHALS_NAZI_VASSAL",
			iThailand : "TXT_KEY_CIV_THAILAND_NAZI_VASSAL",
			iCongo : "TXT_KEY_CIV_CONGO_NAZI_VASSAL",
			iGermany : "TXT_KEY_CIV_GERMANY_NAZI_VASSAL",
                        iAmerica : "TXT_KEY_CIV_AMERICA_NAZI_VASSAL",
                }

                self.fascistNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_FASCIST",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_FASCIST",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_FASCIST",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_FASCIST",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_FASCIST",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_FASCIST",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_FASCIST",
                        iRome : "TXT_KEY_CIV_ROME_DESC_FASCIST",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_FASCIST",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_FASCIST",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_FASCIST",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_FASCIST",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_FASCIST",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_FASCIST",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_FASCIST",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_FASCIST",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_FASCIST",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_FASCIST",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_FASCIST",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_FASCIST",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_FASCIST",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_FASCIST",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_FASCIST",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_FASCIST",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_FASCIST",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_FASCIST",
                        iMali : "TXT_KEY_CIV_MALI_DESC_FASCIST",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_FASCIST",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_FASCIST",
                        iInca : "TXT_KEY_CIV_INCA_DESC_FASCIST",
			iItaly : "TXT_KEY_CIV_ROME_DESC_FASCIST",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_FASCIST",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_FASCIST",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_FASCIST",
			iMughals: "TXT_KEY_CIV_MUGHALS_DESC_FASCIST",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_FASCIST",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_FASCIST",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_FASCIST",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_FASCIST",
                }

                self.communistNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_COMMUNIST",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_COMMUNIST",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_COMMUNIST",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_COMMUNIST",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_COMMUNIST",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_COMMUNIST",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_COMMUNIST",
                        iRome : "TXT_KEY_CIV_ROME_DESC_COMMUNIST",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_COMMUNIST",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_COMMUNIST",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_COMMUNIST",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_COMMUNIST",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_COMMUNIST",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_COMMUNIST",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_COMMUNIST",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_COMMUNIST",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_COMMUNIST",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_COMMUNIST",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_COMMUNIST",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_COMMUNIST",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_COMMUNIST",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_COMMUNIST",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_COMMUNIST",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_COMMUNIST",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_COMMUNIST",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_COMMUNIST",
                        iMali : "TXT_KEY_CIV_MALI_DESC_COMMUNIST",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_COMMUNIST",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_COMMUNIST",
                        iInca : "TXT_KEY_CIV_INCA_DESC_COMMUNIST",
			iItaly : "TXT_KEY_CIV_ROME_DESC_COMMUNIST",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_COMMUNIST",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_COMMUNIST",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_COMMUNIST",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_COMMUNIST",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_COMMUNIST",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_COMMUNIST",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_COMMUNIST",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_COMMUNIST",
                }

                self.democraticNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_DEMOCRATIC",
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_DEMOCRATIC",
                        iChina : "TXT_KEY_CIV_CHINA_DESC_DEMOCRATIC",
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_DEMOCRATIC",
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_DEMOCRATIC",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_DEMOCRATIC",
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_DEMOCRATIC",
                        iRome : "TXT_KEY_CIV_ROME_DESC_DEMOCRATIC",
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_DEMOCRATIC",
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_DEMOCRATIC",
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_DEMOCRATIC",
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_DEMOCRATIC",
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_DEMOCRATIC",
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_DEMOCRATIC",
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_DEMOCRATIC",
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_DEMOCRATIC",
			iTibet : "TXT_KEY_CIV_TIBET_DESC_DEMOCRATIC",
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_DEMOCRATIC",
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_DEMOCRATIC",
			iMoors : "TXT_KEY_CIV_MOORS_DESC_DEMOCRATIC",
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_DEMOCRATIC",
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_DEMOCRATIC",
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_DEMOCRATIC",
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_DEMOCRATIC",
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_DEMOCRATIC",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC",
                        iMali : "TXT_KEY_CIV_MALI_DESC_DEMOCRATIC",
			iPoland : "TXT_KEY_CIV_POLAND_DESC_DEMOCRATIC",
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_DEMOCRATIC",
                        iInca : "TXT_KEY_CIV_INCA_DESC_DEMOCRATIC",
			iItaly : "TXT_KEY_CIV_ROME_DESC_DEMOCRATIC",
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_DEMOCRATIC",
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_DEMOCRATIC",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_DEMOCRATIC",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_DEMOCRATIC",
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_DEMOCRATIC",
			iCongo : "TXT_KEY_CIV_CONGO_DESC_DEMOCRATIC",
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_DEMOCRATIC",
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_DEMOCRATIC",
                }
		
		self.modernIslamNames = {
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_ISLAMIC_MODERN",
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_ISLAMIC_MODERN",
                        iMali : "TXT_KEY_CIV_MALI_DESC_ISLAMIC_MODERN",
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_ISLAMIC_MODERN",
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_ISLAMIC_MODERN",
                }
		
		self.startingLeaders = {
			iEgypt : con.iRamesses,
			iIndia : con.iAsoka,
			iChina : con.iQinShiHuang,
			iBabylonia : con.iGilgamesh,
			iGreece : con.iPericles,
			iPersia : con.iCyrus,
			iCarthage : con.iHiram,
			iRome : con.iJuliusCaesar,
			iJapan : con.iJimmu,
			iTamils : con.iRajendra,
			iEthiopia : con.iZaraYaqob,
			iKorea : con.iWangKon,
			iMaya : con.iPacal,
			iByzantium : con.iJustinian,
			iVikings : con.iRagnar,
			iArabia : con.iHarun,
			iTibet : con.iSongtsen,
			iKhmer : con.iSuryavarman,
			iIndonesia : con.iDharmasetu,
			iMoors : con.iRahman,
			iSpain : con.iIsabella,
			iFrance : con.iCharlemagne,
			iEngland : con.iAlfred,
			iHolyRome : con.iBarbarossa,
			iRussia : con.iYaroslav,
			iNetherlands : con.iWillemVanOranje,
			iMali : con.iMansaMusa,
			iPoland : con.iCasimir,
			iPortugal : con.iAfonso,
			iInca : con.iHuaynaCapac,
			iItaly : con.iLorenzo,
			iMongolia : con.iGenghisKhan,
			iAztecs : con.iMontezuma,
			iMughals : con.iTughluq,
			iTurkey : con.iMehmed,
			iThailand : con.iNaresuan,
			iCongo : con.iMbemba,
			iGermany : con.iFrederick,
			iAmerica : con.iWashington
		}
		
		self.lateStartingLeaders = {
			iChina : con.iTaizong
		}
		
	def getAnarchyTurns(self, iPlayer):
		return sd.scriptDict['lAnarchyTurns'][iPlayer]
		
	def changeAnarchyTurns(self, iPlayer, iAmount):
		sd.scriptDict['lAnarchyTurns'][iPlayer] += iAmount
		
	def getResurrections(self, iPlayer):
		return sd.scriptDict['lResurrections'][iPlayer]
		
	def changeResurrections(self, iPlayer, iAmount):
		sd.scriptDict['lResurrections'][iPlayer] += iAmount
		
	#def getPreviousOwners(self, iPlayer):
        #        return sd.scriptDict['lPreviousOwners']
		
	#def addPreviousOwner(self, iPlayer, iPreviousOwner):
	#	sd.scriptDict['lPreviousOwners'].append(iPreviousOwner)
		
	#def removePreviousOwner(self, iPlayer, iPreviousOwner):
	#	sd.scriptDict['lPreviousOwner'].remove(iPreviousOwner)
                

        def setCivDesc(self, iCiv, sName, sInsert=""):
		if sInsert == "":
			gc.getPlayer(iCiv).setCivDescription(localText.getText(sName, ()))
		else:
			gc.getPlayer(iCiv).setCivDescription(localText.getText(sName, (sInsert,)))
			
	def setCivName(self, iCiv, sName, sShort, sAdjective):
		gc.getPlayer(iCiv).setCivName(localText.getText(sName, ()), localText.getText(sShort, ()), localText.getText(sAdjective, ()))
	
	def setCivAdjective(self, iCiv, sAdj):
		gc.getPlayer(iCiv).setCivAdjective(sAdj)
		
	def setCivShortDesc(self, iCiv, sShort):
		gc.getPlayer(iCiv).setCivShortDescription(sShort)
		
	def setLeader(self, iCiv, iLeader):
		if gc.getPlayer(iCiv).getLeader() != iLeader:
			gc.getPlayer(iCiv).setLeader(iLeader)

        def setup(self):
                for iPlayer in range(iNumPlayers):
                        pPlayer = gc.getPlayer(iPlayer)
                        self.setCivDesc(iPlayer, self.peopleNames[iPlayer])
			
			if not gc.getPlayer(iPlayer).isHuman():
				self.setLeader(iPlayer, self.startingLeaders[iPlayer])
			
				if not gc.getPlayer(iEgypt).isPlayable() and iPlayer in self.lateStartingLeaders:
					self.setLeader(iPlayer, self.lateStartingLeaders[iPlayer])
			
		if not gc.getPlayer(iEgypt).isPlayable():
			self.changeAnarchyTurns(iChina, 3)
			self.setCivDesc(iByzantium, "TXT_KEY_CIV_BYZANTIUM_DESC_DEFAULT")

        def setDetermineds(self, iPlayer, szName="", szFlag=""):
                pPlayer = gc.getPlayer(iPlayer)
                if szName:
                        self.setCivDesc(iPlayer, szName)
                if szFlag:
                        pPlayer.setFlag(szFlag)
			
	def isDemocratic(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic0 = pPlayer.getCivics(0)
		iCivic1 = pPlayer.getCivics(1)
		
		if iCivic0 == con.iRepublic:
			return True
		if iCivic0 == con.iAutocracy and (iCivic1 == con.iRepresentation or iCivic1 == con.iUniversalSuffrage):
			return True
			
		return False
		
	def isCommunist(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic3 = pPlayer.getCivics(3)
		
		if iCivic3 == con.iStateProperty:
			return True
			
		return False
		
	def isFascist(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic2 = pPlayer.getCivics(2)
		
		if iCivic2 == con.iTotalitarianism:
			return True
			
		return False
		
	def isEmpire(self, iPlayer):
		iThreshold = 6
		
		if iPlayer == iCarthage: iThreshold = 4
		elif iPlayer == iIndonesia: iThreshold = 4
		elif iPlayer == iKorea: iThreshold = 3
		elif iPlayer == iRussia: iThreshold = 8
		elif iPlayer == iHolyRome and gc.getPlayer(iHolyRome).isReborn(): iThreshold = 3
		elif iPlayer == iHolyRome: iThreshold = 4
		elif iPlayer == iGermany: iThreshold = 4
		elif iPlayer == iPersia and pPersia.isReborn(): iThreshold = 4
		elif iPlayer == iItaly: iThreshold = 4
		elif iPlayer == iInca: iThreshold = 3
		elif iPlayer == iMongolia: iThreshold = 6
		elif iPlayer == iPoland: iThreshold = 3
		elif iPlayer == iMoors: iThreshold = 3
		elif iPlayer == iTibet: iThreshold = 2
			
		return gc.getPlayer(iPlayer).getNumCities() >= iThreshold
		
		
        def checkName(self, iPlayer, lPreviousOwners=[]):
        
                if iPlayer >= iNumPlayers: return
		
		if not gc.getPlayer(iPlayer).isAlive(): return
        
                bVassal = utils.isAVassal(iPlayer)
                iMaster = utils.getMaster(iPlayer)
                pPlayer = gc.getPlayer(iPlayer)
                tPlayer = gc.getTeam(pPlayer.getTeam())
                if iMaster != -1:
                        pMasterPlayer = gc.getPlayer(iMaster)
                bReborn = pPlayer.isReborn()
                iReligion = pPlayer.getStateReligion()
                capital = gc.getPlayer(iPlayer).getCapitalCity()
                tCapitalCoords = (capital.getX(), capital.getY())
                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iGameTurn = gc.getGame().getGameTurn()
                bAnarchy = pPlayer.isAnarchy()
		bEmpire = self.isEmpire(iPlayer)
		bCityStates = (iCivic0 == con.iCityStates)
		bTheocracy = (iCivic0 == con.iTheocracy)
		bResurrected = (self.getResurrections(iPlayer) > 0)
		iAnarchyTurns = self.getAnarchyTurns(iPlayer)
		iEra = pPlayer.getCurrentEra()
		iGameEra = gc.getGame().getCurrentEra()
		# count number of resurrections (use to determine transition to medieval Egypt, Saudi-Arabia etc.)
		# count anarchy turns (use for different dynasties, e.g. China or Egypt)
		
		if iPlayer in [iRome, iCarthage, iGreece, iIndia, iMaya, iAztecs]:
			if not gc.getTeam(iPlayer).isHasTech(con.iCodeOfLaws):
				bCityStates = True
		
                bWar = False
                for iTarget in range(iNumMajorPlayers):
                        if tPlayer.isAtWar(iTarget):
                                bWar = True
				break
                # Vassalage --> Civics/ Religion/ Size --> Default names
		
		# Leoreth: Vassalage (historical -> generic -> default) -> Civics -> Historical (usually religion -> civics -> size) -> Default
                
                # by vassalage
                if bVassal:
			if iMaster == iRussia and pMasterPlayer.getCivics(3) == con.iStateProperty:
				self.setCivDesc(iPlayer, self.sovietVassals[iPlayer])
				return
			if iMaster == iGermany and pMasterPlayer.getCivics(2) == con.iTotalitarianism:
				self.setCivDesc(iPlayer, self.naziVassals[iPlayer])
				return
				
			# special cases
			if iMaster == iRome and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_ROMAN_VASSAL")
				return
			if iMaster == iHolyRome and iPlayer == iPoland and iGameEra >= con.iIndustrial:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_AUSTRIAN_VASSAL")
				return
			
			if iMaster in self.specificVassalNames and not pMasterPlayer.isReborn():
				if iPlayer in self.specificVassalNames[iMaster]:
					self.setCivDesc(iPlayer, self.specificVassalNames[iMaster][iPlayer])
					return
					
			if iMaster in self.genericVassalNames:
				self.setCivDesc(iPlayer, self.genericVassalNames[iMaster], pPlayer.getCivilizationShortDescriptionKey())
				return
				
			if iPlayer in [iMali, iEthiopia, iCongo, iAztecs, iInca, iMaya]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_COLONY", pPlayer.getCivilizationShortDescriptionKey())
				return
				
			self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_PROTECTORATE", pPlayer.getCivilizationShortDescriptionKey())
			return
		
		# Communism
		if self.isCommunist(iPlayer):
			if iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_COMMUNIST")
				return
			if iPlayer in self.communistNames:
				self.setCivDesc(iPlayer, self.communistNames[iPlayer])
				return
				
		# Fascism
		if self.isFascist(iPlayer):
			if iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_FASCIST")
				return
			if iPlayer in self.fascistNames:
				self.setCivDesc(iPlayer, self.fascistNames[iPlayer])
				return
			
		# Democracy (includes Islamic Republics)
		if self.isDemocratic(iPlayer):
			if iPlayer == iMughals:
				if iEra <= con.iRenaissance:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MUGHALS_REPUBLIC_MEDIEVAL")
					return
			elif iPlayer == iVikings:
				if capital.getName() == "Stockholm":
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDEN_REPUBLIC")
					return
				elif capital.getName() == "Kobenhavn":
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK_REPUBLIC")
					return
			elif iPlayer == iAmerica:
				if iCivic2 == con.iAgrarianism or iCivic3 == con.iForcedLabor:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_AMERICA_CSA")
					return
			elif iPlayer == iHolyRome:
				if iGameTurn < getTurnForYear(1700):
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_GERMAN_CONFEDERATION")
					return
			elif iPlayer == iCarthage:
				if capital.getX() < 73:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_DEMOCRATIC")
					return
		
		
			if iPlayer in self.democraticNames:
				if iPlayer in self.modernIslamNames and iReligion == con.iIslam:
					self.setCivDesc(iPlayer, self.democraticNames[iPlayer])
				else:
					self.setCivDesc(iPlayer, self.democraticNames[iPlayer])
				return
				
		# Handle other names specifically
		if iPlayer == iEgypt:
			if bResurrected:
				if bTheocracy and iReligion == con.iIslam:
					if iEra <= iMedieval:
						if pArabia.isAlive():
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_FATIMID_CALIPHATE")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_AYYUBID_CALIPHATE")
						return
					elif iEra <= iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MAMLUK_CALIPHATE")
						return
				elif iReligion == con.iIslam:
					if iEra <= iMedieval:
						if pArabia.isAlive():
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_FATIMID_SULTANATE")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_AYYUBID_SULTANATE")
						return
					elif iEra <= iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MAMLUK_SULTANATE")
						return
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_COPTIC")
					return
			else:
				if iGreece in lPreviousOwners:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_PTOLEMAIC")
					return
		
				if bCityStates:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_CITY_STATES")
					return
				
				if iEra == iAncient:
					if iAnarchyTurns == 0:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_OLD_KINGDOM")
					elif iAnarchyTurns == 1:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_NEW_KINGDOM")
					return
				elif iEra == iClassical:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_NEW_KINGDOM")
					return
					
		elif iPlayer == iIndia:
			if bReborn or bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MARATHA")
				return
				
			if iReligion == con.iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_SULTANATE")
				return
				
			if bEmpire and iEra <= iClassical:
				if iReligion == con.iBuddhism:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MAURYA")
					return
				elif iReligion == con.iHinduism:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_GUPTA")
					return
		
			if bCityStates:
				if iEra <= iClassical:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MAHAJANAPADAS")
					return
					
			if bEmpire and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_PALA")
				return
				
			if bEmpire and iEra == iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_VIJAYANAGARA") # check if Vijayanagara is owned
				
		elif iPlayer == iChina:
			if not bResurrected:
				if bEmpire:
					if iEra >= iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QING")
						return
						
					if iEra == iRenaissance and iGameTurn >= getTurnForYear(1400):
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_MING")
						return
						
					if iEra == iMedieval:
						#if iAnarchyTurns <= 2:
						#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SUI")
						if teamChina.isHasTech(con.iPaper) and teamChina.isHasTech(con.iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SONG")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_TANG")
						return
						
					if iEra == iClassical:
						if iGameTurn < getTurnForYear(0):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QIN")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_HAN")
						return
				
					if iEra == iAncient:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_ZHOU")
						return
			else:
				if bEmpire:
					if iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_MING")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QING")
					return
					
		elif iPlayer == iBabylonia:
			if bCityStates and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_CITY_STATES")
				return
		
			if capital.getName() == "Ninova" or capital.getName() == "Kalhu":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_ASSYRIA")
				return
		
			if bEmpire and iEra > iAncient:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE")
				return
				
		elif iPlayer == iGreece:
			if bCityStates:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_EMPIRE")
					return
					
				if bWar:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_LEAGUE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_CITY_STATES")
				return
				
			if iEra <= iClassical:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_MACEDONIA_EMPIRE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_MACEDONIA_KINGDOM")
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_EMPIRE")
				return
				
		elif iPlayer == iPersia:
			if not bReborn:
				if bEmpire and iReligion == con.iZoroastrianism:
					if iGameEra < iMedieval:
						if iGreece in lPreviousOwners:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PARTHIA")
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_ACHAEMENID")
						return
					elif iGameEra == iMedieval:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SASSANID")
						return
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_EMPIRE")
						return
			else:
				if iReligion == con.iIslam and bTheocracy:
					if iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SAFAVID_CALIPHATE")
					elif iEra == iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_QAJAR_CALIPHATE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PAHLAVI_CALIPHATE")
					return
				elif bEmpire:
					if iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SAFAVID_EMPIRE")
					elif iEra == iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_QAJAR_EMPIRE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PAHLAVI_EMPIRE")
					return
					
		elif iPlayer == iCarthage:	# change adjectives and short desc here too
			if capital.getX() >= 66:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PHOENICIA_CITY_STATES")
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PHOENICIA_SHORT_DESC")
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PHOENICIA_ADJECTIVE")
				return
				
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_SHORT_DESC")
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_EMPIRE")
				return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_CITY_STATES")
				return
			# make Carthaginian Kingdom default
			
		elif iPlayer == iRome:
			if pByzantium.isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_WESTERN_EMPIRE")
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_EMPIRE")
				return
				
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_REPUBLIC")
				return
					
		elif iPlayer == iJapan:
			if bEmpire or iCivic1 == con.iAbsolutism or iEra >= iIndustrial: # Absolutism
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_JAPAN_EMPIRE")
				return
				
			# make Shogunate default
				
		elif iPlayer == iEthiopia:
			if not gc.getGame().isReligionFounded(con.iIslam):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ETHIOPIA_AKSUM")
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ETHIOPIA_EMPIRE")
				return
				
			# make Ethiopian Kingdom default
			
		elif iPlayer == iKorea:		# difference Goryeo and Joseon with religion?
			if iEra < iMedieval:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_GOGURYEO")
					return
			if iEra <= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_GORYEO")
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_EMPIRE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_JOSEON")
				return
				
		#elif iPlayer == iMaya: # city states are default
				
		elif iPlayer == iByzantium:
			if pRome.isAlive() and not pRome.isReborn():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_EASTERN_EMPIRE")
				return
				
			if capital.getName() == "Trapezounta":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_TREBIZOND_EMPIRE")
				return
			elif capital.getName() == "Dyrrachion":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_EPIRUS_DESPOTATE")
				return
			elif capital.getName() == "Athina":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_MOREA_DESPOTATE")
				return
			elif capital.getName() != "Konstantinoupolis":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_NICAEA_EMPIRE")
				return
				
		elif iPlayer == iVikings:
			if iReligion == -1:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_NORSE_KINGDOMS")
				return
			else:
				if bEmpire:
					if iEra <= iMedieval:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_KALMAR_UNION")
					elif iEra == iRenaissance or capital.getName() == "Stockholm":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDISH_EMPIRE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK_NORWAY")
					return
				else:
					if capital.getName() == "Oslo" or capital.getName() == "Trondheim" or capital.getName() == "Nidaros":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_NORWAY")
						return
					elif capital.getName() == "Stockholm" or capital.getName() == "Kalmar":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDEN")
						return
					elif capital.getName() == "Kobenhavn":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK")
						return
						
		elif iPlayer == iArabia:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_SAUDI")
				return
		
			if iReligion == con.iIslam and bTheocracy:
				if not bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_RASHIDUN_CALIPHATE")
				else:
					if capital.getName() == "Dimashq":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_UMMAYAD_CALIPHATE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_ABBASID_CALIPHATE")
				return
				
			# Arabian Sultanates as default, Arabian leaders should prefer Theocracy
			
		elif iPlayer == iTibet:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TIBET_EMPIRE")
				return
				
			# Kingdom of Tibet as default
			
		elif iPlayer == iKhmer:
			if iEra <= iRenaissance and capital.getName() == "Angkor":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_EMPIRE")
				return
			elif capital.getName() == "Hanoi":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_VIETNAM")
				return
			elif capital.getName() == "Pagan":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_BURMA")
				return
			elif capital.getName() == "Dali":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_NANZHAO")
				return
				
			# Kingdom of Cambodia default
				
		elif iPlayer == iIndonesia:
			if iReligion == con.iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_MATARAM")
				return
		
			if iEra <= iRenaissance:
				if not bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_SRIVIJAYA")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_MAJAPAHIT")
				return
			
			# generic name as default
			
		elif iPlayer == iMoors:
			bAndalusia = utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR)
			
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_TAIFAS")
				return
				
			if bAndalusia:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_CALIPHATE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_CORDOBA")
				return
				
			if bEmpire and iEra <= iRenaissance:
				if bTheocracy and iReligion == con.iIslam:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_ALMOHAD_CALIPHATE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_ALMOHAD_EMPIRE")
				return
				
			# Kingdom of Morocco as default

		elif iPlayer == iSpain:
			if iReligion == con.iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_SULTANATE")
				return
				
			bSpain = True
			if pMoors.isAlive():
				moorishCapital = gc.getPlayer(iMoors).getCapitalCity()
				if utils.isPlotInArea((moorishCapital.getX(), moorishCapital.getY()), vic.tIberiaTL, vic.tIberiaBR):
					bSpain = False
				
			if bEmpire and iEra > iMedieval:
				if bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_CASTILIAN_EMPIRE")
				return
				
			if (capital.getName() == "Barcelona" or capital.getName() == "Valencia") and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_ARAGON")
				return
				
			bSpain = True
			if pMoors.isAlive():
				moorishCapital = gc.getPlayer(iMoors).getCapitalCity()
				if utils.isPlotInArea((moorishCapital.getX(), moorishCapital.getY()), vic.tIberiaTL, vic.tIberiaBR):
					bSpain = False
			
			if iGameTurn > getTurnForYear(con.tBirth[iPortugal]):
				if not pPortugal.isAlive() and bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_IBERIA")
					return
			
				pPortugueseCapital = gc.getPlayer(iPortugal).getCapitalCity()	
				if not utils.isPlotInArea((pPortugueseCapital.getX(), pPortugueseCapital.getY()), con.tCoreAreasTL[0][iPortugal], con.tCoreAreasBR[0][iPortugal], con.tExceptions[0][iPortugal]) and bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_IBERIA")
					return
		
			if not bSpain:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_CASTILLE")
				return
				
		elif iPlayer == iFrance:
			#if capital.getName() == "Nouvelle Orl&#233;ans":
			#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_LOUISIANA")
			#	return
				
			#if utils.isPlotInArea(tCapitalCoords, tNCAmericaTL, tNCAmericaBR):
			#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_QUEBEC")
			#	return
		
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iFrance], con.tCoreAreasBR[0][iFrance], con.tExceptions[0][iFrance]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_EXILE")
				return
		
			if (iEra > iRenaissance and bEmpire) or iCivic0 == 3:	# Autocracy
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_EMPIRE")
				return
				
			if not pHolyRome.isAlive() and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_FRANKISH_EMPIRE")
				return
				
		elif iPlayer == iEngland:
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iEngland], con.tCoreAreasBR[0][iEngland], con.tExceptions[0][iEngland]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_EXILE")
				return
		
			if iEra < iIndustrial:
				if utils.getMaster(iFrance) == iEngland:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE")
					return
			
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN")
					return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_EMPIRE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM")
				return
				
		elif iPlayer == iHolyRome:
			if bEmpire:
				if pGermany.isAlive():
					if iCivic1 == con.iRepresentation:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_HUNGARY")
						return
						
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_EMPIRE")
					return
					
				lEuroCivs = [iVikings, iSpain, iFrance, iEngland, iRome, iItaly, iPoland, iPortugal, iNetherlands]
				iCounter = 0
				
				for iLoopCiv in lEuroCivs:
					if utils.getMaster(iLoopCiv) == iHolyRome:
						iCounter += 1
						
				if iCounter >= 2:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_HABSBURG_EMPIRE")
					return
				
				if iEra <= con.iRenaissance:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_HRE")
					return
			
			if pGermany.isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_ARCHDUCHY")
				return
				
			# Kingdom of Germany as default
			
		elif iPlayer == iRussia:
			if bEmpire and iEra > iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_RUSSIA_EMPIRE")
				return
		
			if iEra == iMedieval and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_RUSSIA_MUSCOVY")
				return
				
		elif iPlayer == iNetherlands:
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC")
				return
		
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iNetherlands], con.tCoreAreasBR[0][iNetherlands], con.tExceptions[0][iNetherlands]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_EXILE")
				return
		
			if iEra < iIndustrial:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM")
					return
			else:
				if bEmpire and not bCityStates:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_EMPIRE")
					return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC")
				return

			# Kingdom as default
			
		elif iPlayer == iMali:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MALI_SONGHAI")
				return
				
			# Empire as default
			
		elif iPlayer == iPoland:
			if bEmpire and iEra >= con.iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_EMPIRE")
				return
				
			if capital.getName() == 'Kowno' or capital.getName() == 'Medvegalis' or capital.getName() == 'Klajpeda' or capital.getName == 'Wilno' or capital.getName() == 'Riga':
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_LITHUANIA")
				return
				
			# Kingdom as default
			
		elif iPlayer == iPortugal:
			if utils.isPlotInArea(tCapitalCoords, tBrazilTL, tBrazilBR):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_BRAZIL")
				return
				
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iPortugal], con.tCoreAreasBR[0][iPortugal], con.tExceptions[0][iPortugal]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_EXILE")
				return
		
			if bEmpire and iEra > iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_EMPIRE")
				return
				
			# Kingdom as default
			
		elif iPlayer == iInca:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_EMPIRE")
				return
				
			# Kingdom of Cuzco as default
			
		elif iPlayer == iItaly:
			if bCityStates:
				if bWar:
					if bEmpire:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_ITALIAN_LEAGUE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_LOMBARD_LEAGUE")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS")
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_KINGDOM")
				else:
					if capital.getName() == "Fiorenza" or capital.getName() == "Firenze":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_TUSCANY")
					elif capital.getName() == "Venezia":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_VENICE")
					elif capital.getName() == "Milano":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_MILAN")
					elif capital.getName() == "Roma":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_PAPAL_STATE")
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_KINGDOM")
				return
			
		elif iPlayer == iMongolia:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_EMPIRE")
				return
				
			if capital.getX() >= 99 and capital.getY() <= 43:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_YUAN")
				return
				
			if capital.getName() == 'Samarkand' or capital.getName() == 'Samarqand' or capital.getName() == 'Merv' or capital.getName() == 'Marv':
				if pMongolia.getStateReligion() == con.iIslam:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_TIMURID")
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_CHAGATAI")
				return
		
			if iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_KHAMAG")
				return
					
			# Mongol State as default
			
		elif iPlayer == iAztecs:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MEXICO_EMPIRE")
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AZTECS_EMPIRE")
				return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AZTECS_ALTEPETL")
				return
				
			# Triple Alliance as default
			
		elif iPlayer == iMughals:
			if iEra == iMedieval and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MUGHALS_DELHI")
				return
				
			# Mughal Empire as default
			
		elif iPlayer == iTurkey:
			if iReligion != con.iIslam:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_EMPIRE")
					return
			
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_STATE")
				return
		
			if bTheocracy:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_CALIPHATE")
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_EMPIRE")
				return
				
			# Ottoman Sultanate as default
			
		elif iPlayer == iThailand:
			if iEra <= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_THAILAND_AYUTTHAYA")
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_THAILAND_EMPIRE")
					return
					
			# Siam as default
			
		elif iPlayer == iGermany:
			if bEmpire:
				if utils.getMaster(iHolyRome) == iGermany:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE")
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_GERMANY_EMPIRE")
				return
				
			# Kingdom of Prussia as default
			
		elif iPlayer == iAmerica:
			if iCivic3 == con.iForcedLabor or iCivic2 == con.iAgrarianism:	# Forced Labor/Agrarianism
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AMERICA_CSA")
				return
				
			# Empire of Columbia as default
		
		#if iPlayer == iCarthage:
		#	self.setCivName(iPlayer, self.defaultNames[iPlayer], "TXT_KEY_CIV_CARTHAGE_SHORT_DESC", "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")
		#elif iPlayer == iHolyRome:
		#	self.setCivName(iPlayer, self.defaultNames[iPlayer], "TXT_KEY_CIV_GERMANY_SHORT_DESC", "TXT_KEY_CIV_GERMANY_ADJECTIVE")
			
		self.setCivDesc(iPlayer, self.defaultNames[iPlayer])
				
	
	def checkLeader(self, iPlayer):
        
                if iPlayer >= iNumPlayers: return
		
		if not gc.getPlayer(iPlayer).isAlive(): return
		
		if gc.getPlayer(iPlayer).isHuman(): return
		
                pPlayer = gc.getPlayer(iPlayer)
                tPlayer = gc.getTeam(pPlayer.getTeam())
                bReborn = pPlayer.isReborn()
                iReligion = pPlayer.getStateReligion()
                capital = gc.getPlayer(iPlayer).getCapitalCity()
                tCapitalCoords = (capital.getX(), capital.getY())
                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iGameTurn = gc.getGame().getGameTurn()
		bEmpire = self.isEmpire(iPlayer)
		bCityStates = (iCivic0 == con.iCityStates or not gc.getTeam(pPlayer.getTeam()).isHasTech(con.iCodeOfLaws))
		bTheocracy = (iCivic0 == con.iTheocracy)
		bResurrected = (self.getResurrections(iPlayer) > 0)
		bMonarchy = not (self.isCommunist(iPlayer) or self.isFascist(iPlayer) or self.isDemocratic(iPlayer))
		iAnarchyTurns = self.getAnarchyTurns(iPlayer)
		iEra = pPlayer.getCurrentEra()
		iGameEra = gc.getGame().getCurrentEra()
		
		
		if iPlayer == iEgypt:
		
			if not bMonarchy and iEra >= con.iModern:
				self.setLeader(iPlayer, con.iNasser)
				return
			
			if bResurrected or not gc.getPlayer(0).isPlayable():
				self.setLeader(iPlayer, con.iBaibars)
				return
				
			if tPlayer.isHasTech(con.iLiterature):
				self.setLeader(iPlayer, con.iCleopatra)
				return
				
		elif iPlayer == iIndia:
		
			if not bMonarchy and iEra >= con.iModern:
				self.setLeader(iPlayer, con.iGandhi)
				return
				
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iShivaji)
				return
				
			if tPlayer.isHasTech(con.iCurrency):
				self.setLeader(iPlayer, con.iChandragupta)
				return
				
		elif iPlayer == iChina:
		
			if self.isCommunist(iPlayer) or self.isDemocratic(iPlayer) and iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iMao)
				return
				
			#if iEra >= con.iIndustrial:
			#	self.setLeader(iPlayer, con.iCixi)
			#	return
				
			if (iEra >= con.iRenaissance and iGameTurn >= getTurnForYear(1400)) or bResurrected:
				self.setLeader(iPlayer, con.iHongwu)
				return
				
			if iEra >= con.iMedieval:
				self.setLeader(iPlayer, con.iTaizong)
				return
				
		elif iPlayer == iBabylonia:
		
			if iGameTurn >= getTurnForYear(-1600):
				self.setLeader(iPlayer, con.iHammurabi)
				return
				
		elif iPlayer == iGreece:
		
			if bEmpire or not bCityStates:
				self.setLeader(iPlayer, con.iAlexander)
				return
				
		elif iPlayer == iPersia:
		
			if bReborn:
				if iEra >= iModern:
					self.setLeader(iPlayer, con.iKhomeini)
					return
					
				self.setLeader(iPlayer, con.iAbbas)
				return
			else:
				if bEmpire:
					self.setLeader(iPlayer, con.iDarius)
					return
					
		elif iPlayer == iCarthage:
		
			if capital.getName() == "Qart-Hadasht" or bEmpire or not bCityStates:
				self.setLeader(iPlayer, con.iHannibal)
				return
				
		elif iPlayer == iRome:
		
			if bReborn:
				self.setLeader(iPlayer, con.iCavour)
				return
			else:
				if bEmpire or not bCityStates:
					self.setLeader(iPlayer, con.iAugustus)
					return
				
		elif iPlayer == iJapan:
		
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iMeiji)
				return
				
			if tPlayer.isHasTech(con.iFeudalism):
				self.setLeader(iPlayer, con.iTokugawa)
				return
				
		elif iPlayer == iEthiopia:
		
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iHaileSelassie)
				return
				
		elif iPlayer == iKorea:
			return
			
		elif iPlayer == iMaya:
			return
			
		elif iPlayer == iByzantium:
			
			if iGameTurn >= getTurnForYear(1000):
				self.setLeader(iPlayer, con.iBasil)
				return
			
		elif iPlayer == iVikings:
		
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iGustav)
				return
				
		elif iPlayer == iArabia:
		
			if iGameTurn >= getTurnForYear(1000):
				self.setLeader(iPlayer, con.iSaladin)
				return
				
		elif iPlayer == iTibet:
		
			if iGameTurn >= getTurnForYear(1500):
				self.setLeader(iPlayer, con.iLobsangGyatso)
				return
				
		elif iPlayer == iKhmer:
			return
			
		elif iPlayer == iIndonesia:
			
			if iEra >= con.iModern:
				self.setLeader(iPlayer, con.iSuharto)
				return
				
			if bEmpire:
				self.setLeader(iPlayer, con.iHayamWuruk)
				return
				
		elif iPlayer == iMoors:
			
			bAndalusia = utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR)
			
			if not bAndalusia:
				self.setLeader(iPlayer, con.iYaqub)
				return
				
		elif iPlayer == iSpain:
		
			if self.isFascist(iPlayer):
				self.setLeader(iPlayer, con.iFranco)
				return
		
			if sd.scriptDict['lFirstContactConquerors'][0] == 1 or sd.scriptDict['lFirstContactConquerors'][1] == 1 or sd.scriptDict['lFirstContactConquerors'][2] == 1:
				self.setLeader(iPlayer, con.iPhilip)
				return
				
		elif iPlayer == iFrance:
		
			if iEra >= con.iModern:
				self.setLeader(iPlayer, con.iDeGaulle)
				return
				
			if iEra >= con.iIndustrial or tPlayer.isHasTech(con.iNationalism):
				self.setLeader(iPlayer, con.iNapoleon)
				return
				
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iLouis)
				return
				
		elif iPlayer == iEngland:
		
			if iEra >= con.iModern:
				self.setLeader(iPlayer, con.iChurchill)
				return
				
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iVictoria)
				return
				
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iElizabeth)
				return
				
		elif iPlayer == iHolyRome:
		
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iFrancis)
		
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iCharles)
				return
				
		elif iPlayer == iRussia:
		
			if not bMonarchy and iEra >= iIndustrial:
				self.setLeader(iPlayer, con.iStalin)
				if self.isCommunist(iPlayer):
                                        CityNameManager.CityNameManager().sovietNames()
				return
				
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iNicholas)
				return
				
			if iEra >= con.iRenaissance:
				if iGameTurn >= getTurnForYear(1700):
					self.setLeader(iPlayer, con.iCatherine)
				else:
					self.setLeader(iPlayer, con.iPeter)
				return
				
		elif iPlayer == iNetherlands:
			return
			
		elif iPlayer == iMali:
			return
			
		elif iPlayer == iPoland:
		
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iSobieski)
				return
			
		elif iPlayer == iPortugal:
		
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iMaria)
				return
			
			if tPlayer.isHasTech(con.iOptics):
				self.setLeader(iPlayer, con.iJoao)
				return
				
		elif iPlayer == iInca:
			return
			
		elif iPlayer == iItaly:
		
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iCavour)
				return
			
		elif iPlayer == iMongolia:
		
			if iGameTurn >= getTurnForYear(1400):
				self.setLeader(iPlayer, con.iKublaiKhan)
				return
				
		elif iPlayer == iAztecs:
			return
			
		elif iPlayer == iMughals:
			
			if tPlayer.isHasTech(con.iPatronage):
				self.setLeader(iPlayer, con.iAkbar)
				return
			
		elif iPlayer == iTurkey:
		
			if not bMonarchy and iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iAtaturk)
				return
				
			if tPlayer.isHasTech(con.iPatronage):
				self.setLeader(iPlayer, con.iSuleiman)
				return
				
		elif iPlayer == iThailand:
		
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iMongkut)
				return
				
		elif iPlayer == iGermany:
		
			if self.isFascist(iPlayer):
				self.setLeader(iPlayer, con.iHitler)
				return
				
			if tPlayer.isHasTech(con.iNationalism):
				self.setLeader(iPlayer, con.iBismarck)
				return
				
		elif iPlayer == iAmerica:
		
			if iEra >= con.iModern:
				self.setLeader(iPlayer, con.iFranklinRoosevelt)
				return
				
			if iGameTurn >= getTurnForYear(1850):
				self.setLeader(iPlayer, con.iLincoln)
				return
				
		if not gc.getPlayer(0).isPlayable() and iPlayer in self.lateStartingLeaders:
			self.setLeader(iPlayer, self.lateStartingLeaders[iPlayer])
			return
				
		self.setLeader(iPlayer, self.startingLeaders[iPlayer])
		

        def onCivRespawn(self, iPlayer, tOriginalOwners):
                #pPlayer = gc.getPlayer(iPlayer)
                #if con.tRebirthCiv[iPlayer] != -1:
                #        pPlayer.setCivilizationType(con.tRebirthCiv[iPlayer])
                #pPlayer.setLeader(con.tRebirthLeaders[iPlayer][0])
		
		print "On Respawn of Civ: "+str(iPlayer)
		
		self.changeResurrections(iPlayer, 1)
		
		if iPlayer == iAztecs:
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_MEXICO_ADJECTIVE")
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_MEXICO_SHORT_DESC")
		elif iPlayer == iInca:
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PERU_ADJECTIVE")
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PERU_SHORT_DESC")
		elif iPlayer == iHolyRome:
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_AUSTRIA_ADJECTIVE")
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_AUSTRIA_SHORT_DESC")
			
		
                self.setCivDesc(iPlayer, self.defaultNames[iPlayer])
                self.checkName(iPlayer, tOriginalOwners)
		self.checkLeader(iPlayer)
                
        def onVassalState(self, argsList):
                iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if iVassal == iAztecs:
			self.setCivAdjective(iVassal, "TXT_KEY_CIV_MEXICO_ADJECTIVE")
			self.setCivShortDesc(iVassal, "TXT_KEY_CIV_MEXICO_SHORT_DESC")
		elif iVassal == iInca:
			self.setCivAdjective(iVassal, "TXT_KEY_CIV_PERU_ADJECTIVE")
			self.setCivShortDesc(iVassal, "TXT_KEY_CIV_PERU_SHORT_DESC")
			
                self.checkName(iVassal)
        
        def onPlayerChangeStateReligion(self, argsList):
                iPlayer, iNewReligion, iOldReligion = argsList
		
		if iNewReligion in [con.iJudaism, con.iChristianity]:
			if iPlayer == iAztecs:
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_MEXICO_ADJECTIVE")
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_MEXICO_SHORT_DESC")
			elif iPlayer == iInca:
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PERU_ADJECTIVE")
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PERU_SHORT_DESC")
			
                self.checkName(iPlayer)

        def onRevolution(self, iPlayer):
		self.changeAnarchyTurns(iPlayer, 1)
	
                self.checkName(iPlayer)
                
        def onCityAcquired(self, argsList):
                iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
                
		self.checkName(iPreviousOwner)
		self.checkName(iNewOwner)
		
                #if city.getNumRealBuilding(con.iPalace):
                #        self.checkName(iPreviousOwner)
                
                #if gc.getPlayer(iNewOwner).getNumCities() in [0, 1, 2, 3, 6]:
                #        self.checkName(iNewOwner)
		
	def onCityRazed(self, argsList):
		city, iPlayer = argsList
		
		self.checkName(iPlayer)
			
	def onCityBuilt(self, iOwner):
		self.checkName(iOwner)

        def checkTurn(self, iGameTurn): # called only once every ten turns
                for iPlayer in range(iNumPlayers):
                        self.checkName(iPlayer)
			self.checkLeader(iPlayer)
