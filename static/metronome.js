
var metronome = null;
function playSound() {
    var tick = new Audio('static/tick.mp3');
    tick.play();
}

function startMetronome() {
    var interval = ($("#bpm").val() / 60) * 1000;
    metronome = setInterval(function() { playSound() }, interval);
}

function stopMetronome() {
    clearInterval(metronome);
    metronome = null;
}