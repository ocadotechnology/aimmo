import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import * as BABYLON from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'
import setOrientation from '../orientation'
import { createMoveAnimation, createWalkAnimation, MAX_KEYFRAMES_PER_SECOND } from '../animations'

const MARKER_HEIGHT = 12

export default class AvatarManager implements GameNode, DiffHandling {
  object: any
  currentAvatarMesh: BABYLON.AbstractMesh
  scene: BABYLON.Scene
  avatarNode: BABYLON.TransformNode
  markerMaterial: BABYLON.StandardMaterial
  currentAvatarID: number
  gameStateProcessor: DiffProcessor
  importMesh: Function
  shaderMaterial: BABYLON.ShaderMaterial

  constructor (
    environment: Environment,
    importMesh: Function = BABYLON.SceneLoader.ImportMeshAsync
  ) {
    this.importMesh = importMesh
    this.gameStateProcessor = new DiffProcessor(this)

    this.scene = environment.scene
    this.avatarNode = new BABYLON.TransformNode('Avatars', environment.scene)
    this.object = this.avatarNode
    this.avatarNode.parent = environment.onTerrainNode

    this.setupMarkerMaterial()
    this.setupShaderMaterial()
  }

  setupMarkerMaterial (): void {
    this.markerMaterial = new BABYLON.StandardMaterial('avatar marker', this.scene)
    this.markerMaterial.diffuseTexture = new BABYLON.Texture(
      '/static/babylon/models/avatar_marker_texture.png',
      this.scene
    )
  }

  setupShaderMaterial (): void {
    this.shaderMaterial = new BABYLON.ShaderMaterial(
      'Avatar shader',
      this.scene,
      '/static/babylon/models/toonshader',
      {
        attributes: ['position', 'normal', 'uv'],
        uniforms: ['world', 'worldView', 'worldViewProjection', 'view', 'projection']
      }
    )
    this.shaderMaterial.setTexture(
      'textureSampler',
      new BABYLON.Texture('/static/babylon/models/avatar_texture.png', this.scene)
    )
  }

  remove (avatar: DiffItem): void {
    const toDelete = this.avatarNode.getChildMeshes(true, function (node): boolean {
      return node.name === `avatar: ${avatar.value.id}`
    })
    toDelete[0].dispose()
  }

  async add (avatar: DiffItem) {
    const { meshes } = await this.importMesh(
      'dee',
      '/static/babylon/models/',
      'avatar_model.babylon',
      this.scene
    )
    var dee = meshes[0]
    dee.name = `avatar: ${avatar.value.id}`
    dee.scaling = new BABYLON.Vector3(0.1, 0.1, 0.1)
    dee.computeBonesUsingShaders = false
    dee.material = this.shaderMaterial
    dee.parent = this.avatarNode
    dee.position = new BABYLON.Vector3(avatar.value.location.x, 0, avatar.value.location.y)
    setOrientation(dee, avatar.value.orientation)

    if (avatar.value.id === this.currentAvatarID) {
      this.attachMarker(dee, avatar)
      this.currentAvatarMesh = dee
    }
  }

  edit (avatar: DiffItem): void {
    const avatarToAnimate = this.avatarNode.getChildMeshes(true, function (node): boolean {
      return node.name === `avatar: ${avatar.value.id}`
    })[0]

    const toPosition = new BABYLON.Vector3(avatar.value.location.x, 0, avatar.value.location.y)

    const moveAnimation = createMoveAnimation(avatarToAnimate.position, toPosition)
    this.scene.beginDirectAnimation(
      avatarToAnimate,
      [moveAnimation],
      0,
      MAX_KEYFRAMES_PER_SECOND,
      false,
      1
    )
    const dee = avatarToAnimate
    createWalkAnimation(dee, this.scene)

    setOrientation(dee, avatar.value.orientation)
  }

  attachMarker (avatarMesh: any, avatar: any): void {
    this.importMesh(
      'avatar_marker',
      '/static/babylon/models/',
      'avatar_marker_model.babylon',
      this.scene,
      (meshes, particleSystems, skeletons, animationGroups) => {
        var marker = meshes[0]

        marker.material = this.markerMaterial

        marker.parent = avatarMesh
        marker.position = new BABYLON.Vector3(0, MARKER_HEIGHT, 0)
      }
    )
  }

  setCurrentAvatarID (avatarID: number) {
    this.currentAvatarID = avatarID
  }
}
