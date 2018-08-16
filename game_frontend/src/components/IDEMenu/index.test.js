/* eslint-env jest */
import React from 'react'
import IDEMenu, { IDEMenuLayout } from 'components/IDEMenu'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEMenu />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEMenu />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<IDEMenuLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEMenuLayout />)
    expect(tree).toMatchSnapshot()
  })
})
