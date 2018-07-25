import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const connectToGameEpic = (action$, store, { api: { get, socket } }) => action$.pipe(
  ofType(types.SOCKET_CONNECT_TO_GAME_REQUEST),
  mergeMap(action =>
    get(`games/${store.getState().game.connectionParameters.id}/connection_parameters/`).pipe(
      socket.connectToGame(),
      socket.startListeners(),
      catchError(error => Observable.of({
        type: types.SOCKET_CONNECT_TO_GAME_FAIL,
        payload: error,
        error: true
      }))
    )
  )
)

const sendGameStateEpic = (action$, store, { api: { unity } }) => action$.pipe(
  ofType(types.SOCKET_GAME_STATE_RECEIVED),
  map(action => actions.unityEvent(
    'ReceiveGameUpdate',
    JSON.stringify(action.payload.gameState),
    actions.sendGameStateSuccess(),
    actions.sendGameStateFail
  )),
  unity.sendExternalEvent(unity.emitToUnity)
)

export default {
  connectToGameEpic,
  sendGameStateEpic
}
