/* eslint-env jest */
import React from 'react'
import { GameView, GameViewLayout } from 'containers/GameView'
import { shallow } from 'enzyme/build/index'

describe('<GameView />', () => {
  it('matches snapshot', () => {
    const props = {
      getConnectionParameters: jest.fn(),
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
    const establishGameConnection = jest.fn()

    const props = {
      getConnectionParameters: jest.fn(),
      establishGameConnection
    }

    const wrapper = shallow(<GameView {...props} />)

    wrapper.instance().sendAllConnect()

    expect(establishGameConnection.mock.calls.length).toBe(1)
  })
})

describe('<GameViewLayout />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<GameViewLayout />)
    expect(tree).toMatchSnapshot()
  })
})
