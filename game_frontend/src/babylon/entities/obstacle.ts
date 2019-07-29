import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'

export default class Obstacle implements GameNode {
    object: any
    scene: BABYLON.Scene
    obstacleNode: BABYLON.Mesh

    onSceneMount(scene: BABYLON.Scene, canvas: HTMLCanvasElement, engine: BABYLON.Engine, onTerrainNode: BABYLON.TransformNode): void {
        this.scene = scene
        this.obstacleNode = BABYLON.Mesh.CreateBox('obstacles', 1, scene)
        this.obstacleNode.parent = onTerrainNode
        this.obstacleNode.isVisible = false
    }

    onGameStateUpdate(obstacleDiff: any): void {
        var updatedObstacle
        for (updatedObstacle in obstacleDiff) {
            let obstacle = obstacleDiff[updatedObstacle]
            // Delete an obstacle
            if (obstacle.updateType === "D") {
                const toDelete = this.obstacleNode.getChildMeshes(true,
                    function (node): boolean {
                        return node.name == `obstacle: ${updatedObstacle}`
                    }
                )
                toDelete[0].dispose()
            }
            // Add an obstacle
            else if (obstacle.updateType === "A") {
                const box = BABYLON.MeshBuilder.CreateBox(`obstacle: ${updatedObstacle}`, { height: 1 }, this.scene)
                const material = new BABYLON.StandardMaterial('obstacle_material_future', this.scene)
                material.diffuseTexture = new BABYLON.Texture('/static/images/obstacle_future_wall1.jpg', this.scene)
                box.position = new BABYLON.Vector3(obstacle.object.location.x, 0.5, obstacle.object.location.y)
                box.parent = this.obstacleNode
                box.material = material
            }
            // Edit an obstacle (move it)
            else {
                const toEdit = this.obstacleNode.getChildMeshes(true,
                    function (node): boolean {
                        return node.name === `obstacle: ${updatedObstacle}`
                    }
                )
                toEdit[0].position = new BABYLON.Vector3(obstacle.object.location.x, 0.5, obstacle.object.location.y)
            }
        }
    }
}
