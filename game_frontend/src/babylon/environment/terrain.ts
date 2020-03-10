import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from './environment'
import { AssetSomethingPack } from '../assetPack'

export default class Terrain implements GameNode {
    object: any;
    assetPack: AssetSomethingPack

    constructor (environment: Environment) {
      this.assetPack = new AssetSomethingPack(environment.era)

      const gridOverlay = BABYLON.Mesh.CreateTiledGround(this.assetPack.grid.name, -15, -15, 16, 16, this.assetPack.grid.tileSize, { w: 1, h: 1 }, environment.scene)
      const gridMat = new BABYLON.StandardMaterial(this.assetPack.grid.materialName, environment.scene)
      gridMat.diffuseColor = new BABYLON.Color3(0, 0, 0)
      gridMat.specularColor = new BABYLON.Color3(0, 0, 0)
      gridMat.ambientColor = BABYLON.Color3.White()
      gridMat.opacityTexture = new BABYLON.Texture(this.assetPack.grid.textureURL, environment.scene)
      gridOverlay.material = gridMat

      this.object = BABYLON.Mesh.CreateTiledGround(this.assetPack.terrain.name, -15, -15, 16, 16, this.assetPack.terrain.tileSize, { w: 1, h: 1 }, environment.scene)

      const mat = new BABYLON.StandardMaterial(this.assetPack.terrain.materialName, environment.scene)

      mat.useReflectionOverAlpha = false
      mat.diffuseTexture = new BABYLON.Texture(this.assetPack.terrain.textureURL, environment.scene)
      mat.diffuseTexture.level = 1.2
      mat.specularColor = new BABYLON.Color3(0, 0, 0)
      mat.ambientColor = BABYLON.Color3.White()
      this.object.material = mat
    }
}
