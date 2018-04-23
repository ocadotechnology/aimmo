/* eslint-env jest */
import React from 'react'
import GameView from 'components/GameView'
import renderer from 'react-test-renderer'

describe('<GameView />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<GameView />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})
