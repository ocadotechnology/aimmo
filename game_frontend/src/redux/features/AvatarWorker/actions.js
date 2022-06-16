import types from './types'

const initializePyodide = () => ({
  type: types.INITIALIZE_PYODIDE,
})

const pyodideInitialized = () => ({
  type: types.PYODIDE_INITIALIZED,
})

const avatarCodeUpdated = (computedTurnResult) => ({
  type: types.AVATAR_CODE_UPDATED,
  payload: {
    ...computedTurnResult,
  },
})

const avatarsNextActionComputed = (computedTurnResult) => ({
  type: types.AVATARS_NEXT_ACTION_COMPUTED,
  payload: {
    ...computedTurnResult,
  },
})

const getBadgesRequest = () => ({
  type: types.GET_BADGES_REQUEST,
})

const getBadgesReceived = (badges) => ({
  type: types.GET_BADGES_SUCCESS,
  payload: badges,
})

const checkBadgesReceived = (badges) => ({
  type: types.BADGES_CHECKED_SUCCESS,
  payload: badges,
})

const postBadgesRequest = (badges) => ({
  type: types.POST_BADGES_REQUEST,
  payload: badges,
})

const postBadgesReceived = () => ({
  type: types.POST_BADGES_SUCCESS,
})

const badgesEarned = (badges) => ({
  type: types.BADGES_EARNED,
  payload: badges,
})

export default {
  initializePyodide,
  pyodideInitialized,
  avatarCodeUpdated,
  avatarsNextActionComputed,
  badgesEarned,
  getBadgesRequest,
  getBadgesReceived,
  checkBadgesReceived,
  postBadgesRequest,
  postBadgesReceived,
}
