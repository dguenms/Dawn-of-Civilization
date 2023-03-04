//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

using namespace std;
typedef list<char*> LISTCHAR;

// rhyes.h
#define EARTH_X					(150)
#define EARTH_Y					(80)

#define MAX_COM_SHRINE			(20)

#define BEGIN_WONDERS				(170) // increment if normal building (not for wonders) is added
#define BEGIN_GREAT_WONDERS			(BEGIN_WONDERS+13) // increment if a national wonder is added

#define NUM_CIVS				(52)

#define NUM_ERAS				(ERA_DIGITAL+1)

#define PAGAN_TEMPLE			((BuildingTypes)GC.getInfoTypeForString("BUILDING_PAGAN_TEMPLE"))
#define BUILDING_PALACE			((BuildingClassTypes)0)
#define BUILDING_PLAGUE			((BuildingTypes)GC.getInfoTypeForString("BUILDING_PLAGUE"))

#define UNITCLASS_SLAVE			((UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SLAVE"))

enum DoCTechs
{
	TANNING,
	MINING,
	POTTERY,
	PASTORALISM,
	AGRICULTURE,
	MYTHOLOGY,
	SAILING,

	SMELTING,
	MASONRY,
	LEVERAGE,
	PROPERTY,
	CEREMONY,
	DIVINATION,
	SEAFARING,

	ALLOYS,
	CONSTRUCTION,
	RIDING,
	ARITHMETICS,
	WRITING,
	CALENDAR,
	SHIPBUILDING,

	BLOOMERY,
	CEMENT,
	MATHEMATICS,
	CONTRACT,
	LITERATURE,
	PRIESTHOOD,
	NAVIGATION,

	GENERALSHIP,
	ENGINEERING,
	AESTHETICS,
	CURRENCY,
	LAW,
	PHILOSOPHY,
	MEDICINE,

	NOBILITY,
	STEEL,
	ARCHITECTURE,
	ARTISANRY,
	POLITICS,
	SCHOLARSHIP,
	ETHICS,

	FEUDALISM,
	FORTIFICATION,
	MACHINERY,
	ALCHEMY,
	GUILDS,
	CIVIL_SERVICE,
	THEOLOGY,

	COMMUNE,
	CROP_ROTATION,
	PAPER,
	COMPASS,
	PATRONAGE,
	EDUCATION,
	DOCTRINE,

	GUNPOWDER,
	COMPANIES,
	FINANCE,
	CARTOGRAPHY,
	HUMANITIES,
	PRINTING,
	JUDICIARY,

	FIREARMS,
	LOGISTICS,
	EXPLORATION,
	OPTICS,
	ACADEMIA,
	STATECRAFT,
	HERITAGE,

	COMBINED_ARMS,
	ECONOMICS,
	GEOGRAPHY,
	SCIENTIFIC_METHOD,
	URBAN_PLANNING,
	CIVIL_LIBERTIES,
	HORTICULTURE,

	REPLACEABLE_PARTS,
	HYDRAULICS,
	PHYSICS,
	GEOLOGY,
	MEASUREMENT,
	SOCIOLOGY,
	SOCIAL_CONTRACT,

	MACHINE_TOOLS,
	THERMODYNAMICS,
	METALLURGY,
	CHEMISTRY,
	BIOLOGY,
	REPRESENTATION,
	NATIONALISM,

	BALLISTICS,
	ENGINE,
	RAILROAD,
	ELECTRICITY,
	REFRIGERATION,
	LABOUR_UNIONS,
	JOURNALISM,

	PNEUMATICS,
	ASSEMBLY_LINE,
	REFINING,
	FILM,
	MICROBIOLOGY,
	CONSUMERISM,
	CIVIL_RIGHTS,

	INFRASTRUCTURE,
	FLIGHT,
	SYNTHETICS,
	RADIO,
	PSYCHOLOGY,
	MACROECONOMICS,
	SOCIAL_SERVICES,

	AVIATION,
	ROCKETRY,
	FISSION,
	ELECTRONICS,
	TELEVISION,
	POWER_PROJECTION,
	GLOBALISM,

	RADAR,
	SPACEFLIGHT,
	NUCLEAR_POWER,
	LASER,
	COMPUTERS,
	TOURISM,
	ECOLOGY,

	AERODYNAMICS,
	SATELLITES,
	SUPERCONDUCTORS,
	ROBOTICS,
	TELECOMMUNICATIONS,
	RENEWABLE_ENERGY,
	GENETICS,

	SUPERMATERIALS,
	FUSION,
	NANTECHNOLOGY,
	AUTOMATION,
	BIOTECHNOLOGY,

