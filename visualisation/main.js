import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow from "./TennentsFlow.js";
import TennentsFlowSocket from './sockets.js';

// ==== Startup ====
let socket;
let flow;
let i = 1;

function inc() {
    flow.displayRevenue("Vic St Andrews", i++);
    setTimeout(() => inc(), 1000);
}

let tickPeriod = 0;

function setTickPeriod(period) {
    tickPeriod = period;
    document.querySelector("#tickRate").innerText = `Tick Rate: ${tickPeriod}`
}

if ( WebGL.isWebGLAvailable() ) {

    setTickPeriod(2200);
    flow = new TennentsFlow();
    await flow.loadModels();
    socket = new TennentsFlowSocket(flow);
    let trigger = () => {
        socket.sendNextStep();
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

    });

}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}