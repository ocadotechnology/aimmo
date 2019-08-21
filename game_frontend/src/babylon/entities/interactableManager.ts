import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'
import { bobbingAnimation, rotationAnimation, MAX_KEYFRAMES_PER_SECOND } from '../animations'

const animation = [rotationAnimation('interactable'), bobbingAnimation('interactable')]

export default class InteractableManager implements GameNode, DiffHandling {
    object: any
    scene: BABYLON.Scene
    interactableNode: BABYLON.TransformNode
    importMesh: Function
    materials: any
    gameStateProcessor: DiffProcessor

    constructor (environment: Environment, importMesh: Function = BABYLON.SceneLoader.ImportMesh) {
      this.importMesh = importMesh
      this.gameStateProcessor = new DiffProcessor(this)

      this.scene = environment.scene
      this.interactableNode = new BABYLON.TransformNode('Interactables', environment.scene)
      this.interactableNode.parent = environment.onTerrainNode
      this.materials = {
        'damage_boost': this.createMaterial('damage_boost'),
        'health': this.createMaterial('health'),
        'invulnerability': this.createMaterial('invulnerability'),
        'score': this.createMaterial('score')
      }
    }

    createMaterial (interactableType: string) : BABYLON.StandardMaterial {
      const texture = `/static/babylon/interactables/${interactableType}_texture.png`

      const material = new BABYLON.StandardMaterial(interactableType, this.scene)
      material.specularColor = new BABYLON.Color3(0, 0, 0)
      material.emissiveColor = new BABYLON.Color3(0.5, 0.5, 0.5)
      material.diffuseTexture = new BABYLON.Texture(texture, this.scene)

      return material
    }

    remove (interactable: DiffItem): void {
      const index = interactable.id
      const toDelete = this.interactableNode.getChildMeshes(true,
        function (node): boolean {
          return node.name === `interactable: ${index}`
        }
      )
      if (toDelete.length > 0) {
        toDelete[0].dispose()
      }
    }

    edit (interactable: DiffItem): void {
      const toEdit = this.interactableNode.getChildMeshes(true,
        function (node): boolean {
          return node.name === `interactable: ${interactable.id}`
        }
      )
      if (toEdit.length > 0) {
        toEdit[0].position = new BABYLON.Vector3(interactable.value.location.x, 0, interactable.value.location.y)
      }
    }

    add (interactable: DiffItem): void {
      var model = ''

      model = `${interactable.value['type']}_model.babylon`

      this.importMesh(interactable.value['type'], '/static/babylon/interactables/', model, this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
        var newInteractable = meshes[0]
        newInteractable.name = `interactable: ${interactable.id}`

        newInteractable.material = this.materials[interactable.value.type]

        newInteractable.parent = this.interactableNode
        newInteractable.position = new BABYLON.Vector3(interactable.value.location.x, 0, interactable.value.location.y)

        if (interactable.value['type'] !== 'score') {
          this.scene.beginDirectAnimation(newInteractable, animation, 0, MAX_KEYFRAMES_PER_SECOND, true)
        }
      })
    }
}
