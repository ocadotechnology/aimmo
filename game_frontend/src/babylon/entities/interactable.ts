import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import Environment from '../environment/environment'
import { DiffResult } from '../diff'

export default class Interactable implements GameNode {
    object: any
    scene: BABYLON.Scene
    interactableNode: BABYLON.TransformNode

    setup (environment: Environment): void {
      this.scene = environment.scene
      this.interactableNode = new BABYLON.TransformNode('Interactable Parent', environment.scene)
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
      toDelete[0].dispose()
    }

    editInteractable (interactable: any): void {
      const toEdit = this.interactableNode.getChildMeshes(true,
        function (node): boolean {
          return node.name === `interactable: ${interactable.id}`
        }
      )
      toEdit[0].position = new BABYLON.Vector3(interactable.value.location.x, 0, interactable.value.location.y)
    }

    addInteractable (interactable: any): void {
      var model = ''
      var texture = ''

      model = `${interactable.value['type']}.babylon`
      texture = `/static/babylon/interactables/${interactable.value['type']}_text.png`

      const material = new BABYLON.StandardMaterial(interactable.value['type'], this.scene)
      material.specularColor = new BABYLON.Color3(0, 0, 0)
      material.emissiveColor = new BABYLON.Color3(0.5, 0.5, 0.5)
      material.diffuseTexture = new BABYLON.Texture(texture, this.scene)

      var frameRate = 5

      var rotationAnim = this.createRotation(frameRate)
      var slideAnim = this.createSlide(frameRate)

      BABYLON.SceneLoader.ImportMesh(interactable.value['type'], '/static/babylon/interactables/', model, this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
        var newInteractable = meshes[0]
        newInteractable.name = `interactable: ${interactable.id}`

        newInteractable.material = material

        newInteractable.parent = this.interactableNode
        newInteractable.position = new BABYLON.Vector3(interactable.value.location.x, 0.5, interactable.value.location.y)

        if (interactable.value['type'] !== 'score') { this.scene.beginDirectAnimation(newInteractable, [rotationAnim, slideAnim], 0, 2 * frameRate, true) }
      })
    }

    createRotation (frameRate: number) : BABYLON.Animation {
      var rotationAnim = new BABYLON.Animation('interactable rotation', 'rotation.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
      var keyFramesR = []

      keyFramesR.push({
        frame: 0,
        value: 0
      })
      keyFramesR.push({
        frame: frameRate,
        value: Math.PI
      })
      keyFramesR.push({
        frame: 2 * frameRate,
        value: 2 * Math.PI
      })

      rotationAnim.setKeys(keyFramesR)

      return rotationAnim
    }

    createSlide (frameRate: number) : BABYLON.Animation {
      var slideAnim = new BABYLON.Animation('interactable translation', 'position.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
      var keyFramesR = []

      for (let i = 0; i <= 2 * frameRate; i++) {
        keyFramesR.push({
          frame: i,
          value: 0.2 * Math.sin(Math.PI * (i / frameRate)) - 0.1
        })
      }

      slideAnim.setKeys(keyFramesR)

      return slideAnim
    }
}
