import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'
import setOrientation from '../orientation'
import { createMoveAnimation, createWalkAnimation, MAX_KEYFRAMES_PER_SECOND } from '../animations'

export default class AvatarManager implements GameNode, DiffHandling {
  object: any
  scene: BABYLON.Scene
  avatarNode: BABYLON.TransformNode
  markerMaterial : BABYLON.StandardMaterial
  currentAvatarID: number
  gameStateProcessor: DiffProcessor

  setup (environment: Environment): void {
    this.gameStateProcessor = new DiffProcessor(this)

    this.scene = environment.scene
    this.avatarNode = new BABYLON.TransformNode('Avatars', environment.scene)
    this.avatarNode.parent = environment.onTerrainNode

    this.markerMaterial = new BABYLON.StandardMaterial('avatar marker', this.scene)
    this.markerMaterial.diffuseTexture = new BABYLON.Texture('/static/models/avatar_marker.png', this.scene)
  }

  delete (avatar: DiffItem): void {
    const toDelete = this.avatarNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `avatar: ${avatar.value.id}`
      }
    )
    toDelete[0].dispose()
  }

  add (avatar: DiffItem): void {
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

      console.log(this.currentAvatarID)
      if (avatar.value.id === this.currentAvatarID) {
        this.attachMarker(dee, avatar)
      }
    })
  }

  update (avatar: DiffItem): void {
    const avatarToAnimate = this.avatarNode.getChildMeshes(true,
      function (node): boolean {
        return node.name === `avatar: ${avatar.value.id}`
      }
    )[0]
    const toPosition = new BABYLON.Vector3(avatar.value.location.x, 0, avatar.value.location.y)
    const moveAnimation = createMoveAnimation(avatarToAnimate.position, toPosition)
    this.scene.beginDirectAnimation(avatarToAnimate, [moveAnimation], 0, MAX_KEYFRAMES_PER_SECOND, false, 1)
    let dee = avatarToAnimate
    createWalkAnimation(dee, this.scene)

    setOrientation(dee, avatar.value.orientation)
  }

  attachMarker (avatarMesh: any, avatar: any): void {
    // Load marker mesh.
    BABYLON.SceneLoader.ImportMesh('avatar_marker', '/static/models/', 'model_avatar_marker.babylon', this.scene, (meshes, particleSystems, skeletons, animationGroups) => {
      var marker = meshes[0]

      marker.material = this.markerMaterial

      marker.parent = avatarMesh
      marker.position = new BABYLON.Vector3(0, 12, 0)
    })
  }

  setCurrentAvatarID (avatarID: number) {
    this.currentAvatarID = avatarID
  }
}
