import Camera from './camera'
import Light from './light'
import Terrain from './terrain'
import { AssetPack } from '../assetPacks/assetPack'

export default class EnvironmentManager {
    camera: Camera
    light: Light
    terrain: Terrain
    assetPack: AssetPack

    constructor (assetPack: AssetPack) {
      this.assetPack = assetPack

      this.camera = new Camera(this.assetPack.environment)
      this.light = new Light(this.assetPack.environment)
      this.terrain = new Terrain(this.assetPack)
    }

    resizeBabylonWindow = () => {
      this.assetPack.environment.engine.resize()
      this.camera.computeCameraView(this.assetPack.environment.canvas)
    }

    centerOn (mesh: any): void {
      this.camera.centerOn(mesh)
    }

    unCenter (mesh: any): void {
      this.camera.unCenter(mesh)
    }
}