	UNIFIED_THEORY,
	ARTIFICIAL_INTELLIGENCE,

	TRANSHUMANISM,
};

enum DoCBuildings
{
	TRADING_COMPANY = BEGIN_WONDERS,
	IBERIAN_TRADING_COMPANY, 
	NATIONAL_MONUMENT, 
	NATIONAL_THEATRE, 
	NATIONAL_GALLERY, 
	NATIONAL_COLLEGE, 
	MILITARY_ACADEMY,
	SECRET_SERVICE, 

	IRONWORKS, 
	RED_CROSS, 
	NATIONAL_PARK, 
	CENTRAL_BANK, 
	SPACEPORT,
	GREAT_SPHINX, 
	PYRAMIDS, 
	ORACLE, 
	GREAT_WALL, 
	ISHTAR_GATE, 

	TERRACOTTA_ARMY, 
	HANGING_GARDENS, 
	GREAT_COTHON, 
	DUJIANGYAN, 
	APADANA_PALACE, 
	COLOSSUS, 
	STATUE_OF_ZEUS, 
	GREAT_MAUSOLEUM, 
	PARTHENON, 
	TEMPLE_OF_ARTEMIS, 

	GREAT_LIGHTHOUSE, 
	MOAI_STATUES, 
	COLOSSEUM, 
	AQUA_APPIA, 
	AL_KHAZNEH, 
	TEMPLE_OF_KUKULKAN, 
	MACHU_PICCHU, 
	GREAT_LIBRARY, 
	FLOATING_GARDENS, 
	GONDESHAPUR, 

	JETAVANAMARAYA,
	NALANDA, 
	THEODOSIAN_WALLS, 
	HAGIA_SOPHIA, 
	BOROBUDUR, 
	MEZQUITA, 
	SHWEDAGON_PAYA, 
	MOUNT_ATHOS, 
	IRON_PILLAR, 
	PRAMBANAN, 

	SALSAL_BUDDHA, 
	CHEOMSEONGDAE, 
	HIMEJI_CASTLE, 
	GRAND_CANAL, 
	WAT_PREAH_PISNULOK, 
	KHAJURAHO, 
	SPIRAL_MINARET, 
	DOME_OF_THE_ROCK, 
	HOUSE_OF_WISDOM, 
	KRAK_DES_CHEVALIERS,

	MONOLITHIC_CHURCH, 
	UNIVERSITY_OF_SANKORE, 
	NOTRE_DAME, 
	OLD_SYNAGOGUE, 
	SAINT_SOPHIA, 
	SILVER_TREE_FOUNTAIN, 
	SANTA_MARIA_DEL_FIORE, 
	ALAMUT, 
	SAN_MARCO_BASILICA, 
	SISTINE_CHAPEL, 

	PORCELAIN_TOWER,
	TOPKAPI_PALACE, 
	KREMLIN, 
	SAINT_THOMAS_CHURCH, 
	VIJAYA_STAMBHA, 
	GUR_E_AMIR, 
	RED_FORT, 
	TAJ_MAHAL, 
	FORBIDDEN_PALACE, 
	VERSAILLES, 

	BLUE_MOSQUE,
	ESCORIAL, 
	TORRE_DE_BELEM, 
	POTALA_PALACE, 
	OXFORD_UNIVERSITY, 
	HARMANDIR_SAHIB, 
	SAINT_BASILS_CATHEDRAL, 
	BOURSE, 
	ITSUKUSHIMA_SHRINE, 
	IMAGE_OF_THE_WORLD_SQUARE, 

	LOUVRE,
	EMERALD_BUDDHA, 
	SHALIMAR_GARDENS, 
	TRAFALGAR_SQUARE, 
	HERMITAGE, 
	GUADALUPE_BASILICA, 
	SALT_CATHEDRAL, 
	AMBER_ROOM, 
	STATUE_OF_LIBERTY, 
	BRANDENBURG_GATE, 

	ABBEY_MILLS,
	BELL_ROCK_LIGHTHOUSE, 
	CHAPULTEPEC_CASTLE,
	EIFFEL_TOWER, 
	WESTMINSTER_PALACE, 
	TRIUMPHAL_ARCH, 
	MENLO_PARK, 
	CRYSTAL_PALACE, 
	TSUKIJI_FISH_MARKET, 
	BROOKLYN_BRIDGE, 

	HOLLYWOOD, 
	EMPIRE_STATE_BUILDING,
	LAS_LAJAS_SANCTUARY, 
	PALACE_OF_NATIONS, 
	MOLE_ANTONELLIANA, 
	NEUSCHWANSTEIN, 
	FRONTENAC,
	WEMBLEY, 
	LUBYANKA, 
	CRISTO_REDENTOR, 

