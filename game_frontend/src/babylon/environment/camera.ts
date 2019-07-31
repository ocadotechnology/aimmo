import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import Environment from '../environment/environment';

const ZOOM_LOWER_BOUND = 5
const ZOOM_UPPER_BOUND = 15
const ZOOM_COEFFICIENT = 20

const PANNING_SENSITITY = 6
const MAXIMUM_PANNING_SENSIBILITY = 130

export default class Camera implements GameNode {
    object: any
    frustum: number
    zoom_factor: number
    view: BABYLON.Vector2

    setup(environment: Environment): void {
        const camera = new BABYLON.ArcRotateCamera('camera1', 0, 0.785, 50, BABYLON.Vector3.Zero(), environment.scene)
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
        camera.panningInertia = 0
        camera.angularSensibilityX = 20
        camera.angularSensibilityY = 20
        camera.panningDistanceLimit = 20

        camera.setTarget(BABYLON.Vector3.Zero())

        camera.attachControl(environment.canvas, true, false, 0)

        this.updatePanningSensibility()
        this.computeCameraView(canvas)

        this.addZoomListener(environment.scene, environment.canvas)
    }

    addZoomListener(scene: BABYLON.Scene, canvas: HTMLCanvasElement) {
        scene.onPrePointerObservable.add(pointerInfo => {
            const event = pointerInfo.event instanceof WheelEvent ? pointerInfo.event : undefined
            if (event) {
                let delta = 0
                if (event.deltaY) {
                    delta = event.deltaY
                }

                if (delta) {
                    this.zoom_factor += delta / ZOOM_COEFFICIENT

                    if (this.zoom_factor + this.frustum >= ZOOM_UPPER_BOUND) {
                        this.zoom_factor = ZOOM_UPPER_BOUND - this.frustum
                    } else if (this.zoom_factor + this.frustum <= ZOOM_LOWER_BOUND) {
                        this.zoom_factor = ZOOM_LOWER_BOUND - this.frustum
                    }

                    this.computeCameraView(canvas)
                    this.updatePanningSensibility()
                }
            }
        }, BABYLON.PointerEventTypes.POINTERWHEEL, false)
    }

    updatePanningSensibility() {
        this.object.panningSensibility = -PANNING_SENSITITY
            * (this.frustum + this.zoom_factor)
            + MAXIMUM_PANNING_SENSIBILITY
    }

    computeCameraView(canvas: HTMLCanvasElement): void {
        this.view = new BABYLON.Vector2(canvas.width, canvas.height)
        this.view.normalize()

        this.object.orthoTop = (this.frustum + this.zoom_factor) * this.view.y
        this.object.orthoBottom = -(this.frustum + this.zoom_factor) * this.view.y
        this.object.orthoLeft = -(this.frustum + this.zoom_factor) * this.view.x
        this.object.orthoRight = (this.frustum + this.zoom_factor) * this.view.x
    }

    onGameStateUpdate(): void { }
}