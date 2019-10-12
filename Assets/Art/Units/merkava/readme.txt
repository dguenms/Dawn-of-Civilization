Merkava

This unit is for everybody in Civ community who wants to use is some cool mod. You may change it as you like.
If you want to create your own mini mod, follow the instructions from this thread: http://forums.civfanatics.com/showthread.php?t=139721
DO NOT overwrite any of your original Civ4 files.
If you want to use alternative texture (e.g. merkava_olive.dds) you need to change its name to merkava.dds

This is how the CIV4ArtDefines_Unit.xml should look like:
		<UnitArtInfo>
			<Type>ART_DEF_UNIT_merkava</Type>
			<fScale>0.5</fScale>
			<fInterfaceScale>0.5</fInterfaceScale>
			<NIF>Art/Units/merkava/merkava.nif</NIF>
			<KFM>Art/Units/merkava/merkava.kfm</KFM>
			<SHADERNIF>Art/Units/merkava/merkava.nif</SHADERNIF>
			<ShadowDef>
				<ShadowNIF>Art/Units/01_UnitShadows/ModernArmorShadow.nif</ShadowNIF>
				<ShadowAttachNode>BIP Pelvis</ShadowAttachNode>
				<fShadowScale>0.1</fShadowScale>
			</ShadowDef>
			<iDamageStates>0</iDamageStates>
			<TrailDefinition>
				<Texture>Art/Shared/tanktread.dds</Texture>
				<fWidth>1.0</fWidth>
				<fLength>180.0</fLength>
				<fTaper>0.0</fTaper>
				<fFadeStartTime>0.2</fFadeStartTime>
				<fFadeFalloff>0.35</fFadeFalloff>
			</TrailDefinition>
			<fBattleDistance>0.5</fBattleDistance>
			<fRangedDeathTime>0.12</fRangedDeathTime>
			<bActAsRanged>1</bActAsRanged>
			<TrainSound>AS2D_UNIT_BUILD_UNIT</TrainSound>
			<AudioRunSounds>
				<AudioRunTypeLoop>LOOPSTEP_MOD_ARMOUR</AudioRunTypeLoop>
				<AudioRunTypeEnd>ENDSTEP_MOD_ARMOUR</AudioRunTypeEnd>
			</AudioRunSounds>
			<SelectionSound>AS3D_UN_MOD_ARMOUR_HEAL</SelectionSound>
			<ActionSound>AS3D_UN_MOD_ARMOUR_HEAL</ActionSound>
		</UnitArtInfo>


Model and texture made by me, based on material found on internet.
Sharick