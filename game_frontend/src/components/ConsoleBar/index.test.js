/* eslint-env jest */
import React from 'react'
import ConsoleBar, { ClearToolbar, StyledConsoleIcon } from 'components/ConsoleBar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<ConsoleBar />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<ConsoleBar />)

    expect(tree).toMatchSnapshot()
  })
})

describe('<ClearToolBar />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<ClearToolbar />)

    expect(tree).toMatchSnapshot()
  })
})

describe('<StyledConsoleIcon />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<StyledConsoleIcon />)

    expect(tree).toMatchSnapshot()
  })
})
