import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { EDIT, DELETE } from '../diff'
import EnvironmentRenderer from '../environment'

export default class Obstacle implements GameNode {
    object: any
    scene: BABYLON.Scene
    obstacleNode: BABYLON.TransformNode

    setup(environmentRenderer: EnvironmentRenderer): void {
        this.scene = environmentRenderer.scene
        this.obstacleNode = new BABYLON.TransformNode('Obstacle Parent', environmentRenderer.scene)
        this.obstacleNode.parent = environmentRenderer.onTerrainNode
    }

    onGameStateUpdate(obstacleDiff: any): void {
        var updatedObstacle
        for (updatedObstacle in obstacleDiff) {
            let obstacle = obstacleDiff[updatedObstacle]
            // Delete an obstacle
            if (obstacle.updateType === DELETE) {
                const toDelete = this.obstacleNode.getChildMeshes(true,
                    function (node): boolean {
                        return node.name == `obstacle: ${updatedObstacle}`
                    }
                )
                toDelete[0].dispose()
            }
            // Edit an obstacle (move it)
            else if (obstacle.updateType === EDIT) {
                const toEdit = this.obstacleNode.getChildMeshes(true,
                    function (node): boolean {
                        return node.name === `obstacle: ${updatedObstacle}`
                    }
                )
                toEdit[0].position = new BABYLON.Vector3(obstacle.object.location.x, 0, obstacle.object.location.y)
            }
            // Add an obstacle
            else {
                // Create mesh
                const box = BABYLON.MeshBuilder.CreateBox(`obstacle: ${updatedObstacle}`, { height: 1 }, this.scene)

                // Create and assign material
                const material = new BABYLON.StandardMaterial('obstacle_material_future', this.scene)
                material.diffuseTexture = new BABYLON.Texture('/static/images/obstacle_future_wall1.jpg', this.scene)
                box.material = material

                // Set parent and relative position
                box.parent = this.obstacleNode
                box.position = new BABYLON.Vector3(obstacle.object.location.x, 0.5, obstacle.object.location.y)
                box.setPivotMatrix(BABYLON.Matrix.Translation(0, -0.5, 0))
            }
        }
    }
}
