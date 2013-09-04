## SvnUtil
##
## Utilities for accessing an SVN repository and local repository.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugUtil
import os.path
import re
import threading
import time
import urllib

MINIMUM_ENTRIES_FORMAT = 7

MAX_READ_LINES = 30
REVISION_PATTERN = re.compile("Revision ([0-9]+):")

done = False
rev = None
error = None
def testL():
	print getLocalRevision("C:/Coding/Civ/BUG/BUG New Core")
def testR():
	print getRemoteRevision("http://civ4bug.svn.sourceforge.net/svnroot/civ4bug/BUG Mod/")
def testW():
	global done
	done = False
	def callback(result):
		done = True
		if isinstance(result, int):
			global rev
			rev = result
		else:
			global error
			error = result.message
	t = getRemoteRevision("http://civ4bug.svn.sourceforge.net/svnroot/civ4bug/BUG Mod/",
			callback)
	count = 0
	while not t.done() and count < 100:
		time.sleep(0.05)
		count += 1
	print t.rev()

def getLocalRevision(path):
	"""
	Parses and returns the revision number from a local SVN working copy.
	
	It is read from the 'entries' file as long as the file has format 7 or higher.
	A BugError exception is raised if the file isn't found or it has an incorrect
	format or revision number format.
	
	Based on 
	  http://svn.collab.net/repos/svn/trunk/tools/client-side/change-svn-wc-format.py
	
	See http://svn.collab.net/repos/svn/trunk/subversion/libsvn_wc/README
	'The entries file' for a description of the entries file format.
	
	In summary, the first line is the format number followed by an entry for
	the directory itself (no name). Each entry is separated by a form feed 0x0c
	and a line feed 0x0a, and each entry contains lines terminated by 0x0a.
	Subsequent empty lines at the end of an entry may be omitted.
	
	The first few lines of each entry that we care about are
	
	  - name		  empty for first entry (a.k.a. this_dir)
	  - kind		  file or dir
	  - revision	  0 for entries not yet in repository
	  - url
	  - repository
	"""
	path = os.path.join(path, ".svn", "entries")
	try:
		BugUtil.debug("SvnUtil.getLocalRevision - opening '%s'", path)
		input = open(path, "r")
		try:
			# Read and discard WC format number from INPUT.  Validate that it
			# is a supported format for conversion.
			format_line = input.readline().strip()
			BugUtil.debug("SvnUtil.getLocalRevision - format '%s'", format_line)
			try:
				format_nbr = int(format_line)
			except ValueError:
				raise BugUtil.BugError("invalid SVN entries file format '%s'" % format_line)
			if not format_nbr >= MINIMUM_ENTRIES_FORMAT:
				raise BugUtil.BugError("SVN entries file format %d too old" % format_nbr)
			
			# Verify first entry's name and kind.
			name = input.readline().strip()
			if name != "":
				BugUtil.warn("SvnUtil.getLocalRevision - first SVN entry has name '%s'", name)
			kind = input.readline().strip()
			if kind != "dir":
				BugUtil.warn("SvnUtil.getLocalRevision - first SVN is not a dir, kind '%s'", kind)
			
			# Extract the revision number for the first entry.
			rev_line = input.readline().strip()
			BugUtil.debug("SvnUtil.getLocalRevision - revision '%s'", rev_line)
			try:
				rev = int(rev_line)
			except ValueError:
				raise BugUtil.BugError("invalid SVN revision number format '%s'" % rev_line)
			
			return rev
		finally:
			input.close()
	except IOError, e:
		raise BugUtil.BugError("failed to read SVN entries file")

def getRemoteRevision(url, callback=None):
	"""
	Retrieves the latest revision for a remote repository directory.
	
	If callback is given, a background thread is used and the callback is called
	after the revision is retrieved or an error occurs. If the operation is successful,
	the revision number (an int) is passed to the callback; otherwise the exception
	caught is passed.
	"""
	if callback is None:
		return _getRemoteRevision(url)
	else:
		t = RemoteRevisionThread(url, callback)
		t.start()
		return t

class RemoteRevisionThread(threading.Thread):
	def __init__(self, url, callback=None):
		super(RemoteRevisionThread, self).__init__()
		self._url = url
		self._callback = callback
		self._error = None
		self._rev = None
		self._done = False
	def run(self):
		try:
			self._rev = _getRemoteRevision(self._url)
			BugUtil.debug("RemoteRevisionThread.run - found revision %d", self._rev)
		except BugError, e:
			self._error = e
			BugUtil.debug("RemoteRevisionThread.run - %s", self._error.message)
		self._done = True
		self.callback()
	def done(self):
		return self._done
	def succeeded(self):
		return self._done and self._rev is not None
	def failed(self):
		return self._done and self._error is not None
	def rev(self):
		return self._rev
	def error(self):
		return self._error
	def callback(self):
		if self.succeeded():
			self._callback(self._rev)
		else:
			self._callback(self._error)

def _getRemoteRevision(url):
	"""
	Parses and returns the revision number from a remote SVN repository.
	
	The URL must be correctly escaped (+ for space, etc).
	A BugError exception is raised if the URL can't be connected to or it doesn't
	have the expected format.
	
	This function looks specifically for the string 'Revision: ####' anywhere
	in the first MAX_READ_LINES
	"""
	try:
		timer = BugUtil.Timer("SvnUtil.getRevision")
		try:
			BugUtil.debug("SvnUtil.getRevision - opening '%s'", url)
			web = urllib.urlopen(urllib.quote(url, "/:"))
			count = 0
			try:
				for line in web:
					result = REVISION_PATTERN.search(line)
					if result:
						BugUtil.debug("SvnUtil.getRevision - found '%s'", result.group())
						try:
							return int(result.group(1))
						except ValueError:
							raise BugUtil.BugError("invalid SVN revision format '%s'" 
									% result.group(1))
					count += 1
					if count > MAX_READ_LINES:
						return None
			finally:
				web.close()
		except IOError, e:
			raise BugUtil.BugError("failed to access SVN repository: %s" % str(e))
		return None
	finally:
		timer.log()
