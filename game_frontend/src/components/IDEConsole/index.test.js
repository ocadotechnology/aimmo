/* eslint-env jest */
import React from 'react'
import IDEConsole, { StyledConsole } from 'components/IDEConsole'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEConsole logs={[{ timestamp: '1', log: 'hello' }, { timestamp: '2', log: 'bye' }]} />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<StyledConsole />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<StyledConsole />)
    expect(tree).toMatchSnapshot()
  })
})
