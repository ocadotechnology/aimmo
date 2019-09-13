import types from './types'

const socketConnectToGameRequest = () => (
  {
    type: types.SOCKET_CONNECT_TO_GAME_REQUEST
  }
)

const sendGameStateSuccess = () => (
  {
    type: types.SEND_GAME_STATE_SUCCESS
  }
)

const sendGameStateFail = error => (
  {
    type: types.SEND_GAME_STATE_FAIL,
    payload: {
      error
    }
  }
)

const socketGameStateReceived = gameState => (
  {
    type: types.SOCKET_GAME_STATE_RECEIVED,
    payload: {
      gameState
    }
  }
)

const connectionParametersReceived = parameters => (
  {
    type: types.CONNECTION_PARAMETERS_RECEIVED,
    payload: {
      parameters
    }
  }
)

const socketFeedbackAvatarUpdatedSuccess = () => (
  {
    type: types.SOCKET_FEEDBACK_AVATAR_UPDATED_SUCCESS
  }
)

const socketFeedbackAvatarUpdatedTimeout = () => (
  {
    type: types.SOCKET_FEEDBACK_AVATAR_UPDATED_TIMEOUT
  }
)

const snackbarShown = () => (
  {
    type: types.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN
  }
)

const setTimeout = () => ({
  type: types.SET_TIMEOUT
})

const socketAvatarReadyReceived = () => ({
  type: types.SOCKET_AVATAR_READY_RECEIVED
})

export default {
  socketConnectToGameRequest,
  sendGameStateFail,
  sendGameStateSuccess,
  socketGameStateReceived,
  connectionParametersReceived,
  socketFeedbackAvatarUpdatedSuccess,
  socketFeedbackAvatarUpdatedTimeout,
  snackbarShown,
  setTimeout,
  socketAvatarReadyReceived
}
