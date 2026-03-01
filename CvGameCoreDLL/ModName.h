#pragma once
#ifndef MOD_NAME_H
#define MOD_NAME_H

/*	advc.106i: Small class for caching the mod's name and install location.
	(Could be expanded to also modify the name stored by the EXE; see the
	ModName class in the Taurus mod.) */

class ModName
{
public:
	/*	The first param (and our m_sFullPath) is for the result of
		CvDLLUtilityIFaceBase::getExternalModName with bFullPath=true,
		the second (our m_sPathInRoot) is the result for bFullPath=false.
		I'm always seeing the same result, namely a path relative to the
		folder containing the Mods folder (I'll refer to that folder as "root"):
		"Mods\AdvCiv\"
		I don't know that the bFullPath parameter will never matter, so
		it seems safer to store both strings. Maybe the full path could
		be longer than what I've seen, maybe the non-full path could be
		just the actual mod name. We will, in any case, extract the actual
		mod name into m_sName. */
	void update(char const* szFullPath, char const* szPathInRoot);
	char const* getFullPath() const { return m_sFullPath.c_str(); }
	char const* getPathInRoot() const { return m_sPathInRoot.c_str(); }
	char const* getName() const { return m_sName.c_str(); } // name of the AdvCiv folder
	
private:
	CvString m_sFullPath;
	CvString m_sPathInRoot;
	CvString m_sName;
};

#endif
