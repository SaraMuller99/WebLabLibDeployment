//----------------------------------Frontend---------------------------------- 

//TURN ON AND OFF SWITCHES
//Turn switch on
function turnOn(number) {
    turnswitch(number, true);
    return false;
}
//Turn switch off
function turnOff(number) {
    turnswitch(number, false);
    return false;
}
//Send petition to backend to change switch status
function turnswitch(num, state) {
    var url = switch_URL.replace("%s", num) + "?state=" + state;
    $.get(url).done(parseStatus);
}

// BUTTONS
//Simulate the pulsation by sending a pulse
function sendPulse(pin_id) {
    var url = "/pulse/" + pin_id;
    $.get(url).done(function(response) {
        console.log("Pulse sent to pin", pin_id);
    }).fail(function() {
        console.log("Error sending pulse to pin", pin_id);
    });
}

//UPLOAD BITSTREAM
//Finds the html element and execute the function when the form is submit
document.getElementById("bitstream-form").addEventListener("submit", async function (e) {
    e.preventDefault(); //Avoid page reloading
    const formData = new FormData(this); //Represent the uploaded .bit
    const res = await fetch("/upload-bitstream", {
        method: "POST",
        body: formData
    });
    const data = await res.json(); //Wait till response from server

    const mensajeDiv = document.getElementById("bitstream-message"); //Finds div
    mensajeDiv.textContent = data.mensaje; //Save rensponse in div
    mensajeDiv.className = data.ok ? "alert alert-success" : "alert alert-danger"; //Shows message
});

//TIME
//Timer variables 
var TIMER_INTERVAL = null;
var TIME_LEFT = null;
//Set laboratory state actualization interval in ms
var STATUS_INTERVAL = setInterval(function () {
    //Clean if error
    $.get(STATUS_URL).done(parseStatus).fail(clean);
}, 1000);
//Get status when load the script
$.get(STATUS_URL).done(parseStatus);

//SINCHRONIZATION
//Synchronizes the frontend with the actual FPGA status
function parseStatus(newStatus) {
    if (newStatus.error == false) {
        //Get the state from the backend (json) and hide/shows the correct switch image
        for (var i = 0; i < 16; i++) { 
            if(newStatus.sw["switch-" + i]) {
                $("#switch_" + i + "_off").hide();
                $("#switch_" + i + "_on").show();
            } else {
                $("#switch_" + i + "_on").hide();
                $("#switch_" + i + "_off").show();
            }
        }
        if (TIMER_INTERVAL == null) {
            //Get time left from backend (json) and shows it
            TIME_LEFT = Math.round(newStatus.time_left);
            $("#timer").text("" + TIME_LEFT + " seconds");
            TIMER_INTERVAL = setInterval(function () {
                TIME_LEFT = TIME_LEFT - 1;
                if (TIME_LEFT >= 0) {
                    $("#timer").text("" + TIME_LEFT + " seconds");
                } else {
                    clean(); //When time=0 close laboratory 
                }
            }, 1000); //Update every second 
        }
    } else {
        clean();
    }
}

//CLEANING
//Clean the laborarory once the sesion is over
function clean() {
	clearInterval(STATUS_INTERVAL);
	clearInterval(TIMER_INTERVAL);
    $("#panel").hide();
    $("#timer").text("Session is over");

    //Hide elements and shows end message
    document.getElementById("main-layout").style.display = "none";
    document.getElementById("presentation").style.display = "none";
    document.getElementById("timeout-message").style.display = "block";
}

