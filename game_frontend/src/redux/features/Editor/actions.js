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

const postCodeRequest = () => (
  {
    type: types.POST_CODE_REQUEST
  }
)

const postCodeReceived = () => (
  {
    type: types.POST_CODE_SUCCESS
  }
)

export default {
  getCodeRequest,
  getCodeReceived,
  postCodeRequest,
  postCodeReceived
}
