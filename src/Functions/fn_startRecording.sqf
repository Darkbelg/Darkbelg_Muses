// diag_log "start recording";
DBMU_is_radio_on = true;
// diag_log format ["start recording %1", DBMU_is_radio_on];
[] call DBMU_fnc_playBeep;
[] spawn DBMU_fnc_toggleMicIcon;
[] spawn DBMU_fnc_pipeline;
