import AssetPack from './assetPack'
import FutureAssetPack from './future'
import PreHistoryAssetPack from './preHistory'
import AncientAssetPack from './ancient'
import ModernAssetPack from './modern'
import WrongFutureAssetPack from './wrongFuture'
import { Scene } from 'babylonjs'

export default function getAssetPackForEra(era: string, scene: Scene): AssetPack {
  switch (era) {
    case 'future':
      return new FutureAssetPack(era, scene)
    case 'prehistory':
      return new PreHistoryAssetPack(era, scene)
    case 'ancient':
      return new AncientAssetPack(era, scene)
    case 'modern':
      return new ModernAssetPack(era, scene)
    case 'wrongfuture':
      return new WrongFutureAssetPack(era, scene)
    default:
      return new AssetPack(era, scene)
  }
}
