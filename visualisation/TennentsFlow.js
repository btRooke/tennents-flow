import * as THREE from "three";
import { FlyControls } from "three/addons/controls/FlyControls.js";
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export default class TennentsFlow {

    constructor() {

        // ==== Scene ====

        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xAFF8E6)

        // test

        this.addRenderer();
        this.addCamera();
        this.addLand();
        this.addAxes();
        this.addLighting();
        this.addPub();

        // clock 

        this.clock = new THREE.Clock()

        // start anim

        this.animate();


    }

    animate() {
        const delta = this.clock.getDelta();
        requestAnimationFrame(() => this.animate());
        this.flyControls.update(delta);
        this.renderer.render(this.scene, this.camera);
    }

    addRenderer() {
        const windowScale = 0.8;

        this.renderer = new THREE.WebGLRenderer({
            antialias: true
        });

        this.renderer.setSize(
            window.innerWidth  * windowScale,
            window.innerHeight * windowScale
        );

        document.body.appendChild(this.renderer.domElement);
    }

    addCamera() {
        // ==== Camera ====

        this.camera = new THREE.PerspectiveCamera(
            75, // field of view
            window.innerWidth / window.innerHeight, // aspect ratio
            0.1, // near clip
            1000 // far clip
        );

        this.flyControls = new FlyControls(this.camera, document.body);
        this.flyControls.dragToLook = true;
        this.flyControls.rollSpeed = 0.5;

        this.camera.position.y = 3;
        this.camera.lookAt(0, 0, 0);
    }

    addPub() {
        
        // ==== GLTF Loader ====

        const loader = new GLTFLoader();

        loader.load(

            // resource URL
            "assets/cartoon_pub.glb",

            // called when the resource is loaded
            (gltf) => {
                const boundingBox = new THREE.Box3().setFromObject(gltf.scene);
                gltf.scene.scale.setScalar(1/Object.values(boundingBox.max).sort()[0]); // normalise to 1 unit
                gltf.scene.position.set(-1, -1.008, -1);
                this.scene.add(gltf.scene);
            },

            // called while loading is progressing
            (xhr) => {
                console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
            },

            // called when loading has errors
            (error) => {
                console.log(error);
            }
        );

        // TODO sort this out

    }

    addLighting() {

        // ==== Lighting ====

        const light = new THREE.AmbientLight( 0xFFFFFF ); // soft white light
        this.scene.add(light);

    }

    addLand() {

        // ==== Land ====

        const planeSize = 10;
        const plane = {
            geometry: new THREE.PlaneGeometry(planeSize, planeSize)
                        .rotateX(Math.PI/2)
                        .translate(0, -1, 0),

            material: new THREE.MeshBasicMaterial({ color: 0x03B003, side: THREE.DoubleSide })
        }

        this.scene.add(new THREE.Mesh(plane.geometry, plane.material));

    }

    addAxes() {

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

        this.scene.add(xLine);
        this.scene.add(yLine);
        this.scene.add(zLine);
        
    }

    

}