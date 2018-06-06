/* eslint-env jest */
import React from 'react'
import IDEConsole from 'components/IDEConsole'
import renderer from 'react-test-renderer'
import withTheme from '../../testHelpers/withTheme'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(withTheme(<IDEConsole />)).toJSON()
    expect(tree).toMatchSnapshot()
  })
})
