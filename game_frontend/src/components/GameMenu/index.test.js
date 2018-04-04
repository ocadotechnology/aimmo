/* eslint-env jest */
import React from 'react'
import GameMenu from 'components/GameMenu'
import renderer from 'react-test-renderer'

describe('<GameMenu />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<GameMenu />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})
