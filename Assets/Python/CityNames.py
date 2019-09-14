from CvPythonExtensions import *

from Consts import *
from RFCUtils import utils
from StoredData import data

def isResurrected(iCiv):
	return (data.players[iCiv].iResurrections > 0)

def getSpecialLanguages(iPlayer):
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = pPlayer.getCivilizationType()

	if iCiv == iCivEgypt:
		if pPlayer.getStateReligion() == iIslam:
			return (iLangEgyptianArabic, iLangArabian)
	
	elif iCiv == iCivInca:
		if isResurrected(iPlayer):
			return (iLangSpanish,)
			
	return None
	
def getLanguages(iPlayer):
	tSpecialLanguages = getSpecialLanguages(iPlayer)
	
	if tSpecialLanguages:
		return tSpecialLanguages
		
	iCiv = gc.getPlayer(iPlayer).getCivilizationType()
	if iCiv in dLanguages:
		return dLanguages[iCiv]

	return None
	
def getTileName(tPlot):
	x, y = tPlot
	return tCities[iWorldY-1-y][x]
	
def getCivicNames(iPlayer):
	return {}
	
def getEraNames(iPlayer):
	iCurrentEra = gc.getPlayer(iPlayer).getCurrentEra()
	
	dNames = {}
	for iEra in range(iCurrentEra+1):
		dNames.update(tEraNames[iEra])
		
	return dNames
	
def findLocations(iPlayer, name):
	return [tPlot for tPlot in utils.getWorldPlotsList() if getName(iPlayer, tPlot) == name or getName(iEngland, tPlot) == name]
	
def getName(iPlayer, tPlot):
	name = getTileName(tPlot)
	
	if name in data.dChangedCities:
		name = data.dChangedCities[name]
		
	if name in data.dChangedNames:
		name = data.dChangedNames[name]
	else:
		dEraNames = getEraNames(iPlayer)
		if name in dEraNames:
			data.dChangedNames[name] = dEraNames[name]
			name = dEraNames[name]
		
	dCivicNames = getCivicNames(iPlayer)
	if name in dCivicNames:
		name = dCivicNames[name]
		
	name = translateName(iPlayer, name)
	
	return name
	
def translateName(iPlayer, name):
	tLanguages = getLanguages(iPlayer)
	if not tLanguages: return name
	
	for iLanguage in tLanguages:
		if name in tRenames[iLanguage]:
			return tRenames[iLanguage]
		if name in tRenames[iLanguage].values():
			return name
			
	return name
	
def checkCity(iPlayer, city):
	name = getName(iPlayer, (city.getX(), city.getY()))
	
	if name:
		city.setName(name, False)
		
def checkCities(iPlayer):
	for city in utils.getCityList(iPlayer):
		checkCity(iPlayer, city)

def setup():
	global tCities
	tCities = utils.readMap('Cities')
	
def onCityAcquired(city, iNewOwner):
	checkCity(iNewOwner, city)
		
def onCityBuilt(city):
	checkCity(city.getOwner(), city)
	
def onRevolution(iPlayer):
	checkCities(iPlayer)
	
def onReligionSpread(iPlayer):
	checkCities(iPlayer)
	
def onTechAcquired(iPlayer):
	checkCities(iPlayer)

tCities = None

iNumLanguages = 41
(iLangEgyptian, iLangEgyptianArabic, iLangIndian, iLangChinese, iLangTibetan, 
iLangBabylonian, iLangPersian, iLangGreek, iLangPhoenician, iLangLatin, 
iLangJapanese, iLangEthiopian, iLangKorean, iLangMayan, iLangByzantine, 
iLangViking, iLangArabian, iLangKhmer, iLangIndonesian, iLangSpanish, 
iLangFrench, iLangEnglish, iLangGerman, iLangRussian, iLangDutch, 
iLangMalian, iLangPolish, iLangPortuguese, iLangQuechua, iLangItalian, 
iLangMongolian, iLangAztec, iLangTurkish, iLangThai, iLangCongolese, 
iLangPrussian, iLangAmerican, iLangCeltic, iLangMexican, iLangPolynesian,
iLangHarappan) = range(iNumLanguages)

