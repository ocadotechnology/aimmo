/* eslint-env jest */
import React from 'react'
import { GameMenu, GameMenuLayout, ExitButton } from 'components/GameMenu'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<GameMenu />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<GameMenu />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<ExitButton />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<ExitButton />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<GameMenuLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<GameMenuLayout />)
    expect(tree).toMatchSnapshot()
  })
})
