import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'

export default class Obstacles implements GameNode {
    object: any
    scene: BABYLON.Scene
    gameState: any

    onSceneMount(scene: BABYLON.Scene): void {
        this.scene = scene
    }

    onGameStateUpdate(gameState: any, onTerrainNode: BABYLON.TransformNode): void {
        if (this.shouldRenderObstacles(this.gameState, gameState)) {
            for (const [index, obstacle] of gameState.obstacles.entries()) {
                const box = BABYLON.MeshBuilder.CreateBox(`hello: ${index}`, { height: 1 }, this.scene)
                const material = new BABYLON.StandardMaterial('', this.scene)
                material.diffuseTexture = new BABYLON.Texture('/static/images/obstacle_future_wall1.jpg', this.scene)
                box.position = new BABYLON.Vector3(obstacle.location.x, 0.5, obstacle.location.y)
                box.parent = onTerrainNode
                box.material = material
            }
        }
        this.gameState = gameState
    }

    shouldRenderObstacles(oldGameState: any, newGameState: any): boolean {
        if (oldGameState) {
            for (const obstacle of newGameState.obstacles.entries())
                if (oldGameState.obstacles.indexOf(obstacle) == -1)
                    return true
        }
        else
            this.gameState = newGameState

        return false
    }
}
