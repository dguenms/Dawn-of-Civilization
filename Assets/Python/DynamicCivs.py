# Dynamic Civs - edead

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
import Victory as vic
from StoredData import sd
import RFCUtils
import CityNameManager as cnm
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
iHarappa = con.iHarappa
iGreece = con.iGreece
iPersia = con.iPersia
iCarthage = con.iCarthage
iPhoenicia = con.iPhoenicia
iPolynesia = con.iPolynesia
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
iArgentina = con.iArgentina
iBrazil = con.iBrazil
iCanada = con.iCanada
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
pPolynesia = gc.getPlayer(iPolynesia)
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
pArgentina = gc.getPlayer(iArgentina)
pBrazil = gc.getPlayer(iBrazil)
pCanada = gc.getPlayer(iCanada)
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
teamPolynesia = gc.getTeam(pPolynesia.getTeam())
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
teamArgentina = gc.getTeam(pArgentina.getTeam())
teamBrazil = gc.getTeam(pBrazil.getTeam())
teamCanada = gc.getTeam(pCanada.getTeam())
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
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_DEFAULT",	# Kingdom of Egypt
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_DEFAULT",	# Maharajate of India
                        iChina : "TXT_KEY_CIV_CHINA_DESC_DEFAULT",	# Middle Kingdom of China
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_DEFAULT",	# Babylonian Empire
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_DEFAULT",	# Indus Valley City States
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_DEFAULT",	# Kingdom of Greece
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_DEFAULT",	# Persian Shahdom
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_DEFAULT",	# Kingdom of Carthage
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_DEFAULT",	# Kingdom of Tonga
                        iRome : "TXT_KEY_CIV_ROME_DESC_DEFAULT",	# Roman Kingdom
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_DEFAULT",	# Japanese Shogunate
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_DEFAULT",	# Chola Kingdom
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_DEFAULT",	# Kingdom of Ethiopia
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_DEFAULT",	# Three Kingdoms of Korea
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_DEFAULT",	# Mayan City-States
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_DEFAULT",	# Byzantine Empire
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_DEFAULT",	# Viking Union
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_DEFAULT",	# Arabian Sultanates
			iTibet : "TXT_KEY_CIV_TIBET_DESC_DEFAULT",	# Kingdom of Tibet
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_DEFAULT",	# Kingdom of Cambodia
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_DEFAULT",	# Kingdom of Indonesia
			iMoors : "TXT_KEY_CIV_MOORS_DESC_DEFAULT",	# Kingdom of Morocco
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_DEFAULT",	# Kingdom of Spain
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_DEFAULT",	# Kingdom of France
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_DEFAULT",	# Kingdom of England
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_DEFAULT",	# Kingdom of Germany
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_DEFAULT",	# Tsardom of Russia
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_DEFAULT",	# Kingdom of the Netherlands
                        iMali : "TXT_KEY_CIV_MALI_DESC_DEFAULT",	# Mali Empire
			iPoland : "TXT_KEY_CIV_POLAND_DESC_DEFAULT",	# Kingdom of Poland
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_DEFAULT",	# Kingdom of Portugal
                        iInca : "TXT_KEY_CIV_INCA_DESC_DEFAULT",	# Kingdom of Cuzco
			iItaly : "TXT_KEY_CIV_ITALY_DESC_DEFAULT",	# Kingdom of Italy
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_DEFAULT",	# Mongol State
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_DEFAULT",	# Aztec Triple Alliance
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_DEFAULT",	# Mughal Empire
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_DEFAULT",	# Ottoman Sultanate
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_DEFAULT",	# Kingdom of Siam
			iCongo : "TXT_KEY_CIV_CONGO_DESC_DEFAULT",	# Kingdom of Kongo
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_DEFAULT",	# Kingdom of Prussia
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_DEFAULT",	# Empire of Columbia
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_DEFAULT",	# United Provinces of the River Plate
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_DEFAULT",	# Kingdom of Brazil
			iCanada : "TXT_KEY_CIV_CANADA_DESC_DEFAULT",	# Dominion of Canada
                }
		
		self.peopleNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_PEOPLES",	# Peoples of the Nile
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_PEOPLES",	# Indo-Aryan Peoples
                        iChina : "TXT_KEY_CIV_CHINA_DESC_PEOPLES",	# Han Peoples
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_PEOPLES",	# Mesopotamian Peoples
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_PEOPLES",	# Indus Valley Peoples
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_PEOPLES",	# Mycenean Peoples
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_PEOPLES",	# Parsi Peoples
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_PEOPLES",	# Canaanite Peoples
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_PEOPLES",	# Polynesian Peoples
                        iRome : "TXT_KEY_CIV_ROME_DESC_PEOPLES",	# Italic Peoples
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_PEOPLES",	# Yamato Peoples
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_PEOPLES",	# Dravidian Peoples
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_PEOPLES",	# Abyssinian Peoples
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_PEOPLES",	# Korean Peoples
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_PEOPLES",	# Maya Peoples
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_PEOPLES",	# Byzantine Peoples
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_PEOPLES",	# Norse Peoples
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_PEOPLES",	# Bedouin Peoples
			iTibet : "TXT_KEY_CIV_TIBET_DESC_PEOPLES",	# Tibetan Peoples
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_PEOPLES",	# Khmer Peoples
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_PEOPLES",	# Malay Peoples
			iMoors : "TXT_KEY_CIV_MOORS_DESC_PEOPLES",	# Andalusian Peoples
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_PEOPLES",	# Asturian Peoples
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_PEOPLES",	# Frankish Peoples
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_PEOPLES",	# Anglo-Saxon Peoples
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_PEOPLES",	# Germanic Peoples
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_PEOPLES",	# Slavic Peoples
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_PEOPLES",	# Dutch Peoples
                        iMali : "TXT_KEY_CIV_MALI_DESC_PEOPLES",	# Mandinka Peoples
			iPoland : "TXT_KEY_CIV_POLAND_DESC_PEOPLES",	# Polish Peoples
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_PEOPLES",	# Lusitanian Peoples
                        iInca : "TXT_KEY_CIV_INCA_DESC_PEOPLES",	# Andean Peoples
			iItaly : "TXT_KEY_CIV_ITALY_DESC_PEOPLES",	# Lombard Peoples
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_PEOPLES",	# Mongolian Peoples
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_PEOPLES",	# Mexica Peoples
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_PEOPLES",	# Ghorid Peoples
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_PEOPLES",	# Turkish Peoples
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_PEOPLES",	# Thai Peoples
			iCongo : "TXT_KEY_CIV_CONGO_DESC_PEOPLES",	# Congolese Peoples
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_PEOPLES",	# Prussian Peoples
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_PEOPLES",	# American Peoples
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_PEOPLES",	# Argentine Peoples
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_PEOPLES",	# Brazilian Peoples
			iCanada : "TXT_KEY_CIV_CANADA_DESC_PEOPLES",	# Canadian Peoples
                }
				
		self.specificVassalNames = {
			iEgypt : {
				iCarthage : "TXT_KEY_CIV_PHOENICIA_EGYPTIAN_VASSAL",	# Province of Retjenu
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_EGYPTIAN_VASSAL"},	# Kingdom of Punt
			#iIndia - none so far
			iChina : {
				iEgypt : "TXT_KEY_CIV_EGYPT_CHINESE_VASSAL",	# Tributary Haixi State
				iIndia : "TXT_KEY_CIV_INDIA_CHINESE_VASSAL",	# Tributary Shendu State
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_CHINESE_VASSAL",	# Tributary Tiaozhi State
				iGreece : "TXT_KEY_CIV_GREECE_CHINESE_VASSAL",	# Tributary Greek State
				iPersia : "TXT_KEY_CIV_PERSIA_CHINESE_VASSAL",	# Tributary Anxi State
				iCarthage : "TXT_KEY_CIV_PHOENICIA_CHINESE_VASSAL",	# Tributary Phoenician State
				iRome : "TXT_KEY_CIV_ROME_CHINESE_VASSAL",	# Tributary Daqin State
				iJapan : "TXT_KEY_CIV_JAPAN_CHINESE_VASSAL",	# Tributary Wo State
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_CHINESE_VASSAL",	# Tributary Ethiopian State
				iKorea : "TXT_KEY_CIV_KOREA_CHINESE_VASSAL",	# Tributary Chaoxian State
				iMaya : "TXT_KEY_CIV_MAYA_CHINESE_VASSAL",	# Tributary Mayan State
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_CHINESE_VASSAL",	# Tributary Daqin State
				iVikings : "TXT_KEY_CIV_VIKINGS_CHINESE_VASSAL",	# Tributary Viking State
				iArabia : "TXT_KEY_CIV_ARABIA_CHINESE_VASSAL",	# Tributary Dashi State
				iTibet : "TXT_KEY_CIV_TIBET_CHINESE_VASSAL",	# Tributary Xizang State
				iKhmer : "TXT_KEY_CIV_KHMER_CHINESE_VASSAL",	# Tributary Gaomian State
				iIndonesia : "TXT_KEY_CIV_INDONESIA_CHINESE_VASSAL",	# Tributary Indonesian State
				iSpain : "TXT_KEY_CIV_SPAIN_CHINESE_VASSAL",	# Tributary Spanish State
				iFrance : "TXT_KEY_CIV_FRANCE_CHINESE_VASSAL",	# Tributary French State
				iEngland : "TXT_KEY_CIV_ENGLAND_CHINESE_VASSAL",	# Tributary English State
				iHolyRome : "TXT_KEY_CIV_GERMANY_CHINESE_VASSAL",	# Tributary German State
				iRussia : "TXT_KEY_CIV_RUSSIA_CHINESE_VASSAL",	# Tributary Russian State
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_CHINESE_VASSAL",	# Tributary Dutch State
				iMali : "TXT_KEY_CIV_MALI_CHINESE_VASSAL",	# Tributary Malian State
				iPortugal : "TXT_KEY_CIV_PORTUGAL_CHINESE_VASSAL",	# Tributary Portuguese State
				iInca : "TXT_KEY_CIV_INCA_CHINESE_VASSAL",	# Tributary Incan State
				iItaly : "TXT_KEY_CIV_ROME_CHINESE_VASSAL",	# Tributary Daqin State
				iMongolia : "TXT_KEY_CIV_MONGOLIA_CHINESE_VASSAL",	# Tributary Meng State
				iAztecs : "TXT_KEY_CIV_AZTECS_CHINESE_VASSAL",	# Tributary Aztec State
				iTurkey : "TXT_KEY_CIV_TURKEY_CHINESE_VASSAL",	# Tributary Tujue State
				iMughals : "TXT_KEY_CIV_MUGHALS_CHINESE_VASSAL",	# Tributary Mughal State
				iThailand : "TXT_KEY_CIV_THAILAND_CHINESE_VASSAL",	# Tributary Thai State
				iGermany : "TXT_KEY_CIV_GERMANY_CHINESE_VASSAL",	# Tributary German State
				iAmerica : "TXT_KEY_CIV_AMERICA_CHINESE_VASSAL"},	# Tributary American State
			iBabylonia : {
				iPhoenicia : "TXT_KEY_CIV_PHOENICIA_BABYLONIAN_VASSAL"},	# Babylonian Phoenicia
			iGreece : {
				iIndia : "TXT_KEY_CIV_INDIA_GREEK_VASSAL",	# Greco-Bactrian Kingdom
				iEgypt : "TXT_KEY_CIV_EGYPT_GREEK_VASSAL",	#  Ptolemid Empire
				iPersia : "TXT_KEY_CIV_PERSIA_GREEK_VASSAL"},	# Seleucid Empire
			iPersia : {
				iEgypt : "TXT_KEY_CIV_EGYPT_PERSIAN_VASSAL",	# Ninth Satrapy
				iIndia : "TXT_KEY_CIV_INDIA_PERSIAN_VASSAL",	# Twentieth Satrapy
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_PERSIAN_VASSAL",	# Sixth Satrapy
				iGreece : "TXT_KEY_CIV_GREECE_PERSIAN_VASSAL",	# First Satrapy
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_PERSIAN_VASSAL",	# Seventeenth Satrapy
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_PERSIAN_VASSAL",	# Satrapy of Anatolia
				iVikings : "TXT_KEY_CIV_VIKINGS_PERSIAN_VASSAL",	# Satrapy of Scandinavia
				iArabia : "TXT_KEY_CIV_ARABIA_PERSIAN_VASSAL",	# Fifth Satrapy
				iKhmer : "TXT_KEY_CIV_KHMER_PERSIAN_VASSAL",	# Satrapy of Kampuchea
				iIndonesia : "TXT_KEY_CIV_INDONESIA_PERSIAN_VASSAL",	# Satrapy of Malacca
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_PERSIAN_VASSAL",	# Satrapy of the Netherlands
				iMongolia : "TXT_KEY_CIV_MONGOLIA_PERSIAN_VASSAL",	# Fifteenth Satrapy
				iAztecs : "TXT_KEY_CIV_AZTECS_PERSIAN_VASSAL",	# Satrapy of Mexico
				iTurkey : "TXT_KEY_CIV_TURKEY_PERSIAN_VASSAL"},	# Fourth Satrapy
			#iCarthage - none so far
			#iPolynesia - none so far
			iRome : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ROMAN_VASSAL",	# Province of Aegyptus
				iChina : "TXT_KEY_CIV_CHINA_ROMAN_VASSAL",	# Province of Sinae
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ROMAN_VASSAL",	# Province of Mesopotamia
				iGreece : "TXT_KEY_CIV_GREECE_ROMAN_VASSAL",	# Province of Achaea
				iPersia : "TXT_KEY_CIV_PERSIA_ROMAN_VASSAL",	# Province of Parthia
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ROMAN_VASSAL",	# Province of Syria
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ROMAN_VASSAL",	# Province of Aethiopia
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ROMAN_VASSAL",	# Province of Thracia
				iVikings : "TXT_KEY_CIV_VIKINGS_ROMAN_VASSAL",	# Province of Scandia
				iKhmer : "TXT_KEY_CIV_KHMER_ROMAN_VASSAL",	# Province of Aurea Chersonesus
				iSpain : "TXT_KEY_CIV_SPAIN_ROMAN_VASSAL",	# Province of Hispania
				iFrance : "TXT_KEY_CIV_FRANCE_ROMAN_VASSAL",	# Province of Gaul
				iEngland : "TXT_KEY_CIV_ENGLAND_ROMAN_VASSAL",	# Province of Britannia
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_ROMAN_VASSAL",	# Province of Germania
				iRussia : "TXT_KEY_CIV_RUSSIA_ROMAN_VASSAL",	# Province of Sarmatia
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ROMAN_VASSAL",	# Province of Belgica
				iMali : "TXT_KEY_CIV_MALI_ROMAN_VASSAL",	# Province of Gaetulia
				iPortugal : "TXT_KEY_CIV_PORTUGAL_ROMAN_VASSAL",	# Province of Lusitania
				iMongolia : "TXT_KEY_CIV_MONGOLIA_ROMAN_VASSAL",	# Province of Serica
				iAztecs : "TXT_KEY_CIV_AZTECS_ROMAN_VASSAL",	# Province of Mexico
				iTurkey : "TXT_KEY_CIV_TURKEY_ROMAN_VASSAL",	# Province of Asia Minor
				iGermany : "TXT_KEY_CIV_GERMANY_ROMAN_VASSAL",	# Province of Borussia
				iThailand : "TXT_KEY_CIV_THAILAND_ROMAN_VASSAL",},	# Province of Siam
			iJapan : {
				iChina : "TXT_KEY_CIV_CHINA_JAPANESE_VASSAL",	# Reorganized National Government of China
				iKorea : "TXT_KEY_CIV_KOREA_JAPANESE_VASSAL",	# Governor-General of Chosen
				iKhmer : "TXT_KEY_CIV_KHMER_JAPANESE_VASSAL",	# Co-Prosperity Kampuchea
				iMongolia : "TXT_KEY_CIV_MONGOLIA_JAPANESE_VASSAL",	# Mengjiang United Autonomous Government
				iAztecs : "TXT_KEY_CIV_AZTECS_JAPANESE_VASSAL",},	# Co-Prosperity Mexico
			#iTamils - none so far
			#iEthiopia - none so far
			#iKorea - none so far
			#iMaya - none so far
			iByzantium : {
				iEgypt : "TXT_KEY_CIV_EGYPT_BYZANTINE_VASSAL",	# Exarchate of Alexandria
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_BYZANTINE_VASSAL",	# Exarchate of Ctesiphon
				iGreece : "TXT_KEY_CIV_GREECE_BYZANTINE_VASSAL",	# Exarchate of Achaia
				iCarthage : "TXT_KEY_CIV_PHOENICIA_BYZANTINE_VASSAL",	# Exarchate of Africa
				iPersia : "TXT_KEY_CIV_PERSIA_BYZANTINE_VASSAL",	# Exarchate of Parthia
				iRome : "TXT_KEY_CIV_ROME_BYZANTINE_VASSAL",	# Exarchate of Ravenna
				iSpain : "TXT_KEY_CIV_SPAIN_BYZANTINE_VASSAL"},	# Exarchate of Spania
			iVikings : {
				iEngland : "TXT_KEY_CIV_ENGLAND_VIKING_VASSAL",	# Danelaw
				iRussia : "TXT_KEY_CIV_RUSSIA_VIKING_VASSAL"},	# Varangian Principalities
			iArabia : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ARABIAN_VASSAL",	# Emirate of Misr
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ARABIAN_VASSAL",	# Emirate of Iraq
				iPersia : "TXT_KEY_CIV_PERSIA_ARABIAN_VASSAL",	# Emirate of Fars
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ARABIAN_VASSAL",	# Emirate of Ifriqiya
				iRome : "TXT_KEY_CIV_ROME_ARABIAN_VASSAL",	# Emirate of Italiya
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ARABIAN_VASSAL",	# Emirate of Abyssinia
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ARABIAN_VASSAL",	# Emirate of Rum
				iVikings : "TXT_KEY_CIV_VIKINGS_ARABIAN_VASSAL",	# Emirate of Scandinavia
				iKhmer : "TXT_KEY_CIV_KHMER_ARABIAN_VASSAL",	# Emirate of Kampuchea
				iMoors : "TXT_KEY_CIV_MOORS_ARABIAN_VASSAL",	# Emirate of Al-Andalus
				iSpain : "TXT_KEY_CIV_SPAIN_ARABIAN_VASSAL",	# Emirate of Esbanya
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARABIAN_VASSAL",	# Emirate of the Netherlands
				iAztecs : "TXT_KEY_CIV_AZTECS_ARABIAN_VASSAL",	# Emirate of Mexico
				iTurkey : "TXT_KEY_CIV_TURKEY_ARABIAN_VASSAL",	# Ottoman Sultanate
				iMughals : "TXT_KEY_CIV_MUGHALS_ARABIAN_VASSAL",	# Emirate of Delhi
				iThailand : "TXT_KEY_CIV_THAILAND_ARABIAN_VASSAL",},	# Emirate of Siam
			#iTibet - none so far
			#iKhmer - none so far
			#iIndonesia - none so far
			iMoors : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ARABIAN_VASSAL",	# Emirate of Misr
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ARABIAN_VASSAL",	# Emirate of Iraq
				iPersia : "TXT_KEY_CIV_PERSIA_ARABIAN_VASSAL",	# Emirate of Fars
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ARABIAN_VASSAL",	# Emirate of Ifriqiya
				iRome : "TXT_KEY_CIV_ROME_ARABIAN_VASSAL",	# Emirate of Italiya
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ARABIAN_VASSAL",	# Emirate of Abyssinia
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ARABIAN_VASSAL",	# Emirate of R&#251;m
				iVikings : "TXT_KEY_CIV_VIKINGS_ARABIAN_VASSAL",	# Emirate of Scandinavia
				iKhmer : "TXT_KEY_CIV_KHMER_ARABIAN_VASSAL",	# Emirate of Kampuchea
				iMoors : "TXT_KEY_CIV_ARABIA_MOORISH_VASSAL",	# Arabian Sultanates
				iSpain : "TXT_KEY_CIV_SPAIN_ARABIAN_VASSAL",	# Emirate of Esbanya
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARABIAN_VASSAL",	# Emirate of the Netherlands
				iAztecs : "TXT_KEY_CIV_AZTECS_ARABIAN_VASSAL",	# Emirate of Mexico
				iTurkey : "TXT_KEY_CIV_TURKEY_ARABIAN_VASSAL",	# Ottoman Sultanate
				iMughals : "TXT_KEY_CIV_MUGHALS_ARABIAN_VASSAL",	# Emirate of Delhi
				iThailand : "TXT_KEY_CIV_THAILAND_ARABIAN_VASSAL",},	# Emirate of Siam
			iSpain : {
				iCarthage : "TXT_KEY_CIV_PHOENICIA_SPANISH_VASSAL",	# Spanish Lebanon
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_SPANISH_VASSAL",	# Spanish East Africa
				iMaya : "TXT_KEY_CIV_MAYA_SPANISH_VASSAL",	# Dicesis of Yucatan
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_SPANISH_VASSAL",	# Latin Empire
				iVikings : "TXT_KEY_CIV_VIKINGS_SPANISH_VASSAL",	# Viceroyalty of Scandinavia
				iKhmer : "TXT_KEY_CIV_KHMER_SPANISH_VASSAL",	# Viceroyalty of Indochina
				iIndonesia : "TXT_KEY_CIV_INDONESIA_SPANISH_VASSAL",	# Spanish East Indies
				iMoors : "TXT_KEY_CIV_MOORS_SPANISH_VASSAL",	# Spanish Protectorate of Morocco
				iFrance : "TXT_KEY_CIV_FRANCE_SPANISH_VASSAL",	# Autonomous Community of France
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_SPANISH_VASSAL",	# Spanish Netherlands
				iMali : "TXT_KEY_CIV_MALI_SPANISH_VASSAL",	# Spanish West Africa
				iPortugal : "TXT_KEY_CIV_PORTUGAL_SPANISH_VASSAL",	# Autonomous Community of Portugal
				iInca : "TXT_KEY_CIV_INCA_SPANISH_VASSAL",	# Viceroyalty of Peru
				iAztecs : "TXT_KEY_CIV_AZTECS_SPANISH_VASSAL",	# Viceroyalty of New Spain
				iMughals : "TXT_KEY_CIV_MUGHALS_SPANISH_VASSAL",	# Viceroyalty of West India
				iThailand : "TXT_KEY_CIV_THAILAND_SPANISH_VASSAL",	# Viceroyalty of Siam
				iAmerica : "TXT_KEY_CIV_AMERICA_SPANISH_VASSAL",	# Province of New Mexico
				iArgentina : "TXT_KEY_CIV_ARGENTINA_SPANISH_VASSAL"},	# Viceroyalty of the Rio de la Plata
			iFrance : {
				iEgypt : "TXT_KEY_CIV_EGYPT_FRENCH_VASSAL",	# French Mandate of Egypt
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_FRENCH_VASSAL",	# French Mandate of Mesopotamia
				iGreece : "TXT_KEY_CIV_GREECE_FRENCH_VASSAL",	# Departments of Greece
				iPersia : "TXT_KEY_CIV_PERSIA_FRENCH_VASSAL",	# French Mandate of Persia
				iCarthage : "TXT_KEY_CIV_PHOENICIA_FRENCH_VASSAL",	# French Mandate of Lebanon
				iRome : "TXT_KEY_CIV_ROME_FRENCH_VASSAL",	# Cisalpine Republic
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_FRENCH_VASSAL",	# French East Africa
				iMaya : "TXT_KEY_CIV_MAYA_FRENCH_VASSAL",	# French Yucatan
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_FRENCH_VASSAL",	# Latin Empire
				iVikings : "TXT_KEY_CIV_VIKINGS_FRENCH_VASSAL",	# Department of Scandinavia
				iArabia : "TXT_KEY_CIV_ARABIA_FRENCH_VASSAL",	# French Mandate of Arabia
				iKhmer : "TXT_KEY_CIV_KHMER_FRENCH_VASSAL",	# French Indochina
				iSpain : "TXT_KEY_CIV_SPAIN_FRENCH_VASSAL",	# Spanish March
				iEngland : "TXT_KEY_CIV_ENGLAND_FRENCH_VASSAL",	# Duchy of Normandy
				iHolyRome : "TXT_KEY_CIV_GERMANY_FRENCH_VASSAL",	# Confederation of the Rhine
				iRussia : "TXT_KEY_CIV_RUSSIA_FRENCH_VASSAL",	# Departments of Russia
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_FRENCH_VASSAL",	# Batavian Republic
				iPoland : "TXT_KEY_CIV_POLAND_FRENCH_VASSAL",	# Duchy of Warsaw
				iMali : "TXT_KEY_CIV_MALI_FRENCH_VASSAL",	# French West Africa
				iPortugal : "TXT_KEY_CIV_PORTUGAL_FRENCH_VASSAL",	# Department of Portugal
				iInca : "TXT_KEY_CIV_INCA_FRENCH_VASSAL",	# Andean France
				iItaly : "TXT_KEY_CIV_ROME_FRENCH_VASSAL",	# Cisalpine Republic
				iAztecs : "TXT_KEY_CIV_AZTECS_FRENCH_VASSAL",	# Mesoamerican France
				iMughals : "TXT_KEY_CIV_MUGHALS_FRENCH_VASSAL",	# French Mandate of West India
				iTurkey : "TXT_KEY_CIV_TURKEY_FRENCH_VASSAL",	# French Mandate of Turkey
				iThailand : "TXT_KEY_CIV_THAILAND_FRENCH_VASSAL",	# French Siam
				iGermany : "TXT_KEY_CIV_GERMANY_FRENCH_VASSAL",	# Confederation of the Rhine
				iAmerica : "TXT_KEY_CIV_AMERICA_FRENCH_VASSAL"},	# New France
			iEngland : {
				iEgypt : "TXT_KEY_CIV_EGYPT_ENGLISH_VASSAL",	# British Mandate of Egypt
				iIndia : "TXT_KEY_CIV_INDIA_ENGLISH_VASSAL",	# British Raj
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_ENGLISH_VASSAL",	# British Mandate of Mesopotamia
				iPersia : "TXT_KEY_CIV_PERSIA_ENGLISH_VASSAL",	# British Mandate of Persia
				iCarthage : "TXT_KEY_CIV_PHOENICIA_ENGLISH_VASSAL",	# British Mandate of Lebanon
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_ENGLISH_VASSAL",	# British East Africa
				iMaya : "TXT_KEY_CIV_MAYA_ENGLISH_VASSAL",	# Colony of British Honduras
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_ENGLISH_VASSAL",	# Latin Empire
				iVikings : "TXT_KEY_CIV_VIKINGS_ENGLISH_VASSAL",	# Duchy of Scandinavia
				iArabia : "TXT_KEY_CIV_ARABIA_ENGLISH_VASSAL",	# British Mandate of Arabia
				iKhmer : "TXT_KEY_CIV_KHMER_ENGLISH_VASSAL",	# Dominion of Indochina
				iFrance : "TXT_KEY_CIV_FRANCE_ENGLISH_VASSAL",	# Duchy of Anjou
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_ENGLISH_VASSAL",	# Duchy of Hanover
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ENGLISH_VASSAL",	# Duchy of Flanders
				iMali : "TXT_KEY_CIV_MALI_ENGLISH_VASSAL",	# British West Africa
				iInca : "TXT_KEY_CIV_INCA_ENGLISH_VASSAL",	# Dominion of Peru
				iAztecs : "TXT_KEY_CIV_AZTECS_ENGLISH_VASSAL",	# Dominion of Mexico
				iTurkey : "TXT_KEY_CIV_TURKEY_ENGLISH_VASSAL",	# British Mandate of Turkey
				iMughals : "TXT_KEY_CIV_MUGHALS_ENGLISH_VASSAL",	# Dominion of Pakistan
				iThailand : "TXT_KEY_CIV_THAILAND_ENGLISH_VASSAL",	# British Siam
				iGermany : "TXT_KEY_CIV_GERMANY_ENGLISH_VASSAL",	# British-Occupied Germany
				iAmerica : "TXT_KEY_CIV_AMERICA_ENGLISH_VASSAL"},	# Thirteen Colonies
			iHolyRome : {
				iRome : "TXT_KEY_CIV_ROME_HOLY_ROMAN_VASSAL",	# Crown of Italy
				iFrance : "TXT_KEY_CIV_FRANCE_HOLY_ROMAN_VASSAL",	# West Francia
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_HOLY_ROMAN_VASSAL",	# Duchy of Brabant
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_HOLY_ROMAN_VASSAL",	# Latin Empire
				iItaly : "TXT_KEY_CIV_ITALY_HOLY_ROMAN_VASSAL",	# Grand Duchy of Tuscany
				iPoland : "TXT_KEY_CIV_POLAND_HOLY_ROMAN_VASSAL"},	# Duchy of Poland
			iNetherlands : {
				iIndonesia : "TXT_KEY_CIV_INDONESIA_DUTCH_VASSAL",	# Dutch East Indies
				iMali : "TXT_KEY_CIV_MALI_DUTCH_VASSAL",	# Dutch West Africa
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DUTCH_VASSAL",	# Dutch East Africa
				iAztecs : "TXT_KEY_CIV_AZTECS_DUTCH_VASSAL",	# Dutch Mexico
				iMaya : "TXT_KEY_CIV_MAYA_DUTCH_VASSAL",	# Dutch Yucatan
				iInca : "TXT_KEY_CIV_INCA_DUTCH_VASSAL"},	# Dutch Peru
			iRussia: {
				iAmerica : "TXT_KEY_CIV_AMERICA_RUSSIAN_VASSAL",	# Russian America
				iPoland : "TXT_KEY_CIV_POLAND_RUSSIAN_VASSAL"},	# Congress Poland
			iPortugal : {
				iIndia : "TXT_KEY_CIV_INDIA_PORTUGUESE_VASSAL",	# Viceroyalty of Portuguese India
				iIndonesia : "TXT_KEY_CIV_INDONESIA_PORTUGUESE_VASSAL",	# Portuguese East Indies
				iAztecs : "TXT_KEY_CIV_AZTECS_PORTUGUESE_VASSAL",	# Portuguese Mexico
				iInca : "TXT_KEY_CIV_INCA_PORTUGUESE_VASSAL",	# Portuguese Peru
				iMaya : "TXT_KEY_CIV_MAYA_PORTUGUESE_VASSAL"},	# Portuguese Yucatan
			#iMali - none so far
			#iPoland - none so far
			#iInca - none so far
			iMongolia : {
				iThailand : "TXT_KEY_CIV_THAILAND_MONGOL_VASSAL",	# Khanate of Siam
				iEgypt : "TXT_KEY_CIV_EGYPT_MONGOL_VASSAL",	# Ilkhanate of Egypt
				iChina : "TXT_KEY_CIV_CHINA_MONGOL_VASSAL",	# Yuan Khanate
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_MONGOL_VASSAL",	# Ilkhanate of Mesopotamia
				iGreece : "TXT_KEY_CIV_GREECE_MONGOL_VASSAL",	# Ilkhanate of Greece
				iPersia : "TXT_KEY_CIV_PERSIA_MONGOL_VASSAL",	# Ilkhanate of Persia
				iCarthage : "TXT_KEY_CIV_PHOENICIA_MONGOL_VASSAL",	# Ilkhanate of Syria
				iRome : "TXT_KEY_CIV_ROME_MONGOL_VASSAL",	# Ilkhanate of Rome
				iItaly : "TXT_KEY_CIV_ITALY_MONGOL_VASSAL",	# Ilkhanate of Italy
				iMaya : "TXT_KEY_CIV_MAYA_MONGOL_VASSAL",	# Khanate of Yucatan
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_MONGOL_VASSAL",	# Khanate of Anatolia
				iVikings : "TXT_KEY_CIV_VIKINGS_MONGOL_VASSAL",	# Khanate of Scandinavia
				iKhmer : "TXT_KEY_CIV_KHMER_MONGOL_VASSAL",	# Khanate of Kampuchea
				iRussia : "TXT_KEY_CIV_RUSSIA_MONGOL_VASSAL",	# Khanate of the Golden Horde
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_MONGOL_VASSAL",	# Khanate of the Netherlands
				iInca : "TXT_KEY_CIV_INCA_MONGOL_VASSAL",	# Khanate of Peru
				iAztecs : "TXT_KEY_CIV_AZTECS_MONGOL_VASSAL",	# Khanate of Mexico
				iTurkey : "TXT_KEY_CIV_TURKEY_MONGOL_VASSAL",	# Khanate of Turkestan
				iMughals : "TXT_KEY_CIV_MUGHALS_MONGOL_VASSAL"},	# Khanate of Delhi
			#iAztecs - none so far
			iTurkey : {
				iThailand : "TXT_KEY_CIV_THAILAND_TURKISH_VASSAL",	# Eyalet of Siam
				iEgypt : "TXT_KEY_CIV_EGYPT_TURKISH_VASSAL",	# Khedivate of Egypt
				iBabylonia : "TXT_KEY_CIV_BABYLONIA_TURKISH_VASSAL",	# Eyalet of Mesopotamia
				iPersia : "TXT_KEY_CIV_PERSIA_TURKISH_VASSAL",	# Eyalet of Sharazor
				iGreece : "TXT_KEY_CIV_GREECE_TURKISH_VASSAL",	# Eyalet of Rumelia
				iCarthage : "TXT_KEY_CIV_PHOENICIA_TURKISH_VASSAL",	# Eyalet of Syria
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_TURKISH_VASSAL",	# Eyalet of Habes
				iMaya : "TXT_KEY_CIV_MAYA_TURKISH_VASSAL",	# Eyalet of Yucatan
				iByzantium : "TXT_KEY_CIV_BYZANTIUM_TURKISH_VASSAL",	# Eyalet of R&#251;m
				iVikings : "TXT_KEY_CIV_VIKINGS_TURKISH_VASSAL",	# Eyalet of Scandinavia
				iArabia : "TXT_KEY_CIV_ARABIA_TURKISH_VASSAL",	# Sharifate of Mekke
				iKhmer : "TXT_KEY_CIV_KHMER_TURKISH_VASSAL",	# Eyalet of Kampuchea
				iRussia : "TXT_KEY_CIV_RUSSIA_TURKISH_VASSAL",	# Eyalet of Yedisan
				iNetherlands : "TXT_KEY_CIV_NETHERLANDS_TURKISH_VASSAL",	# Eyalet of the Netherlands
				iAztecs : "TXT_KEY_CIV_AZTECS_TURKISH_VASSAL",	# Eyalet of Mexico
				iInca : "TXT_KEY_CIV_INCA_TURKISH_VASSAL",	# Eyalet of Peru
				iMughals : "TXT_KEY_CIV_MUGHALS_TURKISH_VASSAL"},	# Eyalet of Pakistan
			iMughals : {
				iIndia : "TXT_KEY_CIV_INDIA_MUGHAL_VASSAL"},	# Deccan Sultanates
			#iThailand - none so far
			#iCongo - none so far
			iGermany : {
				iHolyRome : "TXT_KEY_CIV_HOLY_ROME_GERMAN_VASSAL",	# State of German Austria
				iMaya : "TXT_KEY_CIV_MAYA_GERMAN_VASSAL",	# German Yucatan
				iAztecs : "TXT_KEY_CIV_AZTECS_GERMAN_VASSAL",	# German Mexico
				iInca : "TXT_KEY_CIV_INCA_GERMAN_VASSAL",	# German Peru
				iMali : "TXT_KEY_CIV_MALI_GERMAN_VASSAL",	# German West Africa
				iEthiopia : "TXT_KEY_CIV_ETHIOPIA_GERMAN_VASSAL",	# German East Africa
				iPoland : "TXT_KEY_CIV_POLAND_GERMAN_VASSAL"},	# South Prussia
			iAmerica : {
				iEngland : "TXT_KEY_CIV_ENGLAND_AMERICAN_VASSAL",	# Airstrip One
				iJapan : "TXT_KEY_CIV_JAPAN_AMERICAN_VASSAL",	# Allied Council for Japan
				iGermany : "TXT_KEY_CIV_GERMANY_AMERICAN_VASSAL",	# US-Occupied Germany
				iMaya : "TXT_KEY_CIV_MAYA_AMERICAN_VASSAL",	# American Yucatan
				iKorea : "TXT_KEY_CIV_KOREA_AMERICAN_VASSAL",	# Commander Naval Forces Korea
				iAztecs : "TXT_KEY_CIV_AZTECS_AMERICAN_VASSAL",},	# New Mexico
			# Argentina - none so far
			iBrazil : {
				iArgentina : "TXT_KEY_CIV_ARGENTINA_BRAZILIAN_VASSAL",},	# Transplatine Province
		}
		
		self.genericVassalNames = {
			iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL_GENERIC",	# Satrapy of %s1
			iRome : "TXT_KEY_CIV_ROMAN_VASSAL_GENERIC",	# Province of %s1
			iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL_GENERIC",	# Co-Prosperity %s1
			iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL_GENERIC",	# Exarchate of %s1
			iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL_GENERIC",	# Emirate of %s1
			iMoors : "TXT_KEY_CIV_ARABIAN_VASSAL_GENERIC",	# Emirate of %s1
			iSpain : "TXT_KEY_CIV_SPANISH_VASSAL_GENERIC",	# Viceroyalty of %s1
			iFrance : "TXT_KEY_CIV_FRENCH_VASSAL_GENERIC",	# French %s1
			iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL_GENERIC",	# Dominion of %s1
			iMongolia : "TXT_KEY_CIV_MONGOL_VASSAL_GENERIC",	# Khanate of %s1
			iTurkey : "TXT_KEY_CIV_TURKISH_VASSAL_GENERIC"	# Eyalet of %s1
		}
				
		self.sovietVassals = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_SOVIET_VASSAL",	# Soviet Egypt
                        iIndia : "TXT_KEY_CIV_INDIA_SOVIET_VASSAL",	# Soviet India
                        iChina : "TXT_KEY_CIV_CHINA_SOVIET_VASSAL",	# Chinese Soviet Republic
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_SOVIET_VASSAL",	# Soviet Mesopotamia
			iHarappa : "TXT_KEY_CIV_HARAPPA_SOVIET_VASSAL",	# Soviet Indus
                        iGreece : "TXT_KEY_CIV_GREECE_SOVIET_VASSAL",	# Soviet Greece
                        iPersia : "TXT_KEY_CIV_PERSIA_SOVIET_VASSAL",	# Soviet Gilan
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_SOVIET_VASSAL",	# Soviet Lebanon
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_SOVIET_VASSAL",	# Soviet Polynesia
                        iRome : "TXT_KEY_CIV_ROME_SOVIET_VASSAL",	# Soviet Italy
			iItaly : "TXT_KEY_CIV_ROME_SOVIET_VASSAL",	# Soviet Italy
                        iJapan : "TXT_KEY_CIV_JAPAN_SOVIET_VASSAL",	# Far Eastern Republic
			iTamils : "TXT_KEY_CIV_TAMILS_SOVIET_VASSAL",	# Soviet Dravida
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_SOVIET_VASSAL",	# Soviet Ethiopia
                        iKorea : "TXT_KEY_CIV_KOREA_SOVIET_VASSAL",	# Soviet Korea
                        iMaya : "TXT_KEY_CIV_MAYA_SOVIET_VASSAL",	# Soviet Yucatan
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_SOVIET_VASSAL",	# Soviet Byzantium
                        iVikings : "TXT_KEY_CIV_VIKINGS_SOVIET_VASSAL",	# Soviet Scandinavia
                        iArabia : "TXT_KEY_CIV_ARABIA_SOVIET_VASSAL",	# Soviet Arabia
                        iKhmer : "TXT_KEY_CIV_KHMER_SOVIET_VASSAL",	# Soviet Kampuchea
			iTibet : "TXT_KEY_CIV_TIBET_SOVIET_VASSAL",	# Soviet Tibet
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_SOVIET_VASSAL",	# Soviet Indonesia
			iMoors : "TXT_KEY_CIV_MOORS_SOVIET_VASSAL",	# Soviet Morocco
                        iSpain : "TXT_KEY_CIV_SPAIN_SOVIET_VASSAL",	# Soviet Spain
                        iFrance : "TXT_KEY_CIV_FRANCE_SOVIET_VASSAL",	# Soviet France
                        iEngland : "TXT_KEY_CIV_ENGLAND_SOVIET_VASSAL",	# Soviet England
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_SOVIET_VASSAL",	# Soviet Austria
                        iRussia : "NONE",
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_SOVIET_VASSAL",	# Soviet Netherlands
                        iMali : "TXT_KEY_CIV_MALI_SOVIET_VASSAL",	# Soviet Mali
			iPoland : "TXT_KEY_CIV_POLAND_SOVIET_VASSAL",	# Soviet Poland
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_SOVIET_VASSAL",	# Soviet Portugal
                        iInca : "TXT_KEY_CIV_INCA_SOVIET_VASSAL",	# Soviet Peru
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_SOVIET_VASSAL",	# Soviet Mongolia
                        iAztecs : "TXT_KEY_CIV_AZTECS_SOVIET_VASSAL",	# Soviet Mexico
                        iTurkey : "TXT_KEY_CIV_TURKEY_SOVIET_VASSAL",	# Transcaucasian Socialist Federative Soviet Republic
			iMughals : "TXT_KEY_CIV_MUGHALS_SOVIET_VASSAL",	# Soviet Pakistan
			iThailand : "TXT_KEY_CIV_THAILAND_SOVIET_VASSAL",	# Soviet Thailand
			iCongo : "TXT_KEY_CIV_CONGO_SOVIET_VASSAL",	# Soviet Congo
			iGermany : "TXT_KEY_CIV_GERMANY_SOVIET_VASSAL",	# German Democratic Republic
                        iAmerica : "TXT_KEY_CIV_AMERICA_SOVIET_VASSAL",	# Soviet America
			iArgentina : "TXT_KEY_CIV_ARGENTINA_SOVIET_VASSAL",	# Soviet Argentina
			iBrazil : "TXT_KEY_CIV_BRAZIL_SOVIET_VASSAL",	# Soviet Brazil
			iCanada : "TXT_KEY_CIV_CANADA_SOVIET_VASSAL",	# Soviet Canada
                }
		
		self.naziVassals = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_NAZI_VASSAL",	# Reichsprotektorat Egypt
                        iIndia : "TXT_KEY_CIV_INDIA_NAZI_VASSAL",	# German India
                        iChina : "TXT_KEY_CIV_CHINA_NAZI_VASSAL",	# Reichskommissariat China
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_NAZI_VASSAL",	# German Mesopotamia
			iHarappa : "TXT_KEY_CIV_HARAPPA_NAZI_VASSAL",	# German Indus
                        iGreece : "TXT_KEY_CIV_GREECE_NAZI_VASSAL",	# Hellenic State
                        iPersia : "TXT_KEY_CIV_PERSIA_NAZI_VASSAL",	# German Persia
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_NAZI_VASSAL",	# Reichskommissariat Lebanon
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_NAZI_VASSAL",	# Nazi Polynesia
                        iRome : "TXT_KEY_CIV_ROME_NAZI_VASSAL",	# Italian Social Republic
			iItaly : "TXT_KEY_CIV_ROME_NAZI_VASSAL",	# Italian Social Republic
                        iJapan : "TXT_KEY_CIV_JAPAN_NAZI_VASSAL",	# German Japan
			iTamils : "TXT_KEY_CIV_TAMILS_NAZI_VASSAL",	# German Dravida
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_NAZI_VASSAL",	# German East Africa
                        iKorea : "TXT_KEY_CIV_KOREA_NAZI_VASSAL",	# German Korea
                        iMaya : "TXT_KEY_CIV_MAYA_NAZI_VASSAL",	# German Yucatan
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_NAZI_VASSAL",	# Reichskommissariat Bosphorus
                        iVikings : "TXT_KEY_CIV_VIKINGS_NAZI_VASSAL",	# Reichskommissariat Nordland
                        iArabia : "TXT_KEY_CIV_ARABIA_NAZI_VASSAL",	# German Arabia
			iTibet : "TXT_KEY_CIV_TIBET_NAZI_VASSAL",	# German Tibet
                        iKhmer : "TXT_KEY_CIV_KHMER_NAZI_VASSAL",	# German Indochina
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_NAZI_VASSAL",	# German Indonesia
			iMoors : "TXT_KEY_CIV_MOORS_NAZI_VASSAL",	# German Maghreb
                        iSpain : "TXT_KEY_CIV_SPAIN_NAZI_VASSAL",	# Reichskommissariat Spain
                        iFrance : "TXT_KEY_CIV_FRANCE_NAZI_VASSAL",	# Vichy France
                        iEngland : "TXT_KEY_CIV_ENGLAND_NAZI_VASSAL",	# Reichskommissariat England
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_NAZI_VASSAL",	# Ostmark
                        iRussia : "TXT_KEY_CIV_RUSSIA_NAZI_VASSAL",	# Reichskommissariat Moskowien
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_NAZI_VASSAL",	# Reichsgau Holland
                        iMali : "TXT_KEY_CIV_MALI_NAZI_VASSAL",	# German West Africa
			iPoland : "TXT_KEY_CIV_POLAND_NAZI_VASSAL",	# General Government
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_NAZI_VASSAL",	# Reichskommissariat Portugal
                        iInca : "TXT_KEY_CIV_INCA_NAZI_VASSAL",	# German Peru
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_NAZI_VASSAL",	# German Mongolia
                        iAztecs : "TXT_KEY_CIV_AZTECS_NAZI_VASSAL",	# German Mexico
                        iTurkey : "TXT_KEY_CIV_TURKEY_NAZI_VASSAL",	# Reichskommissariat Turkey
			iMughals : "TXT_KEY_CIV_MUGHALS_NAZI_VASSAL",	# German West India
			iThailand : "TXT_KEY_CIV_THAILAND_NAZI_VASSAL",	# German Thailand
			iCongo : "TXT_KEY_CIV_CONGO_NAZI_VASSAL",	# German Congo
			iGermany : "NONE",
                        iAmerica : "TXT_KEY_CIV_AMERICA_NAZI_VASSAL",	# German America
			iArgentina : "TXT_KEY_CIV_ARGENTINA_NAZI_VASSAL",	# German Argentina
			iBrazil : "TXT_KEY_CIV_BRAZIL_NAZI_VASSAL",	# German Brazil
			iCanada : "TXT_KEY_CIV_CANADA_NAZI_VASSAL",	# Reichskommissariat Kanada
                }

                self.fascistNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_FASCIST",	# Officers' Egypt
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_FASCIST",	# Undivided India
                        iChina : "TXT_KEY_CIV_CHINA_DESC_FASCIST",	# Nationalist China
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_FASCIST",	# Baathist Babylonia
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_FASCIST",	# National Republic of the Indus
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_FASCIST",	# Greek Junta
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_FASCIST",	# Persian Empire
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_FASCIST",	# National Lebanon
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_FASCIST",	# Oceania
                        iRome : "TXT_KEY_CIV_ROME_DESC_FASCIST",	# New Roman Empire
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_FASCIST",	# Empire of Greater Japan
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_FASCIST",	# Dravidian Empire
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_FASCIST",	# Ethiopian Junta
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_FASCIST",	# Supreme Council for National Reconstruction
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_FASCIST",	# Mayan Junta
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_FASCIST",	# Despotate of Byzantium
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_FASCIST",	# National Gathering of Scandinavia
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_FASCIST",	# Pan Arab State
			iTibet : "TXT_KEY_CIV_TIBET_DESC_FASCIST",	# Tibetan Empire
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_FASCIST",	# Nationalist Kampuchea
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_FASCIST",	# Indonesian New Order
			iMoors : "TXT_KEY_CIV_MOORS_DESC_FASCIST",	# Moroccan State
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_FASCIST",	# Spanish State
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_FASCIST",	# French State
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_FASCIST",	# British Union
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_FASCIST",	# Greater Austrian Empire
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_FASCIST",	# Panslavic Empire
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_FASCIST",	# Dutch Empire
                        iMali : "TXT_KEY_CIV_MALI_DESC_FASCIST",	# Military Comittee of Mali
			iPoland : "TXT_KEY_CIV_POLAND_DESC_FASCIST",	# Sanacja Poland
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_FASCIST",	# New State of Portugal
                        iInca : "TXT_KEY_CIV_INCA_DESC_FASCIST",	# Government of the Incan Armed Forces
			iItaly : "TXT_KEY_CIV_ROME_DESC_FASCIST",	# New Roman Empire
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_FASCIST",	# Nationalist Mongolia
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_FASCIST",	# Mexican Empire
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_FASCIST",	# Turkish Junta
			iMughals: "TXT_KEY_CIV_MUGHALS_DESC_FASCIST",	# Pakistani Military Government
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_FASCIST",	# Thai Junta
			iCongo : "TXT_KEY_CIV_CONGO_DESC_FASCIST",	# Republic of Zaire
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_FASCIST",	# Third Reich
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_FASCIST",	# 
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_FASCIST",	# New World Order
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_FASCIST",	# United States of Brazil
			iCanada : "TXT_KEY_CIV_CANADA_DESC_FASCIST",	# Canadian Empire
                }

                self.communistNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_COMMUNIST",	# Liberation Rally of Egypt
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_COMMUNIST",	# People's Republic of India
                        iChina : "TXT_KEY_CIV_CHINA_DESC_COMMUNIST",	# People's Republic of China
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_COMMUNIST",	# Babylonian Golden Square
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_COMMUNIST",	# Democratic Republic of the Indus
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_COMMUNIST",	# Democratic Army of Greece
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_COMMUNIST",	# Persian Socialist Republic
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_COMMUNIST",	# People's Republic of Lebanon
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_COMMUNIST",	# People's Republic of Polynesia
                        iRome : "TXT_KEY_CIV_ROME_DESC_COMMUNIST",	# People's Republic of Italy
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_COMMUNIST",	# People's Republic of Japan
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_COMMUNIST",	# Tamil People's Republic
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_COMMUNIST",	# People's Democratic Republic of Ethiopia
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_COMMUNIST",	# Democratic People's Republic of Korea
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_COMMUNIST",	# Mayan Free State
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_COMMUNIST",	# Byzantine People's Republic
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_COMMUNIST",	# Democratic Republic of Scandinavia
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_COMMUNIST",	# Baathist Arabia
			iTibet : "TXT_KEY_CIV_TIBET_DESC_COMMUNIST",	# People's Republic of Tibet
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_COMMUNIST",	# Democratic Kampuchea
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_COMMUNIST",	# People's Republic of Indonesia
			iMoors : "TXT_KEY_CIV_MOORS_DESC_COMMUNIST",	# Socialist Republic of Morocco
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_COMMUNIST",	# Spanish Republic
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_COMMUNIST",	# French Commune
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_COMMUNIST",	# British Worker's Commonwealth
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_COMMUNIST",	# Socialist Republic of Austria
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_COMMUNIST",	# Union of Soviet Socialist Republics
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_COMMUNIST",	# Democratic Republic of the Netherlands
                        iMali : "TXT_KEY_CIV_MALI_DESC_COMMUNIST",	# People's Republic of Mali
			iPoland : "TXT_KEY_CIV_POLAND_DESC_COMMUNIST",	# People's Republic of Poland
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_COMMUNIST",	# Portuguese Continuing Revolutionary Process
                        iInca : "TXT_KEY_CIV_INCA_DESC_COMMUNIST",	# Incan Revolutionary Movement
			iItaly : "TXT_KEY_CIV_ROME_DESC_COMMUNIST",	# People's Republic of Italy
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_COMMUNIST",	# Mongolian People's Republic
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_COMMUNIST",	# Anti-Reelectionist Mexico
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_COMMUNIST",	# National Democratic Popular Turkey
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_COMMUNIST",	# People's Republic of Pakistan
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_COMMUNIST",	# People's Republic of Thailand
			iCongo : "TXT_KEY_CIV_CONGO_DESC_COMMUNIST",	# People's Republic of the Congo
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_COMMUNIST",	# Free Socialist Republic of Germany
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_COMMUNIST",	# United Socialist States of America
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_COMMUNIST",	# Argentine Socialist Republic
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_COMMUNIST",	# Socialist Republic of Brazil
			iCanada : "TXT_KEY_CIV_CANADA_DESC_COMMUNIST",	# Canadian Worker's Commonwealth
                }

                self.democraticNames = {
                        iEgypt : "TXT_KEY_CIV_EGYPT_DESC_DEMOCRATIC",	# Republic of Egypt
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_DEMOCRATIC",	# Republic of India
                        iChina : "TXT_KEY_CIV_CHINA_DESC_DEMOCRATIC",	# Republic of China
                        iBabylonia : "TXT_KEY_CIV_BABYLONIA_DESC_DEMOCRATIC",	# Babylonian Republic
			iHarappa : "TXT_KEY_CIV_HARAPPA_DESC_DEMOCRATIC",	# Indus River Republic
                        iGreece : "TXT_KEY_CIV_GREECE_DESC_DEMOCRATIC",	# Hellenic Republic
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_DEMOCRATIC",	# Republic of Persia
                        iCarthage : "TXT_KEY_CIV_PHOENICIA_DESC_DEMOCRATIC",	# Republic of Lebanon
			iPolynesia : "TXT_KEY_CIV_POLYNESIA_DESC_DEMOCRATIC",	# Polynesian Republics
                        iRome : "TXT_KEY_CIV_ROME_DESC_DEMOCRATIC",	# Italian Republic
                        iJapan : "TXT_KEY_CIV_JAPAN_DESC_DEMOCRATIC",	# Republic of Japan
			iTamils : "TXT_KEY_CIV_TAMILS_DESC_DEMOCRATIC",	# Republic of Tamil Nadu
                        iEthiopia : "TXT_KEY_CIV_ETHIOPIA_DESC_DEMOCRATIC",	# Republic of Ethiopia
                        iKorea : "TXT_KEY_CIV_KOREA_DESC_DEMOCRATIC",	# Republic of Korea
                        iMaya : "TXT_KEY_CIV_MAYA_DESC_DEMOCRATIC",	# Mayan Federal Republic
                        iByzantium : "TXT_KEY_CIV_BYZANTIUM_DESC_DEMOCRATIC",	# Republic of Rhomania
                        iVikings : "TXT_KEY_CIV_VIKINGS_DESC_DEMOCRATIC",	# Republic of Scandinavia
                        iArabia : "TXT_KEY_CIV_ARABIA_DESC_DEMOCRATIC",	# Arab League
			iTibet : "TXT_KEY_CIV_TIBET_DESC_DEMOCRATIC",	# Republic of Tibet
                        iKhmer : "TXT_KEY_CIV_KHMER_DESC_DEMOCRATIC",	# Republic of Cambodia
                        iIndonesia : "TXT_KEY_CIV_INDONESIA_DESC_DEMOCRATIC",	# Republic of Indonesia
			iMoors : "TXT_KEY_CIV_MOORS_DESC_DEMOCRATIC",	# Moroccan Republic
                        iSpain : "TXT_KEY_CIV_SPAIN_DESC_DEMOCRATIC",	# Spanish Republic
                        iFrance : "TXT_KEY_CIV_FRANCE_DESC_DEMOCRATIC",	# French Republic
                        iEngland : "TXT_KEY_CIV_ENGLAND_DESC_DEMOCRATIC",	# Commonwealth of England
                        iHolyRome : "TXT_KEY_CIV_HOLY_ROME_DESC_DEMOCRATIC",	# Republic of Austria
                        iRussia : "TXT_KEY_CIV_RUSSIA_DESC_DEMOCRATIC",	# Russian Federation
                        iNetherlands : "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC",	# Republic of the Seven United Netherlands
                        iMali : "TXT_KEY_CIV_MALI_DESC_DEMOCRATIC",	# Republic of Mali
			iPoland : "TXT_KEY_CIV_POLAND_DESC_DEMOCRATIC",	# Republic of Poland
                        iPortugal : "TXT_KEY_CIV_PORTUGAL_DESC_DEMOCRATIC",	# Portuguese Republic
                        iInca : "TXT_KEY_CIV_INCA_DESC_DEMOCRATIC",	# Incan Republic
			iItaly : "TXT_KEY_CIV_ROME_DESC_DEMOCRATIC",	# Italian Republic
                        iMongolia : "TXT_KEY_CIV_MONGOLIA_DESC_DEMOCRATIC",	# United Mongolia
                        iAztecs : "TXT_KEY_CIV_AZTECS_DESC_DEMOCRATIC",	# United Mexican States
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_DEMOCRATIC",	# Republic of Turkey
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_DEMOCRATIC",	# Republic of Pakistan
			iThailand : "TXT_KEY_CIV_THAILAND_DESC_DEMOCRATIC",	# Republic of Thailand
			iCongo : "TXT_KEY_CIV_CONGO_DESC_DEMOCRATIC",	# Democratic Republic of the Congo
			iGermany : "TXT_KEY_CIV_GERMANY_DESC_DEMOCRATIC",	# Federal Republic of Germany
                        iAmerica : "TXT_KEY_CIV_AMERICA_DESC_DEMOCRATIC",	# United States of America
			iArgentina : "TXT_KEY_CIV_ARGENTINA_DESC_DEMOCRATIC",	# Argentine Republic
			iBrazil : "TXT_KEY_CIV_BRAZIL_DESC_DEMOCRATIC",	# Federative Republic of Brazil
			iCanada : "TXT_KEY_CIV_CANADA_DESC_DEMOCRATIC",	# Commonwealth of Canada
                }
		
		self.modernIslamNames = {
                        iIndia : "TXT_KEY_CIV_INDIA_DESC_ISLAMIC_MODERN",	# Islamic Republic of India
                        iPersia : "TXT_KEY_CIV_PERSIA_DESC_ISLAMIC_MODERN",	# Islamic Republic of Persia
                        iMali : "TXT_KEY_CIV_MALI_DESC_ISLAMIC_MODERN",	# Islamic Republic of Mali
                        iTurkey : "TXT_KEY_CIV_TURKEY_DESC_ISLAMIC_MODERN",	# Islamic Turkish Democracy
			iMughals : "TXT_KEY_CIV_MUGHALS_DESC_ISLAMIC_MODERN",	# Islamic Republic of Pakistan
                }
		
		self.startingLeaders = {
			iEgypt : con.iRamesses,
			iIndia : con.iAsoka,
			iChina : con.iQinShiHuang,
			iBabylonia : con.iGilgamesh,
			iHarappa : con.iVatavelli,
			iGreece : con.iPericles,
			iPersia : con.iCyrus,
			iCarthage : con.iHiram,
			iPolynesia : con.iAhoeitu,
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
			iAmerica : con.iWashington,
			iArgentina : con.iSanMartin,
			iBrazil : con.iDomPedro,
			iCanada : con.iTrudeau,
		}
		
		self.lateStartingLeaders = {
			iChina : con.iTaizong
		}
		
		self.l1700ADLeaders = {
			iChina : con.iHongwu,
			iIndia : con.iShivaji,
			iPersia : con.iAbbas,
			iJapan : con.iTokugawa,
			iVikings : con.iGustav,
			iSpain : con.iPhilip,
			iFrance : con.iLouis,
			iEngland : con.iVictoria,
			iHolyRome : con.iFrancis,
			iRussia : con.iPeter,
			iPoland : con.iSobieski,
			iPortugal : con.iJoao,
			iMughals : con.iAkbar,
			iTurkey : con.iSuleiman,
			iGermany : con.iFrederick,
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
			
				if utils.getScenario() == con.i600AD and iPlayer in self.lateStartingLeaders:
					self.setLeader(iPlayer, self.lateStartingLeaders[iPlayer])
					
				if utils.getScenario() == con.i1700AD and iPlayer in self.l1700ADLeaders:
					self.setLeader(iPlayer, self.l1700ADLeaders[iPlayer])
			
		if utils.getScenario() == con.i600AD:
			self.changeAnarchyTurns(iChina, 3)
			self.setCivDesc(iByzantium, "TXT_KEY_CIV_BYZANTIUM_DESC_DEFAULT")	# Byzantine Empire
		elif utils.getScenario() == con.i1700AD:
			self.changeResurrections(iEgypt, 1)
			
		if utils.getScenario() == con.i1700AD:
			for iPlayer in [iChina, iIndia, iTamils, iPersia, iKorea, iJapan, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iPoland, iPortugal, iMughals, iTurkey, iThailand, iCongo, iNetherlands, iGermany]:
				self.checkName(iPlayer)

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
		
		if iCivic0 == con.iCivicRepublic:
			return True
		if iCivic0 == con.iCivicAutocracy and (iCivic1 == con.iCivicRepresentation or iCivic1 == con.iCivicEgalitarianism):
			return True
			
		return False
		
	def isCommunist(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic0 = pPlayer.getCivics(0)
		iCivic1 = pPlayer.getCivics(1)
		iCivic3 = pPlayer.getCivics(3)
		
		if iCivic3 != con.iCivicCentralPlanning:
			return False
			
		if iCivic0 == con.iCivicTheocracy:
			return False
			
		if iCivic1 in [con.iCivicVassalage, con.iCivicAbsolutism]:
			return False
			
		return True
		
	def isFascist(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		#iCivic0 = pPlayer.getCivics(0)
		iCivic1 = pPlayer.getCivics(1)
		
		if iCivic1 == con.iCivicTotalitarianism:
			return True
			
		#if iCivic0 == con.iCivicAutocracy and iCivic1 not in [con.iCivicRepresentation, con.iCivicEgalitarianism]:
		#	return True
			
		return False
		
	def isEmpire(self, iPlayer):
		iThreshold = 5
		
		if iPlayer == iCarthage: iThreshold = 4
		elif iPlayer == iIndonesia: iThreshold = 4
		elif iPlayer == iKorea: iThreshold = 4
		elif iPlayer == iRussia: iThreshold = 8
		elif iPlayer == iHolyRome: iThreshold = 3
		elif iPlayer == iGermany: iThreshold = 4
		elif iPlayer == iPersia and pPersia.isReborn(): iThreshold = 4
		elif iPlayer == iItaly: iThreshold = 4
		elif iPlayer == iInca: iThreshold = 3
		elif iPlayer == iMongolia: iThreshold = 6
		elif iPlayer == iPoland: iThreshold = 3
		elif iPlayer == iMoors: iThreshold = 3
		elif iPlayer == iTibet: iThreshold = 2
		elif iPlayer == iPolynesia: iThreshold = 3
		elif iPlayer == iTamils: iThreshold = 3
			
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
		bCityStates = (iCivic0 == con.iCivicCityStates)
		bTheocracy = (iCivic0 == con.iCivicTheocracy)
		bResurrected = (self.getResurrections(iPlayer) > 0)
		bCapitulated = bVassal and tPlayer.isCapitulated()
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

		# Leoreth: Vassalage (historical -> generic -> default) -> Civics -> Historical (usually religion -> civics -> size) -> Default
                
                # by vassalage
                if bCapitulated:
			if iMaster == iRussia and pMasterPlayer.getCivics(3) == con.iCivicCentralPlanning:
				self.setCivDesc(iPlayer, self.sovietVassals[iPlayer])
				return
			if iMaster == iGermany and pMasterPlayer.getCivics(1) == con.iCivicTotalitarianism:
				self.setCivDesc(iPlayer, self.naziVassals[iPlayer])
				return
				
			# special cases
			if iMaster == iRome and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_ROMAN_VASSAL")	# Province of Africa
				return
			if iMaster == iTurkey and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_TURKISH_VASSAL")	# Eyalet of Tunisia
				return
			if iMaster == iSpain and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_SPANISH_VASSAL")	# Spanish North Africa
				return
			if iMaster == iMongolia and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_MONGOL_VASSAL")	# Khanate of Carthage
				return
			if iMaster == iFrance and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_FRENCH_VASSAL")	# French North Africa
				return
			if iMaster == iEngland and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_ENGLISH_VASSAL")	# English North Africa
				return
			if iMaster == iByzantium and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_BYZANTINE_VASSAL")	# Exarchate of Africa
				return
			if iMaster == iBabylonia and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_BABYLONIAN_VASSAL")	# Babylonian Carthage
				return
			if iMaster == iArabia and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_ARABIAN_VASSAL")	# Emirate of Ifriqiya
				return
			if iMaster == iChina and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_CHINESE_VASSAL")	# Tributary Carthaginian State
				return
			if iMaster == iRussia and pMasterPlayer.getCivics(3) == con.iCivicCentralPlanning and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_SOVIET_VASSAL")	# Soviet Tunisia
				return
			if iMaster == iGermany and pMasterPlayer.getCivics(1) == con.iCivicTotalitarianism and iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_NAZI_VASSAL")	# Reichskommissariat North Africa
				return
			if iMaster == iHolyRome and iPlayer == iPoland and iGameEra >= con.iIndustrial:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_AUSTRIAN_VASSAL")	# Kingdom of Galicia and Lodomeria
				return
			if iMaster == iEngland and iPlayer == iMughals and not gc.getPlayer(iIndia).isAlive():
				self.setCivDesc(iPlayer, self.specificVassalNames[iEngland][iIndia])
				return
			if iMaster == iSpain and iPlayer == iMaya and bReborn:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_SPANISH_VASSAL")	# Viceroyalty of New Granada
				return
			if iMaster == iPersia and pMasterPlayer.isReborn():	# Protectorate of %s1
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_PROTECTORATE", pPlayer.getCivilizationShortDescriptionKey())
				return
			
			if iMaster in self.specificVassalNames and not pMasterPlayer.isReborn():
				if iPlayer in self.specificVassalNames[iMaster]:
					self.setCivDesc(iPlayer, self.specificVassalNames[iMaster][iPlayer])
					return
					
			if iMaster in self.genericVassalNames:
				self.setCivDesc(iPlayer, self.genericVassalNames[iMaster], pPlayer.getCivilizationShortDescriptionKey())
				return
				
			if iPlayer in [iMali, iEthiopia, iCongo, iAztecs, iInca, iMaya]:	# Colony of %s1
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_COLONY", pPlayer.getCivilizationShortDescriptionKey())
				return
																				# Protectorate of %s1
			self.setCivDesc(iPlayer, "TXT_KEY_CIV_VASSAL_GENERIC_PROTECTORATE", pPlayer.getCivilizationShortDescriptionKey())
			return
		
		# Communism
		if self.isCommunist(iPlayer):
			if iPlayer == iMaya and bReborn:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_COMMUNIST")	# Socialist Republic of Colombia
				return
			if iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_COMMUNIST")	# Punic People's Republic
				return
			if iPlayer in self.communistNames:
				self.setCivDesc(iPlayer, self.communistNames[iPlayer])
				return
				
		# Fascism
		if self.isFascist(iPlayer):
			if iPlayer == iMaya and bReborn:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_FASCIST")	# Colombian Junta
				return
			if iPlayer == iCarthage and capital.getX() < 73:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_FASCIST")	# New Carthaginian Empire
				return
			if iPlayer in self.fascistNames:
				self.setCivDesc(iPlayer, self.fascistNames[iPlayer])
				return
			
		# Democracy (includes Islamic Republics)
		if self.isDemocratic(iPlayer):
			if iPlayer == iMughals:
				if iEra <= con.iRenaissance:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MUGHALS_REPUBLIC_MEDIEVAL")	# Republic of Delhi
					return
			elif iPlayer == iVikings:
				if capital.getName() == "Stockholm":
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDEN_REPUBLIC")	# Republic of Sweden
					return
				elif capital.getName() == "Kobenhavn":
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK_REPUBLIC")	# Republic of Denmark
					return
			elif iPlayer == iPoland:
				if iEra <= con.iIndustrial:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_EMPIRE")	# Polish-Lithuanian Commonwealth
					return
			elif iPlayer == iAmerica:
				if iCivic2 == con.iCivicAgrarianism or iCivic2 == con.iCivicSlavery:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_AMERICA_CSA")	# Confederate States of America
					return
			elif iPlayer == iHolyRome:
				if iGameTurn < getTurnForYear(1700):
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_GERMAN_CONFEDERATION")	# German Confederation
					return
			elif iPlayer == iCarthage:
				if capital.getX() < 73:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_DESC_DEMOCRATIC")	# Punic Republic
					return
			elif iPlayer == iMaya:
				if bReborn:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_DEMOCRATIC")	# Republic of Colombia
					return
		
		
			if iPlayer in self.democraticNames:
				if iPlayer in self.modernIslamNames and iReligion == con.iIslam:
					self.setCivDesc(iPlayer, self.modernIslamNames[iPlayer])
				else:
					self.setCivDesc(iPlayer, self.democraticNames[iPlayer])
				return
				
		# Handle other names specifically
		if iPlayer == iEgypt:
			if bResurrected and self.getResurrections(iPlayer) < 2:
				if bTheocracy and iReligion == con.iIslam:
					if iEra <= iIndustrial:
						if tPlayer.isHasTech(con.iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MAMLUK_CALIPHATE")	# Mamluk Caliphate
						elif pArabia.isAlive():
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_FATIMID_CALIPHATE")	# Fatimid Caliphate
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_AYYUBID_CALIPHATE")	# Ayyubid Caliphate
						return
				elif iReligion == con.iIslam:
					if iEra <= iIndustrial:
						if tPlayer.isHasTech(con.iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MAMLUK_SULTANATE")	# Mamluk Sultanate
						elif pArabia.isAlive():
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_FATIMID_SULTANATE")	# Fatimid Sultanate
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_AYYUBID_SULTANATE")	# Ayyubid Sultanate
						return
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_COPTIC")	# Coptic Kingdom
					return
			else:
				if iGreece in lPreviousOwners:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_PTOLEMAIC")	# Ptolemaic Empire
					return
		
				if bCityStates:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_CITY_STATES")	# Egyptian City-States
					return
				
				if iEra == iAncient:
					if iAnarchyTurns == 0:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_OLD_KINGDOM")	# Old Kingdom of Egypt
					elif iAnarchyTurns == 1:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM")	# Middle Kingdom of Egypt
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_NEW_KINGDOM")	# New Kingdom of Egypt
					return
				elif iEra == iClassical:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_EGYPT_NEW_KINGDOM")	# New Kingdom of Egypt
					return
					
		elif iPlayer == iIndia:
			if iReligion == con.iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_SULTANATE")	# Sultanate of India
				return
				
			if bEmpire and iEra <= iClassical:
				if iReligion == con.iBuddhism:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MAURYA")	# Maurya Empire
					return
				elif iReligion == con.iHinduism:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_GUPTA")	# Gupta Empire
					return
		
			if bCityStates:
				if iEra <= iClassical:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MAHAJANAPADAS")	# Indian Mahajanapadas
					return
					
			if bEmpire and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_PALA")	# Pala Empire
				return
				
			if iEra >= iRenaissance:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MARATHA_EMPIRE")	# Maratha Empire
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDIA_MARATHA")	# Maratha Confederacy
				return
				
		elif iPlayer == iChina:
			if not bResurrected:
				if bEmpire:
					if iEra >= iIndustrial or utils.getScenario() == con.i1700AD:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QING")	# Empire of the Great Qing
						return
						
					if iEra == iRenaissance and iGameTurn >= getTurnForYear(1400):
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_MING")	# Empire of the Great Ming
						return
						
					if iEra == iMedieval:
						#if iAnarchyTurns <= 2:
						#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SUI")
						if teamChina.isHasTech(con.iPaper) and teamChina.isHasTech(con.iGunpowder):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SONG")	# Song Empire
						elif iGameTurn >= getTurnForYear(600):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_TANG")	# Tang Empire
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SUI")	# Sui Empire
						return
						
					if iEra == iClassical:
						if iGameTurn < getTurnForYear(0):
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QIN")	# Qin Empire
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_HAN")	# Han Empire
						return
				
					if iEra == iAncient:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_ZHOU")	# Zhou Empire
						return
			else:
				if bEmpire:
					if iGameTurn < getTurnForYear(con.tBirth[con.iMongolia]):
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_SONG")	# Song Empire
					elif iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_MING")	# Empire of the Great Ming
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_CHINA_QING")	# Empire of the Great Qing
					return
					
		elif iPlayer == iBabylonia:
			if bCityStates and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_CITY_STATES")	# Mesopotamian City-States
				return
		
			if capital.getName() == "Ninova" or capital.getName() == "Kalhu":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_ASSYRIA")	# Assyrian Empire
				return
		
			if bEmpire and iEra > iAncient:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE")	# Neo-Babylonian Empire
				return
				
		elif iPlayer == iGreece:
			if bCityStates:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_EMPIRE")	# Greek Empire
					return
					
				if bWar:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_LEAGUE")	# Greek League
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_CITY_STATES")	# Greek City-States
				return
				
			if iEra <= iClassical:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_MACEDONIA_EMPIRE")	# Macedonian Empire
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_MACEDONIA_KINGDOM")	# Kingdom of Macedonia
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_GREECE_EMPIRE")	# Greek Empire
				return
				
		elif iPlayer == iPersia:
			if not bReborn:
				if bEmpire and iReligion == con.iZoroastrianism:
					if iGameEra < iMedieval:
						if bResurrected:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PARTHIA")	# Parthian Empire
						else:
							self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_ACHAEMENID")	# Achaemenid Empire
						return
					elif iGameEra == iMedieval:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SASSANID")	# Sassanid Empire
						return
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_EMPIRE")	# Persian Empire
						return
			else:
				if bEmpire:
					if iEra <= iRenaissance:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_SAFAVID_EMPIRE")	# Safavid Empire
					elif iEra == iIndustrial:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_QAJAR_EMPIRE")	# Qajar Empire
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_PERSIA_PAHLAVI_EMPIRE")	# Pahlavi Empire
					return
					
		elif iPlayer == iCarthage:	# change adjectives and short desc here too
			if capital.getX() >= 66:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PHOENICIA_CITY_STATES")	# Phoenician City-States
				self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_PHOENICIA_SHORT_DESC")	# Phoenicia
				self.setCivAdjective(iPlayer, "TXT_KEY_CIV_PHOENICIA_ADJECTIVE")	# Phoenician
				return
				
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_SHORT_DESC")	# Carthage
			self.setCivAdjective(iPlayer, "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")	# Carthaginian
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_EMPIRE")	# Carthaginian Empire
				return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_CARTHAGE_CITY_STATES")	# Carthaginian City-States
				return
			# make Carthaginian Kingdom default
			
		elif iPlayer == iPolynesia:
			if capital.getName() in ["Kaua'i", "O'ahu", "Maui"]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_HAWAII")	# Kingdom of Hawaii
				return
			
			if bEmpire:
				if capital.getName() == "Manu'a": self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_EMPIRE_SAMOA")	# Tu'i Manu'a Empire
				else: self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_EMPIRE")	# Tu'i Tonga Empire
				return
				
			if capital.getName() == "Manu'a": self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_SAMOA")	# Kingdom of Samoa
			elif capital.getName() == "Niue": self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLYNESIA_NIUE")	# Kingdom of Niue
			
			# Kingdom of Tonga as default
			
		elif iPlayer == iRome:
			if pByzantium.isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_WESTERN_EMPIRE")	# Western Roman Empire
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_EMPIRE")	# Roman Empire
				return
				
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ROME_REPUBLIC")	# Roman Republic
				return
					
		elif iPlayer == iJapan:
			if bEmpire or iCivic1 == con.iCivicAbsolutism or iEra >= iIndustrial: # Absolutism
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_JAPAN_EMPIRE")	# Empire of Japan
				return
				
			# make Shogunate default
			
		elif iPlayer == iTamils:
			if iEra >= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_MYSORE")	# Kingdom of Mysore
				return
				
			if iEra >= iMedieval:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_VIJAYANAGARA_EMPIRE")	# Vijayanagara Empire
					return
			
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_VIJAYANAGARA")	# Kingdom of Vijayanagara
				return
				
			if bEmpire:
				if capital.getName() in ["Madurai", "Thiruvananthapuram"]:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_PANDYAN_EMPIRE")	# Pandyan Empire
					return
					
				if capital.getName() in ["Cochin", "Kozhikode"]:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_CHERA_EMPIRE")	# Chera Empire
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_CHOLA_EMPIRE")	# Chola Empire
				return
				
			if capital.getName() in ["Madurai", "Thiruvananthapuram"]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_PANDYAN_KINGDOM")	# Pandyan Kingdom
				return
				
			if capital.getName() in ["Cochin", "Kozhikode"]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TAMILS_CHERA_KINGDOM")	# Chera Kingdom
				return
				
			# Chola Kingdom default
				
		elif iPlayer == iEthiopia:
			if not gc.getGame().isReligionFounded(con.iIslam):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ETHIOPIA_AKSUM")	# Kingdom of Aksum
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ETHIOPIA_EMPIRE")	# Ethiopian Empire
				return
				
			# make Ethiopian Kingdom default
			
		elif iPlayer == iKorea:		# difference Goryeo and Joseon with religion?
			if iEra < iMedieval:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_GOGURYEO")	# Kingdom of Goguryeo
					return
			if iEra < iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_GORYEO")	# Kingdom of Goryeo
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_EMPIRE")	# Korean Empire
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_KOREA_JOSEON")	# Kingdom of Greater Joseon
				return
				
		#elif iPlayer == iMaya: # city states are default
		elif iPlayer == iMaya:
			if bReborn:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_EMPIRE")	# Empire of Gran Colombia
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_COLOMBIA_DESC_DEFAULT")	# Kingdom of New Granada
				return
				
		elif iPlayer == iByzantium:
			if pRome.isAlive() and not pRome.isReborn():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_EASTERN_EMPIRE")	# Eastern Roman Empire
				return
				
			if capital.getName() == "Trapezounta":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_TREBIZOND_EMPIRE")	# Empire of Trebizond
				return
			elif capital.getName() == "Dyrrachion":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_EPIRUS_DESPOTATE")	# Despotate of Epirus
				return
			elif capital.getName() == "Athina":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_MOREA_DESPOTATE")	# Despotate of the Morea
				return
			elif capital.getName() != "Konstantinoupolis":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BYZANTIUM_NICAEA_EMPIRE")	# Empire of Nicaea
				return
				
		elif iPlayer == iVikings:
			if iReligion == -1 and not teamVikings.isHasTech(con.iLiberalism):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_NORSE_KINGDOMS")	# Norse Kingdoms
				return
			else:
				if bEmpire:
					if iEra <= iMedieval:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_KALMAR_UNION")	# Kalmar Union
					elif iEra == iRenaissance or capital.getName() == "Stockholm":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDISH_EMPIRE")	# Swedish Empire
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK_NORWAY")	# Kingdom of Denmark-Norway
					return
				else:
					if capital.getName() == "Oslo" or capital.getName() == "Trondheim" or capital.getName() == "Nidaros":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_NORWAY")	# Kingdom of Norway
						return
					elif capital.getName() == "Stockholm" or capital.getName() == "Kalmar":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_SWEDEN")	# Kingdom of Sweden
						return
					elif capital.getName() == "Kobenhavn" or capital.getName() == "Roskilde":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_VIKINGS_DENMARK")	# Kingdom of Denmark
						return
						
		elif iPlayer == iArabia:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_SAUDI")	# Kingdom of Saudi-Arabia
				return
		
			if iReligion == con.iIslam and bTheocracy:
				if not bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_RASHIDUN_CALIPHATE")	# Rashidun Caliphate
				else:
					if capital.getName() == "Dimashq":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_UMMAYAD_CALIPHATE")	# Ummayad Caliphate
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARABIA_ABBASID_CALIPHATE")	# Abbasid Caliphate
				return
				
			# Arabian Sultanates as default, Arabian leaders should prefer Theocracy
			
		elif iPlayer == iTibet:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TIBET_EMPIRE")	# Tibetan Empire
				return
				
			# Kingdom of Tibet as default
			
		elif iPlayer == iKhmer:
			if iEra <= iRenaissance and capital.getName() == "Angkor":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_EMPIRE")	# Khmer Empire
				return
			elif capital.getName() == "Hanoi":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_VIETNAM")	# Dai Viet
				return
			elif capital.getName() == "Pagan":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_BURMA")	# Kingdom of Burma
				return
			elif capital.getName() == "Dali":
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_KHMER_NANZHAO")	# Kingdom of Nanzhao
				return
				
			# Kingdom of Cambodia default
				
		elif iPlayer == iIndonesia:
			if iReligion == con.iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_MATARAM")	# Sultanate of Mataram
				return
		
			if iEra <= iRenaissance:
				if not bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_SRIVIJAYA")	# Kingdom of Srivijaya
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INDONESIA_MAJAPAHIT")	# Kingdom of Majapahit
				return
			
			# generic name as default
			
		elif iPlayer == iMoors:
			bAndalusia = utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR)
			
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_TAIFAS")	# Andalusian Taifas
				return
				
			if bAndalusia:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_CALIPHATE")	# Caliphate of C&#243;rdoba
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_CORDOBA")	# Emirate of Cordoba
				return
				
			if bEmpire and iEra <= iRenaissance:
				if bTheocracy and iReligion == con.iIslam:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_ALMOHAD_CALIPHATE")	# Almohad Caliphate
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MOORS_ALMOHAD_EMPIRE")	# Almohad Empire
				return
				
			# Kingdom of Morocco as default

		elif iPlayer == iSpain:
			if iReligion == con.iIslam:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_SULTANATE")	# Sultanate of Al-Andalus
				return
				
			bSpain = True
			if pMoors.isAlive():
				moorishCapital = gc.getPlayer(iMoors).getCapitalCity()
				if utils.isPlotInArea((moorishCapital.getX(), moorishCapital.getY()), vic.tIberiaTL, vic.tIberiaBR):
					bSpain = False
				
			if bEmpire and iEra > iMedieval:
				if bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_EMPIRE")	# Spanish Empire
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_CASTILIAN_EMPIRE")	# Castilian Empire
				return
				
			if (capital.getName() == "Barcelona" or capital.getName() == "Valencia") and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_ARAGON")	# Crown of Aragon
				return
				
			bSpain = True
			if pMoors.isAlive():
				moorishCapital = gc.getPlayer(iMoors).getCapitalCity()
				if utils.isPlotInArea((moorishCapital.getX(), moorishCapital.getY()), vic.tIberiaTL, vic.tIberiaBR):
					bSpain = False
			
			if iGameTurn > getTurnForYear(con.tBirth[iPortugal]):
				if not pPortugal.isAlive() and bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_IBERIA")	# Kingdom of Iberia
					return
			
				pPortugueseCapital = gc.getPlayer(iPortugal).getCapitalCity()	
				if not utils.isPlotInArea((pPortugueseCapital.getX(), pPortugueseCapital.getY()), con.tCoreAreasTL[0][iPortugal], con.tCoreAreasBR[0][iPortugal], con.tExceptions[0][iPortugal]) and bSpain:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_IBERIA")	# Kingdom of Iberia
					return
		
			if not bSpain:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_SPAIN_CASTILLE")	# Kingdom of Castille
				return
				
		elif iPlayer == iFrance:
			#if capital.getName() == "Nouvelle Orl&#233;ans":
			#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_LOUISIANA")
			#	return
				
			#if utils.isPlotInArea(tCapitalCoords, tNCAmericaTL, tNCAmericaBR):
			#	self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_QUEBEC")
			#	return
		
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iFrance], con.tCoreAreasBR[0][iFrance], con.tExceptions[0][iFrance]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_EXILE")	# Free France
				return
		
			if (iEra > iRenaissance and bEmpire) or iCivic0 == con.iCivicAutocracy:	# Autocracy
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_EMPIRE")	# French Empire
				return
				
			if not pHolyRome.isAlive() and iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_FRANCE_FRANKISH_EMPIRE")	# Frankish Empire
				return
				
		elif iPlayer == iEngland:
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iEngland], con.tCoreAreasBR[0][iEngland], con.tExceptions[0][iEngland]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_EXILE")	# British Government in Exile
				return
		
			if iEra < iIndustrial:
				if utils.getMaster(iFrance) == iEngland:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE")	# Angevin Empire
					return
			
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN")	# Kingdom of Great Britain
					return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_EMPIRE")	# British Empire
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM")	# United Kingdom of Great Britain
				return
				
		elif iPlayer == iHolyRome:
			if bEmpire:
				if pGermany.isAlive():
					if iCivic1 == con.iCivicRepresentation:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_HUNGARY")	# Austro-Hungarian Empire
						return
						
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_EMPIRE")	# Austrian Empire
					return
					
				lEuroCivs = [iVikings, iSpain, iFrance, iEngland, iRome, iItaly, iPoland, iPortugal, iNetherlands]
				iCounter = 0
				
				for iLoopCiv in lEuroCivs:
					if utils.getMaster(iLoopCiv) == iHolyRome:
						iCounter += 1
						
				if iCounter >= 2:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_HABSBURG_EMPIRE")	# Habsburg Empire
					return
				
				if iEra <= con.iRenaissance:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_HRE")	# Holy Roman Empire
					return
			
			if pGermany.isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_HOLY_ROME_AUSTRIA_ARCHDUCHY")	# Archduchy of Austria
				return
				
			# Kingdom of Germany as default
			
		elif iPlayer == iRussia:
			if bEmpire and iEra > iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_RUSSIA_EMPIRE")	# Russian Empire
				return
		
			if iEra == iMedieval and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_RUSSIA_MUSCOVY")	# Grand Duchy of Muscovy
				return
				
		elif iPlayer == iNetherlands:
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC")	# Republic of the Seven United Netherlands
				return
		
			if not utils.isPlotInArea(tCapitalCoords, con.tCoreAreasTL[0][iNetherlands], con.tCoreAreasBR[0][iNetherlands], con.tExceptions[0][iNetherlands]):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_EXILE")	# Dutch Government in Exile
				return
		
			if iEra < iIndustrial:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM")	# United Kingdom of the Netherlands
					return
			else:
				if bEmpire and not bCityStates:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_EMPIRE")	# Dutch Empire
					return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_NETHERLANDS_DESC_DEMOCRATIC")	# Republic of the Seven United Netherlands
				return

			# Kingdom as default
			
		elif iPlayer == iMali:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MALI_SONGHAI")	# Songhai Empire
				return
				
			# Empire as default
			
		elif iPlayer == iPoland:
			if bEmpire and iEra >= con.iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_EMPIRE")	# Polish-Lithuanian Commonwealth
				return
				
			if capital.getName() == 'Kowno' or capital.getName() == 'Medvegalis' or capital.getName() == 'Klajpeda' or capital.getName == 'Wilno' or capital.getName() == 'Riga':
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_POLAND_LITHUANIA")	# Grand Duchy of Lithuania
				return
				
			# Kingdom as default
			
		elif iPlayer == iPortugal:
			if utils.isPlotInArea(tCapitalCoords, tBrazilTL, tBrazilBR) and not gc.getPlayer(iBrazil).isAlive():
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_BRAZIL")	# United Kingdom of Portugal and Brazil
				return
				
			if not utils.isPlotInArea(tCapitalCoords, vic.tIberiaTL, vic.tIberiaBR):
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_EXILE")	# Portuguese Government in Exile
				return
		
			if bEmpire and iEra > iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_PORTUGAL_EMPIRE")	# Portuguese Empire
				return
				
			# Kingdom as default
			
		elif iPlayer == iInca:
			if bResurrected:
				if capital.getName() == 'La Paz':
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_BOLIVIA")	# Republic of Bolivia
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_PERU")	# Republic of Peru
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_INCA_EMPIRE")	# Four Incan Regions
				return
				
			# Kingdom of Cuzco as default
			
		elif iPlayer == iItaly:
			if bCityStates:
				if bWar:
					if bEmpire:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_ITALIAN_LEAGUE")	# Italian League
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_LOMBARD_LEAGUE")	# Lombard League
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS")	# Italian Maritime Republics
				return
			else:
				if bEmpire or bResurrected:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_KINGDOM")	# Kingdom of Italy
				else:
					if capital.getName() == "Fiorenza" or capital.getName() == "Firenze":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_TUSCANY")	# Duchy of Tuscany
					elif capital.getName() == "Venezia":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_VENICE")	# Duchy of Venice
					elif capital.getName() == "Milano":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_DUCHY_MILAN")	# Duchy of Milan
					elif capital.getName() == "Roma":
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_PAPAL_STATE")	# Papal States
					else:
						self.setCivDesc(iPlayer, "TXT_KEY_CIV_ITALY_KINGDOM")	# Kingdom of Italy
				return
			
		elif iPlayer == iMongolia:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_EMPIRE")	# Mongol Empire
				return
				
			if capital.getX() >= 99 and capital.getY() <= 43:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_YUAN")	# Yuan Empire
				return
				
			if capital.getName() == 'Samarkand' or capital.getName() == 'Samarqand' or capital.getName() == 'Merv' or capital.getName() == 'Marv':
				if pMongolia.getStateReligion() == con.iIslam:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_TIMURID")	# Timurid Empire
				else:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_CHAGATAI")	# Chagatai Khanate
				return
		
			if iEra == iMedieval:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MONGOLIA_KHAMAG")	# Khamag Mongol
				return
					
			# Mongol State as default
			
		elif iPlayer == iAztecs:
			if bResurrected:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MEXICO_EMPIRE")	# Mexican Empire
				return
		
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AZTECS_EMPIRE")	# Aztec Empire
				return
		
			if bCityStates:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AZTECS_ALTEPETL")	# Mexican Altepetl
				return
				
			# Triple Alliance as default
			
		elif iPlayer == iMughals:
			if iEra == iMedieval and not bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_MUGHALS_DELHI")	# Delhi Sultanate
				return
				
			# Mughal Empire as default
			
		elif iPlayer == iTurkey:
			if iReligion != con.iIslam:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_EMPIRE")	# Turkish Empire
					return
			
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_STATE")	# Sublime Ottoman State
				return
		
			if bTheocracy:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_CALIPHATE")	# Ottoman Caliphate
				return
				
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_TURKEY_OTTOMAN_EMPIRE")	# Ottoman Empire
				return
				
			# Ottoman Sultanate as default
			
		elif iPlayer == iThailand:
			if iEra <= iRenaissance:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_THAILAND_AYUTTHAYA")	# Kingdom of Ayutthaya
				return
			else:
				if bEmpire:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_THAILAND_EMPIRE")	# Empire of Siam
					return
					
			# Siam as default
			
		elif iPlayer == iGermany:
			if bEmpire and iEra > con.iRenaissance:
				if utils.getMaster(iHolyRome) == iGermany:
					self.setCivDesc(iPlayer, "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE")	# Greater German Empire
					return
					
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_GERMANY_EMPIRE")	# German Empire
				return
				
			# Kingdom of Prussia as default
			
		elif iPlayer == iAmerica:
			if iCivic2 == con.iCivicSlavery or iCivic2 == con.iCivicAgrarianism:	# Slavery/Agrarianism
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_AMERICA_CSA")	# Confederate States of America
				return
				
			# Empire of Columbia as default
			
		elif iPlayer == iArgentina:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARGENTINA_EMPIRE")	# Argentine Empire
				return
				
			if tCapitalCoords != con.tCapitals[0][iArgentina]:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_ARGENTINA_CONFEDERATION")	# Argentine Empire
				return
			
			
		elif iPlayer == iBrazil:
			if bEmpire:
				self.setCivDesc(iPlayer, "TXT_KEY_CIV_BRAZIL_EMPIRE")	# Empire of Brazil
				return
		
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
		bCityStates = (iCivic0 == con.iCivicCityStates or not gc.getTeam(pPlayer.getTeam()).isHasTech(con.iCodeOfLaws))
		bTheocracy = (iCivic0 == con.iCivicTheocracy)
		bResurrected = (self.getResurrections(iPlayer) > 0)
		bMonarchy = not (self.isCommunist(iPlayer) or self.isFascist(iPlayer) or self.isDemocratic(iPlayer))
		iAnarchyTurns = self.getAnarchyTurns(iPlayer)
		iEra = pPlayer.getCurrentEra()
		iGameEra = gc.getGame().getCurrentEra()
		
		
		if iPlayer == iEgypt:
		
			if not bMonarchy and iEra >= con.iModern:
				self.setLeader(iPlayer, con.iNasser)
				return
			
			if bResurrected or utils.getScenario() >= con.i600AD:
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
				
		elif iPlayer == iTamils:
		
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iKrishnaDevaRaya)
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
				
			if iEra >= con.iIndustrial or utils.getScenario() == con.i1700AD:
				self.setLeader(iPlayer, con.iVictoria)
				return
				
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iElizabeth)
				return
				
		elif iPlayer == iHolyRome:
		
			if iEra >= con.iIndustrial or utils.getScenario() == con.i1700AD:
				self.setLeader(iPlayer, con.iFrancis)
				return
		
			if iEra >= con.iRenaissance:
				self.setLeader(iPlayer, con.iCharles)
				return
				
		elif iPlayer == iRussia:
		
			if not bMonarchy and iEra >= iIndustrial:
				self.setLeader(iPlayer, con.iStalin)
				if self.isCommunist(iPlayer):
                                        cnm.applySovietNames()
				return
				
			if iEra >= con.iIndustrial:
				self.setLeader(iPlayer, con.iNicholas)
				return
				
			if iEra >= con.iRenaissance:
				if iGameTurn >= getTurnForYear(1750):
					self.setLeader(iPlayer, con.iCatherine)
					return
				
				self.setLeader(iPlayer, con.iPeter)
				return
				
		elif iPlayer == iNetherlands:
			return
			
		elif iPlayer == iMali:
			return
			
		elif iPlayer == iPoland:
		
			if iEra >= con.iRenaissance or utils.getScenario() == con.i1700AD:
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
			
			if pPlayer.isReborn():
				if bMonarchy or self.isFascist(iPlayer):
					self.setLeader(iPlayer, con.iSantaAnna)
					return
					
				if iEra >= con.iModern:
					self.setLeader(iPlayer, con.iCardenas)
					return
					
				self.setLeader(iPlayer, con.iJuarez)
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
				
		elif iPlayer == iArgentina:
		
			if iEra >= con.iModern:
				self.setLeader(iPlayer, con.iPeron)
				return
				
		elif iPlayer == iBrazil:
			return
				
		if utils.getScenario() == con.i600AD and iPlayer in self.lateStartingLeaders:
			self.setLeader(iPlayer, self.lateStartingLeaders[iPlayer])
			return
			
		if utils.getScenario() == con.i1700AD and iPlayer in self.l1700ADLeaders:
			self.setLeader(iPlayer, self.l1700ADLeaders[iPlayer])
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
			self.setCivShortDesc(iPlayer, "TXT_KEY_CIV_AUSTRIA_SHORT_DESC")
			
		
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