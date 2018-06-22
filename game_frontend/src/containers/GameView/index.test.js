/* eslint-env jest */
import React from 'react'
import { GameView, GameViewLayout } from 'containers/GameView'
import { shallow } from 'enzyme/build/index'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const props = {
      gameURL: 'test',
      gamePath: '/test',
      gamePort: 8000,
      gameSSL: false,
      getConnectionParameters: jest.fn(),
      setGameURL: jest.fn(),
      setGamePath: jest.fn(),
      setGamePort: jest.fn(),
      setGameSSL: jest.fn(),
      establishGameConnection: jest.fn()
    }

    const component = shallow(<GameView {...props} />)
    expect(component).toMatchSnapshot()
  })

  it('serialisedSSLFlag function returns correctly', () => {
    const props = {
      getConnectionParameters: jest.fn(),
      gameSSL: false
    }

    const flagReturned = shallow(<GameView {...props} />).instance().serialisedSSLFlag()
    expect(flagReturned).toBe('False')
  })

  it('sendAllConnect function calls all action dispatchers', () => {
    const setGameURL = jest.fn()
    const setGamePath = jest.fn()
    const setGamePort = jest.fn()
    const setGameSSL = jest.fn()
    const establishGameConnection = jest.fn()

    const props = {
      gameURL: 'test',
      gamePath: '/test',
      gamePort: 8000,
      gameSSL: false,
      getConnectionParameters: jest.fn(),
      setGameURL,
      setGamePath,
      setGamePort,
      setGameSSL,
      establishGameConnection
    }

    const wrapper = shallow(<GameView {...props} />)

    wrapper.instance().sendAllConnect()

    expect(setGameURL.mock.calls.length).toBe(1)
    expect(setGamePath.mock.calls.length).toBe(1)
    expect(setGamePort.mock.calls.length).toBe(1)
    expect(setGameSSL.mock.calls.length).toBe(1)
    expect(establishGameConnection.mock.calls.length).toBe(1)
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})
