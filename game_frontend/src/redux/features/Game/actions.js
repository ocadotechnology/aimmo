import types from './types'

const socketConnectToGameRequest = () => ({
  type: types.SOCKET_CONNECT_TO_GAME_REQUEST,
})

const sendGameStateSuccess = () => ({
  type: types.SEND_GAME_STATE_SUCCESS,
})

const sendGameStateFail = (error) => ({
  type: types.SEND_GAME_STATE_FAIL,
  payload: {
    error,
  },
})

const socketGameStateReceived = (gameState) => ({
  type: types.SOCKET_GAME_STATE_RECEIVED,
  payload: {
    gameState,
  },
})

const connectionParametersReceived = (parameters) => ({
  type: types.CONNECTION_PARAMETERS_RECEIVED,
  payload: {
    parameters,
  },
})

const gameLoaded = () => ({
  type: types.GAME_LOADED,
})

const setTimeout = () => ({
  type: types.SET_TIMEOUT,
})

const mapPanned = () => ({
  type: types.MAP_PANNED,
})

const centerCameraOnUserAvatar = () => ({
  type: types.CENTER_CAMERA_ON_USER_AVATAR,
})

export default {
  socketConnectToGameRequest,
  sendGameStateSuccess,
  sendGameStateFail,
  socketGameStateReceived,
  connectionParametersReceived,
  gameLoaded,
  setTimeout,
  mapPanned,
  centerCameraOnUserAvatar,
}
