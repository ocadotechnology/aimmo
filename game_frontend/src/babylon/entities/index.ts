import Obstacle from './obstacle'
import diff from '../diff'
import { Environment } from '../environment/environment'
import Interactable from './interactable'

export default class EntityManager {
  environment: Environment
  obstacles: Obstacle
  interactables: Interactable

  constructor (environment: Environment) {
    this.environment = environment
  }

  setup (): void {
    this.obstacles = new Obstacle()
    this.interactables = new Interactable()

    this.obstacles.setup(this.environment)
    this.interactables.setup(this.environment)
  }

  onGameStateUpdate (previousGameState: any, currentGameState: any): void {
    var previousObstacleList = []
    var previousInteractableList = []

    if (previousGameState) {
      previousObstacleList = previousGameState.obstacles
      previousInteractableList = previousGameState.interactables
    }

    const obstacleDiff = diff(previousObstacleList, currentGameState.obstacles)
    const interactableDiff = diff(previousInteractableList, currentGameState.interactables)

    this.obstacles.onGameStateUpdate(obstacleDiff)
    this.interactables.onGameStateUpdate(interactableDiff)
  }
}
