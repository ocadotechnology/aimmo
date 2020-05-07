import {
  SceneLoader,
  StandardMaterial,
  Texture,
  Mesh,
  Color3,
  Scene,
  Vector3,
  TransformNode,
  AbstractMesh
} from 'babylonjs'

const tileSizes = {
  future: { w: 31, h: 31 },
  prehistory: { w: 1, h: 1 },
  ancient: { w: 1, h: 1 },
  modern: { w: 31, h: 31 },
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

export default class AssetPack {
  scene: Scene
  obstacleInfo: StandardAsset
  terrainInfo: PlaneAsset
  gridInfo: PlaneAsset = {
    name: 'grid',
    tileSize: tileSizes.grid,
    materialName: 'grid_material',
    textureURL: '/static/babylon/terrain/grid.png'
  }

  interactableMaterials: Record<string, StandardMaterial>
  importMeshAsync: Function

  constructor (era: string, scene: Scene, importMeshAsync: Function = SceneLoader.ImportMeshAsync) {
    this.scene = scene
    this.importMeshAsync = importMeshAsync
    this.obstacleInfo = getObstacleAssetInfoForEra(era)
    this.terrainInfo = this.getTerrainInfoForEra(era)
    this.interactableMaterials = {
      artefact: this.createInteractableMaterial('artefact')
    }
  }

  createInteractableMaterial (interactableType: string): StandardMaterial {
    const texture = `/static/babylon/interactables/${interactableType}_texture.png`
    const material = new StandardMaterial(interactableType, this.scene)
    material.specularColor = new Color3(0, 0, 0)
    material.emissiveColor = new Color3(0, 0, 0)
    material.diffuseTexture = new Texture(texture, this.scene)
    return material
  }

  async createObstacle (name: string, location: Vector3, parent: TransformNode) {
    const { meshes } = await this.importMeshAsync(
      this.obstacleInfo.name,
      this.obstacleInfo.modelURL,
      this.obstacleInfo.modelName,
      this.scene
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
    const { meshes } = await this.importMeshAsync(
      type,
      '/static/babylon/interactables/',
      model,
      this.scene
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
      this.scene
    )
    const gridOverlayMaterial = new StandardMaterial(this.gridInfo.materialName, this.scene)

    gridOverlayMaterial.diffuseColor = Color3.Black()
    gridOverlayMaterial.specularColor = Color3.Black()
    gridOverlayMaterial.ambientColor = Color3.White()
    gridOverlayMaterial.opacityTexture = new Texture(this.gridInfo.textureURL, this.scene)
    gridOverlay.material = gridOverlayMaterial
    return gridOverlay
  }

  createTerrain (parent: TransformNode): AbstractMesh {
    const terrain = Mesh.CreateTiledGround(
      this.terrainInfo.name,
      -15,
      -15,
      16,
      16,
      this.terrainInfo.tileSize,
      { w: 1, h: 1 },
      this.scene
    )
    const material = new StandardMaterial(this.terrainInfo.materialName, this.scene)

    material.useReflectionOverAlpha = false
    material.diffuseTexture = new Texture(this.terrainInfo.textureURL, this.scene)
    material.diffuseTexture.level = 1.2
    material.specularColor = Color3.Black()
    material.ambientColor = Color3.White()

    terrain.material = material
    return terrain
  }

  protected getTerrainInfoForEra (era: string): PlaneAsset {
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
