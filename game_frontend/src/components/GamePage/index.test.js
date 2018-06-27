/* eslint-env jest */
import React from 'react'
import GamePage, { GamePageLayout } from 'components/GamePage'
import createShallowWithTheme from 'testHelpers/createShallow'
import { shallow } from 'enzyme'

describe('<GamePage />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GamePage />)

    expect(tree).toMatchSnapshot()
  })
})

describe('<GamePageLayout />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<GamePageLayout />)

    expect(tree).toMatchSnapshot()
  })
})
