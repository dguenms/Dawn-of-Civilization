#### Civilization 4 SDK Makefile 2.5 ####
####  Copyright 2015 Nightinggale    ####
# (advc: with some modifications; see below)
#########################################
#### Civilization 4 SDK Makefile 2.0 ####
####  Copyright 2013 Nightinggale    ####
#########################################
#### Civilization 4 SDK Makefile 1.0 ####
####  Copyright 2010 Danny Daemonic  ####
#########################################

# advc (2019/2020):
# Enabled parallel builds (jom) for the Profile configuration
#   (now called "Profile-fast") and added a configuration Debug-fast. Both use
#   precompiled headers through the Z7 option as recommended by billw2015.
# Target 'Debug-opt' added: An almost-Release build that is less likely than a
#   Debug build to obscure accesses to uninitialized memory. Also for inspecting
#   optimized assembly.
# Removed the non-fast Assert configuration. [Parallel builds can make it
#   difficult to associate error messages with a translation unit; but don't need
#   a slow version of every config.]
# YOURMOD2 and YOURLOGS (see under "Paths").
# /Z option for debug builds obtained from Makefile.project, the default being /Z7.
#   To make it easier to switch, temporarily, to /Zd, which links much faster.
# PROJECT_Profile_CFLAGS, PROJECT_Debug_CFLAGS, PROJECT_DebugOpt_CFLAGS added to Makefile.project.
# For selecting a profiler and for balancing speed vs. fidelity of debug builds.
# Removed unused /DCVGAMECOREDLL_EXPORTS
# devolution (Erik) has added the target 'Final_Release' with
#   whole-program optimization. [To avoid confusion, I've removed the Firaxis flag
#   "FINAL_RELEASE", which had merely disabled the OutputDebugString function from
#   debugapi.h in release builds; do that based on _DEBUG instead.]
# CvGameCoreDLL.rc used only for final release.
# Use /arch:SSE2 for all release builds. Removed some redundant release-build flags.
# /W3 moved into PROJECT_CFLAGS.

## User setup
##
## Any setting here can be overwritten by assigning a new value to the variables in Makefile.user
##  Makefile.user is made automatically if it is missing whenever the project is build or cleaned
##
## Not touching the makefile itself can be beneficial if the makefile is committed to svn/git
## Makefile.user can also accept CUSTOM_CFLAGS and CUSTOM_LDFLAGS if you want to ADD additional flags
##   the custom flags will not overwrite any flags the makefile sets itself
##   An example could be you want to define ENABLE_MY_DEBUG_OUTPUT in C++, then you write
##     CUSTOM_CFLAGS -DENABLE_MY_DEBUG_OUTPUT
##     in Makefile.user and it will be defined for you without the risk of committing active debug output to other people
##
##     You can write whatever you want after -D and it will work like you write #DEFINE in C++
## 


#### Paths ####
# Note: Edit Makefile.user instead and add it to .gitignore
# Note: $(PROGRAMFILES) converts to "C:\Program Files", "C:\Program Files (x86)" or whatever fits your system.
# run "nmake.exe /P" in cmd.exe to see what it is on your system
#
#TOOLKIT=$(PROGRAMFILES)\Microsoft Visual C++ Toolkit 2003
#PSDK=$(PROGRAMFILES)\Microsoft SDKs\Windows\v7.0A
#
## Civ install path
## Path to the directory where boost and python is stored
## Overwritten by enviroment variable CIV4_LIB_INSTALL_PATH
#CIV4_PATH=$(PROGRAMFILES)\Sid Meier's Civilization 4\Beyond the Sword
#CIV4_PATH=$(PROGRAMFILES)\2K Games\Firaxis Games\Sid Meier's Civilization IV Colonization\CvGameCoreDLL
#
## Optional:
# To have newly compiled dlls copied to your mod's Assets directory
#YOURMOD=..
# When the same DLL is used for a second mod
#YOURMOD2=$(PROGRAMFILES)\Sid Meier's Civilization 4\Beyond the Sword\Mods\ModName
# To have logs deleted after compilation
# Warning: Make double sure to set the right path and not to move any valuable file
# with .log extension there. Or better don't use it at all.
#YOURLOGS=C:\Users\Administrator\Documents\My Games\Beyond the Sword\Logs

