## BugCreditsOptionsTab
##
## Tab for the BUG Credits.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

import BugOptionsTab

credits = [ 
		"BUG_TEAM|BUG Team",
			"Alerum68 - Release, Documentation",
			"Cammagno - Documentation",
			"Dresden - Coding, Testing",
			"EmperorFool - Coding, Testing",
			"NikNaks - Graphics",
			"Ruff_Hi - Coding, Testing",
		"-",
		"TRANSLATORS|Translators",
			"Cammagno - Italian (Game and Documentation)",
			"Falc - French (Game)",
			"The Doc - German (Game and Documentation)",
		"-",
		"MOD_AUTHORS|Mod Authors",
			"12monkeys - Plot List Enhancements",
			"Alerum68 - Loading Hints & Tips, Sevopedia Strategy Guides",
			"Almightix - Better Espionage Screen",
			"asioasioasio - Wide City Bar",
			"Caesium - Score Delta, (extended Tech Window)",
			"Cammagno - Cammagno's CDA Pages",
			" -    (extended Autolog)",
			"Chinese American - Culture Turns, Great Person Turns",
			"codewarrior - Min/Max Commerce Buttons",
			"DanF5771 - Wonders in Info Screen",
			"daengle - (merged in full PLE)",
			"Del69 - Strategy Layer (idea by Eunomiac)",
			"Dr. Elmer Jiggle - Civ4lerts, CvCustomEventManager, CvPath",
			"Dresden - Improved EFA Info Page, Discoverable Favorite Civics with Random Personalities",
			" -    (extended Autolog, Reversible Power Ratio)",
			"Ekmek - Shortcuts in Civilopedia",
			"EmperorFool - Advanced Scoreboard, BUG Core and Utils, BULL, Great Person Tech Prefs,",
			" -    Military Advisor Deployment and Strategic Advantages, Power Ratio,",
			" -    Raw Yields, Sevopedia Traits, War/Peace/Enemy in EFA Glance, WhipAssist",
			" -    (extended BES, CDA, Civ4lerts, GP Progress Bar, PLE, Reminder, Sevopedia, Strategy Layer)",
			"Eotinb - Autolog, Reminder",
			"Fallblau - Modified Hall of Fame Screen",
			"fitchn - Civilopedia Index",
			"Gaurav - (extended Tech Window)",
			"HOF Team - AutoSave, MapFinder, MoreCiv4lerts",
			"Impaler[WrG] - Great Person Progress Bar",
			"Jeckel - All Eras Dawn of Man Screen",
			"johny smith - Scrolling Religion Advisor, Spy Specialist Civilopedia Fix",
			"NeverMind - Great General Progress Bar (was XP Counter)",
			"PieceOfMind - Advanced Combat Odds",
			"Porges - Attitude Icons",
			"Requies - Exotic Foreign Advisor",
			"ricardojahns - I Love Asphalt (wide screen EFA)",
			"Roamty - (extended Tech Window)",
			"Ruff_Hi - BUG Plot List, Unit Naming, BUG MA Sit-Rep tab, Smilies in EFA Glance tab, BUG Graphs",
			" -    City Specialists Chevons, BUG Religion Advisor, BUG Victory Screen Additions, Tick Marks",
			" -    (extended AutoLog, Reminder, Promo/Actions in PLE, Better Espionage Screen)",
			"Sevo - Raw Commerce, Sevopedia",
			"SimCutie - Attitudes in Scoreboard, City Cycle Arrows",
			"SirRethcir - Tech Window",
			"Sisiutil - Trait Civilopedia Text",
			"Stone-D - SD ToolKit",
			"Taelis - Customizable Domestic Advisor",
			"TheLopez - Dead Civ Scoreboard, Not Just Another Game Clock, Specialist Stacker",
			"turlute - (ported PLE to BtS)",
		"-",
		"MAP_SCRIPTS|Map Scripts",
			"Doug McCreary - SmartMap",
			"LDiCesare - Tectonics",
			"low - Random Map",
			"Nercury - Planet Generator",
			"Ruff_Hi - Ring World",
			"Sto - Full of Resources",
]

class BugCreditsOptionsTab(BugOptionsTab.BugOptionsTab):
	"BUG Credits Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "Credits", "Credits")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		labelNum = 0
		sepNum = 0
		boxNum = 0
		first = True
		for line in credits:
			if line == "-":
				pass
			else:
				pos = line.find(" - ")
				if pos == -1:
					# Header
					if not first:
						label = "CreditsSpacerLabel%d" % labelNum
						screen.attachLabel(column, label, " ")
						labelNum += 1
					else:
						first = False
					pos = line.find("|")
					if pos != -1:
						label = line[:pos]
						text = line[pos+1:]
						self.addLabel(screen, column, label, text)
					else:
						label = "CreditsHeaderLabel%d" % labelNum
						self.addLabel(screen, column, label, line)
					#screen.setLayoutFlag(label, "LAYOUT_CENTER")
					#screen.setLayoutFlag(label, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					labelNum += 1
					screen.attachHSeparator(column, column + "Sep%d" % sepNum)
					sepNum += 1
					box = "CreditsBox%d" % boxNum
					left, right = self.addTwoColumnLayout(screen, column, box)
					screen.setLayoutFlag(box + "HBox", "LAYOUT_CENTER")
					boxNum += 1
				else:
					# Person - Task
					leftLabel = "CreditsLabelLeft%d" % labelNum
					rightLabel = "CreditsLabelRight%d" % labelNum
					leftText = line[:pos] + "   "
					rightText = line[pos+3:]
					screen.attachLabel(left, leftLabel, leftText)
					screen.setLayoutFlag(leftLabel, "LAYOUT_RIGHT")
					#screen.setLayoutFlag(leftLabel, "LAYOUT_SIZE_HPREFERREDEXPANDING")
					screen.attachLabel(right, rightLabel, rightText)
					labelNum += 1
