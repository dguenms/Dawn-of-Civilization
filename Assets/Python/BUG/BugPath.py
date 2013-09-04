## BugPath
##
## Locates all of the necessary directories to provide access to data and asset files.
##
## It exposes several useful variables. Those ending in "Dir" are full paths to directories
## while those ending in "Folder" or "Name" are the base name of the file/folder.
## All directory functions return valid directories or the Python None value if not found.
##
## isMac()
##   Returns True if running on a Mac operating system.
##
## isMod()
##   Returns True if running as a mod, False otherwise.
##
## isNoCustomAssets()
##   Returns True if the NoCustomAssets setting is 1 in the mod's INI file, 
##   False if 0 or when not running as a mod.
##
## getModName()
##   Returns CvModName.modName
##
## getModDir(), getModFolder()
##   Directory of the loaded mod, or None if no mod is loaded.
##
## getUserDir()
##   The "My Documents\My Games" directory on Windows or the "Documents"
##   directory on MacOS X. Both are in the user's private documents area.
##   If it cannot be found, it will be the directory containing <root-dir>.
##
## getRootDir()
##   Directory containing the CivilizationIV.ini file.
##   If it cannot be found, will look in <user-dir> for a folder named <app-folder>
##   Use the CvAltRoot module to override the location found by this module.
##
## getAppDir(), getAppFolder()
##   Directory containing the BTS application (CIV4BeyondSword.exe on Windows).
##   This should be "Beyond the Sword" for most installations.
##
## getDataDir()
##   Directory containing the mod's data files: user settings, help files, etc.
##   This is the first folder containing a folder with a name matching the value of
##   SETTINGS_FOLDER ("UserSettings" by default).
##
##     Search order:
##
##       <user-dir>\<mod-name>      C:\Users\<user>\Documents\BUG Mod
##       <root-dir>\<mod-name>      C:\Users\<user>\Documents\Beyond the Sword\BUG Mod
##       <app-dir>\<mod-name>       C:\Programs\Sid Meier's Civilization IV\Beyond the Sword\BUG Mod
##       <mod-dir>\<data-folder>    C:\Programs\Sid Meier's Civilization IV\Beyond the Sword\Mods\BUG Mod x.x\Data
##       <mod-dir>                  C:\Programs\Sid Meier's Civilization IV\Beyond the Sword\Mods\BUG Mod x.x
##
## getSettingsDir()
##   Directory containing the mod's user settings.
##
## getInfoDir()
##   Directory containing the mod's informational files such as the readme and help files.
##
## TODO
##
##   Add override for dataDir.
##   Add some other setting instead of modName for dataDir search.
##
## Based on CvPath by Dr. Elmer Jiggles.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *
import os
import os.path
import sys
import BugConfigTracker
import BugUtil


## Constants

DATA_FOLDER = "Data"
SETTINGS_FOLDER = "UserSettings"
INFO_FOLDER = "Info"

MODS_FOLDER = "Mods"
ASSETS_FOLDER = "Assets"
CUSTOM_ASSETS_FOLDER = "CustomAssets"

