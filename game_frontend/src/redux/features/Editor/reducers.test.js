/* eslint-env jest */
import editorReducer from './reducers'
import actions from './actions'
import { actions as gameActions } from 'features/Game'
import { avatarWorkerActions } from 'features/AvatarWorker'
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
        codeOnServer: 'class Avatar'
      },
      runCodeButton: {}
    }
    const action = actions.getCodeReceived('class Avatar')
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

    const action = avatarWorkerActions.avatarCodeUpdated()
    expect(editorReducer({}, action)).toEqual(expectedState)
  })

  it('should set the button status to normal when the next game-state comes in', () => {
    const expectedState = {
      code: {},
      runCodeButton: {
        status: RunCodeButtonStatus.normal
      }
    }

    const action = gameActions.socketGameStateReceived({})
    expect(editorReducer({}, action)).toEqual(expectedState)
  })
})

describe('resetCodeReducer', () => {
  it('should reset the code the the initial code', () => {
    const starterCode = `def next_turn(world_state, avatar_state):
    return MoveAction(direction.NORTH)
`
    const initialState = {
      code: {
        starterCode: starterCode
      },
      runCodeButton: {}
    }
    const expectedState = {
      code: {
        starterCode: starterCode,
        resetCodeTo: starterCode
      },
      runCodeButton: {}
    }
    const action = actions.resetCode()
    expect(editorReducer(initialState, action)).toEqual(expectedState)
  })
})
