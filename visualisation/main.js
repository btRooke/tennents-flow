import WebGL from 'three/addons/capabilities/WebGL.js';
import TennentsFlow from "./TennentsFlow.js";

// ==== Startup ====

if ( WebGL.isWebGLAvailable() ) {
	const flow = new TennentsFlow();
}

else {
	const warning = WebGL.getWebGLErrorMessage();
	document.getElementById( 'container' ).appendChild( warning );
}