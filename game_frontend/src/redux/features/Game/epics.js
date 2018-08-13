import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, mergeMap, catchError, delay, tap } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const getConnectionParametersEpic = (action$, store, { api: { get } }) => action$.pipe(
  ofType(types.SOCKET_CONNECT_TO_GAME_REQUEST),
  mergeMap(action =>
    get(`games/${store.getState().game.connectionParameters.game_id}/connection_parameters/`).pipe(
      map(response => actions.connectionParametersReceived(response))
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

const connectToGameEpic = (action$, store, { api: { socket, unity } }) => action$.pipe(
  ofType(types.CONNECTION_PARAMETERS_RECEIVED),
  socket.connectToGame(),
  socket.startListeners(),
  catchError(error => Observable.of({
    type: types.SOCKET_CONNECT_TO_GAME_FAIL,
    payload: error,
    error: true
  }))
)

const sendAvatarIDEpic = (action$, store, { api: { unity } }) => action$.pipe(
  ofType(types.CONNECTION_PARAMETERS_RECEIVED),
  map(action => actions.unityEvent(
    'SetCurrentAvatarID',
    parseInt(action.payload.parameters['avatar_id']),
    actions.unitySendAvatarIDSuccess(),
    actions.unitySendAvatarIDFail
  )),
  unity.sendExternalEvent(unity.emitToUnity)
)

export default {
  getConnectionParametersEpic,
  connectToGameEpic,
  sendGameStateEpic,
  sendAvatarIDEpic
}
