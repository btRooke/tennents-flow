import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow from "./TennentsFlow.js";

// ==== Startup ====

if ( WebGL.isWebGLAvailable() ) {

	const flow = new TennentsFlow();
    await flow.loadModels();

    flow.addPub("Aikmans", -1, -1);
    flow.addPub("Whey Pat", 1, 1);
    flow.addPub("The Keys", 0, 0);
    
}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}