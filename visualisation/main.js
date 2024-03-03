import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow, { formatStringIndent } from "./TennentsFlow.js";
import TennentsFlowSocket from './sockets.js';

// ==== Startup ====

if ( WebGL.isWebGLAvailable() ) {
	const flow = new TennentsFlow();
    await flow.loadModels();

    const sockets = new TennentsFlowSocket(flow);
}

else {
	const warning = WebGL.getWebGLErrorMessage();
    alert("WebGL not working innit.")
}