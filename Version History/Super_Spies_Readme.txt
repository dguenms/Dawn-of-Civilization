Super Spies v1.31 for Civilization 4:BTS 3.17
By: Trojan Sheep
Ported to RevolutionDCM by Glider1 and Jojoweb many thanks for debugging help
Slightly modified and cleaned up by Lord Tirian

Patch Compatibility: BTS 3.17
MP Compatible: Yes???

Installation Instructions:

1) Unzip this into the "BTS_install_folder\Mods\" folder. 
2) Open the CivilizationIV.ini configuration file
3) Change the Mod line to read: Mod = Mods\SuperSpies
4) Load the game. 
5) Then play as normal.


-----Game Play-----

- Spies now have promotions to improve their abilities. See below for details.

- Spies now have access to a special assassination and bribery missions.

- Spies gain xp from performing missions (scales by difficulty), catching other
  spies and from having an Intelligence Agency (2) or a Scotland Yard (3) in the city.

- New counter espionage timer displays next to player's names on the scoreboard

- With the discovery of Paper, you can convert production to espionage in cities.


-----Fixes From Base BTS-----

- You can now sabotage buildings in a city regardless of whether or not it has a
  monument in it.

- You no longer always receive the "recent mission" penalty


-----Promotions-----

Deception I:
- Requires: None	
- Abilities
  - +10% Evasion (Directly modifies your chance of being caught)

Deception II:
- Requires: Deception I Promotion	
- Abilities
  - +10% Evasion (Directly modifies your chance of being caught)

Deception III:
- Requires: Deception II Promotion	
- Abilities
  - +10% Evasion (Directly modifies your chance of being caught)

Informant I:
- Requires: None	
- Abilities
  - +10% Intercept (Directly modifies the chance of catching spies in the same tile)
  - +1 View Distance
  - +50% Additional counter espionage penalty when mission is performed on other nations

Informant II:
- Requires: Informant I Promotion	
- Abilities
  - +10% Intercept (Directly modifies the chance of catching spies in the same tile)
  - +1 View Distance
  - +50% Additional counter espionage penalty when mission is performed on other nations

Informant III:
- Requires: Informant II Promotion	
- Abilities
  - +10% Intercept (Directly modifies the chance of catching spies in the same tile)
  - +1 View Distance
  - +50% Additional counter espionage penalty when mission is performed on other nations

Improviser I:
- Requires: None	
- Abilities
  - +10% Free Preparation Time (Essentially gives you a free turn of fortify, still up to the maximum)

Improviser II:
- Requires: Improviser I Promotion	
- Abilities
  - +10% Free Preparation Time (Essentially gives you a free turn of fortify, still up to the maximum)

Improviser III:
- Requires: Improviser II Promotion	
- Abilities
  - +10% Free Preparation Time (Essentially gives you a free turn of fortify, still up to the maximum)

Improviser IV:
- Requires: Improviser III Promotion	
- Abilities
  - +10% Free Preparation Time (Essentially gives you a free turn of fortify, still up to the maximum)

Improviser V:
- Requires: Improviser IV Promotion	
- Abilities
  - +10% Free Preparation Time (Essentially gives you a free turn of fortify, still up to the maximum)

Logistics I:
- Requires: None	
- Abilities
  - +1 Movement

Logistics II:
- Requires: Logistics I
- Abilities
  - Can use enemy roads
  - -1 Terrain Movement Cost

Logistics III:
- Requires: Logistics II
- Abilities
  - +1 Movement

Loyalty:
- Requires: None
- Abilities
  - Keeps spy from revealing nationality when caught

Instigator I:
- Requires: Deception I
- Abilities
  - +50% Unrest from unhappiness mission

Instigator II:
- Requires: Instigator I
- Abilities
  - +50% Unrest from unhappiness mission

Instigator III:
- Requires: Instigator I
- Abilities
  - +100% Revolt time from city revolt mission

Alchemist I:
- Requires: Deception I
- Abilities
  - +50% Unhealthiness from poison water mission

Alchemist II:
- Requires: Alchemist I
- Abilities
  - +50% Unhealthiness from poison water mission
  
Alchemist III:
- Requires: Alchemist II, Composites Technology
- Abilities
  - Creates fallout on any sabotaged improvement

Escape Artist I:
- Requires: Informant I
- Abilities
  - +40% Chance to escape back to capital after being caught

Escape Artist II:
- Requires: Informant II, Escape Artist I
- Abilities
  - +40% Chance to escape back to capital after being caught

-----Missions (Glider1)---------------
Assassination:
- a spy either human or AI, can assassinate a great specialist in a city. 
  The mission is enabled by default but can be disenabled in CIV4EspionageMissionInfo.xml:
  Change to <iDestroyUnitCostFactor>0</iDestroyUnitCostFactor> under the assassination mission section.
  The cost of the mission and other parameters such as probabilities of success can be changed as per any standard espionage mission in the same file.

