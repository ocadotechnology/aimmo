/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Camera from './camera'

describe('the camera', () => {
  it('loads', () => {
    let camera = new Camera()
    let environment = new MockEnvironment()

    environment.canvas = document.createElement('canvas')

    camera.setup(environment)

    expect(camera.object).toMatchSnapshot()
  })
})