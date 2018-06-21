/* eslint-env jest */
import React from 'react'
import GamePage, { GamePageLayout } from 'components/GamePage'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<GamePage />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<GamePage />)

    expect(tree).toMatchSnapshot()
  })
})

describe('<GamePageLayout />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<GamePageLayout />)

    expect(tree).toMatchSnapshot()
  })
})
