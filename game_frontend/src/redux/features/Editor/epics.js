import actions from './actions'
import types from './types'
import { Scheduler, of } from 'rxjs'
import { map, mergeMap, catchError, debounceTime } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const backgroundScheduler = Scheduler.async

const getCodeEpic = (action$, state$, { api }) =>
  action$.pipe(
    ofType(types.GET_CODE_REQUEST),
    mergeMap(action =>
      api.get(`code/${state$.value.game.connectionParameters.game_id}/`).pipe(
        map(response => actions.getCodeReceived(response.code)),
        catchError(error => of({
          type: types.GET_CODE_FAILURE,
          payload: error.xhr.response,
          error: true
        }))
      )
    )
  )

const postCodeEpic = (action$, state$, { api }) =>
  action$
    .pipe(
      ofType(types.POST_CODE_REQUEST),
      api.post(
        `/aimmo/api/code/${state$.value.game.connectionParameters.game_id}/`,
        () => ({ code: state$.value.editor.code.code })
      ),
      map(response => actions.postCodeReceived()),
      catchError(error => of({
        type: types.POST_CODE_FAILURE,
        payload: error.xhr.response,
        error: true
      }))
    )

const changeCodeEpic = (action$, state$, dependencies, scheduler = backgroundScheduler) =>
  action$.pipe(
    ofType(types.KEY_PRESSED),
    debounceTime(300, scheduler),
    map(action => actions.changeCode(action.payload.code))
  )

export default {
  getCodeEpic,
  postCodeEpic,
  changeCodeEpic
}
