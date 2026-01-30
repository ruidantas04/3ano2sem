/* Este documento apresenta uma solução em construção. É fornecido como 
   material de estudo. Recomenda-se que o revejam e melhorem conforme 
   forem adquirindo novos conhecimentos. */

// Traffic lights v.2025
// App attributes and methods
const app= Vue.createApp({
    data() {
        return {
            redOn: true,
            yellowOn: false,
            greenOn: false,
            auto: null,
            intervalo: null
        }
    },
    methods: {
        stepLights() {
            this.yellowOn = this.greenOn;
            this.greenOn = this.redOn;
            this.redOn =!(this.greenOn || this.yellowOn);
        },
        toggleAuto() {
            if (this.auto) {
                clearInterval(this.auto);
                this.auto = null;
                this.strAuto = "OFF";
            } else {
                this.auto = setInterval(() => {
                    this.stepLights();
                }, 1000);
                this.strAuto = "ON";
            }
        },
        computed : {
            strAuto() {
            if(this.auto) {
                return "ON";
            } else {    
                return "OFF";
            }
        }
        },
        watch: {
            auto(newvalue){
                if(newvalue){
                    clearInterval(this.auto);
                    this.intervalo=null;
                } else {
                    this.intervalo = setInterval(() => {
                        this.stepLights();
                    }
                    , 1000);
                }
            }
        }
    }
});

app.mount('#app');

/*
let trafficLight = {
    _redOn: true,
    _yellowOn: false,
    _greenOn: false,
    auto: null,
    // method to chamge the lights red->green->yellow->red...
    stepLights () {
        this._yellowOn = this._greenOn;
        this._greenOn = this._redOn;
        this._redOn = !(this._greenOn || this._yellowOn);
    }
}

// GUI updating
// we opted for checking that the elemnts with the red, yellow and green IDs exist
function updateUI() {
    const red = document.getElementById('red');
    const yellow = document.getElementById('yellow');
    const green = document.getElementById('green');

    if (trafficLight._redOn && red && yellow) {
        red.classList.add('vermelhoon');
        yellow.classList.remove('amareloon');
    } else if (trafficLight._yellowOn && yellow && green) {
        yellow.classList.add('amareloon');
        green.classList.remove('verdeon');
    } else if (trafficLight._greenOn && green && red) {
        green.classList.add('verdeon');
        red.classList.remove('vermelhoon');
    }
}

// Setup app GUI
document.addEventListener('DOMContentLoaded', function () {
    const mudarbtn = document.getElementById('mudar');
    const pararbtn = document.getElementById('auto');
    // button to step the traffic lights
    if (mudarbtn) {
        mudarbtn.onclick = function() {
            trafficLight.stepLights();
            updateUI();
        };
    }
    // turning test mode on/off
    if (pararbtn) {
        pararbtn.textContent = 'Modo teste: Off';
        pararbtn.onclick = function() {
            if (trafficLight.auto) {
                clearInterval(trafficLight.auto);  // stop invoking stepLights every 1s
                trafficLight.auto = null;
                pararbtn.textContent = 'Modo teste: Off';
                pararbtn.classList.remove('autoon'); // Remove active style
            } else {
                // invoke stepLights every 1s - test mode
                trafficLight.auto = setInterval(() => {
                    trafficLight.stepLights();
                    updateUI();
                }, 1000);
                pararbtn.textContent = 'Modo teste: On';
                pararbtn.classList.add('autoon'); // Apply active style
            }
        };
    }
    updateUI();
});*/