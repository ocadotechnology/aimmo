import { GameNode } from '../interfaces'
import * as BABYLON from 'babylonjs'

export default class Terrain implements GameNode {
    object: any;
    onTerrainNode: any;

    onSceneMount(scene: BABYLON.Scene, canvas: HTMLCanvasElement, engine: BABYLON.Engine): void {
        const ground = BABYLON.Mesh.CreateTiledGround('terrain', -15, -15, 16, 16, { w: 31, h: 31 }, { w: 1, h: 1 }, scene)
        this.object = ground

        const mat = new BABYLON.StandardMaterial('Terrain', scene)
        mat.useReflectionOverAlpha = false
        mat.diffuseTexture = new BABYLON.Texture('/static/images/terrain_future.jpg', scene)
        mat.diffuseTexture.level = 1.2
        mat.specularColor = new BABYLON.Color3(0, 0, 0)
        mat.ambientColor = BABYLON.Color3.White()
        ground.material = mat

        this.onTerrainNode = new BABYLON.TransformNode('On Terrain', scene)
        this.onTerrainNode.position = new BABYLON.Vector3(-0.5, 0, -0.5)
    }


    onGameStateUpdate(): void { }
}
