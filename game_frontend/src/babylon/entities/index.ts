import { Scene, Engine, TransformNode } from 'babylonjs'
import Obstacle from './obstacle'
import arrayDiff from '../../babylon/helpers'

export default class EntityManager {
    scene: Scene
    engine: Engine
    canvas: HTMLCanvasElement

    obstacles: Obstacle

    constructor(canvas: HTMLCanvasElement, engine: Engine, scene: Scene) {
        this.canvas = canvas
        this.engine = engine
        this.scene = scene
    }


    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine, onTerrainNode: TransformNode): void {
        this.obstacles = new Obstacle()

        this.obstacles.onSceneMount(this.scene, canvas, engine, onTerrainNode)
    }

    onGameStateUpdate(prevGameState: any, currGameState: any): void {
        var prevObstacleList = []
        if (prevGameState) {
            prevObstacleList = prevGameState.obstacles
        }
        const obstacleDiff = arrayDiff(prevObstacleList, currGameState.obstacles)
        this.obstacles.onGameStateUpdate(obstacleDiff)
    }
}
