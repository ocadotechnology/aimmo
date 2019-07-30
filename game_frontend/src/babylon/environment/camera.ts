import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import EnvironmentRenderer from '.'

const ZOOM_LOWER_BOUND = 5
const ZOOM_UPPER_BOUND = 15

export default class Camera implements GameNode {
    object: any;
    frustum: number;
    zoom_factor: number;

    setup(environmentRenderer: EnvironmentRenderer): void {
        const camera = new BABYLON.ArcRotateCamera('camera1', 0, 0.785, 50, BABYLON.Vector3.Zero(), environmentRenderer.scene)
        this.frustum = 7.5
        this.zoom_factor = 0
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

        camera.attachControl(environmentRenderer.canvas, true, false, 0)

        this.computeCameraView(environmentRenderer.canvas)

        this.addZoomListener(environmentRenderer.scene, environmentRenderer.canvas)
    }

    addZoomListener(scene: BABYLON.Scene, canvas: HTMLCanvasElement) {
        scene.onPrePointerObservable.add((pointerInfo, eventState) => {
            var event = pointerInfo.event
            var delta = 0
            if (event.wheelDelta) {
                delta = event.wheelDelta
            } else if (event.detail) {
                delta = -event.detail
            }
            if (delta) {
                this.zoom_factor += delta / 20

                if (this.zoom_factor + this.frustum >= ZOOM_UPPER_BOUND) {
                    this.zoom_factor = ZOOM_UPPER_BOUND - this.frustum
                } else if (this.zoom_factor + this.frustum <= ZOOM_LOWER_BOUND) {
                    this.zoom_factor = ZOOM_LOWER_BOUND - this.frustum
                }

                this.computeCameraView(canvas)
                this.updatePanningSensibility()
            }
        }, BABYLON.PointerEventTypes.POINTERWHEEL, false)
    }

    updatePanningSensibility() {
        this.object.panningSensibility = -4 * (this.frustum + this.zoom_factor) + 130
    }

    computeCameraView(canvas: HTMLCanvasElement): void {
        const view = new BABYLON.Vector2(canvas.width, canvas.height)
        view.normalize()

        this.object.orthoTop = (this.frustum + this.zoom_factor) * view.y
        this.object.orthoBottom = -(this.frustum + this.zoom_factor) * view.y
        this.object.orthoLeft = -(this.frustum + this.zoom_factor) * view.x
        this.object.orthoRight = (this.frustum + this.zoom_factor) * view.x
    }

    onGameStateUpdate(): void { }
}