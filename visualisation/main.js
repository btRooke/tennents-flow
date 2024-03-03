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

if ( WebGL.isWebGLAvailable() ) {
	flow = new TennentsFlow();
    await flow.loadModels();

    socket = new TennentsFlowSocket(flow);

    document.getElementById("nextStepButton").onclick = e => socket.sendNextStep();
    setTimeout(() => {
        flow.moveActors("Vic St Andrews", "The Rule", 5);
        inc();
    }
        , 10000);

}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}