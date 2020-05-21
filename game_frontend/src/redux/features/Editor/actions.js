import types from './types'

const getCodeRequest = () => ({
  type: types.GET_CODE_REQUEST
})

const getCodeReceived = code => ({
  type: types.GET_CODE_SUCCESS,
  payload: {
    code
  }
})

const postCodeRequest = () => ({
  type: types.POST_CODE_REQUEST
})

const postCodeReceived = () => ({
  type: types.POST_CODE_SUCCESS
})

const avatarCodeUpdated = () => ({
  type: types.AVATAR_CODE_UPDATED
})

const changeCode = code => ({
  type: types.CHANGE_CODE,
  payload: {
    code
  }
})

const resetCode = () => ({
  type: types.RESET_CODE
})

const keyPressed = code => ({
  type: types.KEY_PRESSED,
  payload: {
    code
  }
})

export default {
  getCodeRequest,
  getCodeReceived,
  postCodeRequest,
  postCodeReceived,
  avatarCodeUpdated,
  changeCode,
  keyPressed,
  resetCode
}