MY_DOCUMENTS_FOLDER_REG_KEYS = (
	("XP", r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders", "Personal"),
	("Vista", r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders", "Personal"),
)
MY_GAMES_FOLDER = "My Games"


def isMac():
	"""
	Returns True if running on a Mac operating system.
	"""
	return sys.platform == 'darwin'


## Mod Info, Folder and Path Accessors

def getModName():
	"""
	Returns the name of the mod as specified in CvModName.
	
	See the file "Assets/Python/Contrib/CvModName.py" for more information.
	"""
	initModName()
	return _modName

def isMod():
	"""
	Returns True if running as a mod, False otherwise.
	"""
	initModFolder()
	return _isMod

def isNoCustomAssets():
	"""
	Returns True if the NoCustomAssets setting is 1 in the mod's INI file, 
	False if 0 or when not running as a mod.
	"""
	initNoCustomAssetsSetting()
	return _noCustomAssets

def getModDir():
	"""
	Returns the full path of the mod directory if running as a mod.
	
	Can be overridden using a CvModFolder module, but this shouldn't be necessary
	as the folder's name is acquired from BTS itself.
	"""
	initModFolder()
	return _modDir

def getModFolder():
	"""
	Returns the name of the mod directory if running as a mod.
	"""
	initModFolder()
	return _modFolder

def getUserDir():
	"""
	Returns the full path of the user's Documents/My Games directory.
	
	See the file "Info/CvAltRoot.py" for more information.
	"""
	initRootFolder()
	return _userDir

def getRootDir():
	"""
	Returns the full path of the directory containing the file "CivilizationIV.ini".
	
	See the file "Info/CvAltRoot.py" for more information.
	"""
	initRootFolder()
	return _rootDir

def getDataDir():
	"""
	Returns the full path of the directory containing the mod's data files: user settings, help files, etc.
	"""
	initDataFolder()
	return _dataDir

def getSettingsDir():
	"""
	Returns the full path of the directory containing the mod's user settings.
	"""
	initDataFolder()
	return _settingsDir

def getInfoDir():
	"""
	Returns the full path of the directory containing the mod's informational files: readme, help files, etc.
	"""
	initDataFolder()
	return _infoDir

def getAppDir():
	"""
	Returns the full path of the directory containing the "Civ4BeyondSword.exe" application.
	"""
	initAppFolder()
	return _appDir

def getAppFolder():
	"""
	Returns the name of the directory containing the "Civ4BeyondSword.exe" application.
	"""
	initAppFolder()
	return _appFolder


## Finding and Creating Files and Directories

def findAssetFile(name, subdir=None):
	"""
	Returns the full path to the named asset file by searching the paths above.
	"""
	initSearchPaths()
	for dir in _assetFileSearchPaths:
		path = getFilePath(dir, name, subdir)
		if path:
			return path
	if subdir:
		BugUtil.warn("BugPath - cannot find asset file %s in %s", name, subdir)
	else:
		BugUtil.warn("BugPath - cannot find asset file %s", name)
	return None

def findDataFile(name, subdir=None):
	"""
	Returns the full path to the named data file.
	"""
	return getFilePath(getDataDir(), name, subdir)

def findSettingsFile(name, subdir=None):
	"""
	Locates and returns the path to the named configuration file or None if not found.
	"""
	return getFilePath(getSettingsDir(), name, subdir)

def findIniFile(name, subdir=None):
	"""
	Locates and returns the path to the named configuration file or None if not found.
	
	Deprecated: Use findSettingsFile() instead.
	"""
	return findSettingsFile(name, subdir)

def findMainModIniFile():
	"""
	Locates and returns the path to the configuration file named for the mod or None if not found.
	"""
	if getModName():
		return findSettingsFile(getModName() + ".ini")
	BugUtil.warn("BugPath - mod name not set")
	return None

def findInfoFile(name, subdir=None):
	"""
	Locates and returns the path to the named informational file or None if not found.
	"""
	return getFilePath(getInfoDir(), name, subdir)


def createDataFile(name, subdir=None):
	"""
	Returns the path to the named data file.
	"""
	return createFile(getDataDir(), name, subdir)

def createSettingsFile(name, subdir=None):
	"""
	Returns the path to the named configuration file.
	"""
	return createFile(getSettingsDir(), name, subdir)

def createIniFile(name, subdir=None):
	"""
	Returns the path to the named configuration file.
	
	Deprecated: Use createSettingsFile() instead.
	"""
	return createSettingsFile(name, subdir)

def createInfoFile(name, subdir=None):
	"""
	Returns the path to the named informational file.
	"""
	return createFile(getInfoDir(), name, subdir)


def findDir(name):
	"""
	Locates the named directory in dataDir.
	"""
	path = join(getDataDir(), name)
	if isdir(path):
		return path
	return None

def makeDir(name):
	"""
	Creates a new directory in the dataDir folder.
	"""
	path = join(getDataDir(), name)
	if path and not isdir(path):
		try:
			safeInfoPath("BugPath - creating '%s'", path)
			os.makedirs(path)
			return path
		except IOError:
			BugUtil.trace("Cannot create directory '%s' in '%s", name, getDataDir())
	return path

def findOrMakeDir(name):
	"""
	Locates or creates the specified directory and returns the path to it.
	"""
	return findDir(name) or makeDir(name)


## Initialization

def init():
	"""
	Initializes the entire module.
	"""
	BugUtil.debug("BugPath - initializing...")
	initAppFolder()
	initModName()
	initModFolder()
	initNoCustomAssetsSetting()
	initRootFolder()
	initDataFolder()
	initSearchPaths()


## Application Directory

_appDir = None
_appFolder = "Beyond the Sword"
_appFolderInitDone = False
def initAppFolder():
	"""
	Locates the directory that contains the BTS application.
	"""
	global _appFolderInitDone
	if _appFolderInitDone:
		return
	BugUtil.debug("BugPath - initializing application folder")
	global _appDir, _appFolder
	
	# Determine the app directory that holds the executable and Mods
	# as well as the folder name inside MY_GAMES_FOLDER that holds CustomAssets and Mods.
	if isMac():
		_appDir = os.getcwd()
	else:
		if isfile(sys.executable):
			#BugUtil.debug("BugPath - exe is '%s'", sys.executable)
			_appDir = dirname(sys.executable)
	if _appDir:
		_appFolder = basename(_appDir)
		safeInfoPath("BugPath - app dir is '%s'", _appDir)
		safeDebugPath("BugPath - app folder is '%s'", _appFolder)
	else:
		BugUtil.warn("BugPath - no executable found")
	_appFolderInitDone = True


## Mod Display Name

_modName = None
_modNameInitDone = False
def initModName():
	"""
	Pulls the modName attribute from the CvModName module.
	"""
	global _modNameInitDone
	if _modNameInitDone:
		return
	global _modName
	try:
		import CvModName
		_modName = CvModName.modName
		safeInfoPath("BugPath - mod name is '%s'", _modName)
	except ImportError:
		BugUtil.error("CvModName.py module not present")
	except AttributeError:
		BugUtil.error("CvModName.py module has no modName setting")
	_modNameInitDone = True

	
## Mod Directory

_isMod = False
_modDir = None
_modFolder = None
_modFolderInitDone = False
def initModFolder():
	"""
	Checks if BUG is running as a mod and sets the folder and name if so.
	"""
	global _modFolderInitDone
	if _modFolderInitDone:
		return
	if not CyGame().isFinalInitialized():
		BugUtil.debug("BugInit - game not fully initialized")
		return
	BugUtil.debug("BugPath - initializing mod folder")
	global _modDir, _modFolder
	try:
		replay = CyReplayInfo()
		replay.createInfo(0)
		modDir = replay.getModName().replace('\\', r'/')
	except:
		BugUtil.trace("replay not ready")
	else:
		if modDir and len(modDir) > 2:
			if not setModDir(abspath(modDir)):
				BugUtil.error("Replay provided invalid mod directory")
	if not _modDir:
		BugUtil.debug("BugPath - checking CvModFolder")
		try:
			import CvModFolder
			modFolder = CvModFolder.modFolder
		except ImportError:
			BugUtil.debug("BugPath - CvModFolder module not present")
		except AttributeError:
			BugUtil.error("CvModFolder.py module has no modFolder setting")
		else:
			if not setModDir(join(getRootDir(), MODS_FOLDER, modFolder)):
				if not setModDir(join(getAppDir(), MODS_FOLDER, modFolder)):
					BugUtil.error("Cannot find mod folder using '%s' from CvModFolder.py", modFolder)
	if not _modFolder:
		BugUtil.debug("BugPath - no mod directory found")
	_modFolderInitDone = True

def setModDir(dir):
	safeDebugPath("BugPath - checking mod dir '%s'", dir)
	if isdir(dir):
		global _isMod, _modDir, _modFolder
		_isMod = True
		_modDir = dir
		_modFolder = basename(dir)
		safeInfoPath("BugPath - mod dir is '%s'", dir)
		safeDebugPath("BugPath - mod folder is '%s'", _modFolder)
		BugConfigTracker.add("Mod_Directory", _modDir)
		return True
	return False


## NoCustomAssets Setting

_noCustomAssets = False
_noCustomAssetsSettingInitDone = False
def initNoCustomAssetsSetting():
	"""
	Checks if the NoCustomAssets setting is enabled when running as a mod.
	"""
	global _noCustomAssetsSettingInitDone
	if _noCustomAssetsSettingInitDone:
		return
	if isMod():
		global _noCustomAssets
# EF: don't check game option because BUG is initialized only once at startup
#		if CyGame().isOption(GameOptionTypes.GAMEOPTION_LOCK_MODS):
#			_noCustomAssets = True
#			BugUtil.debug("BugPath - Lock Modified Assets is set")
#		else:
		if getModDir() and getModFolder():
			BugUtil.debug("BugPath - checking for NoCustomAssets")
			try:
				from configobj import ConfigObj
				config = ConfigObj(join(getModDir(), getModFolder() + ".ini"), encoding='utf_8')
				_noCustomAssets = config["CONFIG"].as_bool("NoCustomAssets")
			except:
				BugUtil.trace("BugPath - failed to parse mod INI file for NoCustomAssets")
		BugUtil.info("BugPath - NoCustomAssets is %s", _noCustomAssets)
	_noCustomAssetsSettingInitDone = True


## User and Root Directories

_userDir = None
_rootDir = None
_rootFolderInitDone = False
def initRootFolder():
	"""
	Finds the directory that contains the CivilizationIV.ini file and the user's documents directory.
	"""
	global _rootFolderInitDone
	if _rootFolderInitDone:
		return
	BugUtil.debug("BugPath - initializing system folders")
	global _rootDir, _userDir
	
	# override root dir from CvAltRoot
	try:
		import CvAltRoot
		altRootDir = CvAltRoot.rootDir
		if not setRootDir(altRootDir):
			BugUtil.error("Directory from CvAltRoot.py is not valid or does not contain CivilizationIV.ini")
	except ImportError:
		BugUtil.debug("BugPath - CvAltRoot module not present")
	except AttributeError:
		BugUtil.error("CvAltRoot.py module has no rootDir setting")
	except IOError, (errno, strerror):
		BugUtil.trace("Error accessing directory from CvAltRoot.py: [%d] %s", errno, strerror)
	
	# user dir
	if isMac():
		# Mac OS X
		if not setUserDir(join(os.environ['HOME'], "Documents")):
			BugUtil.warn("Cannot find user's Documents folder")
	else:
		# Windows
		import _winreg
		def getRegValue(root, subkey, name):
			key = _winreg.OpenKey(root, subkey)
			try:
				value = _winreg.QueryValueEx(key, name)
				return value[0]
			finally:
				key.Close()
		
		for version, key, subkey in MY_DOCUMENTS_FOLDER_REG_KEYS:
			try:
				myDocuments = getRegValue(_winreg.HKEY_CURRENT_USER, key, subkey)
			except:
				pass
			else:
				if setUserDir(join(myDocuments, MY_GAMES_FOLDER)):
					safeInfoPath("BugPath - found valid Windows %s My Documents folder registry key", version)
					break
		else:
			BugUtil.debug("BugPath - no valid My Documents registry key")
	
	# try to determine missing dir from other dir
	if not _rootDir:
		if _userDir:
			if isMac():
				setRootDir(join(_userDir, "Civilization IV " + getAppFolder()))
			else:
				setRootDir(join(_userDir, getAppFolder()))
	else:
		if not _userDir:
			setUserDir(dirname(_rootDir))
	# if neither is found, fail
	if not _rootDir:
		BugUtil.error("Cannot find CivilizationIV.ini; see %s/CvAltRoot.py for instructions", INFO_FOLDER)
	_rootFolderInitDone = True

def setRootDir(dir):
	safeDebugPath("BugPath - Checking root dir '%s'", dir)
	if isdir(dir) and isfile(join(dir, "CivilizationIV.ini")):
		global _rootDir
		_rootDir = dir
		safeInfoPath("BugPath - root dir is '%s'", dir)
		BugConfigTracker.add("Root_Directory", _rootDir)
		return True
	return False

def setUserDir(dir):
	safeDebugPath("BugPath - Checking user dir '%s'", dir)
	if isdir(dir):
		global _userDir
		_userDir = dir
		safeInfoPath("BugPath - user dir is '%s'", dir)
		return True
	return False


## Data Directory

_dataDir = None
_settingsDir = None
_infoDir = None
_dataFolderInitDone = False
def initDataFolder():
	"""
	Finds the first directory that contains a folder named SETTINGS_FOLDER.
	"""
	global _dataFolderInitDone
	if _dataFolderInitDone:
		return
	BugUtil.debug("BugPath - initializing data folder")
	
	dataDirs = (
		join(getUserDir(), getModName()),	# My Games\BUG Mod
		join(getRootDir(), getModName()),	# My Games\BTS\BUG Mod
		join(getAppDir(), getModName()),	 # Civ4\BTS\BUG Mod
		join(getModDir(), DATA_FOLDER),	  # Civ4\BTS\Mods\BUG Mod 3.6\Data
		join(getModDir()),				   # Civ4\BTS\Mods\BUG Mod 3.6
	)
	for dir in dataDirs:
		if setDataDir(dir):
			break
	else:
		BugUtil.error("No valid data directory containing %s found", SETTINGS_FOLDER)
	_dataFolderInitDone = True

def setDataDir(dir):
	if isdir(dir):
		safeDebugPath("BugPath - Checking data dir '%s'", dir)
		settingsDir = join(dir, SETTINGS_FOLDER)
		if isdir(settingsDir):
			safeInfoPath("BugPath - data dir is '%s'", dir)
			global _dataDir, _settingsDir, _infoDir
			_dataDir = dir
			_settingsDir = settingsDir
			_infoDir = join(dir, INFO_FOLDER)
			BugConfigTracker.add("Settings_Directory", _settingsDir)
			return True
	return False


## Asset Directories

_assetFileSearchPaths = []
_searchPathsInitDone = False
def initSearchPaths():
	"""
	Adds the CustomAssets, mod Assets and BTS Assets directories to a list of search paths.
	"""
	global _searchPathsInitDone
	if _searchPathsInitDone:
		return
	BugUtil.debug("BugPath - initializing asset search paths")
	
	assetDirs = [
		join(getModDir(), ASSETS_FOLDER),
		join(getAppDir(), ASSETS_FOLDER),
	]
	# EF: Mod's no longer access CustomAssets folder; too many issues
	if not isNoCustomAssets() and not isMod():
		assetDirs.insert(0, join(getRootDir(), CUSTOM_ASSETS_FOLDER))
	for dir in assetDirs:
		addAssetFileSearchPath(dir)
	
	if _assetFileSearchPaths:
		BugConfigTracker.add("Asset_Search_Paths", _assetFileSearchPaths)
	else:
		BugUtil.error("No asset directories found")
	_searchPathsInitDone = True

def addAssetFileSearchPath(path):
	"""
	Adds the given path to the search list if it is a directory.
	"""
	if isdir(path):
		_assetFileSearchPaths.append(path)


## None-Safe Path/Directory/File Functions

def getFilePath(root, name, subdir=None):
	"""
	Returns the full path to the named file, or None if it doesn't exist.
	"""
	if not root:
		BugUtil.warn("Invalid root directory looking for '%s'", name)
	if subdir:
		path = join(root, subdir, name)
	else:
		path = join(root, name)
	if isfile(path):
		return path
	safeDebugPath("BugPath - not a file: '%s'", path)
	return None

def createFile(root, name, subdir=None):
	"""
	Returns the path to a new file to be created.
	"""
	if subdir:
		return join(root, subdir, name)
	else:
		return join(root, name)

def join(*paths):
	for path in paths:
		if path is None:
			return None
	return os.path.join(*paths)

def dirname(path):
	if path is None:
		return None
	return os.path.dirname(path)

def basename(path):
	if path is None:
		return None
	return os.path.basename(path)

def abspath(path):
	if path is None:
		return None
	return os.path.abspath(path)

def isdir(path):
	if path is None:
		return False
	return os.path.isdir(path)

def isfile(path):
	if path is None:
		return False
	return os.path.isfile(path)


## Non-English-Safe Logging

def safeDebugPath(message, path):
	try:
		BugUtil.debug(message, path)
	except:
		pass

def safeInfoPath(message, path):
	try:
		BugUtil.info(message, path)
	except:
		pass
