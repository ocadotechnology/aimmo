import ObstacleManager from './obstacleManager'
import { diff } from '../diff'
import { Environment } from '../environment/environment'
import InteractableManager from './interactableManager'
import AvatarManager from './avatarManager'
import { AssetPack, getAssetPackForEra } from '../assetPack'

export default class EntityManager {
  environment: Environment
  assetPack: AssetPack

  obstacles: ObstacleManager
  interactables: InteractableManager
  avatars: AvatarManager

  constructor (environment: Environment) {
    this.environment = environment
    this.assetPack = getAssetPackForEra(environment.era, environment)
    this.obstacles = new ObstacleManager(this.environment, this.assetPack)
    this.interactables = new InteractableManager(this.environment, this.assetPack)
    this.avatars = new AvatarManager(this.environment)
  }

  onGameStateUpdate (previousGameState: any, currentGameState: any): void {
    var previousObstacleList = []
    var previousInteractableList = []
    var previousAvatarList = []

    if (previousGameState) {
      previousObstacleList = previousGameState.obstacles
      previousInteractableList = previousGameState.interactables
      previousAvatarList = previousGameState.players
    }

    const obstacleDiff = diff(previousObstacleList, currentGameState.obstacles)
    const interactableDiff = diff(previousInteractableList, currentGameState.interactables)
    const avatarDiff = diff(previousAvatarList, currentGameState.players)

    this.obstacles.gameStateProcessor.handleDifferences(obstacleDiff)
    this.interactables.gameStateProcessor.handleDifferences(interactableDiff)
    this.avatars.gameStateProcessor.handleDifferences(avatarDiff)
  }

  setCurrentAvatarID (avatarID: number): void {
    this.avatars.setCurrentAvatarID(avatarID)
  }
}
