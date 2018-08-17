/* eslint-env jest */
import React from 'react'
import IDEMenuLayout from 'components/IDEMenu'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEMenuLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEMenuLayout />)
    expect(tree).toMatchSnapshot()
  })
})
