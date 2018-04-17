/* eslint-env jest */
import reducers from './reducers'
import actions from './actions'

describe('editorReducer', () => {
  it('should return the initial state', () => {
    expect(reducers.editorReducer(undefined, {})).toEqual({})
  })

  it('should handle GET_CODE_SUCCESS', () => {
    const expectedState = {
      code: 'class Avatar'
    }
    const action = actions.getCodeReceived('class Avatar')
    expect(reducers.editorReducer({}, action)).toEqual(expectedState)
  })
})
