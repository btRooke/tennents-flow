import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow from "./TennentsFlow.js";
import TennentsFlowSocket from './sockets.js';

// ==== Startup ====
let socket;

if ( WebGL.isWebGLAvailable() ) {
	const flow = new TennentsFlow();
    await flow.loadModels();

    socket = new TennentsFlowSocket(flow);

    document.getElementById("nextStepButton").onclick = e => socket.sendNextStep();
} else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}