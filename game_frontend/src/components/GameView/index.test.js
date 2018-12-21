/* eslint-env jest */
import React from 'react'
import GameView, { GameViewLayout, StyledUnity, LoadingBackgroundOverlay, StyledCircularProgress } from 'components/GameView'
import { shallow } from 'enzyme/build/index'
jest.mock('api/unity')

describe('<GameView />', () => {
  it('shows loading bar whilst game is loading', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameDataLoaded: false
    }
    const component = shallow(<GameView {...props} />)
    expect(component).toMatchSnapshot()
  })

  it('does not show the loading bar when the game has loaded', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameDataLoaded: true
    }
    const component = shallow(<GameView {...props} />)
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

describe('<StyledUnity />', () => {
  it('is not shown when game data is loading', () => {
    const component = shallow(<StyledUnity />)
    expect(component).toMatchSnapshot()
  })

  it('is shown when game data has loaded', () => {
    const component = shallow(<StyledUnity gameDataLoaded />)
    expect(component).toMatchSnapshot()
  })
})

describe('<StyledCircularProgress />', () => {
  it('matches snapshot', () => {
    const component = shallow(<StyledCircularProgress />)
    expect(component).toMatchSnapshot()
  })
})

describe('<LoadingBackgroundOverlay />', () => {
  it('matches snapshot', () => {
    const component = shallow(<LoadingBackgroundOverlay />)
    expect(component).toMatchSnapshot()
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})
