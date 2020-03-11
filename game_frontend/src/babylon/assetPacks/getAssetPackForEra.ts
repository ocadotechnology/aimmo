import AssetPack from './assetPack'
import FutureAssetPack from './future'
import PreHistoryAssetPack from './preHistory'
import { Scene } from 'babylonjs'

export default function getAssetPackForEra (era: string, scene: Scene): AssetPack {
  switch (era) {
    case 'future':
      return new FutureAssetPack(era, scene)
    case 'prehistory':
      return new PreHistoryAssetPack(era, scene)
    default:
      return new AssetPack(era, scene)
  }
}
