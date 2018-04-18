import types from './types'

const getCodeRequest = () => (
  {
    type: types.GET_CODE_REQUEST
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