#### Tools ####
CC="$(TOOLKIT)\bin\cl.exe"
CPP="$(TOOLKIT)\bin\cl.exe"
LD="$(TOOLKIT)\bin\link.exe"
RC="$(PSDK)\bin\rc.exe"
## Uncomment to build dependencies using fastdep
## Overwritten by enviroment variable FASTDEP_FULL_PATH
FD="bin\fastdep.exe"

#### BLACKLIST ####
## Uncomment to block CvTextScreen (accidentally included by Firaxis)
# BLACKLIST=CvTextScreens

#### DEFINES ####
Debug_DEFINES=/DWIN32 /D_WINDOWS /D_USRDLL /D_DEBUG
Release_DEFINES=/DWIN32 /D_WINDOWS /D_USRDLL /DNDEBUG
## Optional: Copy the flags above into "Additional options" in NMAKE properties (Configuration Properties)
## to make VC++ aware of what is defined and what isn't, which affects the help popup and red lines.
## Use the Release_DEFINES for all targets except debug. Assert adds /DFASSERT_ENABLE,
## which should be added to additional options too, if you care; however you will
## only be able to tell a difference if you do something with asserts other than FAssert() or FAssertMsg().

#### You shouldn't need to modify anything beyond this point ####
#################################################################

TEMP_FILE_DIR = temp_files
CUSTOM_CFLAGS  =
CUSTOM_LDFLAGS =



!IF [IF NOT EXIST Makefile.user EXIT 1] != 0
!IF [ECHO CUSTOM_CFLAGS = > Makefile.user]
!ENDIF
!ENDIF
!include Makefile.user

PRECOMPILE_DEPENDENCIES =
PROJECT_CFLAGS =
PROJECT_Debug_CFLAGS =
PROJECT_DebugOpt_CFLAGS =
PROJECT_Profile_CFLAGS =
PROJECT_LDFLAGS =
SOURCE_DIR =

SUBDIRPATH1 = ../
SUBDIRPATH2 = ../
SUBDIRPATH3 = ../
SUBDIRPATH4 = ../
SUBDIRPATH5 = ../
SUBDIRPATH6 = ../
SUBDIRPATH7 = ../
SUBDIRPATH8 = ../
SUBDIRPATH9 = ../
SUBDIRPATH10 = ../
SUBDIRPATH11 = ../
SUBDIRPATH12 = ../
SUBDIRPATH13 = ../
SUBDIRPATH14 = ../
SUBDIRPATH15 = ../

!IF [IF NOT EXIST Makefile.project EXIT 1] != 0
!IF [ECHO SOURCE_DIR = .>> Makefile.project]
!ENDIF
!IF [ECHO PROJECT_CFLAGS = /W3 >> Makefile.project]
!ENDIF
!IF [ECHO PROJECT_LDFLAGS = >> Makefile.project]
!ENDIF
!IF [ECHO PROJECT_Profile_CFLAGS = >> Makefile.project]
!ENDIF
!IF [ECHO PROJECT_Debug_CFLAGS = /Z7 >> Makefile.project]
!ENDIF
!IF [ECHO PROJECT_DebugOpt_CFLAGS = /Z7 >> Makefile.project]
!ENDIF
!IF [ECHO PRECOMPILE_DEPENDENCIES = >> Makefile.project]
!ENDIF
!ENDIF
!include Makefile.project

SUBDIRS = . $(SUBDIR1) $(SUBDIR2) $(SUBDIR3) $(SUBDIR4) $(SUBDIR5) $(SUBDIR6) $(SUBDIR7) $(SUBDIR8) $(SUBDIR9) $(SUBDIR10) $(SUBDIR11) $(SUBDIR12) $(SUBDIR13) $(SUBDIR14) $(SUBDIR15)

TEMP_TARGET_FILES = $(TEMP_FILE_DIR)\$(TARGET)

## Environmental path overwrite
!IFDEF CIV4_LIB_INSTALL_PATH
CIV4_PATH=$(CIV4_LIB_INSTALL_PATH)
!ENDIF

!IFDEF FASTDEP_FULL_PATH
FD=$(FASTDEP_FULL_PATH)
!ENDIF

#### Target Files ####
Target_BIN=$(TARGET)\CvGameCoreDLL.dll
Target_BIN_TEMP=$(TEMP_TARGET_FILES)\CvGameCoreDLL.dll

