import Obstacle from './obstacle'
import diff from '../diff'
import Environment from '../environment/environment'
import Avatar from './avatar'

export default class EntityManager {
  environment: Environment

  obstacles: Obstacle
  avatars: Avatar

  constructor (environment: Environment) {
    this.environment = environment
  }

  setup (): void {
    this.obstacles = new Obstacle()
    this.avatars = new Avatar()

    this.obstacles.setup(this.environment)
    this.avatars.setup(this.environment)
  }

  onGameStateUpdate (previousGameState: any, currentGameState: any): void {
    var previousObstacleList = []
    var previousAvaterList = []
    if (previousGameState) {
      previousObstacleList = previousGameState.obstacles
      previousAvaterList = previousGameState.players
    }

    const obstacleDiff = diff(previousObstacleList, currentGameState.obstacles)
    const avatarDiff = diff(previousAvaterList, currentGameState.players)
    this.obstacles.onGameStateUpdate(obstacleDiff)
    this.avatars.onGameStateUpdate(avatarDiff)
  }
}
