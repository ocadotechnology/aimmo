import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const getConnectionParametersEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.GET_CONNECTION_PARAMETERS_REQUEST),
    mergeMap(action =>
      api.get(`games/${store.getState().game.connectionParameters.id}/connection_parameters/`).pipe(
        map(response => actions.getConnectionParametersSuccess(response)),
        catchError(error => Observable.of({
          type: types.GET_CONNECTION_PARAMETERS_FAIL,
          payload: error,
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
      actions.setGameURLFail
    )),
    api.unity.sendExternalEvent(api.unity.emitToUnity)
  )
}

const setGamePathEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SET_GAME_PATH),
    map(action => actions.unityEvent(
      'SetGamePath',
      action.payload.gamePath,
      actions.setGamePathSuccess(),
      actions.setGamePathFail
    )),
    api.unity.sendExternalEvent(api.unity.emitToUnity)
  )
}

const setGamePortEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SET_GAME_PORT),
    map(action => actions.unityEvent(
      'SetGamePort',
      action.payload.gamePort,
      actions.setGamePortSuccess(),
      actions.setGamePortFail
    )),
    api.unity.sendExternalEvent(api.unity.emitToUnity)
  )
}

const setGameSSLEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SET_GAME_SSL),
    map(action => actions.unityEvent(
      'SetSSL',
      action.payload.gameSSLFlag,
      actions.setGameSSLSuccess(),
      actions.setGameSSLFail
    )),
    api.unity.sendExternalEvent(api.unity.emitToUnity)
  )
}

const establishGameConnectionEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.ESTABLISH_GAME_CONNECTION),
    map(action => actions.unityEvent(
      'EstablishConnection',
      '',
      actions.establishGameConnectionSuccess(),
      actions.establishGameConnectionFail
    )),
    api.unity.sendExternalEvent(api.unity.emitToUnity)
  )
}

export default {
  getConnectionParametersEpic,
  setGameURLEpic,
  setGamePathEpic,
  setGamePortEpic,
  setGameSSLEpic,
  establishGameConnectionEpic
}
