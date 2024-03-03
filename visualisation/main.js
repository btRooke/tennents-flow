import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow from "./TennentsFlow.js";
import TennentsFlowSocket from './sockets.js';

// ==== Startup ====
let socket;
let flow;
let i = 1;

let tickPeriod = 0;
let paused = false;
let tickCount = 0;

function setTickPeriod(period) {
    tickPeriod = period;
    document.querySelector("#tickRate").innerText = `Tick Rate: ${tickPeriod}`
}

function addMinutes(date, minutes) {
    return new Date(date.getTime() + minutes*60000);
}

if ( WebGL.isWebGLAvailable() ) {
    setTickPeriod(2200);
    flow = new TennentsFlow();
    await flow.loadModels();
    socket = new TennentsFlowSocket(flow);

    let trigger = () => {
        if (paused) {
            return;
        }

        document.querySelector('#tickCount').innerText = `Tick Count: ${++tickCount}`;
        socket.sendNextStep();

        const date = new Date();
        date.setHours(18, 0, 0, 0);

        document.querySelector('#time').innerText = `Time: ${addMinutes(date, tickCount).toLocaleTimeString()}`;
        setTimeout(trigger, tickPeriod);
    }

    setTimeout(trigger, tickPeriod);

    // buttons
    document.querySelector("#slowDown").addEventListener("click", () => {
        setTickPeriod(tickPeriod + 500);
    });

    document.querySelector("#speedUp").addEventListener("click", () => {
        if (tickPeriod <= 500) return;
        setTickPeriod(tickPeriod - 500);
    });

    document.querySelector("#playPause").addEventListener("click", () => {
        paused = !paused;
        trigger();
    });
}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}