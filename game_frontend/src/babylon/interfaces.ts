import { Engine, Scene, TransformNode } from 'babylonjs'

export interface GameNode {
    object: any
    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine, onTerrainNode?: TransformNode): void
    onGameStateUpdate(gameState: any): void
}
