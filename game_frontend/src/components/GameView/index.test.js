/* eslint-env jest */
import React from 'react'
import GameView, {
  GameViewLayout,
  Compass,
  LoadingBackgroundOverlay,
  PositionedFindMeButton,
  OverlayElements,
  LoadingText,
} from 'components/GameView'
import { shallow } from 'enzyme/build/index'
import createMountWithTheme from 'testHelpers/createMount'
import createShallowWithTheme from 'testHelpers/createShallow'
import { MockEnvironment } from 'testHelpers/mockEnvironment'
import EntityManager from '../../babylon/entities'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameLoaded: true,
    }
    const component = shallow(<GameView {...props} />, { disableLifecycleMethods: true })
    expect(component).toMatchSnapshot()
  })

  it('creates a babylon environment when game is loaded', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      gameLoaded: true,
    }
    const component = createMountWithTheme(<GameView {...props} />).instance()

    expect(component.gameEngine.environment).toBeDefined()
  })

  it('updates the game Engine', () => {
    const props = {
      connectToGame: jest.fn(),
      gameLoaded: true,
      environment: new MockEnvironment(true),
      currentAvatarID: 2,
    }
    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()
    componentInstance.gameEngine.onUpdate = jest.fn()

    const newProps = {
      ...props,
      currentAvatarID: 1,
      gameState: {
        id: 1,
      },
    }
    component.setProps(newProps)

    expect(componentInstance.gameEngine.onUpdate).toBeCalled()
  })

  it('populates the map on first update', () => {
    const props = {
      connectToGame: jest.fn(),
      gameLoaded: true,
      environment: new MockEnvironment(true),
    }

    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()

    componentInstance.gameEngine.onUpdateGameState = jest.fn()
    componentInstance.gameEngine.setCurrentAvatarID = jest.fn()
    componentInstance.gameEngine.centerOn = jest.fn()

    const newProps = {
      ...props,
      currentAvatarID: 1,
      gameState: {
        era: 'future',
        id: 1,
      },
    }

    component.setProps(newProps)

    expect(componentInstance.gameEngine.sceneRenderer).toBeDefined()
    expect(componentInstance.gameEngine.environmentManager).toBeDefined()
    expect(componentInstance.gameEngine.entities).toBeDefined()
  })

  it('does not populate the map if the environment era is set', () => {
    const props = {
      connectToGame: jest.fn(),
      gameLoaded: true,
      environment: new MockEnvironment(true, 'future'),
    }

    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()

    componentInstance.gameEngine.populateMap = jest.fn()
    componentInstance.gameEngine.onUpdateGameState = jest.fn()
    componentInstance.gameEngine.setCurrentAvatarID = jest.fn()
    componentInstance.gameEngine.centerOn = jest.fn()

    const newProps = {
      ...props,
      currentAvatarID: 1,
      gameState: {
        era: 'future',
        id: 1,
      },
    }

    component.setProps(newProps)

    expect(componentInstance.gameEngine.populateMap).toBeCalledTimes(0)
  })

  it('centers camera on cameraCenteredOnUserAvatar', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      gameLoaded: true,
    }
    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()

    componentInstance.gameEngine.centerOn = jest.fn()
    componentInstance.gameEngine.onUpdateGameState = jest.fn()
    componentInstance.gameEngine.setCurrentAvatarID = jest.fn()

    componentInstance.gameEngine.entities = new EntityManager(
      componentInstance.gameEngine.environment
    )
    componentInstance.gameEngine.entities.avatars.currentAvatarMesh = true

    const newProps = {
      ...props,
      cameraCenteredOnUserAvatar: true,
      gameState: {
        id: 1,
      },
      gameLoaded: true,
    }
    component.setProps(newProps)

    expect(componentInstance.gameEngine.centerOn).toBeCalled()
  })

  it('detects panning event from gameEngine and calls its mapping function', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      mapPanned: jest.fn(),
      gameLoaded: true,
    }
    const component = createMountWithTheme(<GameView {...props} />)
    const componentInstance = component.instance()

    componentInstance.gameEngine.panHandler()

    expect(componentInstance.props.mapPanned).toBeCalled()
  })

  it('calls FindMe function upon click when camera is not centered', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      cameraCenteredOnUserAvatar: false,
      centerCameraOnUserAvatar: jest.fn(),
      gameLoaded: true,
    }

    const component = createMountWithTheme(<GameView {...props} />)

    component.find('#find-me-button').at(1).simulate('click')
    expect(props.centerCameraOnUserAvatar).toBeCalled()
  })

  it('does not call FindMe function upon click when camera is centered', () => {
    const props = {
      connectToGame: jest.fn(),
      environment: new MockEnvironment(true),
      cameraCenteredOnUserAvatar: true,
      centerCameraOnUserAvatar: jest.fn(),
      gameLoaded: true,
    }

    const component = createMountWithTheme(<GameView {...props} />)

    component.find('#find-me-button').at(1).simulate('click')
    expect(props.centerCameraOnUserAvatar).not.toBeCalled()
  })

  it('shows the loading screen when the game is loading', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameLoaded: false,
    }
    const component = shallow(<GameView {...props} />, { disableLifecycleMethods: true })
    expect(component).toMatchSnapshot()
  })

  it('opens the Freshdesk widget when clicking on the contact us link in the loading screen', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameLoaded: false,
    }
    const component = shallow(<GameView {...props} />, { disableLifecycleMethods: true })

    window.FreshworksWidget = jest.fn()

    component.find('.freshdesk__contact-us').simulate('click')
    expect(window.FreshworksWidget).toHaveBeenCalled()
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<OverlayElements />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<OverlayElements />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<Compass />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<Compass />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<PositionedFindMeButton/>', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<PositionedFindMeButton />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<LoadingBackgroundOverlay />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<LoadingBackgroundOverlay />)
    expect(tree).toMatchSnapshot()
  })
})

describe('<LoadingText />', () => {
  it('matches snapshot', () => {
    const tree = createShallowWithTheme(<LoadingText />)
    expect(tree).toMatchSnapshot()
  })
})
