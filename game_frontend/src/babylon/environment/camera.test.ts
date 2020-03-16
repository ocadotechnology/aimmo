/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Camera from './camera'

describe('Camera', () => {
  it('loads', () => {
    const environment = new MockEnvironment(true, 'future')
    const camera = new Camera(environment)

    expect(camera.object).toMatchSnapshot()
  })
})
