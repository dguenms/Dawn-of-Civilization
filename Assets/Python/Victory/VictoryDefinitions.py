from VictoryGoalDefinitions import *

import Requirements as req



### AMOUNT REQUIREMENTS ###

AverageCultureAmount = GoalDefinition(req.AverageCultureAmount)
CultureAmount = GoalDefinition(req.CultureAmount)
GoldAmount = GoalDefinition(req.GoldAmount)
ShrineIncome = GoalDefinition(req.ShrineIncome)


### BEST ENTITIES REQUIREMENTS ###

BestCultureCities = GoalDefinition(req.BestCultureCities)
BestCultureCity = GoalDefinition(req.BestCultureCity)
BestPopulationCities = GoalDefinition(req.BestPopulationCities)
BestPopulationCity = GoalDefinition(req.BestPopulationCity)
BestPopulationPlayer = GoalDefinition(req.BestPopulationPlayer)
BestSpecialistCity = GoalDefinition(req.BestSpecialistCity)
BestTechPlayer = GoalDefinition(req.BestTechPlayer)
BestTechPlayers = GoalDefinition(req.BestTechPlayers)
BestTradeIncomeCity = GoalDefinition(req.BestTradeIncomeCity)
BestWonderCity = GoalDefinition(req.BestWonderCity)


### CITY REQUIREMENTS ###

CityBuilding = GoalDefinition(req.CityBuilding)
CityCultureLevel = GoalDefinition(req.CityCultureLevel)
CityDifferentGreatPeopleCount = GoalDefinition(req.CityDifferentGreatPeopleCount)
CitySpecialistCount = GoalDefinition(req.CitySpecialistCount)


### COUNT REQUIREMENTS ###

AttitudeCount = GoalDefinition(req.AttitudeCount)
AveragePopulation = GoalDefinition(req.AveragePopulation)
BuildingCount = GoalDefinition(req.BuildingCount)
CityCount = GoalDefinition(req.CityCount)
ControlledResourceCount = GoalDefinition(req.ControlledResourceCount)
CorporationCount = GoalDefinition(req.CorporationCount)
CultureCity = GoalDefinition(req.CultureCity)
CultureLevelCityCount = GoalDefinition(req.CultureLevelCityCount)
FeatureCount = GoalDefinition(req.FeatureCount)
ImprovementCount = GoalDefinition(req.ImprovementCount)
OpenBorderCount = GoalDefinition(req.OpenBorderCount)
PeakCount = GoalDefinition(req.PeakCount)
PopulationCityCount = GoalDefinition(req.PopulationCityCount)
PopulationCount = GoalDefinition(req.PopulationCount)
ResourceCount = GoalDefinition(req.ResourceCount)
SpecialistCount = GoalDefinition(req.SpecialistCount)
TerrainCount = GoalDefinition(req.TerrainCount)
UnitCombatCount = GoalDefinition(req.UnitCombatCount)
UnitCount = GoalDefinition(req.UnitCount)
UnitLevelCount = GoalDefinition(req.UnitLevelCount)
VassalCount = GoalDefinition(req.VassalCount)


### PERCENT REQUIREMENTS ###

AreaPercent = GoalDefinition(req.AreaPercent)
AreaPopulationPercent = GoalDefinition(req.AreaPercent)
CommercePercent = GoalDefinition(req.CommercePercent)
LandPercent = GoalDefinition(req.LandPercent)
PopulationPercent = GoalDefinition(req.PopulationPercent)
PowerPercent = GoalDefinition(req.PowerPercent)
ReligionSpreadPercent = GoalDefinition(req.ReligionSpreadPercent)
ReligiousVotePercent = GoalDefinition(req.ReligiousVotePercent)


### SIMPLE REQUIREMENTS ###

AllAttitude = GoalDefinition(req.AllAttitude)
AllowNone = GoalDefinition(req.AllowNone)
AllowOnly = GoalDefinition(req.AllowOnly)
AreaNoStateReligion = GoalDefinition(req.AreaNoStateReligion)
Communist = GoalDefinition(req.Communist)
Control = GoalDefinition(req.Control)
CultureCover = GoalDefinition(req.CultureCover)
GoldPercent = GoalDefinition(req.GoldPercent)
MoreCulture = GoalDefinition(req.MoreCulture)
MoreReligion = GoalDefinition(req.MoreReligion)
NoReligionPercent = GoalDefinition(req.NoReligionPercent)
NoStateReligion = GoalDefinition(req.NoStateReligion)
Project = GoalDefinition(req.Project)
Route = GoalDefinition(req.Route)
RouteConnection = GoalDefinition(req.RouteConnection)
StateReligionPercent = GoalDefinition(req.StateReligionPercent)
TradeConnection = GoalDefinition(req.TradeConnection)
Wonder = Wonders = GoalDefinition(req.Wonder)


### STATE REQUIREMENTS ###

ContactBeforeRevealed = GoalDefinition(req.ContactBeforeRevealed)
ConvertAfterFounding = GoalDefinition(req.ConvertAfterFounding)
Discover = GoalDefinition(req.Discover)
EnterEraBefore = GoalDefinition(req.EnterEraBefore)
FirstDiscover = GoalDefinition(req.FirstDiscover)
FirstGreatPerson = GoalDefinition(req.FirstGreatPerson)
FirstSettle = GoalDefinition(req.FirstSettle)
NoCityConquered = GoalDefinition(req.NoCityConquered)
NoCityLost = GoalDefinition(req.NoCityLost)
Settle = GoalDefinition(req.Settle)
TradeMission = GoalDefinition(req.TradeMission)


### TRACK REQUIREMENTS ###

AcquiredCities = GoalDefinition(req.AcquiredCities)
BrokeredPeace = GoalDefinition(req.BrokeredPeace)
CelebrateTurns = GoalDefinition(req.CelebrateTurns)
CombatFood = GoalDefinition(req.CombatFood)
ConqueredCities = GoalDefinition(req.ConqueredCities)
EnslaveCount = GoalDefinition(req.EnslaveCount)
EraFirstDiscover = GoalDefinition(req.EraFirstDiscover)
GoldenAges = GoalDefinition(req.GoldenAges)
GreatGenerals = GoalDefinition(req.GreatGenerals)
HappiestTurns = GoalDefinition(req.HappiestTurns)
HealthiestTurns = GoalDefinition(req.HealthiestTurns)
PeaceTurns = GoalDefinition(req.PeaceTurns)
PillageCount = GoalDefinition(req.PillageCount)
PiracyGold = GoalDefinition(req.PiracyGold)
PopeTurns = GoalDefinition(req.PopeTurns)
RaidGold = GoalDefinition(req.RaidGold)
RazeCount = GoalDefinition(req.RazeCount)
ResourceTradeGold = GoalDefinition(req.ResourceTradeGold)
SacrificeHappiness = GoalDefinition(req.SacrificeHappiness)
SettledCities = GoalDefinition(req.SacrificeHappiness)
SlaveTradeGold = GoalDefinition(req.SlaveTradeGold)
SunkShips = GoalDefinition(req.SunkShips)
TradeGold = GoalDefinition(req.TradeGold)


### ARGUMENTS ###

plots_ = plots
plots = AreaArgumentFactory()

civs = CivsArgument

city_ = city
city = LocationCityArgument

capital_ = capital
capital = CapitalCityArgument