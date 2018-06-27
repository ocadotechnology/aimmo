import types from './types'

const getConnectionParametersRequest = gameID => (
  {
    type: types.GET_CONNECTION_PARAMETERS_REQUEST,
    payload: {
      gameID
    }
  }
)

const getConnectionParametersSuccess = connectionParameters => (
  {
    type: types.GET_CONNECTION_PARAMETERS_SUCCESS,
    payload: {
      connectionParameters
    }
  }
)

const setGameURL = gameURL => (
  {
    type: types.SET_GAME_URL,
    payload: {
      gameURL
    }
  }
)

const setGameURLSuccess = () => (
  {
    type: types.SET_GAME_URL_SUCCESS
  }
)

const setGameURLFail = error => (
  {
    type: types.SET_GAME_URL_FAIL,
    payload: {
      error
    }
  }
)

const setGamePath = gamePath => (
  {
    type: types.SET_GAME_PATH,
    payload: {
      gamePath
    }
  }
)

const setGamePathSuccess = () => (
  {
    type: types.SET_GAME_PATH_SUCCESS
  }
)

const setGamePathFail = error => (
  {
    type: types.SET_GAME_PATH_FAIL,
    payload: {
      error
    }
  }
)

const setGamePort = gamePort => (
  {
    type: types.SET_GAME_PORT,
    payload: {
      gamePort
    }
  }
)

const setGamePortSuccess = () => (
  {
    type: types.SET_GAME_PORT_SUCCESS
  }
)

const setGamePortFail = error => (
  {
    type: types.SET_GAME_PORT_FAIL,
    payload: {
      error
    }
  }
)

const setGameSSL = gameSSLFlag => (
  {
    type: types.SET_GAME_SSL,
    payload: {
      gameSSLFlag
    }
  }
)

const setGameSSLSuccess = () => (
  {
    type: types.SET_GAME_SSL_SUCCESS
  }
)

const setGameSSLFail = error => (
  {
    type: types.SET_GAME_SSL_FAIL,
    payload: {
      error
    }
  }
)

const establishGameConnection = () => (
  {
    type: types.ESTABLISH_GAME_CONNECTION
  }
)

const establishGameConnectionSuccess = () => (
  {
    type: types.ESTABLISH_GAME_CONNECTION_SUCCESS
  }
)

const establishGameConnectionFail = error => (
  {
    type: types.ESTABLISH_GAME_CONNECTION_FAIL,
    payload: {
      error
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
  getConnectionParametersSuccess,
  setGameURL,
  setGameURLSuccess,
  setGameURLFail,
  setGamePath,
  setGamePathSuccess,
  setGamePathFail,
  setGamePort,
  setGamePortSuccess,
  setGamePortFail,
  setGameSSL,
  setGameSSLSuccess,
  setGameSSLFail,
  establishGameConnection,
  establishGameConnectionSuccess,
  establishGameConnectionFail,
  unityEvent
}
