/* eslint-env jest */
import React from 'react'
import ThemeProvider from 'components/ThemeProvider'
import { shallow } from 'enzyme'

describe('<IDEConsole />', () => {
  it('provides a theme', () => {
    const tree = shallow(<ThemeProvider variant='light'>Hello</ThemeProvider>)
    expect(tree).toMatchSnapshot()
  })
})
