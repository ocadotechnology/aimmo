import actions from './actions'
import types from './types'
import { Observable, Scheduler } from 'rxjs'
import { map, mergeMap, catchError, debounceTime } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const backgroundScheduler = Scheduler.async

const getCodeEpic = (action$, store, { api }) =>
  action$.pipe(
    ofType(types.GET_CODE_REQUEST),
    mergeMap(action =>
      api.get(`code/${store.getState().game.connectionParameters.id}/`).pipe(
        map(response => actions.getCodeReceived(response.code)),
        catchError(error => Observable.of({
          type: types.GET_CODE_FAILURE,
          payload: error.xhr.response,
          error: true
        }))
      )
    )
  )

const postCodeEpic = (action$, store, { api }) =>
  action$
    .pipe(
      ofType(types.POST_CODE_REQUEST),
      api.post(
        `/players/api/code/${store.getState().game.connectionParameters.id}/`,
        () => ({ code: store.getState().editor.code })
      ),
      map(response => actions.postCodeReceived()),
      catchError(error => Observable.of({
        type: types.POST_CODE_FAILURE,
        payload: error.xhr.response,
        error: true
      }))
    )

const changeCodeEpic = (action$, store, dependencies, scheduler = backgroundScheduler) =>
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
