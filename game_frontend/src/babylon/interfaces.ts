import { Engine, Scene } from 'babylonjs'

export interface GameNode {
    object: any
    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine): void
    onGameStateUpdate(): void
}