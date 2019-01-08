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

const unityEvent = (unityEvent, unityData, successAction, failAction) => (
  {
    type: types.UNITY_EVENT,
    payload: {
      unityEvent,
      unityData,
      successAction,
      failAction
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

const unitySendAvatarIDSuccess = () => (
  {
    type: types.UNITY_SEND_AVATAR_ID_SUCCESS
  }
)

const unitySendAvatarIDFail = () => (
  {
    type: types.UNITY_SEND_AVATAR_ID_FAIL
  }
)

const socketFeedbackAvatarUpdated = () => (
  {
    type: types.SOCKET_FEEDBACK_AVATAR_UPDATED
  }
)

const snackbarShown = () => (
  {
    type: types.SNACKBAR_FOR_AVATAR_FEEDBACK_SHOWN
  }
)

const gameDataLoaded = () => (
  {
    type: types.GAME_DATA_LOADED
  }
)

const setTimeout = () => ({
  type: types.SET_TIMEOUT
})

export default {
  socketConnectToGameRequest,
  sendGameStateFail,
  sendGameStateSuccess,
  socketGameStateReceived,
  unityEvent,
  connectionParametersReceived,
  unitySendAvatarIDSuccess,
  unitySendAvatarIDFail,
  socketFeedbackAvatarUpdated,
  snackbarShown,
  gameDataLoaded,
  setTimeout
}
