/* eslint-env jest */
import React from 'react'
import GameView, { GameViewLayout, Compass, LoadingBackgroundOverlay } from 'components/GameView'
import { shallow } from 'enzyme/build/index'
import createMountWithTheme from 'testHelpers/createMount'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameLoaded: true
    }
    const component = shallow(<GameView {...props} />, { disableLifecycleMethods: true })
    expect(component).toMatchSnapshot()
  })

  it('creates a babylon environment on mount', () => {
    const props = {
      connectToGame: jest.fn(),
      mockEnvironment: true
    }
    const component = createMountWithTheme(<GameView {...props} />).instance()

    expect(component.gameEngine.environment).toBeDefined()
    expect(component.gameEngine.sceneRenderer).toBeDefined()
    expect(component.gameEngine.environmentManager).toBeDefined()
    expect(component.gameEngine.entities).toBeDefined()
  })

  it('updates the CurrentAvatarID', () => {
    const props = {
      connectToGame: jest.fn(),
      mockEnvironment: true
    }
    const component = createMountWithTheme(<GameView {...props} />)
    var componentInstance = component.instance()
    componentInstance.gameEngine.updateCurrentAvatarID = jest.fn()

    const newProps = {
      ...props,
      currentAvatarID: 1
    }
    component.setProps(newProps)

    expect(componentInstance.gameEngine.updateCurrentAvatarID).toBeCalled()
  })

  it('centers camera on cameraCentered', () => {
    const props = {
      connectToGame: jest.fn(),
      mockEnvironment: true
    }
    const component = createMountWithTheme(<GameView {...props} />)
    var componentInstance = component.instance()
    componentInstance.gameEngine.centerOn = jest.fn()

    const newProps = {
      ...props,
      cameraCentered: true
    }
    component.setProps(newProps)

    expect(componentInstance.gameEngine.centerOn).toBeCalled()
  })

  it('shows the loading screen when the game is loading', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameLoaded: false
    }
    const component = shallow(<GameView {...props} />, { disableLifecycleMethods: true })
    expect(component).toMatchSnapshot()
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<Compass />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<Compass />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<LoadingBackgroundOverlay />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<LoadingBackgroundOverlay />)
    expect(tree).toMatchSnapshot()
  })
})
