import EntityManager from './entities'
import SceneRenderer from './environment'
import EnvironmentManager from './environment/environmentManager'
import { StandardEnvironment } from './environment/environment'
import { MockEnvironment } from 'testHelpers/mockEnvironment'
import * as BABYLON from 'babylonjs'

export default class GameEngine {
    environment: any
    sceneRenderer: SceneRenderer
    environmentManager: EnvironmentManager
    entities: EntityManager
    panHandler: Function

    constructor (canvas: HTMLCanvasElement, handleMapPanned: Function, mock: Boolean) {
      if (mock) {
        this.environment = new MockEnvironment(true)
      } else {
        this.environment = new StandardEnvironment(canvas)
      }

      this.sceneRenderer = new SceneRenderer(this.environment)
      this.environmentManager = new EnvironmentManager(this.environment)
      this.entities = new EntityManager(this.environment)
      this.panHandler = handleMapPanned

      window.addEventListener('resize', this.environmentManager.resizeBabylonWindow)
      this.addPanListener(this.environment.scene)
    }

    onUpdate (previousProps: any, currentProps: any) {
      this.updateGameState(previousProps.gameState, currentProps.gameState)
      this.updateCurrentAvatarID(previousProps.currentAvatarID, currentProps.currentAvatarID)
      this.centerOn(currentProps ? currentProps.cameraCenteredOnUserAvatar : previousProps.cameraCenteredOnUserAvatar)
    }

    centerOn (centerOn: Boolean) {
      if (centerOn && this.entities.avatars.currentAvatarMesh) {
        this.environmentManager.centerOn(this.entities.avatars.currentAvatarMesh)
      }
    }

    updateGameState (previousGameState: any, currentGameState: any) {
      if (currentGameState !== undefined) {
        this.entities.onGameStateUpdate(previousGameState, currentGameState)
      }
    }

    updateCurrentAvatarID (previousAvatarID: number, currentAvatarID: number) {
      if (previousAvatarID !== currentAvatarID) {
        if (currentAvatarID) {
          this.entities.setCurrentAvatarID(currentAvatarID)
        } else {
          this.entities.setCurrentAvatarID(previousAvatarID)
        }
      }
    }

    unmount () {
      window.removeEventListener('resize', this.environmentManager.windowResized)
    }

    addPanListener (scene: BABYLON.Scene) {
      scene.onPrePointerObservable.add(pointerInfo => {
        this.panHandler()
        this.environmentManager.unCenter(this.entities.avatars.currentAvatarMesh)
      }, BABYLON.PointerEventTypes.POINTERDOWN, false)
    }
}
