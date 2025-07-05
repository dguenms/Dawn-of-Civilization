## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# Author - Jon Shafer
# Top Civilizations screen

import PyHelpers
import CvUtil
import CvScreenEnums
import random
from Core import *

NUM_CIVILIZATIONS = 8

HISTORIANS = {
	iEgypt: {
		iAncient: (
			"TXT_KEY_HISTORIAN_KHAEMWASET",
		),
		iClassical: (
			"TXT_KEY_HISTORIAN_MANETHO",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_AL_QIFTI",
			"TXT_KEY_HISTORIAN_AL_MAQRIZI",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_AL_SUYUTI",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_ABD_AL_RAHMAN_AL_RAFAI",
		),
	},
	iBabylonia: {
		iAncient: (
			"TXT_KEY_HISTORIAN_AMMISADUQA",
		),
	},
	iChina: {
		iAncient: (
			"TXT_KEY_HISTORIAN_FU_SHENG",
			"TXT_KEY_HISTORIAN_ZUO_QIUMING",
		),
		iClassical: (
			"TXT_KEY_HISTORIAN_SIMA_QIAN",
			"TXT_KEY_HISTORIAN_LIU_XIANG",
			"TXT_KEY_HISTORIAN_GUO_PU",
			"TXT_KEY_HISTORIAN_CHEN_SHOU",
			"TXT_KEY_HISTORIAN_PEI_SONGZHI",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_SIMA_GUANG",
			"TXT_KEY_HISTORIAN_OUYANG_XIU",
			"TXT_KEY_HISTORIAN_SONG_LIAN",
			"TXT_KEY_HISTORIAN_LIU_ZHIJI",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_HUANG_ZONGXI",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_YANG_SHOUJING",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_LI_XUEQIN",
		),
	},
	iGreece: {
		iAncient: (
			"TXT_KEY_HISTORIAN_HERODOTUS",
		),
		iClassical: (
			"TXT_KEY_HISTORIAN_THUCYDIDES",
			"TXT_KEY_HISTORIAN_XENOPHON",
			"TXT_KEY_HISTORIAN_PLUTARCH",
			"TXT_KEY_HISTORIAN_STRABO",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_KAROLIDIS",
			"TXT_KEY_HISTORIAN_PAPARRIGOPOULOS",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_KORDATOS",
		),
	},
	iIndia: {
		iAncient: (
			"TXT_KEY_HISTORIAN_VYASA",
		),
		iClassical: (
			"TXT_KEY_HISTORIAN_KAUTILYA",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_BANABHATTA",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_PADMANABHA",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_CHOUDHARY",
			"TXT_KEY_HISTORIAN_MAJUMDAR",
		),
	},
	iPhoenicia: {
		iAncient: (
			"TXT_KEY_HISTORIAN_SANCHUNIATHON",
		),
	},
	iPolynesia: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_TEUIRA_HENRY",
			"TXT_KEY_HISTORIAN_TE_RANGIKAHEKE",
		),
	},
	iPersia: {
		iClassical: (
			"TXT_KEY_HISTORIAN_CTESIAS",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_RASHID_AL_DIN",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_FIRISHTA",
			"TXT_KEY_HISTORIAN_MUNSHI",
		),
	},
	iRome: {
		iClassical: (
			"TXT_KEY_HISTORIAN_LIVY",
			"TXT_KEY_HISTORIAN_PLINY",
			"TXT_KEY_HISTORIAN_TACITUS",
			"TXT_KEY_HISTORIAN_AMMIAN",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_SAINT_AUGUSTINE",
			"TXT_KEY_HISTORIAN_PAUL_THE_DEACON",
		),
	},
	iEthiopia: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_BAHREY",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_HERUY_WOLDE_SELASSIE",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_ZEWDE_GEBRE_SELLASSIE",
		),
	},
	iDravidia: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_NILAKANTA_SASTRI",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_PILLAI",
			"TXT_KEY_HISTORIAN_SIVATHAMBY",
		),
	},
	iKorea: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_KIM_PUSIK",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_CHOE_BU",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_MUN_IL_PYEONG",
			"TXT_KEY_HISTORIAN_SHIN_CHAE_HO",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_JEONG_SU_IL",
		),
	},
	iByzantium: {
		iClassical: (
			"TXT_KEY_HISTORIAN_THEOPHANES",
			"TXT_KEY_HISTORIAN_PROCOPIUS",
			"TXT_KEY_HISTORIAN_SAINT_JEROME",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_ANNA_KOMNENE",
		),
	},
	iJapan: {
		iClassical: (
			"TXT_KEY_HISTORIAN_YASUMARO",
			"TXT_KEY_HISTORIAN_TONERI",
		),
		iMedieval: (
			"TXT_KEY_HISTORIAN_KITABATAKE",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_ARAI",
			"TXT_KEY_HISTORIAN_HAYASHI",
			"TXT_KEY_HISTORIAN_MOTOORI",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_RAI",
			"TXT_KEY_HISTORIAN_DATE",
			"TXT_KEY_HISTORIAN_NAITOU",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_INOUE",
		),
	},
	iNorse: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_AGGESEN",
			"TXT_KEY_HISTORIAN_THORGILSSON",
			"TXT_KEY_HISTORIAN_SAXO_GRAMMATICUS",
			"TXT_KEY_HISTORIAN_SNORRI_STURLUSON",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_HOLBERG",
			"TXT_KEY_HISTORIAN_HUITFELDT",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_MUNCH",
		),
	},
	iTurks: {
		iGlobal: (
			"TXT_KEY_HISTORIAN_TOGAN",
		),
	},
	iArabia: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_AL_ZUBAYR",
			"TXT_KEY_HISTORIAN_AL_TABARI",
			"TXT_KEY_HISTORIAN_IBN_FADLAN",
			"TXT_KEY_HISTORIAN_ABUL_FARAJ",
			"TXT_KEY_HISTORIAN_AL_MASUDI",
			"TXT_KEY_HISTORIAN_IBN_MUNQIDH",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_KHULUSI",
			"TXT_KEY_HISTORIAN_AL_ZAHIRI",
		),
	},
	iTibet: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_DRUB",
			"TXT_KEY_HISTORIAN_ZHONNU_PEL",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_THRENGWA",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_PUNTSOK",
		),
	},
	iJava: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_PRAPANCA",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_YASADIPURA",
			"TXT_KEY_HISTORIAN_RANGGAWARSITA",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_NOTOSUSANTO",
			"TXT_KEY_HISTORIAN_KARTODIRDJO",
		),
	},
	iMalays: {
		iGlobal: (
			"TXT_KEY_HISTORIAN_YAMIN",
		),
	},
	iMoors: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_IBN_HAZM",
			"TXT_KEY_HISTORIAN_IBN_BATTUTA",
			"TXT_KEY_HISTORIAN_IBN_KHALDUN",
		),
	},
	iSpain: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_ISIDORE",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_DANGHIERA",
			"TXT_KEY_HISTORIAN_DE_MORGA",
			"TXT_KEY_HISTORIAN_DE_LAS_CASAS",
		),
	},
	iFrance: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_GREGORY_OF_TOURS",
			"TXT_KEY_HISTORIAN_EINHARD",
			"TXT_KEY_HISTORIAN_FROISSART",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_RAMBAUD",
			"TXT_KEY_HISTORIAN_MICHELET",
			"TXT_KEY_HISTORIAN_BLOCH",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_BRAUDEL",
			"TXT_KEY_HISTORIAN_DUBY",
			"TXT_KEY_HISTORIAN_LE_GOFF",
		),
	},
	iKhmer: {
		iGlobal: (
			"TXT_KEY_HISTORIAN_KAONN",
		),
	},
	iEngland: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_BEDE",
			"TXT_KEY_HISTORIAN_ASSER",
			"TXT_KEY_HISTORIAN_AETHELWEARD",
			"TXT_KEY_HISTORIAN_GEOFFREY_OF_MONMOUTH",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_HOLINSHED",
			"TXT_KEY_HISTORIAN_HUME",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_GIBBON",
			"TXT_KEY_HISTORIAN_LORD_MACAULAY",
			"TXT_KEY_HISTORIAN_CARLYLE",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_TOYNBEE",
			"TXT_KEY_HISTORIAN_HOBSBAWM",
		),
	},
	iHolyRome: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_ADAM_OF_BREMEN",
			"TXT_KEY_HISTORIAN_HERMANN_OF_REICHENAU",
		),
	},
	iRus: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_NESTOR_THE_CHRONICLER",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_KOSTOMAROV",
		),
	},
	iRussia: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_NIKITIN",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_KARAMZIN",
			"TXT_KEY_HISTORIAN_MULLER",
			"TXT_KEY_HISTORIAN_TATISHCHEV",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_SOLOVYOV",
			"TXT_KEY_HISTORIAN_KLYUCHEVSKY",
			"TXT_KEY_HISTORIAN_POKROVSKY",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_VOLGIN",
		),
	},
	iMali: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_KATI",
			"TXT_KEY_HISTORIAN_IBN_AL_MUKHTAR",
		),
	},
	iPoland: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_KADLUBEK",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_MIECHOWITA",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_LELEWEL",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_HANDELSMAN",
		),
	},
	iPortugal: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_DE_BARROS",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_HERCULANO",
		),
	},
	iInca: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_DE_LA_VEGA",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_BASADRE",
		),
	},
	iItaly: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_SALIMBENE",
			"TXT_KEY_HISTORIAN_POLO",
			"TXT_KEY_HISTORIAN_RAUL",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_MACHIAVELLI",
			"TXT_KEY_HISTORIAN_VASARI",
			"TXT_KEY_HISTORIAN_VICO",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_CANTU",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_DE_SANCTIS",
			"TXT_KEY_HISTORIAN_DEL_BOCA",
		),
	},
	iMongols: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_TOQTOA",
			"TXT_KEY_HISTORIAN_HAMADANI",
			"TXT_KEY_HISTORIAN_BOLAD",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_LUVSANDAZAN",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_RINCHEN",
		),
	},
	iMughals: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_BHANDARI",
			"TXT_KEY_HISTORIAN_ABUL_FAZL",
			"TXT_KEY_HISTORIAN_LAHORI",
			"TXT_KEY_HISTORIAN_KHAFI_KHAN",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_ROSHAN_KHAN",
			"TXT_KEY_HISTORIAN_IKRAM",
		),
	},
	iOttomans: {
		iMedieval: (
			"TXT_KEY_HISTORIAN_ASHIKPASHAZADE",
			"TXT_KEY_HISTORIAN_NESHRI",
		),
		iRenaissance: (
			"TXT_KEY_HISTORIAN_CHELEBI",
			"TXT_KEY_HISTORIAN_PECHEVI",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_CEVDET_PASHA",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_INAN",
		),
	},
	iSweden: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_OLAUS_MAGNUS",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_GRIMBERG",
			"TXT_KEY_HISTORIAN_GEIJER",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_LONNROTH",
		),
	},
	iThailand: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_RAJANUBHAB",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_WICHIWATHAKAN",
		),
	},
	iNetherlands: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_DE_JONGE",
			"TXT_KEY_HISTORIAN_FRUIN",
		),
	},
	iGermany: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_SCHILLER",
			"TXT_KEY_HISTORIAN_VON_RANKE",
			"TXT_KEY_HISTORIAN_VON_SYBEL",
			"TXT_KEY_HISTORIAN_MARX",
		),
	},
	iAmerica: {
		iRenaissance: (
			"TXT_KEY_HISTORIAN_MATHER",
		),
		iIndustrial: (
			"TXT_KEY_HISTORIAN_ADAMS",
			"TXT_KEY_HISTORIAN_BEARD",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_SCHLESINGER",
		),
	},
	iArgentina: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_MITRE",
			"TXT_KEY_HISTORIAN_LOPEZ",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_LUNA",
		),
	},
	iColombia: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_RESTREPO_VELEZ",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_FRIEDE",
		),
	},
	iBrazil: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_DE_VARNHAGEN",
			"TXT_KEY_HISTORIAN_ROMERO",
			"TXT_KEY_HISTORIAN_DE_ABREU",
		),
		iGlobal: (
			"TXT_KEY_HISTORIAN_FREYRE",
			"TXT_KEY_HISTORIAN_DE_HOLANDA",
			"TXT_KEY_HISTORIAN_PRADO_JUNIOR",
		),
	},
	iCanada: {
		iIndustrial: (
			"TXT_KEY_HISTORIAN_GARNEAU",
			"TXT_KEY_HISTORIAN_GROULX",
		),
	},
}

