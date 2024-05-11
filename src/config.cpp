class CfgPatches
{
	class DarkbelgsMuses
	{
		name = "Darkbelgs Muses";
		author = "Darkbelg";

		requiredVersion = 2.06;
        requiredAddons[] = {"A3_Data_F_AoW_Loadorder", "A3_Data_F_Mod_Loadorder", "cba_common", "cba_events","cba_settings","PY3_Pythia"};
		units[] = {
			"Sound_HelicopterBackgroundSoundVehicle",
		};
		weapons[] = {};

	};
};

class CfgFunctions
{
	class DarkbelgsMuses
	{
		tag= "DBMU";
		class Functions
		{
            file = "darkbelgs_muses\Functions";
			class createAsync{};
			class pipeline{};
			class startRecording{};
			class stopRecording{};
			class setInstructions{};
			class setCallback{};
			class showBattleyeWarning{
				postInit = 1;
			};
			class setOpenAIKey{
				// postInit = 1;
			};
			class toggleMicIcon{};
			class init{
				preInit = 1
			};
		};

		class Settings {
			file = "darkbelgs_muses\Functions\Settings";
			class addSettings {
				preInit = 1;
			};
		};

		class Sound {
			file = "darkbelgs_muses\Functions\Sound";
			class playBeep {};
			class backgroundHelicopter{};	
		};
	};
};

class CfgUserActions
{
	class DBMU_TalkAction
	{
		displayName = "Hold button for when talking on the radio";
		tooltip = "Hold button for when talking on the radio";
		onActivate = "if (not alive player || is3DEN) exitWith {}; [] spawn DBMU_fnc_startRecording";
		onDeactivate = "if (not alive player || is3DEN) exitWith {}; [] spawn DBMU_fnc_stopRecording";
		modifierBlocking=0;
	};
};

class UserActionGroups
{
	class DarkbelgMusesSection // Unique classname of your category.
	{
		name = "Darkbelgs Muses"; // Display name of your category.
		isAddon = 1;
		group[] = {"DBMU_TalkAction"}; // List of all actions inside this category.
	};
};

class CfgVehicles
{
	class Sound;
	class Sound_HelicopterBackgroundSoundVehicle: Sound
	{
		sound="HelicopterBackgroundSounds";
		_generalMacro="Sound_HelicopterBackgroundSoundVehicle";
		scope=2;
		displayName="Helicopter background noise";
	};
};

class CfgSFX
{
	access=1;
	class HelicopterBackgroundSounds
	{
		sounds[] = { "helicopter1", "helicopter2", "helicopter3", "helicopter4", "helicopter5" };
		helicopter1[] = { "\darkbelgs_muses\Functions\Sound\Media\helicopter1.ogg", db-10, 1.0, 1000, 0.2, 0, 0, 0 };
		helicopter2[] = { "\darkbelgs_muses\Functions\Sound\Media\helicopter2.ogg", db-10, 1.0, 1000, 0.2, 0, 0, 0 };
		helicopter3[] = { "\darkbelgs_muses\Functions\Sound\Media\helicopter3.ogg", db-10, 1.0, 1000, 0.2, 0, 0, 0 };
		helicopter4[] = { "\darkbelgs_muses\Functions\Sound\Media\helicopter4.ogg", db-10, 1.0, 1000, 0.2, 0, 0, 0 };
		helicopter5[] = { "\darkbelgs_muses\Functions\Sound\Media\helicopter5.ogg", db-10, 1.0, 1000, 0.2, 0, 0, 0 };
		empty[] = { "", 0, 0, 0, 0, 0, 0, 0 };
	};
};

