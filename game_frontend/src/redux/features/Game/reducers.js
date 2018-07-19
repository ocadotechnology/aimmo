import types from './types'

const gameReducer = (state = {}, action) => {
  switch (action.type) {
    case types.GET_CONNECTION_PARAMETERS_SUCCESS:
      return {
        ...state,
        connectionParameters: action.payload.connectionParameters
      }
    case types.GAME_STATE_EVENT_RECEIVED:
      return {
        ...state,
        gameState: action.payload.gameState
      }
    default:
      return state
  }
}

export default gameReducer