!IF [IF NOT EXIST CvGameCoreDLL.rc EXIT 1] == 0
!IF "$(TARGET)" == "Final_Release"
Target_RESOURCE=$(TEMP_TARGET_FILES)\CvGameCoreDLL.res
!ENDIF
!ENDIF

Target_STATICLIB=$(TEMP_TARGET_FILES)\CvGameCoreDLL.lib

Target_LIBDEF=$(TEMP_TARGET_FILES)\CvGameCoreDLL.def

Target_PCH=$(TEMP_TARGET_FILES)\CvGameCoreDLL.pch

Target_PDB=$(TEMP_TARGET_FILES)\CvGameCoreDLL.pdb

Target_OTHER=$(TEMP_TARGET_FILES)\CvGameCoreDLL.exp

!IFDEF IGNORE_CUSTOM
CUSTOM_CFLAGS  =
CUSTOM_LDFLAGS =
!ENDIF

FILE_DEPENDS = $(TEMP_TARGET_FILES)\depends

#### CFLAGS ####
GLOBAL_CFLAGS=/MD /GR /Gy /EHsc /Gd /Gm- /Fd"$(Target_PDB)" $(CUSTOM_CFLAGS) $(PROJECT_CFLAGS)
Debug_CFLAGS=/Od /RTC1 $(Debug_DEFINES) $(GLOBAL_CFLAGS) $(PROJECT_Debug_CFLAGS)
Release_CFLAGS=/O2 /G7 /arch:SSE2 $(Release_DEFINES) $(GLOBAL_CFLAGS)
Final_Release_CFLAGS=$(Release_CFLAGS) /GL
Debug_Opt_CFLAGS=$(Release_CFLAGS) $(PROJECT_DebugOpt_CFLAGS)

PRECOMPILE_CFLAGS1 = /Yu"
PRECOMPILE_CFLAGS2 = CvGameCoreDLL.h" /Fp"$(Target_PCH)"

#### LDFLAGS ####
GLOBAL_LDFLAGS=/DLL /NOLOGO /SUBSYSTEM:WINDOWS /LARGEADDRESSAWARE /TLBID:1 /PDB:"$(Target_PDB)" $(CUSTOM_LDFLAGS) $(PROJECT_LDFLAGS)
Debug_LDFLAGS=/INCREMENTAL /DEBUG /IMPLIB:"$(Target_STATICLIB)" $(GLOBAL_LDFLAGS)
Release_LDFLAGS=/INCREMENTAL:NO /OPT:REF /OPT:ICF $(GLOBAL_LDFLAGS)
Final_Release_LDFLAGS=/LTCG /INCREMENTAL:NO /OPT:REF /OPT:ICF $(GLOBAL_LDFLAGS)
Final_Profile_LDFLAGS=/LTCG /DEBUG /IMPLIB:"$(Target_STATICLIB)" $(GLOBAL_LDFLAGS)

#### INCLUDES ####
GLOBAL_INCS=/I"$(TOOLKIT)/include" /I"$(PSDK)/Include" /I"$(PSDK)/Include/mfc"

#### boost and python ####

BOOST_LIB_PATH =
!IF [IF NOT EXIST "$(BOOST_LIB_PATH)Boost-1.32.0\libs\boost_python-vc71-mt-gd-1_32.lib" EXIT 1] != 0
BOOST_LIB_PATH = $(SOURCE_DIR)
!IF [IF NOT EXIST "$(BOOST_LIB_PATH)Boost-1.32.0\libs\boost_python-vc71-mt-gd-1_32.lib" EXIT 1] != 0
BOOST_LIB_PATH=$(CIV4_PATH)/
!IF [IF NOT EXIST "$(BOOST_LIB_PATH)Boost-1.32.0\libs\boost_python-vc71-mt-gd-1_32.lib" EXIT 1] != 0
BOOST_LIB_PATH=$(CIV4_LIB_INSTALL_PATH)/
!IF [IF NOT EXIST "$(BOOST_LIB_PATH)Boost-1.32.0\libs\boost_python-vc71-mt-gd-1_32.lib" EXIT 1] != 0
!MESSAGE FATAL ERROR: Failed to locate boost and python
!ENDIF
!ENDIF
!ENDIF
!ENDIF

