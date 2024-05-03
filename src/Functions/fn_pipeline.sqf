_scriptHandle = ["record.startRecordAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle && is_radio_on == false };
_scriptHandle = ["record.stopRecordAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle };
_scriptHandle = ["record.transcribe_audioAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle };
_scriptHandle = ["record.chat_with_gptAsync"] spawn DBMU_fnc_createAsync;
waitUntil { scriptDone _scriptHandle };
_scriptHandle = ["record.text_to_speechAsync"] spawn DBMU_fnc_createAsync;
