/* eslint-env jest */
import React from 'react'
import LogEntries, {
  LogEntry,
  LogData,
  LogTurn,
  BottomSnapper,
  StyledTable
} from 'components/LogEntries'
import createShallowWithTheme from 'testHelpers/createShallow'
import createMountWithTheme from 'testHelpers/createMount'

describe('<LogEntries />', () => {
  it('renders correctly with logs', () => {
    const tree = createShallowWithTheme(
      <LogEntries
        logs={[
          { turnCount: 0, message: 'hello' },
          { turnCount: 1, message: 'bye' }
        ]}
      />,
      'dark'
    )
    expect(tree).toMatchSnapshot()
  })

  it('renders correctly without logs', () => {
    const tree = createShallowWithTheme(<LogEntries logs={[]} />, 'dark')
    expect(tree).toMatchSnapshot()
  })

  it('calls `scrollIntoView` only when shouldActivateSnapToBottom is true', () => {
    const scrollIntoViewMock = jest.fn()
    HTMLElement.prototype.scrollIntoView = scrollIntoViewMock
    const tree = createMountWithTheme(<LogEntries logs={[]} />, 'dark')
    expect(scrollIntoViewMock).not.toBeCalled()
    tree.setProps({ logs: [], shouldActivateSnapToBottom: true })
    expect(scrollIntoViewMock.mock).toMatchSnapshot()
  })
})

describe('<LogData />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<LogData>This is my log</LogData>, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<LogEntry />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<LogEntry>This is my log row</LogEntry>, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<LogTurn />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<LogTurn>My turn number goes here</LogTurn>, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<BottomSnapper />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<BottomSnapper />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})

describe('<StyledTable />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(
      <StyledTable>This is the table containing the logs</StyledTable>,
      'dark'
    )
    expect(tree).toMatchSnapshot()
  })
})
