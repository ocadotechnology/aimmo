import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { EDIT, DELETE } from '../diff'
import Environment from '../environment/environment';

export default class Obstacle implements GameNode {
    object: any
    scene: BABYLON.Scene
    obstacleNode: BABYLON.TransformNode

    setup(environment: Environment): void {
        this.scene = environment.scene
        this.obstacleNode = new BABYLON.TransformNode('Obstacle Parent', environment.scene)
        this.obstacleNode.parent = environment.onTerrainNode
    }

    onGameStateUpdate(obstacleDiff: any): void {
        for (let obstacle of obstacleDiff) {
            // Delete obstacles
            if (obstacle.updateType === DELETE) {
                this.deleteObstacle(obstacleDiff.indexOf(obstacle))
            }
            // Edit obstacles
            else if (obstacle.updateType === EDIT) {
                this.editObstacle(obstacleDiff.indexOf(obstacle), obstacle)
            }
            // Add obstacles
            else {
                this.addObstacle(obstacleDiff.indexOf(obstacle), obstacle)
            }
        }
    }

    deleteObstacle(index: any): void {
        const toDelete = this.obstacleNode.getChildMeshes(true,
            function (node): boolean {
                return node.name == `obstacle: ${index}`
            }
        )
        toDelete[0].dispose()
    }

    editObstacle(index: any, obstacle: any): void {
        const toEdit = this.obstacleNode.getChildMeshes(true,
            function (node): boolean {
                return node.name === `obstacle: ${index}`
            }
        )
        toEdit[0].position = new BABYLON.Vector3(obstacle.object.location.x, 0, obstacle.object.location.y)
    }

    addObstacle(index: any, obstacle: any): void {
        // Create mesh
        const box = BABYLON.MeshBuilder.CreateBox(`obstacle: ${index}`, { height: 1 }, this.scene)

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
