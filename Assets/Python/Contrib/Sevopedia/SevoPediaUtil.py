## SevoPediaUtil
##
## Creates unsaved options for Sevopedia when it's accessed before BUG initializes.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import BugCore
import BugOptions
import BugUtil

AdvisorOpt = BugCore.game.Advisors
enabledOption = None
sortOption = None

if not AdvisorOpt._hasOption("Sevopedia"):
	BugUtil.debug("BUG: creating stub Sevopedia option")
	enabledOption = BugOptions.UnsavedOption(AdvisorOpt, BugOptions.qualify(AdvisorOpt._getID(), "Sevopedia"), "boolean", True)
	AdvisorOpt._addOption(enabledOption)

if not AdvisorOpt._hasOption("SevopediaSortItemList"):
	BugUtil.debug("BUG: creating stub Sevopedia Sort option")
	sortOption = BugOptions.UnsavedOption(AdvisorOpt, BugOptions.qualify(AdvisorOpt._getID(), "SevopediaSortItemList"), "boolean", True)
	AdvisorOpt._addOption(sortOption)
