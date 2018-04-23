/* eslint-env jest */
import React from 'react'
import { shallow } from 'enzyme'
// import toJson from 'enzyme-to-json'
import { GamePage } from 'containers/GamePage'

describe('<GamePage />', () => {
  it('matches snapshot', () => {
    const props = {
      code: 'class Avatar',
      getCode: jest.fn()
    }

    const component = shallow(<GamePage {...props} />)

    expect(component).toMatchSnapshot()
  })
})
