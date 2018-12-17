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

const changeCode = code => (
  {
    type: types.CHANGE_CODE,
    payload: {
      code
    }
  }
)

const keyPressed = code => (
  {
    type: types.KEY_PRESSED,
    payload: {
      code
    }
  }
)

export default {
  getCodeRequest,
  getCodeReceived,
  postCodeRequest,
  postCodeReceived,
  changeCode,
  keyPressed
}
