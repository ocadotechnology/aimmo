import * as BABYLON from 'babylonjs'

export function hoveringRotation (frameRate: number) : BABYLON.Animation {
  var rotationAnimation = new BABYLON.Animation('interactable rotation', 'rotation.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
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

  rotationAnimation.setKeys(keyFramesR)

  return rotationAnimation
}

export function hoveringFloat (frameRate: number) : BABYLON.Animation {
  var slideAnimation = new BABYLON.Animation('interactable translation', 'position.y', frameRate, BABYLON.Animation.ANIMATIONTYPE_FLOAT, BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE)
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
