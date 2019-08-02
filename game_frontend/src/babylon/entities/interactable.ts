import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import Environment from '../environment/environment'
import { DiffResult } from '../diff'

export default class Interactable implements GameNode {
    object: any
    scene: BABYLON.Scene
    interactableNode: BABYLON.TransformNode

    setup(environment: Environment): void {
        this.scene = environment.scene
        this.interactableNode = new BABYLON.TransformNode('Interactable Parent', environment.scene)
        this.interactableNode.parent = environment.onTerrainNode
    }

    onGameStateUpdate(interactableDiff: DiffResult): void {
        for (let interactable of interactableDiff.deleteList) {
            this.deleteInteractable(interactable.id)
        }
        for (let interactable of interactableDiff.editList) {
            this.editInteractable(interactable)
        }
        for (let interactable of interactableDiff.addList) {
            this.addInteractable(interactable)
        }
    }

    deleteInteractable(index: any): void {
        const toDelete = this.interactableNode.getChildMeshes(true,
            function (node): boolean {
                return node.name === `interactable: ${index}`
            }
        )
        toDelete[0].dispose()
    }

    editInteractable(interactable: any): void {
        const toEdit = this.interactableNode.getChildMeshes(true,
            function (node): boolean {
                return node.name === `interactable: ${interactable.id}`
            }
        )
        toEdit[0].position = new BABYLON.Vector3(interactable.value.location.x, 0, interactable.value.location.y)
    }

    addInteractable(interactable: any): void {
        var model = ''
        var texture = ''

        if (interactable.value['type'] === 'damage_boost') {
            model = 'damage.babylon'
            texture = '/static/babylon/interactable/damage_text.jpg'
        }

        else if (interactable.value['type'] === 'invulnerability') {
            model = 'damage.babylon' // TODO change
            texture = '/static/babylon/interactable/damage_text.jpg'
        }

        else {
            model = 'damage.babylon' // TODO change
            texture = '/static/babylon/interactable/damage_text.jpg'
        }

        BABYLON.SceneLoader.ImportMesh(`interactable: ${interactable.id}`, '/static/babylon/interactables/', model, this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
            var newInteractable = meshes[0]
            const material = new BABYLON.StandardMaterial(interactable.value['type'], this.scene)
            material.diffuseTexture = new BABYLON.Texture(texture, this.scene)
            newInteractable.material = material

            newInteractable.parent = this.interactableNode
            newInteractable.position = new BABYLON.Vector3(interactable.value.location.x, 0.5, interactable.value.location.y)
            newInteractable.setPivotMatrix(BABYLON.Matrix.Translation(0, -0.5, 0))

            // this.scene.beginAnimation(skeletons[0], 0, 21, true)
        })
    }
}
