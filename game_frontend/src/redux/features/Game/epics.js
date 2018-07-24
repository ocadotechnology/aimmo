import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError, tap } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const connectToGameEpic = (action$, store, { api }) => action$.pipe(
  ofType(types.GET_CONNECTION_PARAMETERS_REQUEST),
  mergeMap(action =>
    api.get(`games/${store.getState().game.connectionParameters.id}/connection_parameters/`).pipe(
      api.socket.connectToGame(),
      api.socket.startListeners(),
      catchError(error => Observable.of({
        type: types.GET_CONNECTION_PARAMETERS_FAIL,
        payload: error,
        error: true
      })),
    )
  )
)

const sendGameStateEpic = (action$, store, { api }) => action$.pipe(
  ofType(types.SOCKET_GAME_STATE_RECEIVED),
  map(action => actions.unityEvent(
    'ReceiveGameUpdate',
    JSON.stringify(action.payload.gameState),
    actions.sendGameUpdateSuccess(),
    actions.sendGameUpdateFail
  )),
  api.unity.sendExternalEvent(api.unity.emitToUnity)
)

export default {
  connectToGameEpic,
  sendGameStateEpic,
}
