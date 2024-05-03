diag_log "start recording";
is_radio_on = true;
diag_log format ["start recording %1", is_radio_on];
[] spawn DBMU_fnc_pipeline;
