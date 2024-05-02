diag_log "start recording";
isRadioOn = true;
diag_log format ["start recording %1", isRadioOn];
[] spawn DBMU_fnc_pipeline;
