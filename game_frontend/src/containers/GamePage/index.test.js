/* eslint-env jest */
import ConnectedGamePage, { GamePage } from 'containers/GamePage'
import configureStore from 'redux-mock-store'
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

    const store = configureStore([])(testState)
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

  it('should call fetchMovies when I click on the button', () => {
    const fetchMovies = jest.fn()
    const props = {
      movies: [],
      fetchMovies
    }

    const component = shallow(<GamePage {...props} />)

    component.find('#fetch-movies-button').simulate('click')
    expect(fetchMovies.mock.calls.length).toBe(1)
  })
})
