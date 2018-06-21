/* eslint-env jest */
import actions from './actions'
import gameReducer from './reducers'

describe('gameReducer', () => {
  it('should return the initial state', () => {
    expect(gameReducer(undefined, {})).toEqual({})
  })

  it('should handle GET_CONNECTION_PARAMETERS_SUCCESS', () => {
    const expectedState = {
      connectionParameters: {
        id: 1
      },
      initialState: 'someValue'
    }
    const action = actions.getConnectionParametersSuccess({ id: 1 })
    expect(gameReducer({initialState: 'someValue'}, action)).toEqual(expectedState)
  })
})
