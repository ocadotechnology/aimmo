import Obstacle from './obstacle'
import diff from '../diff'
import { Environment } from '../environment/environment'
import Interactable from './interactable'
import Avatar from './avatar'

export default class EntityManager {
  environment: Environment

  obstacles: Obstacle
  interactables: Interactable
  avatars: Avatar

  constructor (environment: Environment) {
    this.environment = environment
  }

  setup (): void {
    this.obstacles = new Obstacle()
    this.interactables = new Interactable()
    this.avatars = new Avatar()

    this.obstacles.setup(this.environment)
    this.interactables.setup(this.environment)
    this.avatars.setup(this.environment)
  }

  onGameStateUpdate (previousGameState: any, currentGameState: any): void {
    var previousObstacleList = []
    var previousInteractableList = []
    var previousAvaterList = []

    if (previousGameState) {
      previousObstacleList = previousGameState.obstacles
      previousInteractableList = previousGameState.interactables
      previousAvaterList = previousGameState.players
    }

    const obstacleDiff = diff(previousObstacleList, currentGameState.obstacles)
    const interactableDiff = diff(previousInteractableList, currentGameState.interactables)
    const avatarDiff = diff(previousAvaterList, currentGameState.players)

    this.obstacles.onGameStateUpdate(obstacleDiff)
    this.interactables.onGameStateUpdate(interactableDiff)
    this.avatars.onGameStateUpdate(avatarDiff)
  }
}
