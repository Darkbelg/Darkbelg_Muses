// diag_log "stop recording";
DBMU_is_radio_on = false;
// diag_log format ["stop recording %1", DBMU_is_radio_on];
// [] spawn DBMU_fnc_toggleMicIcon;
[] call DBMU_fnc_playBeep;