/* eslint-env jest */
import movieReducer from './reducers'
import actions from './actions'

describe('movieReducer', () => {
  it('should return the initial state', () => {
    expect(movieReducer(undefined, {})).toEqual({})
  })

  it('should handle RECEIVE_MOVIES', () => {
    const movies = [
      {
        'title': 'Revenge of the Killer Dees',
        'Director': 'Robert Dee Niro'
      },
      {
        'title': 'Dee-stroyer',
        'Director': 'Alfred HitchCode',
        'Starring': 'Leonardo Dee-Caprio'
      },
      {
        'title': 'A Dee Life',
        'Director': 'Woo-Dee Allen'
      }
    ]
    const action = actions.receiveMovies(movies)
    expect(movieReducer({}, action)).toEqual({
      movies
    })
  })
})
