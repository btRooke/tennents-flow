import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow from "./TennentsFlow.js";

// ==== Startup ====

if ( WebGL.isWebGLAvailable() ) {
	const flow = new TennentsFlow();
    flow.addPub(-1, -1);
    flow.addPub(1, 1);
    flow.addPub(0, 0);
}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}