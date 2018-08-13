/* eslint-env jest */
import React from 'react'
import { shallow } from 'enzyme'
import toJson from 'enzyme-to-json'
import { IDE } from 'containers/IDE'

describe('<IDE />', () => {
  it('renders correctly', () => {
    const tree = shallow(<IDE />)
    expect(toJson(tree)).toMatchSnapshot()
  })
})
