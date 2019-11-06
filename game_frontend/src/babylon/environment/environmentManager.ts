import Camera from './camera'
import Light from './light'
import Terrain from './terrain'
import { Environment } from './environment'

export default class EnvironmentManager {
    camera: Camera
    light: Light
    terrain: Terrain
    environment: Environment

    constructor (environment: Environment) {
      this.environment = environment

      this.camera = new Camera(environment)
      this.light = new Light(environment)
      this.terrain = new Terrain(environment)
    }

    resizeBabylonWindow = () => {
      this.environment.engine.resize()
      this.camera.computeCameraView(this.environment.canvas)
    }

    centerOn (mesh: any): void {
      this.camera.centerOn(mesh)
    }

    unCenter (mesh: any): void {
      this.camera.unCenter(mesh)
    }
}
