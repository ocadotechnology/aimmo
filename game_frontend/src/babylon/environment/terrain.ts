import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from './environment'

export default class Terrain implements GameNode {
    object: any;

    constructor (environment: Environment) {
      const gridOverlay = BABYLON.Mesh.CreateTiledGround('overlay', -15, -15, 16, 16, { w: 31, h: 31 }, { w: 1, h: 1 }, environment.scene)
      const gridMat = new BABYLON.StandardMaterial('Terrain', environment.scene)
      gridMat.diffuseColor = new BABYLON.Color3(0, 0, 0)
      gridMat.specularColor = new BABYLON.Color3(0, 0, 0)
      gridMat.ambientColor = BABYLON.Color3.White()
      gridMat.opacityTexture = new BABYLON.Texture('/static/babylon/terrain/grid.png', environment.scene);
      gridOverlay.material = gridMat

      var tileSize = 31

      if (environment.timeline === 'prehistory') {
        tileSize = 1
      }
      
      const ground = BABYLON.Mesh.CreateTiledGround('terrain', -15, -15, 16, 16, { w: tileSize, h: tileSize}, { w: 1, h: 1 }, environment.scene)
      this.object = ground

      const mat = new BABYLON.StandardMaterial('Terrain', environment.scene)
      const textureUrl = '/static/babylon/terrain/ground_' + environment.timeline + '.jpg'

      mat.useReflectionOverAlpha = false
      mat.diffuseTexture = new BABYLON.Texture(textureUrl, environment.scene)
      mat.diffuseTexture.level = 1.2
      mat.specularColor = new BABYLON.Color3(0, 0, 0)
      mat.ambientColor = BABYLON.Color3.White()
      this.object.material = mat
    }
}
