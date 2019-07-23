import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'

const ZOOM_LOWER_BOUND = 5
const ZOOM_UPPER_BOUND = 15

export default class Camera implements GameNode {
    object: any;
    frustum: number;

    onSceneMount(scene: BABYLON.Scene, canvas: HTMLCanvasElement, engine: BABYLON.Engine): void {
        const camera = new BABYLON.ArcRotateCamera('camera1', 0, 0.785, 50, BABYLON.Vector3.Zero(), scene)
        this.frustum = 7.5
        this.object = camera

        camera.mode = BABYLON.Camera.ORTHOGRAPHIC_CAMERA
        camera.orthoTop = 5
        camera.orthoBottom = -5
        camera.orthoLeft = -5
        camera.orthoRight = 5
        camera.upperAlphaLimit = -(3 * Math.PI) / 4
        camera.lowerAlphaLimit = -(3 * Math.PI) / 4
        camera.upperBetaLimit = Math.PI / 4
        camera.lowerBetaLimit = Math.PI / 4
        camera.upperRadiusLimit = 50
        camera.lowerRadiusLimit = 50
        camera.panningInertia = 0.2
        camera.panningSensibility = 40
        camera.angularSensibilityX = 20
        camera.angularSensibilityY = 20
        camera.panningDistanceLimit = 20

        camera.setTarget(BABYLON.Vector3.Zero())

        camera.attachControl(canvas, true, false, 0)

        this.computeCameraView(canvas)

        this.addZoomListener(scene, canvas)
    }

    addZoomListener(scene: BABYLON.Scene, canvas: HTMLCanvasElement) {
        scene.onPrePointerObservable.add((pointerInfo, eventState) => {
            // console.log(pointerInfo);
            var event = pointerInfo.event
            var delta = 0
            if (event.wheelDelta) {
                delta = event.wheelDelta
            } else if (event.detail) {
                delta = -event.detail
            }
            if (delta) {
                if (this.frustum + (delta / 10) > ZOOM_LOWER_BOUND &&
                    this.frustum + (delta / 10) < ZOOM_UPPER_BOUND) {
                    this.frustum += delta / 10
                }

                this.computeCameraView(canvas)
                this.updatePanningSensibility()
            }
        }, BABYLON.PointerEventTypes.POINTERWHEEL, false)
    }

    updatePanningSensibility() {
        this.object.panningSensibility = -6 * this.frustum + 130
    }

    computeCameraView(canvas: HTMLCanvasElement): void {
        const view = new BABYLON.Vector2(canvas.width, canvas.height)
        view.normalize()

        this.object.orthoTop = this.frustum * view.y
        this.object.orthoBottom = -this.frustum * view.y
        this.object.orthoLeft = -this.frustum * view.x
        this.object.orthoRight = this.frustum * view.x
    }

    onGameStateUpdate(): void { }
}