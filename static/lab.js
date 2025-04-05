function turnOn(number) {
    turnLight(number, true);
    return false;
}

function turnOff(number) {
    turnLight(number, false);
    return false;
}

function turnLight(num, state) {
    var url = LIGHT_URL.replace("%s", num) + "?state=" + state;
    $.get(url).done(parseStatus);
}

function clean() {
	clearInterval(STATUS_INTERVAL);
	clearInterval(TIME_LEFT);
    $("#panel").hide();
    $("#timer").text("session is over");
}
//Switches
function parseStatus(newStatus) {
    if (newStatus.error == false) {
        for (var i = 0; i < 16; i++) { 
            if(newStatus.lights["light-" + i]) {
                $("#light_" + i + "_off").hide();
                $("#light_" + i + "_on").show();
            } else {
                $("#light_" + i + "_on").hide();
                $("#light_" + i + "_off").show();
            }
        }
        if (TIMER_INTERVAL == null) {
            TIME_LEFT = Math.round(newStatus.time_left);
            $("#timer").text("" + TIME_LEFT + " seconds");
            TIMER_INTERVAL = setInterval(function () {
                TIME_LEFT = TIME_LEFT - 1;
                if (TIME_LEFT >= 0) {
                    $("#timer").text("" + TIME_LEFT + " seconds");
                } else {
                    clean();
                }
            }, 1000);
        }
    } else {
        clean();
    }
}
//
// Buttons
function sendPulse(pin_id) {
    var url = "/pulse/" + pin_id;
    $.get(url).done(function(response) {
        console.log("Pulse sent to pin", pin_id);
    }).fail(function() {
        console.log("Error sending pulse to pin", pin_id);
    });
}
//

var STATUS_INTERVAL = setInterval(function () {

    $.get(STATUS_URL).done(parseStatus).fail(clean);

}, 1000);

$.get(STATUS_URL).done(parseStatus);

var TIMER_INTERVAL = null;
var TIME_LEFT = null;