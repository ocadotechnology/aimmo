import { switchMap, mapTo, zip, take, tap } from 'rxjs/operators'

import actions from './actions'
import types from './types'
import { ofType } from 'redux-observable'
import { gameTypes } from '../Game'
import { editorTypes } from '../Editor'

const initializePyodideEpic = (action$, state$, { pyodideRunner: { initializePyodide } }) =>
  action$.pipe(
    ofType(gameTypes.SOCKET_CONNECT_TO_GAME_REQUEST),
    switchMap(initializePyodide),
    mapTo(actions.pyodideInitialized())
  )

const initialUpdateAvatarCodeEpic = (action$, state$, { pyodideRunner: { updateAvatarCode } }) =>
  action$.pipe(
    zip(
      action$.pipe(ofType(types.PYODIDE_INITIALIZED), take(1)),
      action$.pipe(ofType(editorTypes.GET_CODE_SUCCESS), take(1))
    ),
    switchMap(() => updateAvatarCode(state$.value.editor.code.codeOnServer)),
    mapTo(actions.avatarCodeUpdated())
  )

const updateAvatarCodeEpic = (action$, state$, { pyodideRunner: { updateAvatarCode } }) =>
  action$.pipe(
    ofType(editorTypes.POST_CODE_SUCCESS),
    switchMap(() => updateAvatarCode(state$.value.editor.code.codeOnServer)),
    mapTo(actions.avatarCodeUpdated())
  )

const computeNextActionEpic = (
  action$,
  state$,
  { api: { socket }, pyodideRunner: { computeNextAction$ } }
) =>
  action$.pipe(
    ofType(types.PYODIDE_INITIALIZED),
    switchMap(() =>
      action$.pipe(
        ofType(gameTypes.SOCKET_GAME_STATE_RECEIVED),
        switchMap(computeNextAction$),
        tap(socket.emitAction),
        mapTo(actions.avatarsNextActionComputed())
      )
    )
  )

export default {
  initializePyodideEpic,
  initialUpdateAvatarCodeEpic,
  updateAvatarCodeEpic,
  computeNextActionEpic
}
