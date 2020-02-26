import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from './environment'

export default class Terrain implements GameNode {
    object: any;

    constructor (environment: Environment) {
      const grid_overlay = BABYLON.Mesh.CreateTiledGround('overlay', -15, -15, 16, 16, { w: 31, h: 31 }, { w: 1, h: 1 }, environment.scene)
      const grid_mat = new BABYLON.StandardMaterial('Terrain', environment.scene)
      grid_mat.diffuseColor = new BABYLON.Color3(0, 0, 0)
      grid_mat.specularColor = new BABYLON.Color3(0, 0, 0)
      grid_mat.ambientColor = BABYLON.Color3.White()
      grid_mat.opacityTexture = new BABYLON.Texture('/static/babylon/terrain/grid.png', environment.scene);
      grid_overlay.material = grid_mat

      const ground = BABYLON.Mesh.CreateTiledGround('terrain', -15, -15, 16, 16, { w: 1, h: 1}, { w: 1, h: 1 }, environment.scene)
      this.object = ground

      const mat = new BABYLON.StandardMaterial('Terrain', environment.scene)
      const texture_url = '/static/babylon/terrain/ground_' + environment.timeline + '.jpg'

      mat.useReflectionOverAlpha = false
      mat.diffuseTexture = new BABYLON.Texture(texture_url, environment.scene)
      mat.diffuseTexture.level = 1.2
      mat.specularColor = new BABYLON.Color3(0, 0, 0)
      mat.ambientColor = BABYLON.Color3.White()
      ground.material = mat
    }
}
