import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError } from 'rxjs/operators'
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
    map(action => actions.unityEvent(
      'SetGameURL',
      action.payload.gameURL,
      actions.setGameURLSuccess(),
      actions.setGameURLFail()
    )),
    api.sendUnityEvent
  )
}

const setGamePathEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SET_GAME_PATH),
    map(action => actions.unityEvent(
      'SetGamePath',
      action.payload.gamePath,
      actions.setGamePathSuccess(),
      actions.setGamePathFail()
    )),
    api.sendUnityEvent
  )
}

const setGamePortEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SET_GAME_PORT),
    map(action => actions.unityEvent(
      'SetGamePort',
      action.payload.gamePort,
      actions.setGamePortSuccess(),
      actions.setGamePortFail()
    )),
    api.sendUnityEvent
  )
}

const setGameSSLEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SET_GAME_SSL),
    map(action => actions.unityEvent(
      'SetSSL',
      action.payload.gameSSLFlag,
      actions.setGameSSLSuccess(),
      actions.setGameSSLFail()
    )),
    api.sendUnityEvent
  )
}

const establishGameConnectionEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.ESTABLISH_GAME_CONNECTION),
    map(action => actions.unityEvent(
      'EstablishConnection',
      '',
      actions.establishGameConnectionSuccess(),
      actions.establishGameConnectionFail()
    )),
    api.sendUnityEvent
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
