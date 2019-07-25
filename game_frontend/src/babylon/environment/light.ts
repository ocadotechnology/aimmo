import { GameNode } from '../interfaces'
import { HemisphericLight, Vector3, Scene, Engine } from 'babylonjs'


export default class Light implements GameNode {
    object: any;

    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine): void {
        const light = new HemisphericLight('light1', new Vector3(0, 1, 0), scene)
        this.object = light

        light.intensity = 1.45
    }

    onGameStateUpdate(): void { }
}