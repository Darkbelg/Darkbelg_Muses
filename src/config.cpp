class CfgPatches
{
	class DarkbelgsMuses
	{
		name = "Darkbelgs Muses";
		author = "Darkbelg";

		requiredVersion = 2.06;
        requiredAddons[] = {"A3_Data_F_AoW_Loadorder", "A3_Data_F_Mod_Loadorder", "cba_common", "cba_events","cba_settings"};
		units[] = {};
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
            file = "src\Functions";
			isRadioOn = false;
			class createAsync{};
			class pipeline{};
			class startRecording{};
			class stopRecording{};
			class setOpenAIKey{
				postInit = 1;
			};
		};

		class Settings {
			file = "src\Functions\Settings";
			class addSettings {
				preInit = 1;
			};
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
