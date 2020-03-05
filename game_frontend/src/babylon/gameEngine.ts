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
      this.panHandler = handleMapPanned
    }

    onUpdate (previousProps: any, currentProps: any) {
      if (currentProps.gameState) {
        if (this.environment.era === '') {
          this.environment.era = currentProps.gameState['era']
          this.populateMap()
        }
        
        this.onUpdateGameState(previousProps.gameState, currentProps.gameState)
        this.setCurrentAvatarID(currentProps.currentAvatarID)
        this.centerOn(currentProps)
      }
    }

    populateMap(): void {
      this.sceneRenderer = new SceneRenderer(this.environment)
      this.environmentManager = new EnvironmentManager(this.environment)
      this.entities = new EntityManager(this.environment)

      window.addEventListener('resize', this.environmentManager.resizeBabylonWindow)
      this.addPanListener(this.environment.scene)
    }

    setCurrentAvatarID(props: any) {
      this.entities.setCurrentAvatarID(props)
    }

    centerOn (props: any) {
      if (props.cameraCenteredOnUserAvatar) {
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
      this.entities.onGameStateUpdate(previousGameState, currentGameState)
    }

    unmount () {
      window.removeEventListener('resize', this.environmentManager.resizeBabylonWindow)
    }

    addPanListener (scene: BABYLON.Scene) {
      scene.onPrePointerObservable.add(pointerInfo => {
        this.panHandler()
        this.environmentManager.unCenter(this.entities.avatars.currentAvatarMesh)
      }, BABYLON.PointerEventTypes.POINTERDOWN, false)
    }

    getAvatarLocation (playerID: number, players: any) : BABYLON.Vector3 {
      for (let player in players) {
        if (players[player]['id'] === playerID) {
          const location = players[player]['location']
          return new BABYLON.Vector3(location.x, 0, location.y)
        }
      }
      return null
    }
}
