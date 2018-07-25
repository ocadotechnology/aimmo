/* eslint-env jest */
import React from 'react'
import { GameView, GameViewLayout } from 'containers/GameView'
import { shallow } from 'enzyme/build/index'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const props = {
      connectToGame: jest.fn()
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
