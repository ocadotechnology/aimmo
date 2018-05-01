/* eslint-env jest */
import editorReducer from './reducers'
import actions from './actions'

describe('editorReducer', () => {
  it('should return the initial state', () => {
    expect(editorReducer(undefined, {})).toEqual({})
  })

  it('should handle GET_CODE_SUCCESS', () => {
    const expectedState = {
      code: 'class Avatar'
    }
    const action = actions.getCodeReceived('class Avatar')
    expect(editorReducer({}, action)).toEqual(expectedState)
  })

  it('should handle CHANGE_CODE', () => {
    const expectedState = {
      code: 'class Avatar'
    }
    const action = actions.changeCode('class Avatar')
    expect(editorReducer({}, action)).toEqual(expectedState)
  })
})
