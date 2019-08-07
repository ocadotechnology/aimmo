/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Light from './light'

describe('the light', () => {
  it('loads', () => {
    let light = new Light()
    let environment = new MockEnvironment()

    light.setup(environment)

    expect(light.object).toMatchSnapshot()
  })
})