	METROPOLITAIN, 
	NOBEL_PRIZE, 
	GOLDEN_GATE_BRIDGE, 
	BLETCHLEY_PARK, 
	SAGRADA_FAMILIA, 
	CERN, 
	ITAIPU_DAM, 
	GRACELAND, 
	CN_TOWER, 
	PENTAGON, 

	UNITED_NATIONS, 
	CRYSTAL_CATHEDRAL, 
	MOTHERLAND_CALLS,
	BERLAYMONT, 
	WORLD_TRADE_CENTER, 
	ATOMIUM, 
	IRON_DOME, 
	HARBOUR_OPERA, 
	LOTUS_TEMPLE, 
	GLOBAL_SEED_VAULT, 

	GARDENS_BY_THE_BAY, 
	BURJ_KHALIFA, 
	HUBBLE_SPACE_TELESCOPE,
	CHANNEL_TUNNEL, 
	SKYTREE, 
	ORIENTAL_PEARL_TOWER, 
	DELTA_WORKS, 
	SPACE_ELEVATOR, 
	LARGE_HADRON_COLLIDER, 
	ITER
};

enum DoCEras
{
	ERA_ANCIENT,
	ERA_CLASSICAL,
	ERA_MEDIEVAL,
	ERA_RENAISSANCE,
	ERA_INDUSTRIAL,
	ERA_GLOBAL,
	ERA_DIGITAL,
	ERA_MIDDLE_EAST,
	ERA_EAST_ASIA,
	ERA_SOUTH_ASIA,
	ERA_NATIVE_AMERICA,
};

enum Regions
{
	REGION_BRITAIN,
	REGION_IRELAND,
	REGION_FRANCE,
	REGION_IBERIA,
	REGION_ITALY,
	REGION_LOWER_GERMANY,
	REGION_CENTRAL_EUROPE,
	REGION_BALKANS,
	REGION_GREECE,
	REGION_POLAND,
	REGION_BALTICS,
	REGION_SCANDINAVIA,
	REGION_RUTHENIA,
	REGION_PONTIC_STEPPE,
	REGION_EUROPEAN_ARCTIC,
	REGION_URALS,
	REGION_ANATOLIA,
	REGION_CAUCASUS,
	REGION_LEVANT,
	REGION_MESOPOTAMIA,
	REGION_ARABIA,
	REGION_EGYPT,
	REGION_NUBIA,
	REGION_MAGHREB,
	REGION_PERSIA,
	REGION_KHORASAN,
	REGION_TRANSOXIANA,
	REGION_SINDH,
	REGION_PUNJAB,
	REGION_RAJPUTANA,
	REGION_HINDUSTAN,
	REGION_BENGAL,
	REGION_DECCAN,
	REGION_DRAVIDA,
	REGION_INDOCHINA,
	REGION_INDONESIA,
	REGION_PHILIPPINES,
	REGION_SOUTH_CHINA,
	REGION_NORTH_CHINA,
	REGION_KOREA,
	REGION_JAPAN,
	REGION_TIBET,
	REGION_TARIM_BASIN,
	REGION_MONGOLIA,
	REGION_MANCHURIA,
	REGION_AMUR,
	REGION_CENTRAL_ASIAN_STEPPE,
	REGION_SIBERIA,
	REGION_AUSTRALIA,
	REGION_OCEANIA,
	REGION_ETHIOPIA,
	REGION_HORN_OF_AFRICA,
	REGION_SWAHILI_COAST,
	REGION_GREAT_LAKES,
	REGION_ZAMBEZI,
	REGION_MADAGASCAR,
	REGION_CAPE,
	REGION_KALAHARI,
	REGION_CONGO,
	REGION_GUINEA,
	REGION_SAHEL,
	REGION_SAHARA,
	REGION_ATLANTIC_SEABOARD,
	REGION_DEEP_SOUTH,
	REGION_MIDWEST,
	REGION_GREAT_PLAINS,
	REGION_ARIDOAMERICA,
	REGION_CALIFORNIA,
	REGION_CASCADIA,
	REGION_ONTARIO,
	REGION_QUEBEC,
	REGION_MARITIMES,
	REGION_AMERICAN_ARCTIC,
	REGION_CARIBBEAN,
	REGION_MESOAMERICA,
	REGION_CENTRAL_AMERICA,
	REGION_NEW_GRANADA,
	REGION_ANDES,
	REGION_AMAZONIA,
	REGION_BRAZIL,
	REGION_SOUTHERN_CONE,
	REGION_ANTARCTICA,
	NUM_REGIONS,
};

