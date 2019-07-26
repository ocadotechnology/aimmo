import { Engine, Scene, TransformNode } from 'babylonjs'

export interface GameNode {
    object: any
    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine): void
    onGameStateUpdate(gameState: any, onTerrainNode: TransformNode): void
}
