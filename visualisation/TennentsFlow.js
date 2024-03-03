    import * as THREE from "three";
import { FlyControls } from "three/addons/controls/FlyControls.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { FontLoader } from "three/addons/loaders/FontLoader.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";

function quaternionFromYAngle(angle) {
    const quat = new THREE.Quaternion();
    return quat.setFromAxisAngle(new THREE.Vector3( 0, 1, 0 ), angle);
}

function largest(elements) {
    let largest = -999999;

    for (let e of elements) {
        if (e > largest) {
            largest = e;
        }
    }
    return largest;
}

function smallRandom() {
    return Math.random() * 0.3 - 0.15;
}

export function formatStringIndent(inputString, maxCharacters) {
    const words = inputString.split(' ');

    let resultantString = [];
    resultantString.push("");

    for (const word of words) {
        let lastLine = resultantString[resultantString.length - 1];

        if (lastLine.length >= maxCharacters) {
            resultantString.push("");
            lastLine = resultantString[resultantString.length - 1];
        }

        if (lastLine !== "" && lastLine.length + word.length > maxCharacters) {
            resultantString.push("");
            lastLine = resultantString[resultantString.length - 1];
        }

        lastLine += `${word} `;
        resultantString[resultantString.length - 1] = lastLine;
    }

    return resultantString.map(line => {
        const l = line.replace(/~+$/, '')
        const padding = maxCharacters - l.length / 2;
        return `${" ".repeat(padding)}${l}${" ".repeat(padding)}`
    }).join("\n");
}

export default class TennentsFlow {

    constructor() {

        this.pubs = [];
        this.signs = [];
        this.mixers = [];

        this.#addClock();
        this.#addScene();
        this.#addRenderer();
        this.#addCamera();
        this.#addAxes();
        this.#addLighting();
        this.#animate();
    }

