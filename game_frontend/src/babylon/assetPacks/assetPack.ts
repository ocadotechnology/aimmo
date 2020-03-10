import {
  Vector3,
  SceneLoader,
  AbstractMesh,
  StandardMaterial,
  Texture,
  TransformNode,
  Mesh,
  Color3
} from 'babylonjs'
import { Environment } from '../environment/environment'

const tileSizes = {
  future: { w: 31, h: 31 },
  prehistory: { w: 1, h: 1 },
  grid: { w: 31, h: 31 }
}

export interface StandardAsset {
  name: string
  modelURL: string
  modelName: string
  textureURL: string
  materialName: string
}

export interface PlaneAsset {
  name: string
  tileSize: any
  materialName: string
  textureURL: string
}

export class AssetPack {
  environment: Environment
  obstacleInfo: StandardAsset
  terrianInfo: PlaneAsset
  gridInfo: PlaneAsset = {
    name: 'grid',
    tileSize: tileSizes['grid'],
    materialName: 'grid_material',
    textureURL: '/static/babylon/terrain/grid.png'
  }
  interactableMaterials: Record<string, StandardMaterial>

  constructor (environment: Environment) {
    this.environment = environment
    this.obstacleInfo = getObstacleAssetInfoForEra(environment.era)
    this.terrianInfo = this.getTerrainInfoForEra(environment.era)
    this.interactableMaterials = {
      artefact: this.createInteractableMaterial('artefact')
    }
  }

  createInteractableMaterial (interactableType: string): StandardMaterial {
    const texture = `/static/babylon/interactables/${interactableType}_texture.png`
    const material = new StandardMaterial(interactableType, this.environment.scene)
    material.specularColor = new BABYLON.Color3(0, 0, 0)
    material.emissiveColor = new BABYLON.Color3(0, 0, 0)
    material.diffuseTexture = new Texture(texture, this.environment.scene)
    return material
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
    type: string,
    location: Vector3,
    parent: TransformNode
  ): Promise<AbstractMesh> {
    const model = `${type}_model.babylon`
    const { meshes } = await SceneLoader.ImportMeshAsync(
      type,
      '/static/babylon/interactables/',
      model,
      this.environment.scene
    )
    const interactable = meshes[0]
    interactable.material = this.interactableMaterials[type]
    interactable.name = name
    interactable.parent = parent
    interactable.position = location
    return interactable
  }

  createGridOverlay (parent: TransformNode): AbstractMesh {
    const gridOverlay = Mesh.CreateTiledGround(
      this.gridInfo.name,
      -15,
      -15,
      16,
      16,
      this.gridInfo.tileSize,
      { w: 1, h: 1 },
      this.environment.scene
    )
    const gridOverlayMaterial = new StandardMaterial(
      this.gridInfo.materialName,
      this.environment.scene
    )

    gridOverlayMaterial.diffuseColor = Color3.Black()
    gridOverlayMaterial.specularColor = Color3.Black()
    gridOverlayMaterial.ambientColor = BABYLON.Color3.White()
    gridOverlayMaterial.opacityTexture = new BABYLON.Texture(
      this.gridInfo.textureURL,
      this.environment.scene
    )
    gridOverlay.material = gridOverlayMaterial
    return gridOverlay
  }

  createTerrain (parent: TransformNode): AbstractMesh {
    const terrain = Mesh.CreateTiledGround(
      this.terrianInfo.name,
      -15,
      -15,
      16,
      16,
      this.terrianInfo.tileSize,
      { w: 1, h: 1 },
      this.environment.scene
    )
    const material = new StandardMaterial(this.terrianInfo.materialName, this.environment.scene)

    material.useReflectionOverAlpha = false
    material.diffuseTexture = new Texture(this.terrianInfo.textureURL, this.environment.scene)
    material.diffuseTexture.level = 1.2
    material.specularColor = Color3.Black()
    material.ambientColor = Color3.White()

    terrain.material = material
    return terrain
  }

  protected getTerrainInfoForEra(era: string): PlaneAsset {
    return {
      name: 'terrain',
      tileSize: tileSizes[era],
      materialName: `terrain_material_${era}`,
      textureURL: `/static/babylon/terrain/terrain_${era}.jpg`
    }
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
