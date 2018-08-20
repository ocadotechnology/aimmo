/* eslint-env jest */
import React from 'react'
import { GameView, GameViewLayout } from 'components/GameView'
import { shallow } from 'enzyme/build/index'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const component = shallow(<GameView />)
    expect(component).toMatchSnapshot()
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})
