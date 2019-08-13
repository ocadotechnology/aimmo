import * as BABYLON from 'babylonjs'

export default function dummyImportMesh (meshName: string, filePath: string, fileName: string, scene: BABYLON.Scene, onSuccess: Function): void {
  const meshes = []
  meshes[0] = BABYLON.MeshBuilder.CreateBox('', { height: 1 }, this.scene)

  onSuccess(meshes, [], [], [])
}
