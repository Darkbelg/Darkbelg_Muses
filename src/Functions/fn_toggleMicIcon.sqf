disableSerialization;

// Get the display
_display = findDisplay 46;

// Check if the picture control already exists
_picCtrl = _display displayCtrl -1;

// Create the picture control
_picCtrl = _display ctrlCreate ["RscPicture", -1];

// Set the picture control's texture
_picCtrl ctrlSetText "A3\ui_f\data\igui\rscingameui\rscdisplayvoicechat\microphone_ca.paa";

_picCtrl ctrlSetPosition [safezoneX + 0.25 * safeZoneW, safezoneY + 0.75 * safeZoneH, 0.04, 0.04];
_picCtrl ctrlCommit 0;

waitUntil {is_radio_on == false};

ctrlDelete _picCtrl;

