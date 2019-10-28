import EntityManager from './entities'
import SceneRenderer from './environment'
import EnvironmentManager from './environment/environmentManager'
import { Environment } from './environment/environment'
import * as BABYLON from 'babylonjs'

export default class GameEngine {
    environment: Environment
    sceneRenderer: SceneRenderer
    environmentManager: EnvironmentManager
    entities: EntityManager
    panHandler: Function

    constructor (canvas: HTMLCanvasElement, handleMapPanned: Function, environment: Environment, props: any) {
      this.environment = environment
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
      this.centerOn(currentProps ? currentProps : previousProps)
    }

    centerOn (props: any) {
      if (props.cameraCenteredOnUserAvatar && props.gameLoaded) {
        if (this.entities.avatars.currentAvatarMesh) {
          this.environmentManager.centerOn(this.entities.avatars.currentAvatarMesh)
        } else if (props.gameState.players){
          let location = this.getAvatarLocation(props.currentAvatarID, props.gameState.players)
          this.environmentManager.camera.object.setTarget(new BABYLON.Vector3(location.x, 0, location.y))
        }
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

    getAvatarLocation (playerID: number, players: any) : any {
      for (let player of players) {
        if (player['id'] === playerID) {
          return player['location']
        }
      }
    }
}
