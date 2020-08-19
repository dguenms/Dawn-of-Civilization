
	//CIV4EffectInfos.xml

This goes in the effects XML. Required for the flames to work.
	(\Assets\XML\Misc\CIV4EffectInfos.xml)
/////////////////////////////////////////////////////////////////////////////////////////////////

<!-- Fire_Beam:-->
		<EffectInfo>
			<Type>EFFECT_FIRE_BOLT</Type>
			<Description>Greek Fire for Dromon</Description>
			<fScale>1.5</fScale>
			<fUpdateRate>1</fUpdateRate>
			<Path>Art\Units\Dromon_Civ5/Fire_Bolt.nif</Path>
			<bIsProjectile>1</bIsProjectile>
			<fSpeed>275.0</fSpeed>
			<fArcValue>0.75</fArcValue>
		</EffectInfo>

/////////////////////////////////////////////////////////////////////////////////////////////////

	//CIV4ArtDefines_Unit.xml

//This ship requires a bit more set up in the art defines than most. As you know, ships
//usually come along side each other during combat, and exchange broadsides.
// The exception being the submarines. This is what we want to this ship to do. Here are the
//entries of interest to us:

<fExchangeAngle>0</fExchangeAngle>
// !!!This is the angle the ships do battle at. The submarine has this entry omitted entirely. Which is why
// it attacks head on. I found setting it to "0" has the same effect as deleting the entry.

<fScale>0.20</fScale>
// This is the scale I used

<iDamageStates>4</iDamageStates>
// Required for the damage textures to function.

<fBattleDistance>1.20</fBattleDistance>
// Distance battle occurs obviously. The submarine is set to ".55" I believe.

<fBankRate>.4</fBankRate>
// I don't know what this does. Submarine is set to ".2"

<bActAsRanged>1</bActAsRanged>
// Acts as a ranged unit. Doesn't really matter since all other ships are "melee", and close the distance anyway.

// Here is an example:

/////////////////////////////////////
<UnitArtInfo>
			<Type>ART_DEF_UNIT_DROMON_CIV5</Type>
			<Button>Art/Units/dromon_Civ5/dromon_but.dds</Button>
			<fScale>.20</fScale>
			<fInterfaceScale>0.5</fInterfaceScale>
			<bActAsLand>0</bActAsLand>
			<bActAsAir>0</bActAsAir>
			<NIF>Art/Units/dromon_Civ5/dromon_Civ5.nif</NIF>
			<KFM>Art/Units/dromon_Civ5/dromon_Civ5.kfm</KFM>
			<SHADERNIF>Art/Units/dromon_Civ5/dromon_Civ5.nif</SHADERNIF>
			<ShadowDef>
				<ShadowNIF>Art/Units/01_UnitShadows/CaravelShadow.nif</ShadowNIF>
				<ShadowAttachNode>BIP Pelvis</ShadowAttachNode>
				<fShadowScale>1.0</fShadowScale>
			</ShadowDef>
			<iDamageStates>4</iDamageStates>
			<TrailDefinition>
				<Texture>Art/Shared/water_ship_wake.dds</Texture>
				<fWidth>1</fWidth>
				<fLength>180.0</fLength>
				<fTaper>1</fTaper>
				<fFadeStartTime>.2</fFadeStartTime>
				<fFadeFalloff>0.35</fFadeFalloff>
			</TrailDefinition>
			<fBattleDistance>1.20</fBattleDistance>
			<fRangedDeathTime>0.31</fRangedDeathTime>
			<bSmoothMove>1</bSmoothMove>
			<fAngleInterpRate>720.0</fAngleInterpRate>
			<fBankRate>.2</fBankRate>
			<bActAsRanged>1</bActAsRanged>
			<TrainSound>AS2D_UNIT_BUILD_UNIT</TrainSound>
			<AudioRunSounds>
				<AudioRunTypeLoop>LOOPSTEP_OCEAN2</AudioRunTypeLoop>
				<AudioRunTypeEnd>ENDSTEP_OCEAN2</AudioRunTypeEnd>
			</AudioRunSounds>
			<SelectionSound>AS3D_UN_OCEAN_END1</SelectionSound>
			<ActionSound>AS3D_UN_OCEAN_END1</ActionSound>
		</UnitArtInfo>


