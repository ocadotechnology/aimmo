/* eslint-env jest */
import editorReducer from './reducers'
import actions from './actions'
import { actions as gameActions } from 'features/Game'
import { RunCodeButtonStatus } from 'components/RunCodeButton'

describe('editorReducer', () => {
  it('should return the initial state', () => {
    const initialState = {
      code: {},
      runCodeButton: {}
    }
    expect(editorReducer(undefined, {})).toEqual(initialState)
  })

  it('should handle GET_CODE_SUCCESS', () => {
    const expectedState = {
      code: {
        code: 'class Avatar',
        codeOnServer: 'class Avatar'
      },
      runCodeButton: {}
    }
    const action = actions.getCodeReceived('class Avatar')
    expect(editorReducer({}, action)).toEqual(expectedState)
  })

  it('should handle CHANGE_CODE', () => {
    const expectedState = {
      code: {
        code: 'class Avatar'
      },
      runCodeButton: {}
    }
    const action = actions.changeCode('class Avatar')
    expect(editorReducer({}, action)).toEqual(expectedState)
  })
})

describe('runCodeButtonReducer', () => {
  it('should set the button status to updating when the code is sent to the server', () => {
    const expectedState = {
      code: {},
      runCodeButton: {
        status: RunCodeButtonStatus.updating
      }
    }

    const action = actions.postCodeRequest()
    expect(editorReducer({}, action)).toEqual(expectedState)
  })

  it('should set the button status to done when the avatar is updated', () => {
    const expectedState = {
      code: {},
      runCodeButton: {
        status: RunCodeButtonStatus.done
      }
    }

    const action = gameActions.socketFeedbackAvatarUpdated()
    expect(editorReducer({}, action)).toEqual(expectedState)
  })

  it('should set the button status to normal when the snackbar has been shown', () => {
    const expectedState = {
      code: {},
      runCodeButton: {
        status: RunCodeButtonStatus.normal
      }
    }

    const action = gameActions.snackbarShown()
    expect(editorReducer({}, action)).toEqual(expectedState)
  })
})
