import { GameNode } from '../interfaces'
import { Mesh, Color3, Scene, Engine, StandardMaterial, Texture } from 'babylonjs'

export default class Terrain implements GameNode {
    object: any;

    onSceneMount(scene: Scene, canvas: HTMLCanvasElement, engine: Engine): void {
        const ground = Mesh.CreateTiledGround('terrain', -15, -15, 16, 16, { w: 31, h: 31 }, { w: 1, h: 1 }, scene)
        this.object = ground

        const mat = new StandardMaterial('Terrain', scene)
        mat.useReflectionOverAlpha = false
        mat.diffuseTexture = new Texture('/static/images/terrain_future.jpg', scene)
        mat.diffuseTexture.level = 1.2
        mat.specularColor = new Color3(0, 0, 0)
        mat.ambientColor = Color3.White()
        ground.material = mat
    }


    onGameStateUpdate(): void { }
}