import types from './types'

const pyodideInitialized = () => ({
  type: types.PYODIDE_INITIALIZED
})

const avatarCodeUpdated = () => ({
  type: types.AVATAR_CODE_UPDATED
})

const avatarsNextActionComputed = () => ({
  type: types.AVATARS_NEXT_ACTION_COMPUTED
})

export default {
  pyodideInitialized,
  avatarCodeUpdated,
  avatarsNextActionComputed
}
