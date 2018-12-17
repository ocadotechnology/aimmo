import actions from './actions'
import types from './types'
import { of } from 'rxjs'
import { map, mergeMap, catchError, switchMap, first, mapTo, debounceTime } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const timeoutEpic = (action$) =>
  action$.pipe(
    ofType(types.SOCKET_GAME_STATE_RECEIVED),
    debounceTime(12000),
    map(action => actions.setTimeout())
  )

const getConnectionParametersEpic = (action$, state$, { api: { get } }) => action$.pipe(
  ofType(types.SOCKET_CONNECT_TO_GAME_REQUEST),
  mergeMap(action =>
    get(`games/${state$.value.game.connectionParameters.game_id}/connection_parameters/`).pipe(
      map(response => actions.connectionParametersReceived(response))
    )
  )
)

const sendGameStateEpic = (action$, state$, { api: { unity } }) => action$.pipe(
  ofType(types.SOCKET_GAME_STATE_RECEIVED),
  map(action => actions.unityEvent(
    'ReceiveGameUpdate',
    JSON.stringify(action.payload.gameState),
    actions.sendGameStateSuccess(),
    actions.sendGameStateFail
  )),
  unity.sendExternalEvent(unity.emitToUnity)
)

const gameLoadedEpic = action$ => action$.pipe(
  ofType(types.SOCKET_CONNECT_TO_GAME_REQUEST),
  switchMap(() =>
    action$.pipe(
      ofType(types.SOCKET_GAME_STATE_RECEIVED),
      first(),
      mapTo(actions.gameDataLoaded())
    )
  )
)

const connectToGameEpic = (action$, state$, { api: { socket, unity } }) => action$.pipe(
  ofType(types.CONNECTION_PARAMETERS_RECEIVED),
  socket.connectToGame(),
  socket.startListeners(),
  catchError(error => of({
    type: types.SOCKET_CONNECT_TO_GAME_FAIL,
    payload: error,
    error: true
  }))
)

const sendAvatarIDEpic = (action$, state$, { api: { unity } }) => action$.pipe(
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
  gameLoadedEpic,
  sendGameStateEpic,
  sendAvatarIDEpic,
  timeoutEpic
}
