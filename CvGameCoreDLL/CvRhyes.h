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
#define KOREA                   (10)
#define MAYA					(11)
#define BYZANTIUM               (12)
#define VIKING					(13)
#define ARABIA					(14)
#define KHMER					(15)
#define SPAIN					(16)
#define FRANCE					(17)
#define ENGLAND					(18)
#define GERMANY					(19)
#define RUSSIA					(20)
#define NETHERLANDS				(21)
#define MALI					(22)
#define PORTUGAL				(23)
#define INCA					(24)
#define MONGOLIA				(25)
#define AZTEC					(26)
#define TURKEY					(27)
#define AMERICA					(28)
#define NUM_MAJOR_PLAYERS		(29)
#define INDEPENDENT				(29)
#define INDEPENDENT2			(30)
#define NATIVE					(31)
#define CELTIA					(32)
#define BARBARIAN				(33)


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
#define SCIENTIFIC_METHOD       (44)
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

#define HEROICEPIC				(109)
#define FLAVIANAMPHITHEATRE		(109)
#define NATIONALEPIC			(110)
#define TRIUMPHALARCH			(111)
#define GLOBETHEATRE			(112)
#define HERMITAGE				(113)
#define NATIONALGALLERY			(113)
#define CHANNELTUNNEL			(114)
#define WALLSTREET				(115)
#define IRONWORKS				(116)
#define TRADINGCOMPANY			(117)
#define MTRUSHMORE				(118)
#define REDCROSS				(119)
#define INTERPOL				(120)
#define SCOTLANDYARD			(120)
#define PYRAMID					(121)
#define STONEHENGE				(122)
#define GREATLIBRARY			(123)
#define GREATLIGHTHOUSE			(124)
#define HANGINGGARDEN			(125)
#define COLOSSUS				(126)
#define ORACLE					(127)
#define PARTHENON				(128)
#define ANGKORWAT				(129)
#define HAGIASOPHIA				(130)
#define CHICHENITZA				(131)
#define TEMPLEOFKUKULKAN		(131)
#define SISTINECHAPEL			(132)
#define SPIRALMINARET			(133)
#define NOTREDAME				(134)
#define TAJMAHAL				(135)
#define KREMLIN					(136)
#define EIFFELTOWER				(137)
#define STATUEOFLIBERTY			(138)
#define BROADWAY				(139)
#define WEMBLEY					(139)
#define ROCKNROLL				(140)
#define GRACELAND				(140)
#define HOLLYWOOD				(141)
#define GREATDAM				(142)
#define PENTAGON				(143)
#define UNITEDNATIONS			(144)
#define SPACEELEVATOR			(145)
#define ARTEMIS					(146)
#define SANKORE					(147)
#define GREATWALL				(148)
#define ZEUS					(149)
#define MAUSOLLOS				(151)
#define CRISTO					(152)
#define PAYA					(153)
#define MOAI					(154)
#define APOSTOLIC				(155)
#define LEANINGTOWER			(156)
#define OLYMPICPARK				(157)
#define SOLOMON                 (158)
#define ISHTAR                  (159)
#define THEODOSIAN              (160)
#define TERRACOTTA              (161)
#define MEZQUITA                (162)
#define DOMEROCK                (163)
#define TOPKAPI                 (164)
#define BRANDENBURG             (165)
#define SANMARCO                (166)
#define WESTMINSTER             (167)
#define BOROBUDUR               (169)
#define KHAJURAHO               (170)
#define HIMEJI                  (171)
#define PORCELAIN               (172)
#define HARMANDIR_SAHIB         (173)
#define GREAT_BATH              (174)

#define NUM_WONDERS             (175)

#define NUM_BUILDINGS_PLAGUE	(176)

#define NUM_BUILDINGTYPES_PLAGUE	(137)

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

extern int turnPlayed[34];
extern int civSpreadFactor[34][8];
extern int civicMatrix[29][6][5];
extern int borders[29][29];
extern wchar civDynamicNames[2][29][22][19]; //(dynamic civ names - not jdog's)
extern int civDynamicNamesFlag[29];
extern int civDynamicNamesEraThreshold[29];
extern int settlersMaps[2][29][68][124];


