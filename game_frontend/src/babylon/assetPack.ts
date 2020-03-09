const tileSizes = {
  future: { w: 31, h: 31 },
  prehistory: { w: 1, h: 1 },
  grid: { w: 31, h: 31 }
}

export interface StandardAsset {
  name: string,
  modelURL: string,
  modelName: string,
  textureURL: string,
  materialName: string
}

export interface PlaneAsset {
  name: string,
  tileSize: any,
  materialName: string,
  textureURL: string
}

/**
 * Used to store game assets and map them to eras
 */
export class AssetPack {
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
