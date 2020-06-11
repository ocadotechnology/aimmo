import actions from './actions'
import { actions as analyticActions } from 'redux/features/Analytics'
import types from './types'
import { Scheduler, of } from 'rxjs'
import { map, mergeMap, catchError, mapTo } from 'rxjs/operators'
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
    api.post(`/kurono/api/code/${state$.value.game.connectionParameters.game_id}/`, action => ({
      code: action.payload.code
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

const resetCodeAnalyticsEpic = action$ =>
  action$.pipe(
    ofType(types.RESET_CODE),
    mapTo(analyticActions.sendAnalyticsEvent('Kurono', 'Click', 'Reset Code'))
  )

export default {
  getCodeEpic,
  postCodeEpic,
  postCodeAnalyticsEpic,
  resetCodeAnalyticsEpic
}
