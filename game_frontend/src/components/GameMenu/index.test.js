/* eslint-env jest */
import React from 'react'
import GameMenu from 'components/GameMenu'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<GameMenu />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<GameMenu />)
    expect(tree).toMatchSnapshot()
  })
})
