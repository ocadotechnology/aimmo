import { GameNode, DiffHandling, DiffProcessor } from '../interfaces'
import {
  AbstractMesh,
  SceneLoader,
  TransformNode,
  StandardMaterial,
  Texture,
  Vector3,
  ShaderMaterial,
  Scene,
  Color3,
} from 'babylonjs'
import { Environment } from '../environment/environment'
import { DiffItem } from '../diff'
import setOrientation from '../orientation'
import { createMoveAnimation, createWalkAnimation, MAX_KEYFRAMES_PER_SECOND } from '../animations'

const MARKER_HEIGHT = 17

export default class AvatarManager implements GameNode, DiffHandling {
  object: any
  currentAvatarMesh: AbstractMesh
  scene: Scene
  avatarNode: TransformNode
  markerMaterial: StandardMaterial
  currentAvatarID: number
  gameStateProcessor: DiffProcessor
  importMesh: Function
  shaderMaterial: ShaderMaterial

  constructor(environment: Environment, importMesh: Function = SceneLoader.ImportMeshAsync) {
    this.importMesh = importMesh
    this.gameStateProcessor = new DiffProcessor(this)

    this.scene = environment.scene
    this.avatarNode = new TransformNode('Avatars', environment.scene)
    this.object = this.avatarNode
    this.avatarNode.parent = environment.onTerrainNode

    this.setupMarkerMaterial()
    this.setupShaderMaterial()
  }

  setupMarkerMaterial(): void {
    this.markerMaterial = new StandardMaterial('avatar marker', this.scene)
    this.markerMaterial.diffuseTexture = new Texture(
      '/static/babylon/models/avatar_marker_texture.png',
      this.scene
    )
    this.markerMaterial.specularColor = new Color3(0, 0, 0)
  }

  setupShaderMaterial(): void {
    this.shaderMaterial = new ShaderMaterial(
      'Avatar shader',
      this.scene,
      '/static/babylon/models/toonshader',
      {
        attributes: ['position', 'normal', 'uv'],
        uniforms: ['world', 'worldView', 'worldViewProjection', 'view', 'projection'],
      }
    )
    this.shaderMaterial.setTexture(
      'textureSampler',
      new Texture('/static/babylon/models/avatar_texture.png', this.scene)
    )
  }

  remove(avatar: DiffItem): void {
    const toDelete = this.avatarNode.getChildMeshes(true, function (node): boolean {
      return node.name === `avatar: ${avatar.value.id}`
    })
    toDelete[0].dispose()
  }

  async add(avatar: DiffItem) {
    const { meshes } = await this.importMesh(
      'avatar',
      '/static/babylon/models/',
      'avatar_model.babylon',
      this.scene
    )
    const avatarMesh = meshes[0]
    avatarMesh.name = `avatar: ${avatar.value.id}`
    avatarMesh.scaling = new Vector3(0.2, 0.2, 0.2)
    avatarMesh.computeBonesUsingShaders = false
    avatarMesh.material = this.shaderMaterial
    avatarMesh.parent = this.avatarNode
    avatarMesh.position = new Vector3(avatar.value.location.x, 0, avatar.value.location.y)
    setOrientation(avatarMesh, avatar.value.orientation)

    if (avatar.value.id === this.currentAvatarID) {
      await this.attachMarker(avatarMesh)
      this.currentAvatarMesh = avatarMesh
    }
  }

  edit(avatar: DiffItem): void {
    const avatarToAnimate = this.avatarNode.getChildMeshes(true, function (node): boolean {
      return node.name === `avatar: ${avatar.value.id}`
    })[0]

    const toPosition = new Vector3(avatar.value.location.x, 0, avatar.value.location.y)

    const moveAnimation = createMoveAnimation(avatarToAnimate.position, toPosition)
    this.scene.beginDirectAnimation(
      avatarToAnimate,
      [moveAnimation],
      0,
      MAX_KEYFRAMES_PER_SECOND,
      false,
      1
    )
    const walkingAvatar = avatarToAnimate
    createWalkAnimation(walkingAvatar, this.scene)

    setOrientation(walkingAvatar, avatar.value.orientation)
  }

  async attachMarker(avatarMesh: any) {
    const { meshes } = await this.importMesh(
      'avatar_marker',
      '/static/babylon/models/',
      'avatar_marker_model_new.babylon',
      this.scene
    )
    const marker = meshes[0]

    marker.material = this.markerMaterial

    marker.parent = avatarMesh
    const markerScale = 300
    console.log('markerScale: ', markerScale);
    marker.scaling = new Vector3(markerScale, markerScale, markerScale)
    marker.position = new Vector3(0, MARKER_HEIGHT, 0)
  }

  setCurrentAvatarID(avatarID: number) {
    this.currentAvatarID = avatarID
  }
}
