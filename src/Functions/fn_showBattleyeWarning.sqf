diag_log 'show battle eye warning';
[] spawn {
	sleep 1;

	DBMU_is_battleye_off = uiNamespace getVariable ["DBMU_is_battleye_off", false];

	if(DBMU_is_battleye_off == true) exitwith {
		diag_log format ['DBMU_is_battleye_off: %1', DBMU_is_battleye_off];
	};

	sleep 1;
	diag_log format ['DBMU_is_battleye_off: %1', DBMU_is_battleye_off];
	diag_log 'show popup';
	private _result = ["Has Battleye been deactivated?"] call BIS_fnc_guiMessage;
	uiNamespace setVariable ["DBMU_is_battleye_off", true];
};
