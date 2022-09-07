import * as BABYLON from 'babylonjs'

/**
 * This function is used by tests to override the Babylon JS ImportMesh function, since importing meshes doesn't work
 * without a running server. It creates a dummy cube to replace the mesh that would be imported otherwise.
 * @param meshName
 * @param filePath
 * @param fileName
 * @param scene
 * @param onSuccess
 */
export default async function dummyImportMeshAsync(
  meshName: string,
  filePath: string,
  fileName: string,
  scene: BABYLON.Scene
): Promise<any> {
  const meshes: BABYLON.AbstractMesh[] = []
  meshes[0] = BABYLON.MeshBuilder.CreateBox('', { height: 1 }, scene)
  meshes[0].skeleton = new BABYLON.Skeleton('box bones', 'box bones', scene)
  return Promise.resolve({ meshes })
}
