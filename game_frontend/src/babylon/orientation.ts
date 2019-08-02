import * as BABYLON from 'babylonjs'

export default function setOrientation (mesh: BABYLON.AbstractMesh, orientation: string): void {
  let yAxis = new BABYLON.Vector3(0, 1, 0)
  switch (orientation) {
    case 'north':
      mesh.rotate(
        yAxis,
        Math.PI
      )
      break
    case 'east':
      mesh.rotate(
        yAxis,
        3 * Math.PI / 2
      )
      break
    case 'south':
      mesh.rotate(
        yAxis,
        0
      )
      break
    case 'west':
      mesh.rotate(
        yAxis,
        Math.PI / 2
      )
      break
    default:
      console.log(`${mesh} was not provided with a valid orientation: ${orientation}`)
  }
}
