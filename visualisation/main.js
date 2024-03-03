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

    setTimeout(() => {
        flow.moveActors("Toastie Bar", "Greyfriars Inn", 5);
        inc();
    }, 10000);

}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}