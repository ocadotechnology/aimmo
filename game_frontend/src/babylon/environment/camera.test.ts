/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Camera from './camera'

describe('Camera', () => {
  it('loads', () => {
    let environment = new MockEnvironment(true, 'future')
    let camera = new Camera(environment)

    expect(camera.object).toMatchSnapshot()
  })
})
