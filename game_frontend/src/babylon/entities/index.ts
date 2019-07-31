import Obstacle from './obstacle'
import diff from '../diff'
import Environment from '../environment/environment'

export default class EntityManager {
    environment: Environment

    obstacles: Obstacle

    constructor (environment: Environment) {
      this.environment = environment
    }

    setup (): void {
      this.obstacles = new Obstacle()

      this.obstacles.setup(this.environment)
    }

    onGameStateUpdate (previousGameState: any, currentGameState: any): void {
      var previousObstacleList = []
      if (previousGameState) {
        previousObstacleList = previousGameState.obstacles
      }
      const obstacleDiff = diff(previousObstacleList, currentGameState.obstacles)
      this.obstacles.onGameStateUpdate(obstacleDiff)
    }
}
