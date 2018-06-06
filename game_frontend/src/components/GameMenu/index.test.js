/* eslint-env jest */
import React from 'react'
import GameMenu from 'components/GameMenu'
import renderer from 'react-test-renderer'
import withTheme from '../../testHelpers/withTheme'

describe('<GameMenu />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(withTheme(<GameMenu />)).toJSON()
    expect(tree).toMatchSnapshot()
  })
})
