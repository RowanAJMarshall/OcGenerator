
var metronome = null;
function playSound() {
    // File sourced from http://soundbible.com/2044-Tick.html under the MIT Attribution 3.0 licence
    // https://creativecommons.org/licenses/by/3.0/
    var tick = new Audio('static/tick.mp3');
    tick.play();
}

function startMetronome() {
   $("#stop").prop('disabled', false)
    $("#start").prop('disabled', true)
   var interval = 1000 * 60 / $("#bpm").val();
    console.log(interval)
    metronome = setInterval(function() { playSound() }, interval);
}

function stopMetronome() {
    $("#stop").prop('disabled', true)
    $("#start").prop('disabled', false)
    clearInterval(metronome);
    metronome = null;
}