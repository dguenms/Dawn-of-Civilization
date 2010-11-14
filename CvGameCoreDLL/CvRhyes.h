//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

using namespace std;
typedef list<char*> LISTCHAR;

// rhyes.h
#define EARTH_X					(124)
#define EARTH_Y					(68)


#define MAX_COM_SHRINE			(20)


#define EGYPT					(0)
#define INDIA					(1)
#define CHINA					(2)
#define BABYLONIA				(3)
#define GREECE					(4)
#define PERSIA					(5)
#define CARTHAGE				(6)
#define ROME					(7)
#define JAPAN					(8)
#define ETHIOPIA				(9)
#define MAYA					(10)
#define BYZANTIUM               (11)
#define VIKING					(12)
#define ARABIA					(13)
#define KHMER					(14)
#define SPAIN					(15)
#define FRANCE					(16)
#define ENGLAND					(17)
#define GERMANY					(18)
#define RUSSIA					(19)
#define NETHERLANDS				(20)
#define MALI					(21)
#define PORTUGAL				(22)
#define INCA					(23)
#define MONGOLIA				(24)
#define AZTEC					(25)
#define TURKEY					(26)
#define AMERICA					(27)
#define NUM_MAJOR_PLAYERS		(28)
#define INDEPENDENT				(28)
#define INDEPENDENT2			(29)
#define NATIVE					(30)
#define CELTIA					(31)
#define BARBARIAN				(32)


#define MEDITATION				(1)
#define POLYTHEISM				(2)
#define PRIESTHOOD				(3)
#define MONOTHEISM				(4)
#define MONARCHY				(5)
#define LITERATURE				(6)
#define CODEOFLAWS				(7)
#define DRAMA					(8)
#define FEUDALISM				(9)
#define THEOLOGY				(10)
#define MUSIC					(11)
#define CIVIL_SERVICE			(12)
#define GUILDS					(13)
#define DIVINERIGHT				(14)
#define NATIONALISM				(15)
#define MILITARY_TRADITION		(16)
#define LIBERALISM				(18)
#define FASCISM					(21)
#define COMMUNISM				(22)
#define MASS_MEDIA				(23)

#define FISHING					(25)
#define POTTERY					(28)
#define AESTHETICS				(29)
#define SAILING					(30)
#define WRITING					(31)
#define MATHEMATICS				(32)
#define ALPHABET				(33)
#define CALENDAR				(34)
#define CURRENCY				(35)
#define PHILOSOPHY				(36)
#define PAPER					(37)
#define BANKING                 (38)
#define EDUCATION               (39)
#define PRINTING_PRESS			(40)
#define ECONOMICS				(41)
#define ASTRONOMY				(42)
#define CHEMISTRY				(43)
#define ELECTRICITY				(48)
#define FISSION					(50)
#define FIBER_OPTICS			(57)

#define HUNTING					(59)
#define ARCHERY					(61)
#define MASONRY					(62)
#define BRONZEWORKING			(64)
#define IRONWORKING				(66)
#define METALCASTING			(67)
#define COMPASS					(68)
#define CONSTRUCTION			(69)
#define MACHINERY				(70)
#define ENGINEERING				(71)
#define OPTICS					(72)
#define GUNPOWDER				(73)
#define MILITARY_SCIENCE		(75)
#define RIFLING					(76)
#define ASSEMBLY_LINE			(79)
#define INDUSTRIALISM			(82)
#define RADIO                   (83)
#define ROBOTICS				(90)



#define GREATPALACE				(1)
#define SUMMERPALACE			(1)
#define VERSAILLES				(2)
#define FORBIDDENPALACE			(2)

#define HEROICEPIC				(105)
#define FLAVIANAMPHITHEATRE		(105)
#define NATIONALEPIC			(106)
#define TRIUMPHALARCH			(106)
#define GLOBETHEATRE			(107)
#define HERMITAGE				(109)
#define NATIONALGALLERY			(109)
#define CHANNELTUNNEL			(110)
#define WALLSTREET				(111)
#define IRONWORKS				(112)
#define TRADINGCOMPANY			(113)
#define MTRUSHMORE				(114)
#define REDCROSS				(115)
#define INTERPOL				(116)
#define SCOTLANDYARD			(116)
#define PYRAMID					(117)
#define STONEHENGE				(118)
#define GREATLIBRARY			(119)
#define GREATLIGHTHOUSE			(120)
#define HANGINGGARDEN			(121)
#define COLOSSUS				(122)
#define ORACLE					(123)
#define PARTHENON				(124)
#define ANGKORWAT				(125)
#define HAGIASOPHIA				(126)
#define CHICHENITZA				(127)
#define TEMPLEOFKUKULKAN		(127)
#define SISTINECHAPEL			(128)
#define SPIRALMINARET			(129)
#define NOTREDAME				(130)
#define TAJMAHAL				(131)
#define KREMLIN					(132)
#define EIFFELTOWER				(133)
#define STATUEOFLIBERTY			(134)
#define BROADWAY				(135)
#define WEMBLEY					(135)
#define ROCKNROLL				(136)
#define GRACELAND				(136)
#define HOLLYWOOD				(137)
#define GREATDAM				(138)
#define PENTAGON				(139)
#define UNITEDNATIONS			(140)
#define SPACEELEVATOR			(141)
#define ARTEMIS					(143)
#define SANKORE					(144)
#define GREATWALL				(145)
#define ZEUS					(146)
#define MAUSOLLOS				(147)
#define CRISTO					(148)
#define PAYA					(149)
#define MOAI					(150)
#define APOSTOLIC				(158)
#define LEANINGTOWER			(159)
#define OLYMPICPARK				(160)
#define SOLOMON                 (161)
#define ISHTAR                  (162)
#define THEODOSIAN              (163)
#define TERRACOTTA              (164)
#define MEZQUITA                (165)
#define DOMEROCK                (166)
#define TOPKAPI                 (167)
#define BRANDENBURG             (168)
#define SANMARCO                (169)
#define WESTMINSTER             (170)

#define NUM_WONDERS             (171)

#define NUM_BUILDINGS_PLAGUE	(173)

#define NUM_BUILDINGTYPES_PLAGUE	(138)

#endif	// CVRHYES_H



extern int startingTurn[];
extern int startingTurnYear[]; // edead
extern char loadingTime[35][4];
extern char loadingTime600AD[35][4];
extern char startingYear[35][6];
extern bool startingEra[35];
extern char startingYear600AD[35][6];
extern bool startingEra600AD[35];
//extern int militaryBonus[2][18];
extern char uniquePower[35][2][16];
extern char uniqueGoals[35][3][18];
extern char rating[35][6][15];

extern int turnPlayed[33];
extern int civSpreadFactor[33][7];
extern int civicMatrix[28][6][5];
extern int borders[28][28];
extern wchar civDynamicNames[2][28][22][19]; //(dynamic civ names - not jdog's)
extern int civDynamicNamesFlag[28];
extern int civDynamicNamesEraThreshold[28];
extern list<CvWString> GPNameList[38][6];
extern int settlersMaps[2][28][68][124];

extern void fillGPNamesList();


