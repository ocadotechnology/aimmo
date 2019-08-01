import Camera from './camera'
import Light from './light'
import Terrain from './terrain'
import Environment from './environment'

export default class EnvironmentManager {
    camera: Camera
    light: Light
    terrain: Terrain
    environment: Environment

    setup (environment: Environment): void {
      this.environment = environment

      this.camera = new Camera()
      this.light = new Light()
      this.terrain = new Terrain()

      this.camera.setup(environment)
      this.light.setup(environment)
      this.terrain.setup(environment)
    }

    windowResized = () => {
      this.camera.computeCameraView(this.environment.canvas)
    }
}
