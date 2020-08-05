import Camera from './camera'
import Light from './light'
import Terrain from './terrain'
import AssetPack from '../assetPacks/assetPack'
import { Environment } from './environment'

export default class EnvironmentManager {
  camera: Camera
  light: Light
  terrain: Terrain
  environment: Environment
  assetPack: AssetPack

  constructor (environment: Environment, assetPack: AssetPack) {
    this.environment = environment
    this.assetPack = assetPack

    this.camera = new Camera(this.environment)
    this.light = new Light(this.environment)
    this.terrain = new Terrain(this.assetPack)

    this.setSceneBackground()
  }

  private setSceneBackground () {
    this.environment.scene.clearColor = this.assetPack.backgroundColor
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
