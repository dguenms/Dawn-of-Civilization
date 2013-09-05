## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvScreen - Base class for all of the Screens

from CvPythonExtensions import *
import CvUtil
import CvScreen

class CvPediaScreen( CvScreen.CvScreen ):
	"Civilopedia Base Screen"
	
	def getSortedList( self, numInfos, getInfo ):
		' returned a list of infos sorted alphabetically '
		infoList = [(0,0)] * numInfos
		for i in range( numInfos ):
			infoList[i] = (getInfo(i).getDescription(), i)
		#infoList.sort() #Rhye
		return infoList
	
