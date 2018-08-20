/* eslint-env jest */
import React from 'react'
import { Game } from 'containers/Game'
import { shallow } from 'enzyme'
import toJson from 'enzyme-to-json'

describe('<Game />', () => {
  it('renders correctly', () => {
    const props = {
      connectToGame: jest.fn()
    }
    const tree = shallow(<Game {...props} />)
    expect(toJson(tree)).toMatchSnapshot()
  })
})
