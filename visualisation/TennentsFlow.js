import * as THREE from "three";
import { FlyControls } from "three/addons/controls/FlyControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { FontLoader } from "three/addons/loaders/FontLoader.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";

function quaternionFromYAngle(angle) {
    const quat = new THREE.Quaternion();
    return quat.setFromAxisAngle(new THREE.Vector3( 0, 1, 0 ), angle);
}

export default class TennentsFlow {

    constructor() {

        this.signs = [];
        this.mixers = [];

        this.#addClock();
        this.#addScene();
        this.#addRenderer();
        this.#addCamera();
        this.#addLand();
        this.#addAxes();
        this.#addLighting();
        this.#animate();
    }

    async loadModels() {
        this.models = await this.#loadPubModels();
        this.fonts = await this.#loadFonts();
    }

    #loadFonts() {

        return new Promise((res, rej) => {

            const loader = new FontLoader();

            loader.load(

                "fonts/concert_one.json",

                (font) => {

                    res({
                        default: {
                            font: font,
                            size: 0.2,
                            height: 0.04,
                            curveSegments: 12,
                            bevelEnabled: true,
                            bevelThickness: 0,
                            bevelSize: 0,
                            bevelOffset: 0,
                            bevelSegments: 5
                        }
                    });

                }


            );

        });

    }

    addPub(pubName, x, z) {

        // adding the pub model

        const newPub = this.models.small.clone();
        newPub.position.setX(x);
        newPub.position.setZ(z);
        this.scene.add(newPub);

        // adding its name

        const rotationTrack = new THREE.QuaternionKeyframeTrack(
            ".quaternion", [0, 5, 10], [
                quaternionFromYAngle(0).toArray(),
                quaternionFromYAngle(Math.PI).toArray(),
                quaternionFromYAngle(Math.PI*2).toArray()
            ].flat()
        );

        const bobTrack = new THREE.VectorKeyframeTrack(
            ".position", [0, 1, 2], [x, 0, z, x, 0.3, z, x, 0, z]
        );

        const clip = new THREE.AnimationClip(
            "pubNameBob",
            -1, // -1 means auto
            [bobTrack, rotationTrack]
        );

        const name = {
            geometry: new TextGeometry(pubName, this.fonts.default).center(),
            material: new THREE.MeshBasicMaterial({ color: 0x0E0E0E })
        }

        const nameMesh = new THREE.Mesh(name.geometry, name.material);

        const mixer = new THREE.AnimationMixer(nameMesh);

        this.mixers.push(mixer);
        const action = mixer.clipAction(clip);
        action.setEffectiveTimeScale(0.5);
        action.play();

        nameMesh.position.setX(x);
        nameMesh.position.setZ(z);

        this.signs.push(nameMesh);
        this.scene.add(nameMesh);


    }

    #addScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xAFF8E6);
    }

    #addClock() {
        this.clock = new THREE.Clock();
    }

    #animate() {

        // dunno

        requestAnimationFrame(() => this.#animate());

        // fly camera shit

        const delta = this.clock.getDelta();
        this.flyControls.update(delta);

        // mixesr 

        this.mixers.forEach(mixer => {
            mixer.update(delta);
        });

        // render it

        this.renderer.render(this.scene, this.camera);
    }

    #addRenderer() {
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

    #addCamera() {
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
        this.flyControls.movementSpeed = 2;

        this.camera.position.x = 0.5;
        this.camera.position.y = 0.5;
        this.camera.position.z = 3;
        this.camera.lookAt(0, 0, 0);
    }

     #loadPubModels() {

        return new Promise(async (res, rej) => {

            const loader = new GLTFLoader();

            const pubs = [
                { file: "assets/cartoon_pub.glb", key: "default" },
                { file: "assets/small_pub.glb", key: "small" },
                { file: "assets/large_pub.glb", key: "large" },
            ];

            let loadingPromises = pubs.map(p => {

                return new Promise(res => {

                    loader.load(
                        p.file,
                        (gltf) => {
                            const pub = gltf.scene;
                            const boundingBox = new THREE.Box3().setFromObject(pub);
                            pub.scale.setScalar(1/Object.values(boundingBox.max).sort().reverse()[0]); // normalise to 1 unit
                            console.trace(pub);
                            pub.position.set(0, -1.01, 0);
                            res(pub);
                        },
                        (xhr) => {
                            console.log(`${p.file} %${(xhr.loaded/xhr.total*100)}} loaded`);
                        },
                        (error) => {
                            console.error(error);
                        }
                    );

                });

            });

            let models = {};

            for (let index in pubs) {
                models[pubs[index].key] = await loadingPromises[index];
            }

            console.log(models);

            res(models);

        });

    }

    #addLighting() {

        // ==== Lighting ====

        const light = new THREE.AmbientLight( 0xFFFFFF ); // soft white light
        this.scene.add(light);

        const pointLight = new THREE.PointLight(0xFF0000, 500, 0, 2);
        pointLight.castShadow = true;
        pointLight.position.set(5, 1, 1);
        this.scene.add(pointLight);

    }

    #addLand() {

        // ==== Land ====

        const planeSize = 21;
        const plane = {
            geometry: new THREE.PlaneGeometry(planeSize, planeSize)
                        .rotateX(Math.PI/2)
                        .translate(0, -1, 0),

            material: new THREE.MeshLambertMaterial({ color: 0x03B003, side: THREE.DoubleSide })
        }

        this.scene.add(new THREE.Mesh(plane.geometry, plane.material));

    }

    #addAxes() {

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