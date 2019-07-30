import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'
import EnvironmentRenderer from '.'

export default class Terrain implements GameNode {
    object: any;

    setup(environmentRenderer: EnvironmentRenderer): void {
        const ground = BABYLON.Mesh.CreateTiledGround('terrain', -15, -15, 16, 16, { w: 31, h: 31 }, { w: 1, h: 1 }, environmentRenderer.scene)
        this.object = ground

        const mat = new BABYLON.StandardMaterial('Terrain', environmentRenderer.scene)
        mat.useReflectionOverAlpha = false
        mat.diffuseTexture = new BABYLON.Texture('/static/images/terrain_future.jpg', environmentRenderer.scene)
        mat.diffuseTexture.level = 1.2
        mat.specularColor = new BABYLON.Color3(0, 0, 0)
        mat.ambientColor = BABYLON.Color3.White()
        ground.material = mat
    }


    onGameStateUpdate(): void { }
}
