import * as BABYLON from 'babylonjs'

export const MAX_KEYFRAMES_PER_SECOND = 24

/**
 * This function creates an animation that rotates an object around the y axis
 *
 * @param {string} objectType - the type of object the animation is created for
 * @return {BABYLON.Animation} A Babylon JS animation object
 *
 * @example
 *
 *     rotationAnimation(5, 'interactable')
 */
export function rotationAnimation(objectType: string): BABYLON.Animation {
  const rotation = new BABYLON.Animation(
    `${objectType} rotation`,
    'rotation.y',
    1,
    BABYLON.Animation.ANIMATIONTYPE_FLOAT,
    BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE
  )
  const keyFrames = []

  keyFrames.push({
    frame: 0,
    value: 0,
  })
  keyFrames.push({
    frame: 1,
    value: Math.PI,
  })
  keyFrames.push({
    frame: 2,
    value: 2 * Math.PI,
  })

  rotation.setKeys(keyFrames)

  return rotation
}
/**
 *  Creates an animation that moves an object up and down across the y axis
 *
 * @param {string} objectType - the type of object the animation is created for
 * @return {BABYLON.Animation} A Babylon JS animation object
 *
 * @example
 *
 *     bobbingAnimation(5, 'interactable')
 */
export function bobbingAnimation(objectType: string): BABYLON.Animation {
  const bobbing = new BABYLON.Animation(
    `${objectType} bobbing`,
    'position.y',
    1,
    BABYLON.Animation.ANIMATIONTYPE_FLOAT,
    BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE
  )
  const keyFrames = [
    {
      frame: 0,
      value: 0,
    },
    {
      frame: 1,
      value: 0.3,
    },
    {
      frame: 2,
      value: 0,
    },
  ]

  bobbing.setKeys(keyFrames)
  bobbing.setEasingFunction(new BABYLON.SineEase())

  return bobbing
}

export function createMoveAnimation(
  fromPosition: BABYLON.Vector3,
  toPosition: BABYLON.Vector3
): BABYLON.Animation {
  const move = new BABYLON.Animation(
    'move',
    'position',
    1,
    BABYLON.Animation.ANIMATIONTYPE_VECTOR3,
    BABYLON.Animation.ANIMATIONLOOPMODE_CONSTANT
  )
  const keyFrames = [
    {
      frame: 0,
      value: fromPosition,
    },
    {
      frame: 1,
      value: toPosition,
    },
  ]

  move.setKeys(keyFrames)
  const easingFunction = new BABYLON.QuadraticEase()
  easingFunction.setEasingMode(BABYLON.EasingFunction.EASINGMODE_EASEINOUT)
  move.setEasingFunction(easingFunction)

  return move
}
/**
 * Gets the `runAnimation` from the skeleton of the given mesh (Avatar) and
 * plays it.
 * @param mesh
 * @param scene
 */
export function createWalkAnimation(mesh: BABYLON.AbstractMesh, scene: BABYLON.Scene) {
  // Load animation
  const runningRange = mesh.skeleton.getAnimationRange('runAnimation')
  if (runningRange) {
    scene.beginAnimation(mesh.skeleton, 10, 35, false)
  }
}
