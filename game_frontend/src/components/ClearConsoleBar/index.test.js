/* eslint-env jest */
import React from 'react'
import ClearConsoleBar from 'components/ClearConsoleBar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<ClearConsoleBar />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<ClearConsoleBar />)

    expect(tree).toMatchSnapshot()
  })
})
