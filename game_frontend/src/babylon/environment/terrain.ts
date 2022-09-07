import { GameNode } from '../interfaces'
import { TransformNode } from 'babylonjs'
import AssetPack from '../assetPacks/assetPack'

export default class Terrain implements GameNode {
  object: any
  assetPack: AssetPack

  constructor(assetPack: AssetPack) {
    this.assetPack = assetPack

    this.object = new TransformNode('Terrain', this.assetPack.scene)

    assetPack.createGridOverlay(this.object)
    assetPack.createTerrain(this.object)
  }
}
