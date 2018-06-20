/* eslint-env jest */
import React from 'react'
import IDEConsole from 'components/IDEConsole'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEConsole />)
    expect(tree).toMatchSnapshot()
  })
})
