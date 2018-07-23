import types from './types'

const getConnectionParametersRequest = gameID => (
  {
    type: types.GET_CONNECTION_PARAMETERS_REQUEST,
    payload: {
      gameID
    }
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
  getConnectionParametersRequest,
  sendGameUpdateFail,
  sendGameUpdateSuccess,
  socketGameStateReceived,
  unityEvent
}
