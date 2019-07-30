import { Scene, Engine } from 'babylonjs'
import Camera from './camera'
import Light from './light'
import Terrain from './terrain'

export default class Environment {
    scene: Scene
    engine: Engine
    canvas: HTMLCanvasElement

    camera: Camera
    light: Light
    terrain: Terrain

    constructor(canvas: HTMLCanvasElement) {
        this.canvas = canvas
    }


    setup(): void {
        this.engine = new Engine(
            this.canvas,
            true,
            {},
            true
        )

        this.scene = new Scene(this.engine)

        this.camera = new Camera()
        this.light = new Light()
        this.terrain = new Terrain()

        this.camera.setup(this)
        this.light.setup(this)
        this.terrain.setup(this)

        this.engine.runRenderLoop(() => {
            this.scene.render()
        })
    }

    windowResized = () => {
        this.engine.resize()
        this.camera.computeCameraView(this.canvas)
    }
}
