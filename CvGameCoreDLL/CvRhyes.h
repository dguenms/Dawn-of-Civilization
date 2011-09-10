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

#define PAGAN_TEMPLE			(37)

#define HEROICEPIC				(111)
#define FLAVIANAMPHITHEATRE		(111)
#define NATIONALEPIC			(112)
#define TRIUMPHALARCH			(113)
#define GLOBETHEATRE			(114)
#define HERMITAGE				(115)
#define NATIONALGALLERY			(115)
#define CHANNELTUNNEL			(116)
#define WALLSTREET				(117)
#define IRONWORKS				(118)
#define TRADINGCOMPANY			(119)
#define MTRUSHMORE				(120)
#define REDCROSS				(121)
#define INTERPOL				(122)
#define SCOTLANDYARD			(122)
#define PYRAMID					(123)
#define STONEHENGE				(124)
#define GREATLIBRARY			(125)
#define GREATLIGHTHOUSE			(126)
#define HANGINGGARDEN			(127)
#define COLOSSUS				(128)
#define ORACLE					(129)
#define PARTHENON				(130)
#define ANGKORWAT				(131)
#define HAGIASOPHIA				(132)
#define CHICHENITZA				(133)
#define TEMPLEOFKUKULKAN		(133)
#define SISTINECHAPEL			(134)
#define SPIRALMINARET			(135)
#define NOTREDAME				(136)
#define TAJMAHAL				(137)
#define KREMLIN					(138)
#define EIFFELTOWER				(139)
#define STATUEOFLIBERTY			(140)
#define BROADWAY				(141)
#define WEMBLEY					(141)
#define ROCKNROLL				(142)
#define GRACELAND				(142)
#define HOLLYWOOD				(143)
#define GREATDAM				(144)
#define PENTAGON				(145)
#define UNITEDNATIONS			(146)
#define SPACEELEVATOR			(147)
#define ARTEMIS					(149)
#define SANKORE					(150)
#define GREATWALL				(151)
#define ZEUS					(152)
#define MAUSOLLOS				(153)
#define CRISTO					(154)
#define PAYA					(155)
#define MOAI					(156)
#define APOSTOLIC				(157)
#define LEANINGTOWER			(158)
#define OLYMPICPARK				(159)
#define SOLOMON                 (160)
#define ISHTAR                  (161)
#define THEODOSIAN              (162)
#define TERRACOTTA              (163)
#define MEZQUITA                (164)
#define DOMEROCK                (165)
#define TOPKAPI                 (166)
#define BRANDENBURG             (167)
#define SANMARCO                (168)
#define WESTMINSTER             (169)
#define BOROBUDUR               (171)
#define KHAJURAHO               (172)
#define HIMEJI                  (173)
#define PORCELAIN               (174)
#define HARMANDIR_SAHIB         (175)
#define GREAT_BATH              (176)

#define NUM_WONDERS             (177)

#define NUM_BUILDINGS_PLAGUE	(178)

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

extern int takenTiles[30];
extern int distanceSubtrahend[30];
extern int distanceSubtrahendAstronomy[30];
extern int distanceMultiply[30];
extern int distanceMultiplayAstronomy[30];
extern int compactEmpireModifier[30];
extern int compactEmpireModifierAstronomy[30];
extern int targetCityValueDivisor[30];

extern int eraModifierInit[30];
extern int cultureModifier[30];

extern int unitCostModifier[30];
extern int researchModifier[30];
extern int distanceMaintenanceModifier[30];
extern int numMaintenanceModifier[30];
extern int civicUpkeepModifier[30];
extern int healthMultiplier[30];

extern int startingEraFound[30];
extern int startingEraFound600AD[30];
extern int startingEraFoundAstronomy[30];
extern int unitCostModifier2[30];
extern int wonderCostModifier[30];
extern int buildingCostModifier[30];
extern int inflationRateModifier[30];
extern int greatPeopleThreshold[30];
extern int currentEra[30];
extern int currentEra600AD[30];
extern int growthThreshold[30];

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


