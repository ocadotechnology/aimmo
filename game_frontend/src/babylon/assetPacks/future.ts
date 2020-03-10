import { StandardMaterial, Texture, Color3, Vector3, TransformNode, AbstractMesh } from 'babylonjs'
import { AssetPack } from './assetPack'
import { Environment } from '../environment/environment'

export default class FutureAssetPack extends AssetPack {
    obstacleMaterial: StandardMaterial

    constructor (environment: Environment) {
      super(environment)
      this.obstacleMaterial = this.makeObstacleMaterial()
    }

    makeObstacleMaterial (): StandardMaterial {
      const material = new StandardMaterial(this.obstacleInfo.materialName, this.environment.scene)
      material.diffuseTexture = new Texture(this.obstacleInfo.textureURL, this.environment.scene)
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