enum RegionGroup
{
	NO_REGION_GROUP = -1,
	REGION_GROUP_NORTH_AMERICA,
	REGION_GROUP_SOUTH_AMERICA,
	REGION_GROUP_EUROPE,
	REGION_GROUP_MIDDLE_EAST,
	REGION_GROUP_NORTH_AFRICA,
	REGION_GROUP_SUB_SAHARAN_AFRICA,
	REGION_GROUP_SOUTH_ASIA,
	REGION_GROUP_NORTH_ASIA,
	REGION_GROUP_EAST_ASIA,
	REGION_GROUP_OCEANIA,
	NUM_REGION_GROUPS,
};

enum ECSArtStyles
{
	ARTSTYLE_AFRICA,
	ARTSTYLE_ANGLO_AMERICA,
	ARTSTYLE_ARABIA,
	ARTSTYLE_ASIA,
	ARTSTYLE_BARBARIAN,
	ARTSTYLE_CRESCENT,
	ARTSTYLE_EGYPT,
	ARTSTYLE_EUROPE,
	ARTSTYLE_GRECO_ROMAN,
	ARTSTYLE_INDIA,
	ARTSTYLE_IBERIA,
	ARTSTYLE_JAPAN,
	ARTSTYLE_MESO_AMERICA,
	ARTSTYLE_MONGOLIA,
	ARTSTYLE_NATIVE_AMERICA,
	ARTSTYLE_NORSE,
	ARTSTYLE_RUSSIA,
	ARTSTYLE_SOUTH_AMERICA,
	ARTSTYLE_SOUTH_EAST_ASIA,
	ARTSTYLE_SOUTH_PACIFIC,
};

#endif	// CVRHYES_H

static const int lTechLeaderPenalty[NUM_ERAS] = {0, 0, 20, 25, 30, 40, 50};
static const int lTechBackwardsBonus[NUM_ERAS] = {0, 20, 30, 40, 50, 60, 75};

// Leoreth: order of persecution
static const int persecutionOrder[NUM_RELIGIONS][NUM_RELIGIONS-1] = 
{
	// Judaism
	{HINDUISM, BUDDHISM, TAOISM, CONFUCIANISM, ZOROASTRIANISM, ISLAM, PROTESTANTISM, CATHOLICISM, ORTHODOXY},
	// Orthodoxy
	{ISLAM, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Catholicism
	{ISLAM, PROTESTANTISM, ORTHODOXY, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Protestantism
	{ISLAM, CATHOLICISM, ORTHODOXY, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Islam
	{ZOROASTRIANISM, HINDUISM, PROTESTANTISM, CATHOLICISM, ORTHODOXY, JUDAISM, BUDDHISM, CONFUCIANISM, TAOISM},
	// Hinduism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, CONFUCIANISM, TAOISM, ZOROASTRIANISM, BUDDHISM},
	// Buddhism
	{ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, TAOISM, ISLAM, CONFUCIANISM, HINDUISM},
	// Confucianism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, TAOISM},
	// Taoism
	{ISLAM, ORTHODOXY, PROTESTANTISM, CATHOLICISM, JUDAISM, ZOROASTRIANISM, HINDUISM, BUDDHISM, CONFUCIANISM},
	// Zoroastrianism
	{ISLAM, PROTESTANTISM, CATHOLICISM, ORTHODOXY, JUDAISM, HINDUISM, BUDDHISM, CONFUCIANISM, TAOISM},
};

// Leoreth: persecution priority
static const int persecutionValue[NUM_RELIGIONS][NUM_RELIGIONS] =
{
	// JUD ORT CAT PRO ISL HIN BUD CON TAO ZOR
	{  -1,  1,  1,  1,  1,  1,  1,  1,  1,  1 }, // Judaism
	{   1, -1,  3,  3,  4,  1,  1,  1,  1,  2 }, // Orthodoxy
	{   2,  2, -1,  3,  4,  1,  1,  1,  1,  2 }, // Catholicism
	{   3,  2,  3, -1,  4,  1,  1,  1,  1,  2 }, // Protestantism
	{   1,  2,  2,  2, -1,  3,  1,  1,  1,  4 }, // Islam
	{   1,  3,  3,  3,  4, -1,  0,  1,  1,  2 }, // Hinduism
	{   1,  3,  3,  3,  4,  0, -1,  1,  1,  2 }, // Buddhism
	{   1,  2,  2,  2,  3,  1,  1, -1,  0,  1 }, // Confucianism
	{   1,  2,  2,  2,  3,  1,  1,  0, -1,  1 }, // Taoism
	{   1,  3,  3,  3,  4,  1,  1,  1,  1, -1 }, // Zoroastrianism
};