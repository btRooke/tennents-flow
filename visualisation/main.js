import * as THREE from "three";
import { FlyControls } from "three/addons/controls/FlyControls.js";
import WebGL from 'three/addons/capabilities/WebGL.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// ==== Scene ====

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xAFF8E6)

// ==== Renderer ====

const windowScale = 0.8;

const renderer = new THREE.WebGLRenderer({
    antialias: true
});
renderer.setSize(
    window.innerWidth  * windowScale,
    window.innerHeight * windowScale
);

document.body.appendChild(renderer.domElement);

// ==== Camera ====

const camera = new THREE.PerspectiveCamera(
    75, // field of view
    window.innerWidth / window.innerHeight, // aspect ratio
    0.1, // near clip
    1000 // far clip
);

let fly = new FlyControls(camera, document.body);
fly.dragToLook = true;
fly.rollSpeed = 0.5;

camera.position.y = 1;
camera.position.z = 5;
camera.position.x = 1;
camera.lookAt(0, 0, 0);

// ==== Axes ====

const xAxis = [
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(1, 0, 0)
];

const xColour = new THREE.LineBasicMaterial({ color: 0xFF0000 });

const yAxis = [
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(0, 1, 0)
];

const yColour = new THREE.LineBasicMaterial({ color: 0x00FF00 });

const zAxis = [
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(0, 0, 1)
];

const zColour = new THREE.LineBasicMaterial({ color: 0x0000FF });

const xLineGeom = new THREE.BufferGeometry().setFromPoints(xAxis);
const yLineGeom = new THREE.BufferGeometry().setFromPoints(yAxis);
const zLineGeom = new THREE.BufferGeometry().setFromPoints(zAxis);

const xLine = new THREE.Line(xLineGeom, xColour);
const yLine = new THREE.Line(yLineGeom, yColour);
const zLine = new THREE.Line(zLineGeom, zColour);

scene.add(xLine);
scene.add(yLine);
scene.add(zLine);

// ==== Land ====

const planeSize = 10;
const plane = {
    geometry: new THREE.PlaneGeometry(planeSize, planeSize)
                .rotateX(Math.PI/2)
                .translate(0, -1, 0),

    material: new THREE.MeshBasicMaterial({ color: 0x03B003, side: THREE.DoubleSide })
}

scene.add(new THREE.Mesh(plane.geometry, plane.material));

// ==== Lighting ====

const light = new THREE.AmbientLight( 0xFFFFFF ); // soft white light
scene.add(light);

// ==== GLTF Loader ====

const loader = new GLTFLoader();

loader.load(

	// resource URL
	"assets/cartoon_pub.glb",

	// called when the resource is loaded
	function (gltf) {
        const boundingBox = new THREE.Box3().setFromObject(gltf.scene);
        gltf.scene.scale.setScalar(1/Object.values(boundingBox.max).sort()[0]); // normalise to 1 unit
        gltf.scene.position.set(-1, -1, -1);
        scene.add(gltf.scene);
	},

	// called while loading is progressing
	function ( xhr ) {
		console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
	},

	// called when loading has errors
	function ( error ) {
		console.log(error);
	}
);

// ==== Animation ====

const clock = new THREE.Clock()

function animate() {

    const delta = clock.getDelta();
    requestAnimationFrame(animate);
    fly.update(delta);
    renderer.render(scene, camera);

}

// ==== Startup ====

if ( WebGL.isWebGLAvailable() ) {
	animate();
} else {
	const warning = WebGL.getWebGLErrorMessage();
	document.getElementById( 'container' ).appendChild( warning );
}