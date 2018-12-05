/* eslint-env jest */
import React from 'react'
import GameView, { GameViewLayout } from 'components/GameView'
import { shallow } from 'enzyme/build/index'

describe('<GameView />', () => {
  it('shows loading bar whilst unity is loading', () => {
    const component = shallow(<GameView />)
    expect(component).toMatchSnapshot()
  })

  it('does not show the loading bar when unity has loaded', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame
    }
    const component = shallow(<GameView {...props} />)
    component.instance().unityContentLoaded()
    expect(component).toMatchSnapshot()
  })

  it('connects to the game only after unity has been loaded', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame
    }
    const component = shallow(<GameView {...props} />)
    expect(connectToGame).not.toBeCalled()
    component.instance().unityContentLoaded()
    expect(connectToGame).toBeCalled()
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})
