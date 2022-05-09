import AssetPack from './assetPack'
import {
  StandardMaterial,
  Texture,
  Color3,
  Vector3,
  TransformNode,
  Axis,
  Space,
  AbstractMesh,
  Scene,
  Color4,
} from 'babylonjs'

export default class ModernAssetPack extends AssetPack {
  obstacleMaterials: StandardMaterial[]

  backgroundColor = new Color4(0.525, 0.729, 0.851)

  constructor(era: string, scene: Scene) {
    super(era, scene)
    this.obstacleMaterials = this.makeObstacleMaterials()
  }

  async createInteractable(
    name: string,
    type: string,
    location: Vector3,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const model = `${type}.babylon`
    const { meshes } = await this.importMeshAsync(
      'artefact',
      '/static/babylon/interactables/modern/',
      model,
      this.scene
    )
    const interactable = meshes[0]
    interactable.name = name
    interactable.parent = parent
    interactable.position = location
    interactable.scaling = new Vector3(0.6, 0.6, 0.6)
    interactable.rotation = new Vector3(0, Math.PI, 0)
    interactable.metadata = {
      type: type,
    }
    return interactable
  }

  makeObstacleMaterials(): StandardMaterial[] {
    return [1, 2].map((textureChoice) => {
      const material = new StandardMaterial(
        `${this.obstacleInfo.materialName}_${textureChoice}`,
        this.scene
      )
      material.diffuseTexture = new Texture(this.getTextureURL(textureChoice), this.scene)
      material.specularColor = new Color3(0, 0, 0)
      material.diffuseColor = new Color3(0.7, 0.8, 1)
      return material
    })
  }

  async createObstacle(
    name: string,
    location: Vector3,
    textureChoice: number,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const obstacle = await super.createObstacle(name, location, textureChoice, parent)
    obstacle.material = this.obstacleMaterials[textureChoice - 1]
    obstacle.rotate(Axis.Y, this.createRandomRotation(), Space.WORLD)
    return obstacle
  }

  /**
   * This function returns a random angle in radians
   *
   * @return {number} a random angle in radians, in increments of a quarter
   *
   */
  createRandomRotation(): number {
    return Math.PI / (Math.floor(Math.random() * Math.floor(4)) + 1)
  }
}
