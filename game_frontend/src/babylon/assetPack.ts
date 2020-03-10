import {
  Vector3,
  Scene,
  SceneLoader,
  AbstractMesh,
  StandardMaterial,
  Texture,
  Color3,
  TransformNode,
  Space,
  Axis
} from 'babylonjs'
import { Environment } from './environment/environment'

const tileSizes = {
  future: { w: 31, h: 31 },
  prehistory: { w: 1, h: 1 },
  grid: { w: 31, h: 31 }
}

export interface StandardAsset {
  name: string;
  modelURL: string;
  modelName: string;
  textureURL: string;
  materialName: string;
}

export interface PlaneAsset {
  name: string;
  tileSize: any;
  materialName: string;
  textureURL: string;
}

export class AssetPack {
  environment: Environment
  obstacleInfo: StandardAsset
  terrianInfo: PlaneAsset
  gridInfo: PlaneAsset

  constructor (environment: Environment) {
    this.environment = environment
    this.obstacleInfo = getObstacleAssetInfoForEra(environment.era)
  }

  async createObstacle (name: string, location: Vector3, parent: TransformNode) {
    const { meshes } = await SceneLoader.ImportMeshAsync(
      this.obstacleInfo.name,
      this.obstacleInfo.modelURL,
      this.obstacleInfo.modelName,
      this.environment.scene
    )
    const obstacle = meshes[0]
    obstacle.name = name
    obstacle.position = location
    obstacle.parent = parent
    return obstacle
  }

  async createInteractable (
    name: string,
    location: Vector3
  ): Promise<AbstractMesh> {
    throw new Error('Method not implemented.')
  }
  async createGrid (): Promise<AbstractMesh> {
    throw new Error('Method not implemented.')
  }
  async createTerrain (): Promise<AbstractMesh> {
    throw new Error('Method not implemented.')
  }
}

function getObstacleAssetInfoForEra (era: string): StandardAsset {
  return {
    name: 'obstacle',
    modelURL: '/static/babylon/obstacles/',
    modelName: `obstacle_model_${era}.babylon`,
    textureURL: `/static/babylon/obstacles/obstacle_${era}.jpg`,
    materialName: `obstacle_material_${era}`
  }
}

export class FutureAssetPack extends AssetPack {
  obstacleMaterial: StandardMaterial

  constructor (environment: Environment) {
    super(environment)
    this.obstacleMaterial = this.makeObstacleMaterial()
  }

  makeObstacleMaterial (): StandardMaterial {
    const material = new StandardMaterial(
      this.obstacleInfo.materialName,
      this.environment.scene
    )
    material.diffuseTexture = new Texture(
      this.obstacleInfo.textureURL,
      this.environment.scene
    )
    material.specularColor = new Color3(0, 0, 0)
    material.diffuseColor = new Color3(1, 1, 1)
    return material
  }

  async createObstacle (
    name: string,
    location: Vector3,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const obstacle = await super.createObstacle(name, location, parent)
    obstacle.material = this.obstacleMaterial
    return obstacle
  }
}

export class PreHistoryAssetPack extends AssetPack {
  obstacleMaterial: StandardMaterial

  constructor (environment: Environment) {
    super(environment)
    this.obstacleMaterial = this.makeObstacleMaterial()
  }

  makeObstacleMaterial (): StandardMaterial {
    const material = new StandardMaterial(
      this.obstacleInfo.materialName,
      this.environment.scene
    )
    material.diffuseTexture = new Texture(
      this.obstacleInfo.textureURL,
      this.environment.scene
    )
    material.specularColor = new Color3(0, 0, 0)
    material.diffuseColor = new Color3(0.70, 0.80, 1)
    return material
  }

  async createObstacle (
    name: string,
    location: Vector3,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const obstacle = await super.createObstacle(name, location, parent)
    obstacle.material = this.obstacleMaterial
    obstacle.rotate(Axis.Y, this.createRandomRotation(), Space.WORLD)
    return obstacle
  }

  /**
   * This function returns a random angle in radians
   *
   * @return {number} a random angle in radians, in increments of a quarter
   *
   */
  createRandomRotation (): number {
    return Math.PI / (Math.floor(Math.random() * Math.floor(4)) + 1)
  }
}

/**
 * Used to store game assets and map them to eras
 */
export class AssetSomethingPack {
  obstacles: StandardAsset
  terrain: PlaneAsset
  grid: PlaneAsset

  constructor (era: string) {
    this.createObstacles(era)
    this.createTerrain(era)
    this.createGrid()
  }

  createObstacles (era: string): void {
    this.obstacles = {
      name: 'obstacle',
      modelURL: '/static/babylon/obstacles/',
      modelName: `obstacle_model_${era}.babylon`,
      textureURL: `/static/babylon/obstacles/obstacle_${era}.jpg`,
      materialName: `obstacle_material_${era}`
    }
  }

  createTerrain (era: string): void {
    this.terrain = {
      name: 'terrain',
      tileSize: tileSizes[era],
      materialName: `terrain_material_${era}`,
      textureURL: `/static/babylon/terrain/terrain_${era}.jpg`
    }
  }

  createGrid (): void {
    this.grid = {
      name: 'grid',
      tileSize: tileSizes['grid'],
      materialName: 'grid_material',
      textureURL: '/static/babylon/terrain/grid.png'
    }
  }
}

export function getAssetPackForEra (era: string, environment: Environment): AssetPack {
  switch (environment.era) {
    case 'future':
      return new FutureAssetPack(environment)
    default:
      return new FutureAssetPack(environment)
  }
}
