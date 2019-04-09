/* eslint-env jest */
import React from 'react'
import { IDEConsole, StyledConsole } from 'containers/IDEConsole'
import ConsoleBar from 'components/ConsoleBar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(
      <IDEConsole logs={[{ timestamp: '1', log: 'hello' }, { timestamp: '2', log: 'bye' }]} />,
      'dark'
    )
    expect(tree).toMatchSnapshot()
  })
})

describe('<StyledConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<StyledConsole />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<ConsoleBar />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<ConsoleBar />)

    expect(tree).toMatchSnapshot()
  })
})
