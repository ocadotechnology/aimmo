/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Light from './light'

describe('Light', () => {
  it('loads', () => {
    let environment = new MockEnvironment()
    let light = new Light(environment)

    expect(light.object).toMatchSnapshot()
  })
})
