import * as BABYLON from 'babylonjs'

const northOrientation = new BABYLON.Vector3(0, Math.PI, -0)
const eastOrientation = new BABYLON.Vector3(0, 3 * (Math.PI / 2), 0)
const southOrientation = new BABYLON.Vector3(0, 0, 0)
const westOrientation = new BABYLON.Vector3(0, Math.PI / 2, 0)

export default function setOrientation(mesh: BABYLON.AbstractMesh, orientation: string): void {
  switch (orientation) {
    case 'north':
      if (mesh.rotation !== northOrientation) {
        mesh.rotation = northOrientation
      }
      break
    case 'east':
      if (mesh.rotation !== eastOrientation) {
        mesh.rotation = eastOrientation
      }
      break
    case 'south':
      if (mesh.rotation !== southOrientation) {
        mesh.rotation = southOrientation
      }
      break
    case 'west':
      if (mesh.rotation !== westOrientation) {
        mesh.rotation = westOrientation
      }
      break
    default:
      console.warn(`${mesh} was not provided with a valid orientation: ${orientation}`)
  }
}
