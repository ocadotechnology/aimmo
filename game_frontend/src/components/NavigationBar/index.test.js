/* eslint-env jest */
import React from 'react'
import { NavigationBarLayout } from 'components/NavigationBar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<NavigationBarLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<NavigationBarLayout />)
    expect(tree).toMatchSnapshot()
  })
})
