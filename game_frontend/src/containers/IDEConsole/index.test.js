/* eslint-env jest */
import React from 'react'
import { IDEConsole, StyledConsole } from 'containers/IDEConsole'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(
      <IDEConsole logs={[{ timestamp: '1', log: 'hello' }, { timestamp: '2', log: 'bye' }]} />,
      'dark'
    )
    expect(tree).toMatchSnapshot()
  })

  it('clears logs properly when clearLogs is called', () => {
    const tree = createShallowWithTheme(
      <IDEConsole logs={[{ timestamp: '1', log: 'hello' }, { timestamp: '2', log: 'bye' }]} />,
      'dark'
    )

    expect(tree.props.logs.length).toBe(0)
  })
})

describe('<StyledConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<StyledConsole />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})
