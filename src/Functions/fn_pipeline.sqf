diag_log format ["pipeline %1", isRadioOn];

diag_log "start pipeline";
_scriptHandle = ["record.startRecordAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle && isRadioOn == false };
_scriptHandle = ["record.stopRecordAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle };
_scriptHandle = ["record.transcribe_audioAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle };
_scriptHandle = ["record.chat_with_gptAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle };
_scriptHandle = ["record.text_to_speechAsync"] spawn DBMU_fnc_createAsync;
diag_log "stop pipeline";
