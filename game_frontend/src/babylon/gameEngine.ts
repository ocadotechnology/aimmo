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

    constructor (handleMapPanned: Function, environment: Environment) {
      this.environment = environment
      this.sceneRenderer = new SceneRenderer(this.environment)
      this.environmentManager = new EnvironmentManager(this.environment)
      this.entities = new EntityManager(this.environment)
      this.panHandler = handleMapPanned

      window.addEventListener('resize', this.environmentManager.resizeBabylonWindow)
      this.addPanListener(this.environment.scene)
    }

    onUpdate (previousProps: any, currentProps: any) {
      this.onUpdateGameState(previousProps.gameState, currentProps.gameState)
      this.onUpdateCurrentAvatarID(previousProps.currentAvatarID, currentProps.currentAvatarID)
      this.centerOn(currentProps)
    }

    centerOn (props: any) {
      if (props.cameraCenteredOnUserAvatar && props.gameLoaded) {
        if (this.entities.avatars.currentAvatarMesh) {
          this.environmentManager.centerOn(this.entities.avatars.currentAvatarMesh)
        } else if (props.gameState.players) {
          const location = this.getAvatarLocation(props.currentAvatarID, props.gameState.players)
          this.environmentManager.camera.object.setTarget(location)
          this.environmentManager.camera.object.panningOriginTarget = location
        }
      }
    }

    onUpdateGameState (previousGameState: any, currentGameState: any) {
      if (currentGameState !== undefined) {
        this.entities.onGameStateUpdate(previousGameState, currentGameState)
      }
    }

    onUpdateCurrentAvatarID (previousAvatarID: number, currentAvatarID: number) {
      if (previousAvatarID !== currentAvatarID) {
        this.entities.setCurrentAvatarID(currentAvatarID)
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
      for (let player in players) {
        if (players[player]['id'] === playerID) {
          const location = players[player]['location']
          return new BABYLON.Vector3(location.x, 0, location.y)
        }
      }
    }
}
