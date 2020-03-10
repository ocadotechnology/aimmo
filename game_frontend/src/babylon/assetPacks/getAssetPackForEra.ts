import { Environment } from '../environment/environment'
import { AssetPack } from './assetPack'
import FutureAssetPack from './future'
import PreHistoryAssetPack from './preHistory'

export default function getAssetPackForEra (era: string, environment: Environment): AssetPack {
  switch (environment.era) {
    case 'future':
      return new FutureAssetPack(environment)
    case 'prehistory':
      return new PreHistoryAssetPack(environment)
    default:
      return new AssetPack(environment)
  }
}
