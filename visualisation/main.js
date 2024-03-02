import * as THREE from "three";

const scene = new THREE.Scene();

const windowScale = 0.75;

const camera = new THREE.PerspectiveCamera(
    75, // field of view
    window.innerWidth / window.innerHeight, // aspect ratio
    0.1, // near clip
    1000 // far clip
);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(
    window.innerWidth  * windowScale,
    window.innerHeight * windowScale
);
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({
    color: 0x00FFFF
});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

function animate() {

    requestAnimationFrame(animate);

    cube.rotation.x += 0.1;
    cube.rotation.y += 0.1;

    renderer.render(scene, camera);

}

animate();