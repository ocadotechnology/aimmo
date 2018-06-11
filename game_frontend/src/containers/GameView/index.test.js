/* eslint-env jest */
import React from 'react'
import { GameView } from 'containers/GameView'
import { shallow } from 'enzyme/build/index'

describe('<GameView />', () => {
  it('matches snapshot', () => {

    const props = {
      gameURL: 'test',
      gamePath: '/test',
      gamePort: 8000,
      gameSSL: false,
      getConnectionParams: jest.fn(),
      setGameURL: jest.fn(),
      setGamePath: jest.fn(),
      setGamePort: jest.fn(),
      setGameSSL: jest.fn(),
      establishGameConnection: jest.fn()
    }

    const component = shallow(<GameView {...props} />)
    expect(component).toMatchSnapshot()
  })
})
