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

const setGamePath = gamePath => (
  {
    type: types.SET_GAME_PATH,
    payload: {
      gamePath
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

const setGameSSL = gameSSLFlag => (
  {
    type: types.SET_GAME_SSL,
    payload: {
      gameSSLFlag
    }
  }
)

const establishGameConnection = () => (
  {
    type: types.ESTABLISH_GAME_CONNECTION
  }
)

export default {
  getConnectionParamsRequest,
  getConnectionParamsSuccess,
  setGameURL,
  setGamePath,
  setGamePort,
  setGameSSL,
  establishGameConnection
}
