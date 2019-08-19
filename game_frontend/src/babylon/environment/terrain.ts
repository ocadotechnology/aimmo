import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from './environment'

export default class Terrain implements GameNode {
    object: any;

    constructor (environment: Environment) {
      const ground = BABYLON.Mesh.CreateTiledGround('terrain', -15, -15, 16, 16, { w: 31, h: 31 }, { w: 1, h: 1 }, environment.scene)
      this.object = ground

      const mat = new BABYLON.StandardMaterial('Terrain', environment.scene)
      mat.useReflectionOverAlpha = false
      mat.diffuseTexture = new BABYLON.Texture('/static/babylon/terrain/ground_future.jpg', environment.scene)
      mat.diffuseTexture.level = 1.2
      mat.specularColor = new BABYLON.Color3(0, 0, 0)
      mat.ambientColor = BABYLON.Color3.White()
      ground.material = mat
    }
}
