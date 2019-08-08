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
export function rotationAnimation (objectType: string) : BABYLON.Animation {
  let rotation = new BABYLON.Animation(`${objectType} rotation`, 'rotation.y', 1, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
  let keyFrames = []

  keyFrames.push({
    frame: 0,
    value: 0
  })
  keyFrames.push({
    frame: 1,
    value: Math.PI
  })
  keyFrames.push({
    frame: 2,
    value: 2 * Math.PI
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
export function bobbingAnimation (objectType: string) : BABYLON.Animation {
  let bobbing = new BABYLON.Animation(`${objectType} bobbing`, 'position.y', 1, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
  let keyFrames = []

  keyFrames.push({
    frame: 0,
    value: -0.15
  })
  keyFrames.push({
    frame: 1,
    value: 0.15
  })
  keyFrames.push({
    frame: 2,
    value: -0.15
  })

  bobbing.setKeys(keyFrames)
  bobbing.setEasingFunction(new BABYLON.SineEase())

  return bobbing
}
