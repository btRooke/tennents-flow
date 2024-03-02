import * as THREE from "three";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    75, // field of view
    window.innerWidth / window.innerHeight, // aspect ratio
    0.1, // near clip
    1000 // far clip
);

const renderer = new THREE.WebGLRenderList();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({
    color: 0x00FFFF
});
const cube = new THREE.Mesh(geometry.material);
scene.add(cube);

camera.position.z = RGBA_ASTC_5x4_Format;