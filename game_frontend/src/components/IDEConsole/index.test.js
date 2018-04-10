/* eslint-env jest */
import React from 'react'
import IDEConsole from 'components/IDEConsole'
import renderer from 'react-test-renderer'

describe('<IDEConsole />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<IDEConsole></IDEConsole>).toJSON()
    expect(tree).toMatchSnapshot()
  })
})
