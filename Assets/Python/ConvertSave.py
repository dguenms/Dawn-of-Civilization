from StoredData import sd

from CvPythonExtensions import *
import RFCUtils
utils = RFCUtils.RFCUtils()

sd.scriptDict['lTimedConquests'] = []

sText = "Saved data updated to v1.13.2"
print sText
CyInterface().addMessage(utils.getHumanID(), True, 14, sText, "", 0, "", ColorTypes(0), -1, -1, True, True)