Bribery
- a spy either human or AI, can bribe a single worker for an espionage cost.
  The mission is enabled by but can be disenabled in CIV4EspionageMissionInfo.xml:
  Change to <iBuyUnitCostFactor>0</iBuyUnitCostFactor> under the bribery mission section.
  The cost of the mission and other parameters such as probabilities of success can be changed as per any standard espionage mission in the same file.
  
-----Notes to Modmakers-----

If you want to use the spy promotions in your mod I have tried to make things as 
easy as possible for you. In the SDK files I have added  
//TSHEEP and //TSHEEP End in all of the places 
that I have made changes to the original files.

->Note (Lord Tirian): I also marked all changes with Super Spies, helping you to catch TSheep and glider1's modifications at once.

There is only one python addition thus far which is this statement, you should be able to find it by searching for the "if" line:
if (gc.getTeam(gc.getGame().getActiveTeam()).getCounterespionageTurnsLeftAgainstTeam(eTeam) != 0):
	szTempBuffer = u"(%d)%c" %(gc.getTeam(gc.getGame().getActiveTeam()).getCounterespionageTurnsLeftAgainstTeam(eTeam), CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR))
	szBuffer = szBuffer + szTempBuffer


-----Version Information-----

-----v1.31 (Lord Tirian) -----
Changed - Separated Super Spies from RevolutionDCM.
Changed - Turned Assassination & Bribe Worker missions on on default.
Changed - Implemented as non-modular (currently), since it messes with promotions anyway... which makes things weird.
Changed - Integrated Dresden and Solver's Unofficial Patch 0.21.
Changed - Renamed Improvise to Improviser and Security to Informant (closer to some Civ 4 naming like City Raider, Woodsman etc.).
Changed - Cleaned up comments in source code a bit.

Added - Proper German translation, added Babelfish-produced French, Italian and Spanish translations.
Added  - Shiny new buttons for the promotions, more in line with Civ 4's style.
Added -  Production -> Espionage conversion (originally by deanej)

-----v1.30 (Glider1) -----
This mod is not not compatible with base BTS yet and requires RevolutionDCM
Removed assassination mission as per version 1.23  because it was not implemented as per BTS standard
Re-implemented assassination mission as per BTS standard (see assets/xml/gameinfo/CIV4EspionageMissionInfo.xml). The mission is "off" by default in order not to disturb game balance.
Introduced a bribery mission as per BTS standard (see assets/xml/gameinfo/CIV4EspionageMissionInfo.xml). The mission is "off by default in order not to disturb game balance.
Tweaked the AI's urge to poison cities down just a little, using XML (/assets/xml/gameinfo/CIV4EspionageMissionInfo.xml). This results in the AI using other minor espionage missions a little more often.

-----v1.23----
Fixed - CTDs! Finally discovered the bugs and smashed them over and over again. Reimplemented Modular XML as it was not to blame.

-----v1.22----
More Attempts...

-----v1.21----
Attempts at fixing CTDs

-----v1.2-----
Added - Assassination Mission, see above for details
Added - Alchemist III promotion which adds a fallout effect to all sabotaged improvements
Added - AI Promotion Logic, they will now do their best to create formidible foes for your own intelligence network
Added - Dynamic overall AI espionage targetting, AI will now vastly prioritize tech leaders and people they don't like, while ignoring others 
Added - AI weight and usage of counter espionage missions (No they never use them in vanilla)
Added - AI requirement of annoyed or worse to use aggressive missions (They would waste away their EP on neutral neighbors in vanilla 3.13) 
Added - Additional details to destroy improvement and destroy unit missions saying which city they occured near 

Fixed - Graphical display error for promotion effects
Fixed - Got rid of innate chance of escape without promotion
Fixed - Nationality of escaping spies automatically being revealed to player

-----v1.1-----
Added - "Bonus Unrest" Promotion Effect
Added - "Bonus Revolt" Promotion Effect
Added - "Bonus Unhealthiness" Promotion Effect
Added - "Escape" Promotion Effect
Added - "Loyalty" Promotion Effect
Added - Counter Espionage Ticker
Added - "Bonus Counter Espionage" Promotion Effect

Fixed - Mission XP bug (Only gave max or minimum because of a stupid error on my part)
 
-----v1.0-----

Added - "Evasion" Promotion Effect
Added - "Intercept" Promotion Effect
Added - "Preparation" Promotion Effect
Added - Spy XP gain from missions
Added - Proper Spy XP gain from buildings
Added - Spy XP gain from catching spies

Fixed - Building sabotage bug from 3.13
Fixed - "Recent Mission" bug from 3.13


-----===Credits & Thanks===-----

- Skodkim
	For all the help testing... that was the most elusive and frustrating bug ever! :-)

- Jen
	For putting up with my tinkering even when I partially destroyed our multiplayer game through DLL changes
	And for refining all the icons for the promotions
- Zuul
	From whom I shamelessly stole the bases of several promotion icons
- White Rabbit
	From whom I also shamelessly stole the bases of several promotion icons
- The Lopez
	From whom I shamelessly stole the layout for this readme