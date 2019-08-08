import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffResult } from '../diff'
import { bobbingAnimation, rotationAnimation } from '../animations'

const frameRate = 5
const animation = [rotationAnimation(frameRate, 'interactable'), bobbingAnimation(frameRate, 'interactable')]

export default class Interactable implements GameNode {
    object: any
    scene: BABYLON.Scene
    interactableNode: BABYLON.TransformNode
    importMesh: Function

    constructor (importMesh: Function = BABYLON.SceneLoader.ImportMesh) {
      this.importMesh = importMesh
    }

    setup (environment: Environment): void {
      this.scene = environment.scene
      this.interactableNode = new BABYLON.TransformNode('Interactables', environment.scene)
      this.interactableNode.parent = environment.onTerrainNode
    }

    onGameStateUpdate (interactableDiff: DiffResult): void {
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

    deleteInteractable (index: any): void {
      const toDelete = this.interactableNode.getChildMeshes(true,
        function (node): boolean {
          return node.name === `interactable: ${index}`
        }
      )
      if (toDelete.length > 0){
        toDelete[0].dispose()
      }
    }

    editInteractable (interactable: any): void {
      const toEdit = this.interactableNode.getChildMeshes(true,
        function (node): boolean {
          return node.name === `interactable: ${interactable.id}`
        }
      )
      if (toEdit.length > 0){
        toEdit[0].position = new BABYLON.Vector3(interactable.value.location.x, 0.5, interactable.value.location.y)
      }
    }

    addInteractable (interactable: any): void {
      var model = ''
      var texture = ''

      model = `model_${interactable.value['type']}.babylon`
      texture = `/static/babylon/interactables/interactable_${interactable.value['type']}.png`

      const material = new BABYLON.StandardMaterial(interactable.value['type'], this.scene)
      material.specularColor = new BABYLON.Color3(0, 0, 0)
      material.emissiveColor = new BABYLON.Color3(0.5, 0.5, 0.5)
      material.diffuseTexture = new BABYLON.Texture(texture, this.scene)

      this.importMesh(interactable.value['type'], '/static/babylon/interactables/', model, this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
        var newInteractable = meshes[0]
        newInteractable.name = `interactable: ${interactable.id}`

        newInteractable.material = material

        newInteractable.parent = this.interactableNode
        newInteractable.position = new BABYLON.Vector3(interactable.value.location.x, 0.5, interactable.value.location.y)

        if (interactable.value['type'] !== 'score') { this.scene.beginDirectAnimation(newInteractable, animation, 0, 2 * frameRate, true) }
      })
    }
}
