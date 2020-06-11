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

const postCodeRequest = code => ({
  type: types.POST_CODE_REQUEST,
  payload: {
    code
  }
})

const postCodeReceived = () => ({
  type: types.POST_CODE_SUCCESS
})

const avatarCodeUpdated = () => ({
  type: types.AVATAR_CODE_UPDATED
})

const resetCode = () => ({
  type: types.RESET_CODE
})

export default {
  getCodeRequest,
  getCodeReceived,
  postCodeRequest,
  postCodeReceived,
  avatarCodeUpdated,
  resetCode
}
