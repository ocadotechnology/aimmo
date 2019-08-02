import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import Environment from '../environment/environment'
import { DiffResult, DiffItem } from '../diff'

export default class Avatar implements GameNode {
    object: any
    scene: BABYLON.Scene
    AvatarNode: BABYLON.TransformNode

    setup (environment: Environment): void {
      this.scene = environment.scene
      this.AvatarNode = new BABYLON.TransformNode('Avatar Parent', environment.scene)
      this.AvatarNode.parent = environment.onTerrainNode
    }

    onGameStateUpdate (avatarDiff: DiffResult): void {
      for (let avatar of avatarDiff.deleteList) {
        this.removeAvatar(avatar)
      }
      for (let avatar of avatarDiff.addList) {
        this.addAvatar(avatar)
      }
      for (let avatar of avatarDiff.editList) {
        this.animateAvatar(avatar)
      }
    }

    removeAvatar (avatar: DiffItem): void { }

    addAvatar (avatar: DiffItem): void {
      // import Dee
      BABYLON.SceneLoader.ImportMesh(`Dee`, '/static/models/', 'dee.babylon', this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
        var dee = meshes[0]
        dee.scaling = new BABYLON.Vector3(0.1, 0.1, 0.1)
        dee.computeBonesUsingShaders = false
        var shaderMaterial = new BABYLON.ShaderMaterial('shader', this.scene, '/static/models/toonshader',
          {
            attributes: ['position', 'normal', 'uv'],
            uniforms: ['world', 'worldView', 'worldViewProjection', 'view', 'projection']
          })
        shaderMaterial.setTexture('textureSampler', new BABYLON.Texture('/static/models/DEE.png', this.scene))
        dee.material = shaderMaterial
        dee.parent = this.AvatarNode
        dee.position = new BABYLON.Vector3(avatar.value.location.x, 0, avatar.value.location.y)
        this.object = dee
      })
    }

    animateAvatar (avatar: DiffItem): void { }
}
