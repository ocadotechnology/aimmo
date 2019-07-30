import Obstacle from './obstacle'
import diff from '../diff'
import EnvironmentRenderer from '../environment'

export default class EntityManager {
    environmentRenderer: EnvironmentRenderer

    obstacles: Obstacle

    constructor(environmentRenderer: EnvironmentRenderer) {
        this.environmentRenderer = environmentRenderer
    }


    setup(): void {
        this.obstacles = new Obstacle()

        this.obstacles.setup(this.environmentRenderer)
    }

    onGameStateUpdate(previousGameState: any, currentGameState: any): void {
        var previousObstacleList = []
        if (previousGameState) {
            previousObstacleList = previousGameState.obstacles
        }
        const obstacleDiff = diff(previousObstacleList, currentGameState.obstacles)
        this.obstacles.onGameStateUpdate(obstacleDiff)
    }
}
