/* eslint-env jest */
import React from 'react'
import { IDEConsole, StyledConsole } from 'containers/IDEConsole'
import LogEntries from 'components/LogEntries'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const logs = new Map([
      [0, 'hello'],
      [1, 'bye']
    ])
    const tree = createShallowWithTheme(<IDEConsole logs={logs} />, 'dark')
    expect(tree).toMatchSnapshot()
  })

  it('sends activates snap to bottom on the LogEntries if the console log is overflown', () => {
    const tree = createShallowWithTheme(<IDEConsole logs={new Map()} />, 'dark')
    tree.instance().consoleRef = true
    expect(tree.state('activatedScrollToBottom')).toBeFalsy()
    expect(tree.state('shouldActivateSnapToBottom')).toBeFalsy()
    expect(tree.find(LogEntries).props.shoudActivateSnapToBottom).toBeFalsy()
    const setStateSpy = jest.spyOn(tree.instance(), 'setState')
    tree.instance().isOverflown = jest.fn(() => true)
    tree.setProps({ logs: new Map() })
    expect(setStateSpy.mock.calls).toMatchInlineSnapshot(`
      Array [
        Array [
          Object {
            "activatedScrollToBottom": true,
            "shouldActivateSnapToBottom": true,
          },
        ],
        Array [
          Object {
            "activatedScrollToBottom": true,
            "shouldActivateSnapToBottom": false,
          },
        ],
      ]
    `)
    expect(setStateSpy).toHaveBeenCalledTimes(2)
  })
})

describe('<StyledConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<StyledConsole />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})
