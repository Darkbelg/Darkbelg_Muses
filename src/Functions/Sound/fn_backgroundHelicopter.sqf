// playSound3D [format ["\darkbelgs_muses\Functions\Sound\Media\helicopter%1.ogg", ceil(random 5)], player, true, getPosASL player, 1, 1, 0];
// diag_log "Play helicopter sound";
private _helicopterSound = createSoundSource ["Sound_HelicopterBackgroundSoundVehicle", position player, [], 0];
// systemChat format ["_helicopterSound %1", _helicopterSound];
// diag_log format ["%1", DBMU_is_fak_responding];
waitUntil { DBMU_is_fak_responding; };
// diag_log "stop helicopter sound";
deleteVehicle _helicopterSound;
DBMU_is_fak_responding = false;