    async loadModels() {
        this.models = await this.#loadPubModels();
        this.textures = await this.#loadTextures();
        this.fonts = await this.#loadFonts();
        this.#addLand();
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
                            size: 0.12,
                            height: 0.03,
                            curveSegments: 1,
                            bevelEnabled: true,
                            bevelThickness: 0,
                            bevelSize: 0,
                            bevelOffset: 0,
                            bevelSegments: 1
                        }
                    });

                }


            );

        });

    }

    addPub(pubName, x, z, size="medium") {

        this.pubs[pubName] = [x, z];

        // adding the pub model

        const newPub = this.models[size].clone();
        newPub.position.setX(x);
        newPub.position.setZ(z);
        newPub.rotateY(Math.random() * 2 * Math.PI);
        this.scene.add(newPub);

        const pubBox = new THREE.Box3();
        pubBox.setFromObject(newPub);
        const pubHeight = pubBox.max.y - pubBox.min.y;

        // adding its name

        const randomOffset = Math.PI * 2 * Math.random();

        const rotationTrack = new THREE.QuaternionKeyframeTrack(
            ".quaternion", [0, 5, 10], [
                quaternionFromYAngle(randomOffset + 0).toArray(),
                quaternionFromYAngle(Math.PI + randomOffset).toArray(),
                quaternionFromYAngle(Math.PI*2 + randomOffset).toArray()
            ].flat()
        );

        const name = {
            geometry: new TextGeometry(formatStringIndent(pubName, 10), this.fonts.default).center(),
            material: new THREE.MeshBasicMaterial({ color: 0x0E0E0E })
        }

        const nameMesh = new THREE.Mesh(name.geometry, name.material);

        this.signs[pubName] = nameMesh;

        const box = new THREE.Box3();
        box.setFromObject(nameMesh);
        const height = box.max.y

        const bobTrack = new THREE.VectorKeyframeTrack(
            ".position", [0, 1, 2], [x, pubHeight + height - 1, z, x, pubHeight + height - 1 + 0.18, z, x, pubHeight + height - 1, z]
        );

        const clip = new THREE.AnimationClip(
            "pubNameBob",
            -1, // -1 means auto
            [bobTrack]
        );

        const spinClip = new THREE.AnimationClip(
            "pubNameSpin",
            -1,
            [rotationTrack]
        )

        const mixer = new THREE.AnimationMixer(nameMesh);

        this.mixers.push(mixer);

        mixer.clipAction(clip).play();
        mixer.clipAction(spinClip).play();

        nameMesh.position.setX(x);
        nameMesh.position.setZ(z);

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
        const windowScale = 1;

        this.renderer = new THREE.WebGLRenderer({
            antialias: true
        });

        this.renderer.setSize(
            window.innerWidth  * windowScale,
            window.innerHeight * windowScale
        );

        document.querySelector("#tfdiv").appendChild(this.renderer.domElement);
    }

    #addCamera() {
        // ==== Camera ====

        this.camera = new THREE.PerspectiveCamera(
            75, // field of view
            window.innerWidth / window.innerHeight, // aspect ratio
            0.1, // near clip
            1000 // far clip
        );

        // this.flyControls = new OrbitControls(this.camera, this.renderer.domElement);
        // this.flyControls.autoRotate = true;
        // this.camera.position.set(0, 1, 5);

        this.flyControls = new FlyControls(this.camera, document.body);
        this.flyControls.dragToLook = true;
        this.flyControls.rollSpeed = 0.8;
        this.flyControls.movementSpeed = 5;

        this.camera.position.x = 0.5;
        this.camera.position.y = 0.5;
        this.camera.position.z = 3;
        this.camera.lookAt(0, 0, 0);
    }

    #loadTextures() {

        return new Promise(async (res, rej) => {

            const loader = new THREE.TextureLoader();

            const textures = [
                { file: "assets/grass.jpg", key: "diff" },
                { file: "assets/rocks_ground_03_disp_4k.png", key: "disp" }
            ];

            let loadingPromises = textures.map(t => {

                return new Promise(res => {

                    loader.load(
                        t.file,
                        (text) => {
                            text.repeat.set(1000, 1000);
                            text.wrapS = THREE.RepeatWrapping;
                            text.wrapT = THREE.RepeatWrapping;
                            res(text);
                        },
                        (xhr) => {
                            console.log(`${t.file} ${(xhr.loaded/xhr.total*100)}% loaded`);
                        },
                        (error) => {
                            console.error(error);
                        }
                    );

                });

            });

            let loadedTextures = {};

            for (let index in textures) {
                loadedTextures[textures[index].key] = await loadingPromises[index];
            }

            res(loadedTextures);

        });

    }

     #loadPubModels() {

        return new Promise(async (res, rej) => {

            const loader = new GLTFLoader();

            const pubs = [
                { file: "assets/cartoon_pub.glb", key: "medium", scale: 0.85 },
                { file: "assets/small_pub.glb", key: "small", scale: 0.4 },
                { file: "assets/new_large_pub.glb", key: "large", scale: 0.7 },
            ];

            let loadingPromises = pubs.map(p => {

                return new Promise(res => {

                    loader.load(
                        p.file,
                        (gltf) => {
                            const pub = gltf.scene;
                            const boundingBox = new THREE.Box3().setFromObject(pub);
                            // no idea why I had to write my own function here
                            pub.scale.setScalar((1 / largest(Object.values(boundingBox.max))*p.scale)); // normalise to 1 unit
                            pub.position.set(0, -1.01, 0);
                            res(pub);
                        },
                        (xhr) => {
                            console.log(`${p.file} ${(xhr.loaded/xhr.total*100)}% loaded`);
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

            res(models);

        });

    }

    #addLighting() {
        // ==== Lighting ====
        const light = new THREE.AmbientLight( 0xFFFFFF ); // soft white light
        this.scene.add(light);

        // const pointLight = new THREE.PointLight(0xFF0000, 500, 0, 2);
        // pointLight.castShadow = true;
        // pointLight.position.set(5, 1, 1);
        // this.scene.add(pointLight);

    }

    #addLand() {

        // ==== Land ====

        const planeSize = 1000;
        const plane = {
            geometry: new THREE.PlaneGeometry(planeSize, planeSize)
                        .rotateX(Math.PI/2)
                        .translate(0, -1, 0),

            material: new THREE.MeshStandardMaterial({ map: this.textures.diff, side: THREE.DoubleSide })
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

    displayRevenue(pubName, amount) {
        const aString = ` Count: ${Number(amount)}`;
        this.signs[pubName].geometry = new TextGeometry(formatStringIndent(pubName + aString, 12), this.fonts.default).center();
    }

    moveActors(srcPub, destPub, numberActors) {

        for (let i = 0; i < numberActors; i++) {

            const sphere = {
                geometry: new THREE.SphereGeometry(0.06, 3, 3).center(),
                material: new THREE.MeshPhysicalMaterial({ color: 0x0000FF, transparent: true, opacity: 0.5 })
            };

            const height = -1 + 0.18;

            const ballMesh = new THREE.Mesh(sphere.geometry, sphere.material);

            const pubSwap = new THREE.VectorKeyframeTrack(
                ".position", [0, 2 + smallRandom() * 2], [
                    this.pubs[srcPub][0] + smallRandom(), height, this.pubs[srcPub][1] + smallRandom(),
                    this.pubs[destPub][0] + smallRandom(), height, this.pubs[destPub][1] + smallRandom()
                ]
            );

            const clip = new THREE.AnimationClip(
                "actorSwap",
                -1, // -1 means auto
                [pubSwap]
            );

            const mixer = new THREE.AnimationMixer(ballMesh);
            this.mixers.push(mixer);
            const action = mixer.clipAction(clip);
            action.loop = THREE.LoopOnce;
            action.play();
            this.scene.add(ballMesh);
            mixer.addEventListener( 'finished', (e) => {
                action.stop();
                mixer.uncacheRoot(ballMesh);
                mixer.uncacheClip(clip);
                mixer.uncacheAction(action);
                this.scene.remove(ballMesh);
            });


        }

    }

}