PROJECT_INCS=/I"$(BOOST_LIB_PATH)Boost-1.32.0/include" /I"$(BOOST_LIB_PATH)Python24/include"
PROJECT_LIBS=/LIBPATH:"$(BOOST_LIB_PATH)Python24/libs" /LIBPATH:"$(BOOST_LIB_PATH)boost-1.32.0/libs/" boost_python-vc71-mt-1_32.lib

INCS = $(PROJECT_INCS) $(GLOBAL_INCS)

#### LIBS ####
GLOBAL_LIBS=/LIBPATH:"$(TOOLKIT)/lib" /LIBPATH:"$(PSDK)/Lib" winmm.lib user32.lib
LIBS = $(PROJECT_LIBS) $(GLOBAL_LIBS)


!IF "$(TARGET)" == "Debug"
CFLAGS  = $(Debug_CFLAGS)
LDFLAGS = $(Debug_LDFLAGS)
LIBS    = $(LIBS) msvcprt.lib
!ENDIF
!IF "$(TARGET)" == "Debug-opt"
CFLAGS  = $(Debug_Opt_CFLAGS)
LDFLAGS = $(Debug_LDFLAGS)
# Leaving out msvcprt might help with debugging memory (but I doubt it)
LIBS    = $(LIBS) msvcprt.lib
!ENDIF
!IF "$(TARGET)" == "Release"
CFLAGS  = $(Release_CFLAGS)
LDFLAGS = $(Release_LDFLAGS)
!ENDIF
!IF "$(TARGET)" == "Assert"
CFLAGS  = $(Release_CFLAGS) /DFASSERT_ENABLE
LDFLAGS = $(Release_LDFLAGS)
!ENDIF
!IF "$(TARGET)" == "Profile"
CFLAGS  = $(Release_CFLAGS) $(PROJECT_Profile_CFLAGS) /Z7
LDFLAGS = $(Debug_LDFLAGS)
!ENDIF
!IF "$(TARGET)" == "Final_Release"
CFLAGS  = $(Final_Release_CFLAGS)
LDFLAGS = $(Final_Release_LDFLAGS)
!ENDIF


!IFNDEF CFLAGS
!ERROR Target "$(TARGET)" not supported. Supported targets: Debug Release Assert Profile Final_Release
!ENDIF

!IF EXIST ($(FILE_DEPENDS))
!INCLUDE $(FILE_DEPENDS)
!ENDIF

#### Targets ####
#################

.PHONY: all clean build precompile Make_Dir fastdep source_list

all: Precompile build

dll: all

clean:
	@IF EXIST "$(TEMP_TARGET_FILES)" RMDIR /s /q "$(TEMP_TARGET_FILES)"
	@FOR %i IN ($(Target_BIN) $(Target_STATICLIB) $(Target_LIBDEF) $(Target_RESOURCE) \
		$(Target_PCH) $(Target_PDB) $(Target_OTHER)) DO @IF EXIST "%i" DEL "%i"

$(Target_BIN): $(Target_BIN_TEMP)
	-COPY "$(Target_BIN_TEMP)" "$(Target_BIN)"


build: $(Target_BIN)
!IFDEF YOURMOD
	-COPY "$(Target_BIN)" "$(YOURMOD)\Assets\."
!ENDIF
!IFDEF YOURMOD2
	-COPY "$(Target_BIN)" "$(YOURMOD2)\Assets\."
!ENDIF
!IFDEF YOURLOGS
	-FOR %i IN ("$(YOURLOGS)"\*.log) DO @IF EXIST "%i" DEL "%i"
!ENDIF


precompile: Make_Dir Target_unfinished $(Target_PCH)

source_list: Make_Dir
	@ECHO Building source list
	@ECHO SOURCES= \> $(FILE_DEPENDS)
	@FOR %j in ($(SUBDIRS)) DO @(FOR %i IN ($(SOURCE_DIR)\%j\*.cpp) DO @ECHO %i \>> $(FILE_DEPENDS))
    @ECHO.>> $(FILE_DEPENDS)
	@ECHO OBJS= \>> $(FILE_DEPENDS)
    @FOR %j in ($(SUBDIRS)) DO @(FOR /F "delims=." %i IN ('dir /b $(SOURCE_DIR)\%j\*.cpp') DO @ECHO. $(TEMP_TARGET_FILES)\%j\%i.obj \>> $(FILE_DEPENDS))
    @ECHO.>> $(FILE_DEPENDS)

