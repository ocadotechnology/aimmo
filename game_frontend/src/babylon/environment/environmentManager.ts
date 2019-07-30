import Camera from './camera'
import Light from './light'
import Terrain from './terrain'
import EnvironmentRenderer from '.';

export default class EnvironmentManager {
    camera: Camera
    light: Light
    terrain: Terrain
    environmentRenderer: EnvironmentRenderer

    setup(environmentRenderer: EnvironmentRenderer): void {
        this.environmentRenderer = environmentRenderer

        this.camera = new Camera()
        this.light = new Light()
        this.terrain = new Terrain()

        this.camera.setup(environmentRenderer)
        this.light.setup(environmentRenderer)
        this.terrain.setup(environmentRenderer)
    }

    windowResized = () => {
        this.camera.computeCameraView(this.environmentRenderer.canvas)
    }
}

