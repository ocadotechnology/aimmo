/* eslint-env jest */
import React from 'react'
import GameView, { GameViewLayout, Compass, LoadingBackgroundOverlay } from 'components/GameView'
import { shallow } from 'enzyme/build/index'
import createMountWithTheme from 'testHelpers/createMount'
import createShallowWithTheme from 'testHelpers/createShallow'
import { MockEnvironment } from 'testHelpers/mockEnvironment'

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
      environment: new MockEnvironment(true)
    }
    const component = createMountWithTheme(<GameView {...props} />).instance()

    expect(component.gameEngine.environment).toBeDefined()
    expect(component.gameEngine.sceneRenderer).toBeDefined()
    expect(component.gameEngine.environmentManager).toBeDefined()
    expect(component.gameEngine.entities).toBeDefined()
  })

  it('updates the game Engine', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      currentAvatarID: 2
    }
    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()
    componentInstance.gameEngine.onUpdate = jest.fn()

    const newProps = {
      ...props,
      currentAvatarID: 1,
      gameState: {
        id: 1
      }
    }
    component.setProps(newProps)

    expect(componentInstance.gameEngine.onUpdate).toBeCalled()
  })

  it('centers camera on cameraCenteredOnUserAvatar', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true)
    }
    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()
    componentInstance.gameEngine.centerOn = jest.fn()
    componentInstance.gameEngine.entities.avatars.currentAvatarMesh = true

    const newProps = {
      ...props,
      cameraCenteredOnUserAvatar: true,
      gameLoaded: true
    }
    component.setProps(newProps)

    expect(componentInstance.gameEngine.centerOn).toBeCalled()
  })

  it('detects panning event from gameEngine and calls its mapping function', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      mapPanned: jest.fn()
    }
    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()

    componentInstance.gameEngine.panHandler()

    expect(componentInstance.props.mapPanned).toBeCalled()
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
