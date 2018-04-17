import types from './types'

const getCodeRequest = gameID => (
  {
    type: types.GET_CODE_REQUEST,
    payload: {
      gameID
    }
  }
)

const getCodeReceived = code => (
  {
    type: types.GET_CODE_SUCCESS,
    payload: {
      code
    }
  }
)

export default {
  getCodeRequest,
  getCodeReceived
}
