import Environment from '../environment/environment'

export default class SceneRenderer {
    environment: Environment

    constructor (environment: Environment) {
      this.environment = environment
    }

    setup (): void {
      this.environment.engine.runRenderLoop(() => {
        this.environment.scene.render()
      })
    }

    windowResized = () => {
      this.environment.engine.resize()
    }
}
