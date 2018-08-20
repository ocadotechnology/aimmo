/* eslint-env jest */
import React from 'react'
import { Game } from 'containers/Game'
import { shallow } from 'enzyme'
import toJson from 'enzyme-to-json'

describe('<Game />', () => {
  it('renders correctly', () => {
    const tree = shallow(<Game />)
    expect(toJson(tree)).toMatchSnapshot()
  })
})
