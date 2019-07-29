import { Scene, Engine, TransformNode } from 'babylonjs'
import Obstacles from './obstacles'
import arrayDiff from '../../babylon/helpers'

export default class Entities {
    scene: Scene
    engine: Engine
    canvas: HTMLCanvasElement

    obstacles: Obstacles

    constructor(canvas: HTMLCanvasElement, engine: Engine, scene: Scene) {
        this.canvas = canvas
        this.engine = engine
        this.scene = scene
    }


    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine, onTerrainNode: TransformNode): void {
        this.obstacles = new Obstacles()

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
