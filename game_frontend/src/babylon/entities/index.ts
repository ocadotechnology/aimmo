import { Scene, Engine, TransformNode } from 'babylonjs'
import Obstacles from './obstacles'

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


    onSceneMount(): void {
        this.obstacles = new Obstacles()

        this.obstacles.onSceneMount(this.scene)
    }

    onGameStateUpdate(gameState: any, onTerrainNode: TransformNode): void {
        this.obstacles.onGameStateUpdate(gameState, onTerrainNode)
    }
}
