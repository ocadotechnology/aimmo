/* eslint-env jest */
import React from 'react'
import LogEntries, { StyledLogEntries, LogEntry } from 'components/LogEntries'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<LogEntries />', () => {
  it('renders correctly with logs', () => {
    const tree = createShallowWithTheme(
      <LogEntries logs={[{ turn_count: 0, message: 'hello' }, { turn_count: 1, message: 'bye' }]} />,
      'dark'
    )
    expect(tree).toMatchSnapshot()
  })

  it('renders correctly without logs', () => {
    const tree = createShallowWithTheme(<LogEntries logs={[]} />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<StyledLogEntries />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(
      <StyledLogEntries logs={[{ timestamp: '1', log: 'hello' }, { timestamp: 2, log: 'bye' }]} />,
      'dark'
    )
    expect(tree).toMatchSnapshot()
  })
})

describe('<LogEntry />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<LogEntry>hello</LogEntry>, 'dark')
    expect(tree).toMatchSnapshot()
  })
})
