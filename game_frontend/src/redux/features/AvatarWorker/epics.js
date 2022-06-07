import { switchMap, mapTo, zip, take, tap, map, mergeMap, catchError } from 'rxjs/operators'

import actions from './actions'
import types from './types'
import { timeoutIfWorkerTakesTooLong } from './operators'
import { ofType } from 'redux-observable'
import { gameTypes } from '../Game'
import { editorTypes } from '../Editor'
import { from, of, Scheduler } from 'rxjs'

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

/**
 * Get the user's badges information.
 * @returns a redux action that contains a string storing the user's earned badges information.
 */
const getBadgesEpic = (action$, state$, { api }) =>
  action$.pipe(
    ofType(types.GET_BADGES_REQUEST),
    mergeMap((action) =>
      api.get(`badges/${state$.value.game.connectionParameters.game_id}/`).pipe(
        map((response) => actions.filterBadges(response.badges)),
        catchError((error) =>
          of({
            type: types.GET_BADGES_FAILURE,
            payload: error.xhr.response,
            error: true,
          })
        )
      )
    )
  )

const filterBadgesEpic = (action$, state$, { pyodideRunner: { filterByWorksheet } }) =>
  action$.pipe(
    ofType(types.FILTER_BADGES),
    switchMap(({ payload: badges }) =>
      from(filterByWorksheet(badges, state$.value.game.gameState))
    ),
    map((badges) => actions.getBadgesReceived(badges)),
    catchError((error) =>
      of({
        type: types.BADGES_CHECKED_FAILURE,
        payload: error,
        error: true,
      })
    )
  )

/**
 * Whenever the avatar's code is updated, get the user's badges information.
 * @returns a redux action that contains a string storing the user's earned badges information.
 */
const checkBadgesEpic = (action$, state$, { api }) =>
  action$.pipe(
    ofType(types.AVATAR_CODE_UPDATED),
    mergeMap((action) =>
      api.get(`badges/${state$.value.game.connectionParameters.game_id}/`).pipe(
        map((response) => actions.checkBadgesReceived(response.badges)),
        catchError((error) =>
          of({
            type: types.GET_BADGES_FAILURE,
            payload: error.xhr.response,
            error: true,
          })
        )
      )
    )
  )

/**
 * Every time the avatar's code's been updated and the user's current badges have been read from Django, run a badge
 * check that evaluates if any new badges have been earned.
 * @returns a redux action that holds the result of the badge check.
 */
const checkBadgesEarnedEpic = (action$, state$, { pyodideRunner: { checkIfBadgeEarned } }) =>
  action$.pipe(
    ofType(types.BADGES_CHECKED_SUCCESS),
    switchMap(({ payload: badges }) =>
      action$.pipe(
        ofType(types.AVATAR_CODE_UPDATED),
        switchMap(({ payload: computedTurnResult }) =>
          from(
            checkIfBadgeEarned(
              badges,
              computedTurnResult,
              state$.value.editor.code.codeOnServer,
              state$.value.game.gameState,
              state$.value.game.connectionParameters.currentAvatarID
            )
          )
        ),
        map(actions.badgesEarned),
        catchError((error) =>
          of({
            type: types.BADGES_CHECKED_FAILURE,
            payload: error,
            error: true,
          })
        )
      )
    )
  )

/**
 * Once the badge check has been run on the user's new code to see if they've earned any new badges, send a POST request
 * with the updated information.
 * @returns a redux action that confirms the success or failure of the POST request.
 */
const postBadgesEpic = (action$, state$, { api }) =>
  action$.pipe(
    ofType(types.BADGES_EARNED),
    api.post(`/kurono/api/badges/${state$.value.game.connectionParameters.game_id}/`, (action) => {
      return { badges: action.payload }
    }),
    map(() => actions.postBadgesReceived()),
    catchError((error) =>
      of({
        type: types.POST_BADGES_FAILURE,
        payload: error.xhr.response,
        error: true,
      })
    )
  )

export default {
  initializePyodideEpic,
  initialUpdateAvatarCodeEpic,
  updateAvatarCodeEpic,
  computeNextActionEpic,
  getBadgesEpic,
  checkBadgesEpic,
  postBadgesEpic,
  checkBadgesEarnedEpic,
}
