import { switchMap, mapTo, zip, take, tap, map } from 'rxjs/operators'

import actions from './actions'
import types from './types'
import { timeoutIfWorkerTakesTooLong } from './operators'
import { ofType } from 'redux-observable'
import { gameTypes } from '../Game'
import { editorTypes } from '../Editor'
import { from, Scheduler } from 'rxjs'

const backgroundScheduler = Scheduler.async

const initializePyodideEpic = (action$, state$, { pyodideRunner: { initializePyodide } }) =>
  action$.pipe(
    ofType(gameTypes.SOCKET_CONNECT_TO_GAME_REQUEST, types.INITIALIZE_PYODIDE),
    switchMap(initializePyodide),
    mapTo(actions.pyodideInitialized())
  )

/**
 * Sets the avatar code in the pyodide worker as soon as the worker is fully initialized and we have fetched the code.
 */
const initialUpdateAvatarCodeEpic = (action$, state$, { pyodideRunner: { updateAvatarCode } }) =>
  action$.pipe(
    zip(
      action$.pipe(ofType(types.PYODIDE_INITIALIZED), take(1)),
      action$.pipe(ofType(editorTypes.GET_CODE_SUCCESS), take(1))
    ),
    switchMap(() => updateAvatarCode(state$.value.editor.code.codeOnServer)),
    map(actions.avatarCodeUpdated)
  )

const updateAvatarCodeEpic = (
  action$,
  state$,
  { api: { socket }, pyodideRunner: { updateAvatarCode, resetWorker } },
  scheduler = backgroundScheduler
) =>
  action$.pipe(
    ofType(types.PYODIDE_INITIALIZED),
    switchMap(() =>
      action$.pipe(
        ofType(editorTypes.POST_CODE_SUCCESS),
        switchMap(() =>
          from(
            updateAvatarCode(
              state$.value.editor.code.codeOnServer,
              state$.value.game.gameState,
              state$.value.game.connectionParameters.currentAvatarID
            )
          ).pipe(timeoutIfWorkerTakesTooLong(state$, resetWorker, scheduler))
        ),
        tap(socket.emitAction),
        map(actions.avatarCodeUpdated)
      )
    )
  )

/**
 * For each game state that we receive, we compute the avatar's next action and send it to the game server.
 * @returns a redux action that contains the avatar's next action
 */
const computeNextActionEpic = (
  action$,
  state$,
  { api: { socket }, pyodideRunner: { computeNextAction$, resetWorker } },
  scheduler = backgroundScheduler
) =>
  action$.pipe(
    ofType(types.PYODIDE_INITIALIZED),
    switchMap(() =>
      action$.pipe(
        ofType(gameTypes.SOCKET_GAME_STATE_RECEIVED),
        switchMap(({ payload: { gameState } }) =>
          computeNextAction$(
            gameState,
            state$.value.game.connectionParameters.currentAvatarID
          ).pipe(timeoutIfWorkerTakesTooLong(state$, resetWorker, scheduler))
        ),
        tap(socket.emitAction),
        map(actions.avatarsNextActionComputed)
      )
    )
  )

export default {
  initializePyodideEpic,
  initialUpdateAvatarCodeEpic,
  updateAvatarCodeEpic,
  computeNextActionEpic
}
