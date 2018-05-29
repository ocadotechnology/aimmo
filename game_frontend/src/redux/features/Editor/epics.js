import actions from './actions'
import types from './types'
import { Observable, Scheduler } from 'rxjs'
import { map, mergeMap, catchError, debounceTime, tap } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const backgroundScheduler = Scheduler.async

const getCodeEpic = (action$, store, { api }) =>
  action$.pipe(
    ofType(types.GET_CODE_REQUEST),
    mergeMap(action =>
      api.get(`code/${store.getState().game.id}/`).pipe(
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
        `/players/api/code/${store.getState().game.id}/`,
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

const getConnectionParamsEpic = (action$, store, { api }) => {
  console.log(api)
  return action$.pipe(
      ofType(types.GET_CONNECTION_PARAMS_REQUEST),
      tap(console.log),
      mergeMap(action => 
        api.get(`games/${store.getState().game.id}/get_connection_params/`)
      ),
      tap(console.log)
    )
  }

export default {
  getCodeEpic,
  postCodeEpic,
  changeCodeEpic,
  getConnectionParamsEpic
}
