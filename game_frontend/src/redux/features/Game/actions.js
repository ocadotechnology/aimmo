import types from './types'

const socketConnectToGameRequest = () => (
  {
    type: types.SOCKET_CONNECT_TO_GAME_REQUEST
  }
)

const sendGameUpdateSuccess = () => (
  {
    type: types.SEND_GAME_UPDATE_SUCCESS
  }
)

const sendGameUpdateFail = error => (
  {
    type: types.SEND_GAME_UPDATE_FAIL
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

export default {
  socketConnectToGameRequest,
  sendGameUpdateFail,
  sendGameUpdateSuccess,
  socketGameStateReceived,
  unityEvent
}
