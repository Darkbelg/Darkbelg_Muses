params ["_command"];
diag_log "create async";
diag_log format ["thread command: %1", _command];

private _thread_id = [_command, []] call py3_fnc_callExtension;

diag_log format ["thread id: %1", _thread_id];

// diag_log format ["%1",["thread_example.has_call_finished", [_thread_id]] call py3_fnc_callExtension];

// while {
// 	! (["thread_example.has_call_finished", [_thread_id]] call py3_fnc_callExtension)
// } do {
// 	systemChat format ["%1",["thread_example.has_call_finished", [_thread_id]] call py3_fnc_callExtension];
// 	sleep 1;
// };

waitUntil { ["record.has_call_finished", [_thread_id]] call py3_fnc_callExtension};

_response = ["record.get_call_value", [_thread_id]] call py3_fnc_callExtension;

// systemChat format ["Debug: %1: %2",str _response, count _response];

if(str _response find "start recording" >= 0) then {
	// systemChat format ["%1",_response];
};

if(str _response find "stop recording" >= 0) then {
	// systemChat format ["%1",_response];
};

if(str _response find "complete transcription" >= 0) then {
	// systemChat format ["%1",_response#0];
	player sideChat format ["%1", _response#1];
};

if(str _response find "complete communication chatGPT" >= 0) then {
	if(not (isNil "callback_chat_gpt")) exitWith{
		[_response] spawn callback_chat_gpt;
	};

	diag_log format ["Execute this: %1", _response];
	// systemChat format ["%1",_response#0];
	// he_fak sideChat format ["%1", _response#1];

	// _coordinatesArr = parseSimpleArray (_response#1);
	_coordinatesArr = _response#1;
	// systemChat format ["call: %1", _coordinatesArr#0];
	// systemChat format ["X: %1", _coordinatesArr#1];
	// systemChat format ["Y: %1", _coordinatesArr#2];
	_xCoordinate = ((parseNumber(_coordinatesArr#1)) * 100);
	_yCoordinate = ((parseNumber(_coordinatesArr#2)) * 100);
	_myNearestEnemy = player findNearestEnemy [_xCoordinate, _yCoordinate];
	_nearestEnemyPosition = [_xCoordinate, _yCoordinate,0];

	diag_log format ["_myNearestEnemy:%1", str _myNearestEnemy];

	if ( not (isNull _myNearestEnemy) && getPosASL _myNearestEnemy distance2D  [_xCoordinate, _yCoordinate] <= 100) then {
		_nearestEnemyPosition = getPosATL _myNearestEnemy;
	};
	// [_response#1] spawn rhinoIsGo;

	diag_log format ["_nearestEnemyPosition:%1", _nearestEnemyPosition];

	if((str (_coordinatesArr)) find "vn_fnc_artillery_arc_light" > -1) then {
		he_fak sideChat format ["%1", _coordinatesArr#3];
		
		[_nearestEnemyPosition, objNull, _nearestEnemyPosition] spawn VN_fnc_artillery_arc_light;

		// _code = compile (_response#1);
		// [] spawn _code;
	};

	if((str (_coordinatesArr)) find "vn_fnc_artillery_plane" > -1) then {
		he_fak sideChat format ["%1", _coordinatesArr#3];
		// systemChat format ["%1:%2",_xCoordinate,_yCoordinate];
		// systemChat format ["%1",_nearestEnemyPosition];
		vn_artillery_captive = false;
		[0, configfile >> "CfgVehicles" >> "vn_b_air_f4b_navy_at", "vn_b_air_f4b_navy_at", _nearestEnemyPosition, _nearestEnemyPosition vectorAdd [100,100,0], 0, [_coordinatesArr#4], objNull, 0] spawn VN_fnc_artillery_plane;

		// _code = compile (_response#1);
		// [] spawn _code;
	};

	if((str (_coordinatesArr)) find "vn_fnc_artillery_heli" > -1) then {
		he_fak sideChat format ["%1", _coordinatesArr#3];
		// systemChat format ["%1:%2",_xCoordinate,_yCoordinate];
		// systemChat format ["%1",_nearestEnemyPosition];
		vn_artillery_captive = false;
		[0, configfile >> "CfgVehicles" >> "vn_b_air_uh1c_01_03", "vn_b_air_uh1c_01_03", _nearestEnemyPosition, _nearestEnemyPosition vectorAdd [100,100,0],0,[_coordinatesArr#4],objNull,0] spawn VN_fnc_artillery_heli;
		
		// _code = compile (_response#1);
		// [] spawn _code;
	};
};
// if(count _response < 1) then {
// 	systemChat format ["%1",_response];
// };

// if(count _response < 2) then {
// 	systemChat format ["%1",_response#0];
// };

// if(count _response < 3) then {
// 	systemChat format ["%1",_response#0];
// 	player sideChat format ["%1", _response#1];
// };

