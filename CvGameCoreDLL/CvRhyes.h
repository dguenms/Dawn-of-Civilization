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
#define INDONESIA				(16)
#define SPAIN					(17)
#define FRANCE					(18)
#define ENGLAND					(19)
#define GERMANY					(20)
#define RUSSIA					(21)
#define NETHERLANDS				(22)
#define MALI					(23)
#define PORTUGAL				(24)
#define INCA					(25)
#define MONGOLIA				(26)
#define AZTEC					(27)
#define TURKEY					(28)
#define AMERICA					(29)
#define NUM_MAJOR_PLAYERS		(30)
#define INDEPENDENT				(30)
#define INDEPENDENT2			(31)
#define NATIVE					(32)
#define CELTIA					(33)
#define BARBARIAN				(34)


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

#define HEROICEPIC				(110)
#define FLAVIANAMPHITHEATRE		(110)
#define NATIONALEPIC			(111)
#define TRIUMPHALARCH			(112)
#define GLOBETHEATRE			(113)
#define HERMITAGE				(114)
#define NATIONALGALLERY			(114)
#define CHANNELTUNNEL			(115)
#define WALLSTREET				(116)
#define IRONWORKS				(117)
#define TRADINGCOMPANY			(118)
#define MTRUSHMORE				(119)
#define REDCROSS				(120)
#define INTERPOL				(121)
#define SCOTLANDYARD			(121)
#define PYRAMID					(122)
#define STONEHENGE				(123)
#define GREATLIBRARY			(124)
#define GREATLIGHTHOUSE			(125)
#define HANGINGGARDEN			(126)
#define COLOSSUS				(127)
#define ORACLE					(128)
#define PARTHENON				(129)
#define ANGKORWAT				(130)
#define HAGIASOPHIA				(131)
#define CHICHENITZA				(132)
#define TEMPLEOFKUKULKAN		(132)
#define SISTINECHAPEL			(133)
#define SPIRALMINARET			(134)
#define NOTREDAME				(135)
#define TAJMAHAL				(136)
#define KREMLIN					(137)
#define EIFFELTOWER				(138)
#define STATUEOFLIBERTY			(139)
#define BROADWAY				(140)
#define WEMBLEY					(140)
#define ROCKNROLL				(141)
#define GRACELAND				(141)
#define HOLLYWOOD				(142)
#define GREATDAM				(143)
#define PENTAGON				(144)
#define UNITEDNATIONS			(145)
#define SPACEELEVATOR			(146)
#define ARTEMIS					(148)
#define SANKORE					(149)
#define GREATWALL				(150)
#define ZEUS					(151)
#define MAUSOLLOS				(152)
#define CRISTO					(153)
#define PAYA					(154)
#define MOAI					(155)
#define APOSTOLIC				(156)
#define LEANINGTOWER			(157)
#define OLYMPICPARK				(158)
#define SOLOMON                 (159)
#define ISHTAR                  (160)
#define THEODOSIAN              (161)
#define TERRACOTTA              (162)
#define MEZQUITA                (163)
#define DOMEROCK                (164)
#define TOPKAPI                 (165)
#define BRANDENBURG             (166)
#define SANMARCO                (167)
#define WESTMINSTER             (168)
#define BOROBUDUR               (170)
#define KHAJURAHO               (171)
#define HIMEJI                  (172)
#define PORCELAIN               (173)
#define HARMANDIR_SAHIB         (174)
#define GREAT_BATH              (175)

#define NUM_WONDERS             (176)

#define NUM_BUILDINGS_PLAGUE	(177)

#define NUM_BUILDINGTYPES_PLAGUE	(137)

#endif	// CVRHYES_H

enum MyReligions
{
	PROTESTANTISM,
	CATHOLICISM,
	ISLAM,
	HINDUISM,
	BUDDHISM,
	CONFUCIANISM,
	TAOISM,
	ZOROASTRIANISM
};

extern int startingTurn[];
extern int startingTurnYear[]; // edead
extern char loadingTime[36][4];
extern char loadingTime600AD[36][4];
extern char startingYear[36][6];
extern bool startingEra[36];
extern char startingYear600AD[36][6];
extern bool startingEra600AD[36];
//extern int militaryBonus[2][18];
extern char uniquePower[36][2][16];
extern char uniqueGoals[36][3][18];
extern char rating[36][6][15];

extern int turnPlayed[35];
extern int civSpreadFactor[35][8];
extern int civicMatrix[30][6][5];
extern int borders[30][30];
extern wchar civDynamicNames[2][30][22][19]; //(dynamic civ names - not jdog's)
extern int civDynamicNamesFlag[30];
extern int civDynamicNamesEraThreshold[30];
extern int settlersMaps[2][30][68][124];


