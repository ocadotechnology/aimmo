import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError } from 'rxjs/operators'
import { ofType } from 'redux-observable'

// TODO: maybe refactor all these catchErrors into individual actions instead of creating them here each time
const getConnectionParamsEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.GET_CONNECTION_PARAMS_REQUEST),
        mergeMap(action => 
          api.get(`games/${store.getState().game.id}/connection_params/`).pipe(
            map(response => actions.getConnectionParamsSuccess(response)),
            catchError(error => Observable.of({
              type: types.GET_CONNECTION_PARAMS_FAIL,
              payload: error.xhr.response,
              error: true
            }))
          )
        )
      )
    }
  
const emitUnityEventEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.EMIT_UNITY_EVENT),
        mergeMap(action =>
        Observable.of(action).pipe(
            api.emitUnityEvent,
            map(event => ({ type: types.EMIT_UNITY_EVENT_SUCCESS })),
            catchError(error => Observable.of({
                type: types.EMIT_UNITY_EVENT_FAIL,
                error: true
            })
            )
        )
        )
    )
}

export default {
    getConnectionParamsEpic,
    emitUnityEventEpic
}