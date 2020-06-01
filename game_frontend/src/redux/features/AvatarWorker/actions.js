import types from './types'

const pyodideInitialized = () => ({
  type: types.PYODIDE_INITIALIZED
})

const avatarCodeUpdated = computedTurnResult => ({
  type: types.AVATAR_CODE_UPDATED,
  payload: {
    ...computedTurnResult
  }
})

const avatarsNextActionComputed = computedTurnResult => ({
  type: types.AVATARS_NEXT_ACTION_COMPUTED,
  payload: {
    ...computedTurnResult
  }
})

export default {
  pyodideInitialized,
  avatarCodeUpdated,
  avatarsNextActionComputed
}
