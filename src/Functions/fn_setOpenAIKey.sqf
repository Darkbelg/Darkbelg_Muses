diag_log "check openai key";
if(DBMU_open_ai_key == "") then {
	diag_log "no openai key";
	[] spawn {
		sleep 1;
		["No OpenAI key set in the addon settings."] spawn BIS_fnc_guiMessage;
	}
} else {
	diag_log ["set open ai key to python"];
	["record.set_api_key", [DBMU_open_ai_key]] call py3_fnc_callExtension;
}