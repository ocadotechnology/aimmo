/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import EnvironmentManager from './environmentManager'
import AssetPack from './../assetPacks/assetPack'
import dummyImportMeshAsync from 'testHelpers/dummyImportMeshAsync'
import { Color4 } from 'babylonjs'

describe('EnvironmentManager', () => {
  it('loads', () => {
    const environment = new MockEnvironment(true, 'future')
    const assetPack = new AssetPack('testera', environment.scene, dummyImportMeshAsync)
    const backgroundColor = new Color4(0.5, 0.6, 0.7)
    assetPack.backgroundColor = backgroundColor
    const environmentManager = new EnvironmentManager(environment, assetPack)

    expect(environmentManager.environment.scene.clearColor).toEqual(backgroundColor)
  })
})
