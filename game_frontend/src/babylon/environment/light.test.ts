/* eslint-env jest */
import { MockEnvironment } from '../../testHelpers/mockEnvironment'
import Light from './light'

describe('Light', () => {
  it('loads', () => {
    const environment = new MockEnvironment(true, 'future')
    const light = new Light(environment)

    expect(light.object).toMatchSnapshot()
  })
})
