# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvScreenUtilsInterface.py
#
# * This file stores the version of CvScreenUtils that is active
# * It is called from CvScreensInterface
# * When modding, this file should be replaced with one that has
#   screenUtils pointing to the mods <Mod>ScreenUtils
#
# No other modules should import this
#
#######################################
## Strategy Overlay Changed 10/20/2008
##
## Changed import to import CvOverlayScreenUtils
## Changed normalScreenUtils to return the CvOverlayScreenUtils class
## Placed in CustomAssets/Python/EntryPoints for bug mod use
##########################################

import CvOverlayScreenUtils

normalScreenUtils = CvOverlayScreenUtils.CvOverlayScreenUtils()

def getScreenUtils():
	return normalScreenUtils
