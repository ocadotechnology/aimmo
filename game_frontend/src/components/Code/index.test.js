/* eslint-env jest */
import React from 'react'
import Code from 'components/Code'
import { shallow } from 'enzyme'
import toJson from 'enzyme-to-json'
import withTheme from 'testHelpers/withTheme'

describe('<Code />', () => {
  it('renders correctly', () => {
    const tree = shallow(withTheme(<Code>Code</Code>))
    expect(toJson(tree)).toMatchSnapshot()
  })
})
