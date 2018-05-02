/* eslint-env jest */
import React from 'react'
import { shallow } from 'enzyme'
import GamePage from 'components/GamePage'

describe('<GamePage />', () => {
  it('matches snapshot', () => {
    const component = shallow(<GamePage />)

    expect(component).toMatchSnapshot()
  })
})
