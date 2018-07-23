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

const receiveConnectionParametersEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.GET_CONNECTION_PARAMETERS_SUCCESS),
    mergeMap(action => {
      const { game_url_base, game_id } = action.payload.connectionParameters;
      const socket$ = Observable.of(api.socket.connectToGame(game_url_base, game_id));
      return socket$.switchMap(socket => {
        return Observable.fromEvent(socket, 'game-state').map((s) => actions.socketGameStateReceived(s));
      })
    })
  )
}

const sendGameStateEpic = (action$, store, { api }) => {
  return action$.pipe(
    ofType(types.SOCKET_GAME_STATE_RECEIVED),
    map(action => actions.unityEvent(
      'ReceiveGameUpdate',
      JSON.stringify(action.payload.gameState),
      actions.sendGameUpdateSuccess(),
      actions.sendGameUpdateFail
    )),
    api.unity.sendExternalEvent(api.unity.emitToUnity)
  )
}

export default {
  getConnectionParametersEpic,
  sendGameStateEpic,
  receiveConnectionParametersEpic,
}
