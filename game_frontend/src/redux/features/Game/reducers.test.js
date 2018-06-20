/* eslint-env jest */
import actions from './actions'
import gameReducer from './reducers'

describe('gameReducer', () => {
  it('should return the initial state', () => {
    expect(gameReducer(undefined, {})).toEqual({})
  })

  it('should handle GET_CONNECTION_PARAMS_SUCCESS', () => {
    const expectedState = {
      connectionParams: {
        id: 1
      },
      initialState: 'someValue'
    }
    const action = actions.getConnectionParamsSuccess({ id: 1 })
    expect(gameReducer({initialState: 'someValue'}, action)).toEqual(expectedState)
  })
})
