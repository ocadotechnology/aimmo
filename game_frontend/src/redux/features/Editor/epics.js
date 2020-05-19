import actions from './actions'
import { actions as analyticActions } from 'redux/features/Analytics'
import { gameTypes } from 'redux/features/Game'
import types from './types'
import { Scheduler, of } from 'rxjs'
import {
  map,
  mergeMap,
  catchError,
  debounceTime,
  mapTo,
  switchMap,
  tap,
  take,
  zip
} from 'rxjs/operators'
import { ofType } from 'redux-observable'

const backgroundScheduler = Scheduler.async

const getCodeEpic = (action$, state$, { api }) =>
  action$.pipe(
    ofType(types.GET_CODE_REQUEST),
    mergeMap(action =>
      api.get(`code/${state$.value.game.connectionParameters.game_id}/`).pipe(
        map(response => actions.getCodeReceived(response.code)),
        catchError(error =>
          of({
            type: types.GET_CODE_FAILURE,
            payload: error.xhr.response,
            error: true
          })
        )
      )
    )
  )

const postCodeEpic = (action$, state$, { api }) =>
  action$.pipe(
    ofType(types.POST_CODE_REQUEST),
    api.post(`/kurono/api/code/${state$.value.game.connectionParameters.game_id}/`, () => ({
      code: state$.value.editor.code.code
    })),
    map(() => actions.postCodeReceived()),
    catchError(error =>
      of({
        type: types.POST_CODE_FAILURE,
        payload: error.xhr.response,
        error: true
      })
    )
  )

const postCodeAnalyticsEpic = action$ =>
  action$.pipe(
    ofType(types.POST_CODE_REQUEST),
    mapTo(analyticActions.sendAnalyticsEvent('Kurono', 'Click', 'Run Code'))
  )

const initialUpdateAvatarCodeEpic = (action$, state$, { pyodideRunner: { updateAvatarCode } }) =>
  action$.pipe(
    zip(
      action$.pipe(ofType('PYTHON_INITIALISED'), take(1)),
      action$.pipe(ofType(types.GET_CODE_SUCCESS), take(1))
    ),
    switchMap(() => updateAvatarCode(state$.value.editor.code.codeOnServer)),
    mapTo(actions.avatarCodeUpdated())
  )

const updateAvatarCodeEpic = (action$, state$, { pyodideRunner: { updateAvatarCode } }) =>
  action$.pipe(
    ofType(types.POST_CODE_SUCCESS),
    switchMap(() => updateAvatarCode(state$.value.editor.code.codeOnServer)),
    mapTo(actions.avatarCodeUpdated())
  )

const resetCodeAnalyticsEpic = action$ =>
  action$.pipe(
    ofType(types.RESET_CODE),
    mapTo(analyticActions.sendAnalyticsEvent('Kurono', 'Click', 'Reset Code'))
  )

const changeCodeEpic = (action$, state$, dependencies, scheduler = backgroundScheduler) =>
  action$.pipe(
    ofType(types.KEY_PRESSED),
    debounceTime(300, scheduler),
    map(action => actions.changeCode(action.payload.code))
  )

const nextActionEpic = (action$, state$, { api: { socket }, pyodideRunner: { runNextTurn } }) =>
  action$.pipe(
    ofType(gameTypes.SOCKET_GAME_STATE_RECEIVED),
    switchMap(async () => {
      const nextAction = await runNextTurn(
        state$.value.editor.code.codeOnServer,
        state$.value.editor.code.pythonInitialised
      )
      socket.emitAction(nextAction)
    }),
    mapTo({ type: 'dummy' })
  )

export default {
  getCodeEpic,
  postCodeEpic,
  changeCodeEpic,
  postCodeAnalyticsEpic,
  initialUpdateAvatarCodeEpic,
  updateAvatarCodeEpic,
  resetCodeAnalyticsEpic,
  nextActionEpic
}