dLanguages = {
	iCivEgypt:	(iLangEgyptian,),
	iCivBabylonia: (iLangBabylonian,),
	iCivHarappa: (iLangHarappan, iLangIndian),
	iCivChina: (iLangChinese,),
	iCivGreece: (iLangGreek,),
	iCivIndia: (iLangIndian,),
	iCivCarthage: (iLangPhoenician,),
	iCivPolynesia: (iLangPolynesian,),
	iCivPersia: (iLangPersian,),
	iCivRome: (iLangLatin,),
	iCivMaya: (iLangMayan, iLangAztec),
	iCivTamils: (iLangIndian,),
	iCivEthiopia: (iLangEthiopian,),
	iCivKorea: (iLangKorean, iLangChinese),
	iCivByzantium: (iLangByzantine, iLangLatin),
	iCivJapan: (iLangJapanese,),
	iCivVikings: (iLangViking,),
	iCivTurks: (iLangTurkish, iLangArabian, iLangPersian),
	iCivArabia: (iLangArabian,),
	iCivTibet: (iLangTibetan, iLangChinese),
	iCivKhmer: (iLangKhmer, iLangIndonesian),
	iCivIndonesia: (iLangIndonesian, iLangKhmer),
	iCivMoors: (iLangArabian,),
	iCivSpain: (iLangSpanish,),
	iCivFrance: (iLangFrench,),
	iCivEngland: (iLangEnglish,),
	iCivHolyRome: (iLangGerman,),
	iCivRussia: (iLangRussian,),
	iCivMali: (iLangMalian,),
	iCivPoland: (iLangPolish, iLangRussian),
	iCivPortugal: (iLangPortuguese, iLangSpanish),
	iCivInca: (iLangQuechua,),
	iCivItaly: (iLangItalian,),
	iCivMongols: (iLangMongolian, iLangTurkish, iLangChinese),
	iCivAztecs: (iLangAztec,),
	iCivMughals: (iLangPersian, iLangArabian, iLangIndian),
	iCivOttomans: (iLangTurkish, iLangArabian),
	iCivThailand: (iLangThai, iLangKhmer, iLangIndonesian),
	iCivCongo: (iLangCongolese,),
	iCivIran: (iLangArabian, iLangPersian),
	iCivNetherlands: (iLangDutch,),
	iCivGermany: (iLangPrussian, iLangGerman),
	iCivAmerica: (iLangAmerican, iLangEnglish),
	iCivArgentina: (iLangSpanish,),
	iCivMexico: (iLangSpanish,),
	iCivColombia: (iLangSpanish,),
	iCivBrazil: (iLangPortuguese, iLangSpanish),
	iCivCanada: (iLangAmerican, iLangEnglish, iLangFrench),
	iCivCeltia: (iLangCeltic,),
}
			
tEraNames = (
# ancient
{},
# classical
{},
# medieval
{
	"Chang'an"		:	"Xi'an",
	'Zhongdu'		:	'Beijing',
	'Indraprastha'		:	'Dilli',
	'Roha'			:	'Lalibela',
},
# renaissance
{
	'Pataliputra'		:	'Patna',
	'Haojing'		:	'Aomen',
	'Nidaros'		:	'Trondheim',
	'Roskilde'		:	'K&#248;benhavn',
	'Haithabu'		:	'Hamburg',
	'Novokholmogory'	:	"Arkhangel'sk",
	'Spas na Kholmu'	:	'Krasnyj Kholm',
	'Tumasik'		:	'Singapura',
	'Sundapura'		:	'Jayakarta',
	'Buda'			:	'Budapest',
},
# industrial
{
	'Yax Mutal'		:	'Tikal',
	'Edo'			:	'Toukyou',
	'Mo&#231;ambique'	:	'Lauren&#231;o Marques',
	'Constantinopolis'	:	'Istanbul',
	'Fiorenza'		:	'Firenze',
	'Dagou'			:	'Gaoxiong',
	'Ayutthaya'		:	'Bangkok',
	'York'			:	'Toronto',
	'Barara'		:	'Addis Ababa',
},
# modern
{
	'Angora'		:	'Ankara',
	'Hanseong'		:	'Seoul',
	'Jehol'			:	'Chengde',
},
# future
{},
)
	
dCommunistNames = {
	'Caricyn'		:	'Stalingrad',
	'Sankt-Peterburg'	:	'Leningrad',
	"Tver'"			:	'Kalinin',
	'Ekaterinburg'		:	'Sverdlovsk',
	'Nizhnij Novgorod'	:	'Gorki',
	'Samara'		:	'Kujbyshev',
	"Car'grad"		:	"Konstantinopol'",
	'Bobrujsk'		:	'Stalink',
	'Vjatka'		:	'Kirov',
	'Bavly'			:	"Oktjabr'skij",
	'Sumin'			:	'Sumy',
	'Sjangan'		:	'Gon Kong',
}

tRenames = (
#Language: Egyptian
{
},
#Language: Egyptian Arabic
{
},
#Language: Indian
{
},
#Language: Chinese
{
},
#Language: Tibetan
{
},
#Language: Babylonian
{
},
#Language: Persian
{
},
#Language: Greek
{
},
#Language: Phoenician
{
},
#Language: Latin
{
},
#Language: Mayan
{
},
#Language: Japanese
{
},
#Language: Ethiopian
{
},
#Language: Korean
{
},
#Language: Byzantine
{
},
#Language: Viking
{
},
#Language: Arabian
{
},
#Language: Khmer
{
},
#Language: Indonesian
{
},
#Language: Spanish
{
},
#Language: French
{
},
#Language: English
{
},
#Language: German
{
},
#Language: Russian
{
},
#Language: Dutch
{
},
#Language: Malian
{
},
#Language: Polish
{
},
#Language: Portuguese
{
},
#Language: Quechua
{
},
#Language: Italian
{
},
#Language: Mongolian
{
},
#Language: Aztec
{
},
#Language: Turkish
{
},
#Language: Thai
{
},
#Language: Congolese
{
},
#Language: Prussian
{
},
#Language: American
{
},
#Language: Celtic
{
},
#Language: Mexican
{
},
#Language: Polynesian
{
},
#Language: Harappan
{
},
)
	
