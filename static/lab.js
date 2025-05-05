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

//Clean the laborarory once the sesion is over
function clean() {
	clearInterval(STATUS_INTERVAL);
	clearInterval(TIMER_INTERVAL);
    $("#panel").hide();
    $("#timer").text("Session is over");

    document.getElementById("main-layout").style.display = "none";
    document.getElementById("presentation").style.display = "none";
    document.getElementById("timeout-message").style.display = "block";
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

//Upload bitstream
document.getElementById("bitstream-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const res = await fetch("/upload-bitstream", {
        method: "POST",
        body: formData
    });
    const data = await res.json();

    const mensajeDiv = document.getElementById("bitstream-message");
    mensajeDiv.textContent = data.mensaje;
    mensajeDiv.className = data.ok ? "alert alert-success" : "alert alert-danger";
});