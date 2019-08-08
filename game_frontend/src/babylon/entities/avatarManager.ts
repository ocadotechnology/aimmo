import { GameNode, DiffHandling } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffResult, DiffItem } from '../diff'
import setOrientation from '../orientation'
import { createMoveAnimation, MAX_KEYFRAMES_PER_SECOND } from '../animations'

export default class AvatarManager implements GameNode, DiffHandling {
  object: any
  scene: BABYLON.Scene
  avatarNode: BABYLON.TransformNode

  setup (environment: Environment): void {
    this.scene = environment.scene
    this.avatarNode = new BABYLON.TransformNode('Avatars', environment.scene)
    this.avatarNode.parent = environment.onTerrainNode
  }

  handleDifferences (differences: DiffResult): void {
    for (let avatar of differences.deleteList) {
      this.removeAvatar(avatar)
    }
    for (let avatar of differences.editList) {
      this.animateAvatar(avatar)
    }
    for (let avatar of differences.addList) {
      this.addAvatar(avatar)
    }
  }

  removeAvatar (avatar: DiffItem): void {
    const toDelete = this.avatarNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `avatar: ${avatar.value.id}`
      }
    )
    toDelete[0].dispose()
  }

  addAvatar (avatar: DiffItem): void {
    // import Dee
    BABYLON.SceneLoader.ImportMesh(`Dee`, '/static/models/', 'dee.babylon', this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
      var dee = meshes[0]
      dee.name = `avatar: ${avatar.value.id}`
      dee.scaling = new BABYLON.Vector3(0.1, 0.1, 0.1)
      dee.computeBonesUsingShaders = false
      var shaderMaterial = new BABYLON.ShaderMaterial('shader', this.scene, '/static/models/toonshader',
        {
          attributes: ['position', 'normal', 'uv'],
          uniforms: ['world', 'worldView', 'worldViewProjection', 'view', 'projection']
        })
      shaderMaterial.setTexture('textureSampler', new BABYLON.Texture('/static/models/DEE.png', this.scene))
      dee.material = shaderMaterial
      dee.parent = this.avatarNode
      dee.position = new BABYLON.Vector3(avatar.value.location.x, 0, avatar.value.location.y)
      setOrientation(dee, avatar.value.orientation)
      // Check if the avatar is for the player loading the page (somehow)
      // this.attachMarker(dee)
    })
  }

  animateAvatar (avatar: DiffItem): void {
    const avatarToAnimate = this.avatarNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `avatar: ${avatar.value.id}`
      }
    )[0]
    const toPosition = new BABYLON.Vector3(avatar.value.location.x, 0, avatar.value.location.y)
    const moveAnimation = createMoveAnimation(avatarToAnimate.position, toPosition)
    this.scene.beginDirectAnimation(avatarToAnimate, [moveAnimation], 0, MAX_KEYFRAMES_PER_SECOND, false, 1)
    // console.log(avatarToAnimate)
    let dee = avatarToAnimate

    setOrientation(dee, avatar.value.orientation)
  }

  attachMarker (avatarMesh: any): void {
    // Load marker mesh.

    // Apply marker texture.

    // Make Parent node the given avatar.
  }
}
