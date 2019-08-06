import Environment from '../environment/environment'

export default class SceneRenderer {
    environment: Environment

    constructor (environment: Environment) {
      this.environment = environment
    }

    setup (): void {
      this.environment.scene.debugLayer.show({
        overlay: true,
        globalRoot: document.getElementById('root'),
        // embedMode: true,
        showInspector: true
      })

      this.environment.engine.runRenderLoop(() => {
        this.environment.scene.render()
      })
    }

    windowResized = () => {
      this.environment.engine.resize()
      document.getElementById('scene-explorer-host').style.setProperty('z-index', '100000')
      document.getElementById('inspector-host').style.setProperty('z-index', '100000')
    }
}
