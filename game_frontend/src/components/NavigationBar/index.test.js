/* eslint-env jest */
import React from 'react'
import NavigationBar, { NavigationBarLayout } from 'components/NavigationBar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<NavigationBar />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<NavigationBar />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<NavigationBarLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<NavigationBarLayout />)
    expect(tree).toMatchSnapshot()
  })
})
