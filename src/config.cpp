class CfgPatches
{
	class DarkbelgsMuses
	{
		name = "Darkbelgs Muses";
		author = "Darkbelg";

		requiredVersion = 2.06;
        requiredAddons[] = {"A3_Data_F_AoW_Loadorder", "A3_Data_F_Mod_Loadorder", "cba_common", "cba_events","cba_settings","PY3_Pythia"};
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
            file = "darkbelgs_muses\Functions";
			is_radio_on = false;
			callback_chat_gpt = nill;
			class createAsync{};
			class pipeline{};
			class startRecording{};
			class stopRecording{};
			class setInstructions{};
			class setCallback{};
			class setOpenAIKey{
				postInit = 1;
			};
			class toggleMicIcon{};
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

