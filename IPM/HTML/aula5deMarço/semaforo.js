const lightState = {
    redOn: true,
    yellowOn: false,
    greenOn: false,
    next: function () {
        if (this.redOn) {
            this.redOn = false;
            this.greenOn = true;
        } else if (this.greenOn) {
            this.greenOn = false;
            this.yellowOn = true;
        } else if (this.yellowOn) {
            this.yellowOn = false;
            this.redOn = true;
        }
    }
};

function updateUI() {
    document.getElementById('red').style.backgroundColor = lightState.redOn ? 'red' : 'black';
    document.getElementById('yellow').style.backgroundColor = lightState.yellowOn ? 'yellow' : 'black';
    document.getElementById('green').style.backgroundColor = lightState.greenOn ? 'green' : 'black';
}

// Inicializar la UI
document.addEventListener("DOMContentLoaded", function () {
    updateUI();
    document.getElementById('changeLight').addEventListener('click', function () {
        lightState.next();
        updateUI();
    });
});