fastdep:
	@ECHO Running fastdep
	@$(FD) --objectextension=pch -q --removepath=$(SOURCE_DIR)\ -O $(TEMP_TARGET_FILES) $(SOURCE_DIR)\CvGameCoreDLL.cpp >> $(FILE_DEPENDS)
    @$(FD) --objectextension=obj -q --removepath=$(SOURCE_DIR)\ -O $(TEMP_TARGET_FILES) $(SOURCES) >> $(FILE_DEPENDS)

Make_Dir:
	@FOR %j in ($(SUBDIRS)) DO @(IF NOT EXIST "$(TEMP_TARGET_FILES)\%j\." MKDIR "$(TEMP_TARGET_FILES)\%j")
	@IF NOT EXIST "$(TARGET)\." MKDIR $(TARGET)

Target_unfinished:
	@ECHO.>$(TEMP_TARGET_FILES)\unfinished.@
	@FOR /F "delims=@" %i IN ('dir /b $(TEMP_TARGET_FILES)\*.@') DO \
		@IF EXIST "$(TEMP_TARGET_FILES)\%i" DEL "$(TEMP_TARGET_FILES)\%i"
	@FOR /F %i IN ('dir /b $(TEMP_TARGET_FILES)\*.@') DO \
		@IF EXIST "$(TEMP_TARGET_FILES)\%i" DEL "$(TEMP_TARGET_FILES)\%i"

$(Target_BIN_TEMP): $(OBJS) $(Target_RESOURCE)
	@ECHO.Linking DLL
	@$(LD) /out:$(Target_BIN_TEMP) $(LDFLAGS) $(LIBS) $(OBJS) $(Target_RESOURCE)

{$(SOURCE_DIR)\.}.cpp{$(TEMP_TARGET_FILES)\.}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR1)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR1)}.obj:
	@ECHO.>"$*.obj.@"
    @$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH1)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR2)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR2)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH2)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR3)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR3)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH3)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR4)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR4)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH4)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"
	
{$(SOURCE_DIR)\$(SUBDIR5)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR5)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH5)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR6)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR6)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH6)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR7)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR7)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH7)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR8)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR8)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH8)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR9)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR9)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH9)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR10)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR10)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH10)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR11)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR11)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH11)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR12)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR12)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH12)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR13)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR13)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH13)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR14)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR14)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH14)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"

{$(SOURCE_DIR)\$(SUBDIR15)}.cpp{$(TEMP_TARGET_FILES)\$(SUBDIR15)}.obj:
	@ECHO.>"$*.obj.@"
	@$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(SUBDIRPATH15)$(PRECOMPILE_CFLAGS2) $(INCS) /Fo$*.obj /c $<
	@DEL "$*.obj.@"


$(Target_PCH) $(TEMP_TARGET_FILES)\_precompile.obj: $(PRECOMPILE_DEPENDENCIES)
	@ECHO.>"$(Target_PCH).@"
	@ECHO.>"$(TEMP_TARGET_FILES)\_precompile.obj.@"
	@FOR %i IN ($(TEMP_TARGET_FILES)\*.obj) DO @IF EXIST "%i" DEL "%i"
    @$(CPP) /nologo $(CFLAGS) $(PRECOMPILE_CFLAGS1)$(PRECOMPILE_CFLAGS2) $(INCS) /YcCvGameCoreDLL.h /Fo"$(TEMP_TARGET_FILES)\_precompile.obj" /c $(SOURCE_DIR)\_precompile.cpp
	@DEL "$(Target_PCH).@"
	@DEL "$(TEMP_TARGET_FILES)\_precompile.obj.@"

.rc{$(TEMP_TARGET_FILES)}.res:
	@ECHO.>"$*.res.@"
	$(RC) /Fo$@ $(INCS) $<
	@DEL "$*.res.@"

!IFDEF BLACKLIST
$(TEMP_TARGET_FILES)\$(BLACKLIST).obj: $(BLACKLIST).cpp
	@ECHO.>"$*.obj.@"
	@ECHO.>"$*-dummy.cpp"
	@$(CPP) /nologo $(Release_CFLAGS) $(Release_INCS) /Y- /Fo$@ /c "$*-dummy.cpp"
	@DEL "$*-dummy.cpp"
	@DEL "$*.obj.@"

!ENDIF
