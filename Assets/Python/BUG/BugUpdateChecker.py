## BugUpdateChecker
##
## Uses SvnUtil and BUG Core options to check for BUG updates and releases.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugCore
import BugUtil
import SvnUtil

CoreOpt = BugCore.game.Core

g_checkingForUpdates = False
g_checkPending = False
g_checkingThread = None
g_lastRemoteUrl = None

def onCheckForUpdatesChanged(option, value):
	scheduleSvnCheck()

def onLocalRootChanged(option, value):
	CoreOpt.LocalVersion.resetValue()

def onRepositoryUrlChanged(option, value):
	CoreOpt.RepositoryVersion.resetValue()

def scheduleSvnCheck():
	if (CoreOpt.isCheckForUpdates() 
	and CoreOpt.getRepositoryUrl() 
	and CoreOpt.getLocalRoot()):
		checkForSvnUpdates()

def checkForSvnUpdates():
	"""
	Uses the SVN options in the Core module to check for updates.
	"""
#	global g_checkingForUpdates, g_checkPending
#	if g_checkPending:
#		return
#	if g_checkingForUpdates:
#		g_checkPending = True
#		return
	if getRemoteVersion() > getLocalVersion():
		BugUtil.alert("SVN updates are available.")

def getLocalVersion():
	localRev = CoreOpt.getLocalVersion()
	if not localRev:
		root = CoreOpt.getLocalRoot()
		if root:
			localRev = SvnUtil.getLocalRevision(root)
			if not localRev:
				return 0
			CoreOpt.setLocalVersion(localRev)
	return localRev

def getRemoteVersion():
	remoteRev = CoreOpt.getRepositoryVersion()
	url = CoreOpt.getRepositoryUrl()
	if url:
		global g_lastRemoteUrl
		if not remoteRev or (url and url != g_lastRemoteUrl):
			g_lastRemoteUrl = url
			remoteRev = SvnUtil.getRemoteRevision(url)
			if not remoteRev:
				return 0
			CoreOpt.setRepositoryVersion(remoteRev)
	return remoteRev

#def _remoteRevisionCallback(result):
#	if isinstance(result, int):
#		
#	else:
#		global error
#		error = result.message
