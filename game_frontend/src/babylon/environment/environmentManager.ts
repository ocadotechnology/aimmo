import Camera from './camera'
import Light from './light'
import Terrain from './terrain'
import { Environment } from './environment'

export default class EnvironmentManager {
    camera: Camera
    light: Light
    terrain: Terrain
    environment: Environment

    constructor (environment: Environment): void {
      this.environment = environment

      this.camera = new Camera(environment)
      this.light = new Light(environment)
      this.terrain = new Terrain(environment)
    }

    windowResized = () => {
      this.camera.computeCameraView(this.environment.canvas)
    }
}
