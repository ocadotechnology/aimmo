import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError, tap } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const getConnectionParamsEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.GET_CONNECTION_PARAMS_REQUEST),
        mergeMap(action => 
          api.get(`games/${store.getState().game.connectionParams.id}/connection_params/`).pipe(
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

const setGameURLEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.SET_GAME_URL),
        mergeMap(action =>
        Observable.of(action).pipe(
            api.setGameURL,
            map(event => ({ type: types.SET_GAME_URL_SUCCESS })),
            catchError(error => Observable.of({
                type: types.SET_GAME_URL_FAIL,
                error: true
            })
            )
        )
        )
    )
}

const setGamePathEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.SET_GAME_PATH),
        mergeMap(action =>
        Observable.of(action).pipe(
            api.setGamePath, 
            map(event => ({ type: types.SET_GAME_PATH_SUCCESS })),
            catchError(error => Observable.of({
                type: types.SET_GAME_PATH_FAIL,
                error: true
            })
            )
        )
        )
    )
}

const setGamePortEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.SET_GAME_PORT),
        mergeMap(action =>
        Observable.of(action).pipe(
            api.setGamePort, 
            map(event => ({ type: types.SET_GAME_PORT_SUCCESS })),
            catchError(error => Observable.of({
                type: types.SET_GAME_PORT_FAIL,
                error: true
            })
            )
        )
        )
    )
}

const setGameSSLEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.SET_GAME_SSL),
        mergeMap(action =>
        Observable.of(action).pipe(
            api.setGameSSL, 
            map(event => ({ type: types.SET_GAME_SSL_SUCCESS })),
            catchError(error => Observable.of({
                type: types.SET_GAME_SSL_FAIL,
                error: true
            })
            )
        )
        )
    )
}

const establishGameConnectionEpic = (action$, store, { api }) => {
    return action$.pipe(
        ofType(types.ESTABLISH_GAME_CONNECTION),
        mergeMap(action =>
        Observable.of(action).pipe(
            api.establishGameConnection, 
            map(event => ({ type: types.ESTABLISH_GAME_CONNECTION_SUCCESS })),
            catchError(error => Observable.of({
                type: types.ESTABLISH_GAME_CONNECTION_FAIL,
                error: true
            })
            )
        )
        )
    )
}

export default {
    getConnectionParamsEpic,
    setGameURLEpic,
    setGamePathEpic,
    setGamePortEpic,
    setGameSSLEpic,
    establishGameConnectionEpic
}