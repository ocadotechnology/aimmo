/* eslint-env jest */
import React from 'react'
import IDEConsole from 'components/IDEConsole'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEConsole />', () => {
  it('renders correctly with logs', () => {
    const tree = createShallowWithTheme(<IDEConsole logs='test logs' />)
    expect(tree).toMatchSnapshot()
  })
  
  it('renders correctly without logs', () => {
    const tree = createShallowWithTheme(<IDEConsole />)
    expect(tree).toMatchSnapshot()
  })
})
