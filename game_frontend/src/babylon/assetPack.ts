import { StandardMaterial } from "babylonjs"

const tileSizes = {
    'future': { w: 31, h: 31 },
    'prehistory': { w: 1, h: 1 },
    'grid': { w: 31, h: 31 }
}

export class StandardAsset {
    name: string
    modelURL: string
    modelName: string
    textureURL: string
    materialName: string

    constructor(name: string, modelURL: string, modelName: string, textureURL: string, materialName: string): void {
        this.name = name
        this.modelURL = modelURL
        this.modelName = modelName
        this.textureURL = textureURL
        this.materialName = materialName
    }
}

export class PlaneAsset {
    name: string
    tileSize: any
    materialName: string
    textureURL: string

    constructor(name: string, tileSize: any, materialName: string, textureURL: string): void {
        this.name = name
        this.tileSize = tileSizes
        this.materialName = materialName
        this.textureURL = textureURL
    }
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

    createObstacles(era: string): void {
        var name = 'obstacle'
        var modelURL = '/static/babylon/obstacles/'
        var modelName = 'obstacle_model_' + era + '.babylon'
        var textureURL = '/static/babylon/obstacles/obstacle_' + era + '.jpg'
        var materialName = 'obstacle_material_' + era

        this.obstacles = new StandardAsset(name, modelURL, modelName, textureURL, materialName)
    }

    createTerrain(era: string): void {
        var name = 'terrain'
        var tileSize = tileSizes[era]
        var materialName = 'terrain_material_' + era
        var textureURL = '/static/babylon/terrain/terrain_' + era + '.jpg'

        this.terrain = new PlaneAsset(name, tileSize, materialName, textureURL)
    }

    createGrid(): void {
        var name = 'grid'
        var tileSize = tileSizes['grid']
        var materialName = 'grid_material'
        var textureURL = '/static/babylon/grid.png'

        this.grid = new PlaneAsset(name, tileSize, materialName, textureURL)
    }
}  