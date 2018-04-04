/* eslint-env jest */
import React from 'react'
import Game from 'components/Game'
import renderer from 'react-test-renderer'

describe('<Game />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<Game />).toJSON()
    expect(tree).toMatchSnapshot()
  })
})
