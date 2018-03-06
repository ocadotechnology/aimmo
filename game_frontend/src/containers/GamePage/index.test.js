/* eslint-env jest */
// import { shallowWithStore } from 'enzyme'
// import { createMockStore } from 'redux-te'
import ConnectedGamePage, { GamePage } from 'containers/GamePage'
import { createMockStore } from 'redux-test-utils'
import { shallow } from 'enzyme'
import shallowWithStore from 'containers/testHelpers/shallowWithStore'
import React from 'react'

describe('<GamePage />', () => {
  it('should render successfully with a mock store', () => {
    const testState = {
      movieReducer: {
        movies: []
      }
    }

    const store = createMockStore(testState)
    const component = shallowWithStore(<ConnectedGamePage />, store)

    expect(component.dive()).toBeDefined()
  })

  it('should render successfully with no movies', () => {
    const props = {
      movies: []
    }

    const component = shallow(<GamePage {...props} />)

    expect(component).toMatchSnapshot()
  })
})
