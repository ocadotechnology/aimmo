import types from './types'

const getConnectionParamsRequest = gameID => (
    {
      type: types.GET_CONNECTION_PARAMS_REQUEST,
      payload: {
        gameID
      }
    }
)

const getConnectionParamsSuccess = connectionParams => (
  {
    type: types.GET_CONNECTION_PARAMS_SUCCESS,
    payload: {
      connectionParams
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

const setGameURLFail = () => (
  {
    type: types.SET_GAME_URL_FAIL
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

const setGamePathFail = () => (
  {
    type: types.SET_GAME_PATH_FAIL
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

const setGamePortFail = () => (
  {
    type: types.SET_GAME_PORT_FAIL
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

const setGameSSLFail = () => (
  {
    type: types.SET_GAME_SSL_FAIL
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

const establishGameConnectionFail = () => (
  {
    type: types.ESTABLISH_GAME_CONNECTION_FAIL
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
  getConnectionParamsRequest,
  getConnectionParamsSuccess,
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
