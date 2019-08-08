import * as BABYLON from 'babylonjs'

/**
  * This function creates an animation that rotates an object around the y axis
  *
  * @param {number} frameRate - duration of half the animation, in frames
  * @param {string} objectType - the type of object the animation is created for
  * @return {BABYLON.Animation} A Babylon JS animation object
  *
  * @example
  *
  *     rotationAnimation(5, 'interactable')
  */
export function rotationAnimation (frameRate: number, objectType: string) : BABYLON.Animation {
  var rotation = new BABYLON.Animation(`${objectType} rotation`, 'rotation.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
  var keyFrames = []

  keyFrames.push({
    frame: 0,
    value: 0
  })
  keyFrames.push({
    frame: frameRate,
    value: Math.PI
  })
  keyFrames.push({
    frame: 2 * frameRate,
    value: 2 * Math.PI
  })

  rotation.setKeys(keyFrames)

  return rotation
}
/**
  *  Creates an animation that moves an object up and down across the y axis
  *
  * @param {number} frameRate - duration of half the animation, in frames
  * @param {string} objectType - the type of object the animation is created for
  * @return {BABYLON.Animation} A Babylon JS animation object
  *
  * @example
  *
  *     bobbingAnimation(5, 'interactable')
  */
export function bobbingAnimation (frameRate: number, objectType: string) : BABYLON.Animation {
  var bobbing = new BABYLON.Animation(`${objectType} bobbing`, 'position.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
  var keyFrames = []

  for (let i = 0; i <= 2 * frameRate; i++) {
    keyFrames.push({
      frame: i,
      value: 0.2 * Math.sin(Math.PI * (i / frameRate))
    })
  }

  bobbing.setKeys(keyFrames)

  return bobbing
}