class CvTopCivs:
	"The Greatest Civilizations screen"
	
	def __init__(self):
		
		self.X_SCREEN = 0#205
		self.Y_SCREEN = 0#27
		self.W_SCREEN = 1024#426
		self.H_SCREEN = 768#470

		self.X_MAIN_PANEL = 250
		self.Y_MAIN_PANEL = 70
		self.W_MAIN_PANEL = 550
		self.H_MAIN_PANEL = 500
		
		self.iMarginSpace = 15
		
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_HEADER_PANEL = self.H_MAIN_PANEL - (self.iMarginSpace * 2)
		
#		iWHeaderPanelRemainingAfterLeader = self.W_HEADER_PANEL - self.W_LEADER_ICON + (self.iMarginSpace * 3)
#		iXHeaderPanelRemainingAfterLeader = self.X_LEADER_ICON + self.W_LEADER_ICON + self.iMarginSpace
		self.X_LEADER_TITLE_TEXT = 500#iXHeaderPanelRemainingAfterLeader + (iWHeaderPanelRemainingAfterLeader / 2)
		self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.iMarginSpace
		self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3
		self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 3
		
		self.X_TEXT_PANEL = self.X_HEADER_PANEL + self.iMarginSpace
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + 132
		self.W_TEXT_PANEL = self.W_HEADER_PANEL - (self.iMarginSpace * 2)
		self.H_TEXT_PANEL = 265#self.H_MAIN_PANEL - self.H_HEADER_PANEL - (self.iMarginSpace * 3) + 10 #10 is the fudge factor
		self.iTEXT_PANEL_MARGIN = 35
		
		self.X_RANK_TEXT = 430
		self.Y_RANK_TEXT = 230
		self.W_RANK_TEXT = 300
		self.H_RANK_TEXT = 30
		
		self.X_EXIT = 460
		self.Y_EXIT = self.Y_MAIN_PANEL + 440
		self.W_EXIT = 120
		self.H_EXIT = 30

	def showScreen(self):
			  
		'Use a popup to display the opening text'
		if ( CyGame().isPitbossHost() ):
			return

		# Text
		self.TITLE_TEXT = u"<font=3>" + text("TXT_KEY_TOPCIVS_TITLE").upper() + u"</font>"
		self.EXIT_TEXT = text("TXT_KEY_PEDIA_SCREEN_EXIT").upper()
					
		self.RankList = [
			text("TXT_KEY_TOPCIVS_RANK1"),
			text("TXT_KEY_TOPCIVS_RANK2"),
			text("TXT_KEY_TOPCIVS_RANK3"),
			text("TXT_KEY_TOPCIVS_RANK4"),
			text("TXT_KEY_TOPCIVS_RANK5"),
			text("TXT_KEY_TOPCIVS_RANK6"),
			text("TXT_KEY_TOPCIVS_RANK7"),
			text("TXT_KEY_TOPCIVS_RANK8")
		]

		self.TypeList = [
			"TXT_KEY_TOPCIVS_WEALTH",
			"TXT_KEY_TOPCIVS_POWER",
			"TXT_KEY_TOPCIVS_TECH",
			"TXT_KEY_TOPCIVS_CULTURE",
			"TXT_KEY_TOPCIVS_SIZE",
			"TXT_KEY_TOPCIVS_POPULATION",
		]

		# Randomly choose what category will be used
		szTypeRand = random.choice(self.TypeList)
		
		# Create screen
		
		self.screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )

		self.screen.setSound("AS2D_TOP_CIVS")
		self.screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		self.screen.showWindowBackground( False )
		self.screen.setDimensions(self.screen.centerX(self.X_SCREEN), self.screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
		
		# Create panels
		
		# Main
		szMainPanel = "TopCivsMainPanel"
		self.screen.addPanel( szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		
		# Top
		szHeaderPanel = "TopCivsHeaderPanel"
		szHeaderText = ""#gc.getLeaderHeadInfo(self.player.getLeaderType()).getDescription() + "\n-" + self.player.getCivilizationDescription(0) + "-"
		self.screen.addPanel( szHeaderPanel, szHeaderText, "", true, true,
			self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		
		# Bottom
		szTextPanel = "TopCivsTextPanel"
		szHeaderText = ""#self.Text_Title
		self.screen.addPanel( szTextPanel, szHeaderText, "", true, true,
			self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP )
		
		self.screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT,self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		# Title Text
		self.X_TITLE_TEXT = self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2)
		self.Y_TITLE_TEXT = self.Y_HEADER_PANEL + 15
		self.screen.setLabel("DawnTitle", "Background", self.TITLE_TEXT, CvUtil.FONT_CENTER_JUSTIFY,
				self.X_TITLE_TEXT, self.Y_TITLE_TEXT, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		self.populateList(szTypeRand)
		
		szHistorianKey = self.getHistorian()
		szHistorian = text(szHistorianKey)
		szType = text(szTypeRand)
		
		# 1 Text
		self.X_INFO_TEXT = self.X_TITLE_TEXT - 260#self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2)
		self.Y_INFO_TEXT = self.Y_TITLE_TEXT + 50
		self.W_INFO_TEXT = self.W_HEADER_PANEL
		self.H_INFO_TEXT = 70
		szText = text("TXT_KEY_TOPCIVS_TEXT1", szHistorian) + u"\n" + text("TXT_KEY_TOPCIVS_TEXT2", szType)
		self.screen.addMultilineText( "InfoText1", szText, self.X_INFO_TEXT, self.Y_INFO_TEXT, self.W_INFO_TEXT, self.H_INFO_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		
		self.printList()
		
	def populateList(self, szType):
		
		print "populateList for %s" % szType

		# Determine the list of top civs
		
		typeFunction = None
		
		if szType == "TXT_KEY_TOPCIVS_WEALTH":
			typeFunction = CyPlayer.getGold
		elif szType == "TXT_KEY_TOPCIVS_POWER":
			typeFunction = CyPlayer.getPower
		elif szType == "TXT_KEY_TOPCIVS_TECH":
			typeFunction = lambda p: team(p).getTotalTechValue()
		elif szType == "TXT_KEY_TOPCIVS_CULTURE":
			typeFunction = CyPlayer.countTotalCulture
		elif szType == "TXT_KEY_TOPCIVS_SIZE":
			typeFunction = CyPlayer.getTotalLand
		elif szType == "TXT_KEY_TOPCIVS_POPULATION":
			typeFunction = CyPlayer.getTotalPopulation
			
		self.topPlayers = players.major().existing().sort(lambda p: typeFunction(player(p)), reverse=True)
		
	def printList(self):
		for iRank, iPlayer in enumerate(self.topPlayers.limit(8)):
			if iPlayer == active() or team().isHasMet(player(iPlayer).getTeam()):
				szCivText = fullname(iPlayer)
			else:
				szCivText = text("TXT_KEY_TOPCIVS_UNKNOWN")
			
			szWidgetName = "Text" + str(iRank)
			szWidgetDesc = "%d) %s" % (iRank + 1, szCivText)
			
			iXLoc = self.X_RANK_TEXT
			iYLoc = self.Y_RANK_TEXT + iRank * self.H_RANK_TEXT
			
			self.screen.addMultilineText(szWidgetName, unicode(szWidgetDesc), iXLoc, iYLoc, self.W_RANK_TEXT, self.H_RANK_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
	
	def getHistorian(self):
		iHistorianPlayer = self.topPlayers.where(lambda p: team().isHasMet(player(p).getTeam())).limit(4).where(lambda p: civ(p) in HISTORIANS).random(otherwise=active())
		
		tHistorianNames = self.getHistorianNames(iHistorianPlayer)
		if not tHistorianNames:
			return "TXT_KEY_HISTORIAN_GENERIC"
		
		return random_entry(tHistorianNames)
	
	def getHistorianNames(self, iPlayer):
		iCiv = civ(iPlayer)
		iCurrentEra = player(iPlayer).getCurrentEra()
		
		if iCiv not in HISTORIANS:
			return tuple()
		
		for iEra in reversed(range(iCurrentEra+1)):
			if iEra in HISTORIANS[iCiv]:
				return HISTORIANS[iCiv][iEra]
		
		for iEra in range(iCurrentEra+1, iNumEras):
			if iEra in HISTORIANS[iCiv]:
				return HISTORIANS[iCiv][iEra]
		
		return tuple()
		
				
	def turnChecker(self, iTurnNum):

		# Check to see if this is a turn when the screen should pop up (every 50 turns)
		if (not CyGame().isNetworkMultiPlayer() and CyGame().getActivePlayer()>=0):
			if (iTurnNum % 50 == 0 and iTurnNum > 0 and gc.getPlayer(CyGame().getActivePlayer()).isAlive()):
				self.showScreen()

	#####################################################################################################################################
	      
	def handleInput( self, inputClass ):
		self.screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )		

		if ( inputClass.getFunctionName() == "Exit" and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.screen.hideScreen()
			return 1
		elif ( inputClass.getData() == int(InputTypes.KB_RETURN) ):
			self.screen.hideScreen()
			return 1
		return 0

	def update(self, fDelta):
		return
