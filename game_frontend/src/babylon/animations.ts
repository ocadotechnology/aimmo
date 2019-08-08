import * as BABYLON from 'babylonjs'

// Creates an animation that rotates an object around the y axis 
export function rotationAnimation (frameRate: number) : BABYLON.Animation {
  var rotation = new BABYLON.Animation('rotation', 'rotation.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
  var keyFramesR = []

  keyFramesR.push({
    frame: 0,
    value: 0
  })
  keyFramesR.push({
    frame: frameRate,
    value: Math.PI
  })
  keyFramesR.push({
    frame: 2 * frameRate,
    value: 2 * Math.PI
  })

  rotation.setKeys(keyFramesR)

  return rotation
}

// Creates an animation that moves an object up and down across the y axis
export function hoveringFloat (frameRate: number) : BABYLON.Animation {
  var slideAnimation = new BABYLON.Animation('translation', 'position.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
  var keyFramesR = []

  for (let i = 0; i <= 2 * frameRate; i++) {
    keyFramesR.push({
      frame: i,
      value: 0.2 * Math.sin(Math.PI * (i / frameRate))
    })
  }

  slideAnimation.setKeys(keyFramesR)

  return slideAnimation
}
