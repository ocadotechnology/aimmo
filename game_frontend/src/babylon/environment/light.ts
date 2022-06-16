import { GameNode } from '../interfaces'
import { HemisphericLight, Vector3 } from 'babylonjs'
import { Environment } from './environment'

export default class Light implements GameNode {
  object: any

  constructor(environment: Environment) {
    const light = new HemisphericLight('light1', new Vector3(0, 1, 0), environment.scene)
    this.object = light

    light.intensity = 1.45
  }
}
