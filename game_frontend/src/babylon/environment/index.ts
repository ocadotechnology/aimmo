import { Environment } from './environment'

export default class SceneRenderer {
  environment: Environment

  constructor(environment: Environment) {
    this.environment = environment

    this.environment.engine.runRenderLoop(() => {
      this.environment.scene.render()
    })
    // this.showDebugLayer()
  }

  showDebugLayer(): void {
    setTimeout(() => {
      this.environment.scene.debugLayer.show({
        overlay: true,
        showExplorer: true,
        showInspector: true,
        globalRoot: document.getElementById('root'),
      })
    }, 2000)
    setTimeout(() => {
      document.getElementById('scene-explorer-host').style.setProperty('z-index', '15000')
      document.getElementById('inspector-host').style.setProperty('z-index', '15000')
    }, 4000)
  }
}
