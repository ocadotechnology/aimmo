/* eslint-env jest */
import React from 'react'
import GameView, { GameViewLayout, Compass } from 'components/GameView'
import { shallow } from 'enzyme/build/index'
import createMountWithTheme from 'testHelpers/createMount'
import createShallowWithTheme from 'testHelpers/createShallow'
import { MockEnvironment } from 'testHelpers/mockEnvironment'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const connectToGame = jest.fn()
    const props = {
      connectToGame,
      gameDataLoaded: true
    }
    const component = shallow(<GameView {...props} />, { disableLifecycleMethods: true })
    expect(component).toMatchSnapshot()
  })

  it('creates a babylon environment on mount', () => {
    const props = {
      connectToGame: jest.fn(),
      EnvironmentClass: MockEnvironment
    }
    const component = createMountWithTheme(<GameView {...props} />).instance()

    expect(component.environment).toBeDefined()
    expect(component.sceneRenderer).toBeDefined()
    expect(component.environmentManager).toBeDefined()
    expect(component.entities).toBeDefined()
  })

  it('Updates the CurrentAvatarID', () => {
    const props = {
      connectToGame: jest.fn(),
      EnvironmentClass: MockEnvironment
    }
    const component = createMountWithTheme(<GameView {...props} />)
    var componentInstance = component.instance()
    componentInstance.updateCurrentAvatarID = jest.fn()

    const newProps = {
      ...props,
      currentAvatarID: 1
    }
    component.setProps(newProps)

    expect(componentInstance.updateCurrentAvatarID).toBeCalled()
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
