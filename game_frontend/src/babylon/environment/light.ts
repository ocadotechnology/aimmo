import { GameNode } from '../interfaces'
import { HemisphericLight, Vector3 } from 'babylonjs'
import EnvironmentRenderer from '.'


export default class Light implements GameNode {
    object: any;

    setup(environmentRenderer: EnvironmentRenderer): void {
        const light = new HemisphericLight('light1', new Vector3(0, 1, 0), environmentRenderer.scene)
        this.object = light

        light.intensity = 1.45
    }

    onGameStateUpdate(): void { }
}