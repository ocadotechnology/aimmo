/* eslint-env jest */
import React from 'react'
import GameView, { GameViewLayout } from 'components/GameView'
import { shallow } from 'enzyme/build/index'

jest.mock('api/unity')

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameDataLoaded: true
    }
    const component = shallow(<GameView {...props} />)
    expect(component).toMatchSnapshot()
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})
