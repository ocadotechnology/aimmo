import types from './types'

const getCodeRequest = () => ({
  type: types.GET_CODE_REQUEST,
})

const getCodeReceived = (code, starterCode) => ({
  type: types.GET_CODE_SUCCESS,
  payload: {
    code,
    starterCode,
  },
})

const postCodeRequest = (code) => ({
  type: types.POST_CODE_REQUEST,
  payload: {
    code,
  },
})

const postCodeReceived = () => ({
  type: types.POST_CODE_SUCCESS,
})

const avatarCodeUpdated = () => ({
  type: types.AVATAR_CODE_UPDATED,
})

const resetCode = () => ({
  type: types.RESET_CODE,
})

const codeReset = () => ({
  type: types.CODE_RESET,
})

export default {
  getCodeRequest,
  getCodeReceived,
  postCodeRequest,
  postCodeReceived,
  avatarCodeUpdated,
  resetCode,
  codeReset,
}
