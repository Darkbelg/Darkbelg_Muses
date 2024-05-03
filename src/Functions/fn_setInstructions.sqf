params ["_systemChat"];
diag_log "setting custom instructions";
["record.set_instructions", [_systemChat]] call py3_fnc_callExtension;
