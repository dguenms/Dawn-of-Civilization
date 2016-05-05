## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import PyHelpers
import CvUtil
import ScreenInput
import CvScreenEnums
import string

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvEraMovieScreen:
	"Wonder Movie Screen"
	def interfaceScreen (self, iEra):
	
		mainScreen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		self.W_SCREEN = 775
		self.H_SCREEN = 660
		
		self.X_SCREEN = (mainScreen.getXResolution() - self.W_SCREEN) / 2 #100
		self.Y_SCREEN = (mainScreen.getYResolution() - self.H_SCREEN) / 2 #40
		
		self.Y_TITLE = self.Y_SCREEN + 20
		
		self.X_EXIT = self.X_SCREEN + self.W_SCREEN/2 - 50
		self.Y_EXIT = self.Y_SCREEN + self.H_SCREEN - 50
		self.W_EXIT = 120
		self.H_EXIT = 30
		
		if (CyInterface().noTechSplash()):
			return 0
				
		player = PyPlayer(CyGame().getActivePlayer())
			
		screen = CyGInterfaceScreen( "EraMovieScreen" + str(iEra), CvScreenEnums.ERA_MOVIE_SCREEN)
		screen.addPanel("EraMoviePanel", "", "", true, true,
			self.X_SCREEN, self.Y_SCREEN, self.W_SCREEN, self.H_SCREEN, PanelStyles.PANEL_STYLE_MAIN)
		
		screen.showWindowBackground(True)
		screen.setRenderInterfaceOnly(False);
		screen.setSound("AS2D_NEW_ERA")
		screen.showScreen(PopupStates.POPUPSTATE_MINIMIZED, False)
		
		# Header...
		szHeader = localText.getText("TXT_KEY_ERA_SPLASH_SCREEN", (gc.getEraInfo(iEra).getTextKey(), ))
		szHeaderId = "EraTitleHeader" + str(iEra)
		screen.setText(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY,
			       self.X_SCREEN + self.W_SCREEN / 2, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setButtonGFC("EraExit" + str(iEra), localText.getText("TXT_KEY_MAIN_MENU_OK", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		# Play the movie
		if iEra == 1:
			szMovie = "Art/Movies/Era/Era01-Classical.dds"
		elif iEra == 2:
			szMovie = "Art/Movies/Era/Era02-Medeival.dds"
		elif iEra == 3:
			szMovie = "Art/Movies/Era/Era03-Renaissance.dds"
		elif iEra == 4:
			szMovie = "Art/Movies/Era/Era04-Industrial.dds"
		else:
			szMovie = "Art/Movies/Era/Era05-Modern.dds"

		screen.addDDSGFC("EraMovieMovie" + str(iEra), szMovie, self.X_SCREEN + 27, self.Y_SCREEN + 50, 720, 540, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				
		return 0
		
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0

	def update(self, fDelta):
		return

