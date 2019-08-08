import ObstacleManager from './obstacleManager'
import diff from '../diff'
import { Environment } from '../environment/environment'
import InteractableManager from './interactableManager'
import AvatarManager from './avatarManager'

export default class EntityManager {
  environment: Environment

  obstacles: ObstacleManager
  interactables: InteractableManager
  avatars: AvatarManager

  constructor (environment: Environment) {
    this.environment = environment
  }

  setup (): void {
    this.obstacles = new ObstacleManager()
    this.interactables = new InteractableManager()
    this.avatars = new AvatarManager()

    this.obstacles.setup(this.environment)
    this.interactables.setup(this.environment)
    this.avatars.setup(this.environment)
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

    this.obstacles.handleDifferences(obstacleDiff)
    this.interactables.handleDifferences(interactableDiff)
    this.avatars.handleDifferences(avatarDiff)
  }
}
