import { Scene, Engine } from 'babylonjs'
import Obstacle from './obstacle'
import diff from '../../babylon/helpers'
import Environment from '../../babylon/environment'

export default class EntityManager {
    environment: Environment

    obstacles: Obstacle

    constructor(environment: Environment) {
        this.environment = environment
    }


    setup(): void {
        this.obstacles = new Obstacle()

        this.obstacles.setup(this.environment)
    }

    onGameStateUpdate(prevGameState: any, currGameState: any): void {
        var prevObstacleList = []
        if (prevGameState) {
            prevObstacleList = prevGameState.obstacles
        }
        const obstacleDiff = diff(prevObstacleList, currGameState.obstacles)
        this.obstacles.onGameStateUpdate(obstacleDiff)
    }
}
