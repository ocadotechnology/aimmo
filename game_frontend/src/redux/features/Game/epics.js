import actions from './actions'
import types from './types'
import { editorTypes } from 'features/Editor'
import { Scheduler, of } from 'rxjs'
import { map, mergeMap, catchError, switchMap, first, mapTo, timeout, ignoreElements, timeInterval } from 'rxjs/operators'
import { ofType } from 'redux-observable'
import { actions as analyticActions } from 'redux/features/Analytics'

const backgroundScheduler = Scheduler.async

const getConnectionParametersEpic = (action$, state$, { api: { get } }) => action$.pipe(
  ofType(types.SOCKET_CONNECT_TO_GAME_REQUEST),
  mergeMap(action =>
    get(`games/${state$.value.game.connectionParameters.game_id}/connection_parameters/`).pipe(
      map(response => actions.connectionParametersReceived(response))
    )
  )
)

const gameLoadedEpic = action$ => action$.pipe(
  ofType(types.SOCKET_CONNECT_TO_GAME_REQUEST),
  switchMap(() =>
    action$.pipe(
      ofType(types.SOCKET_GAME_STATE_RECEIVED),
      first(),
      mapTo(actions.gameLoaded())
    )
  )
)

const gameLoadedIntervalEpic = (action$, state$, dependencies, scheduler = backgroundScheduler) =>
  action$.pipe(
    ofType(types.GAME_LOADED),
    timeInterval(scheduler),
    map(timeInterval =>
      analyticActions.sendAnalyticsTimingEvent('Kurono', 'Load', 'Game', timeInterval.interval)
    )
  )

const connectToGameEpic = (action$, state$, { api: { socket } }) => action$.pipe(
  ofType(types.CONNECTION_PARAMETERS_RECEIVED),
  socket.connectToGame(),
  socket.startListeners(),
  catchError(error => of({
    type: types.SOCKET_CONNECT_TO_GAME_FAIL,
    payload: error,
    error: true
  }))
)

const avatarUpdatingTimeoutEpic = (action$, state$, dependencies, scheduler = backgroundScheduler) => action$.pipe(
  ofType(editorTypes.POST_CODE_REQUEST),
  switchMap(() =>
    action$.pipe(
      ofType(types.SOCKET_FEEDBACK_AVATAR_UPDATED_SUCCESS),
      timeout(25000, scheduler),
      first(),
      ignoreElements(),
      catchError(() =>
        of(actions.socketFeedbackAvatarUpdatedTimeout())
      )
    )
  )
)

const codeUpdatingIntervalEpic = (action$, state$, dependencies, scheduler = backgroundScheduler) =>
  action$.pipe(
    ofType(editorTypes.POST_CODE_REQUEST),
    switchMap(() =>
      action$.pipe(
        ofType(types.SOCKET_FEEDBACK_AVATAR_UPDATED_SUCCESS, types.SOCKET_FEEDBACK_AVATAR_UPDATED_TIMEOUT),
        timeInterval(scheduler),
        map(timeInterval =>
          analyticActions.sendAnalyticsTimingEvent('Kurono', 'Update', 'User code', timeInterval.interval)
        )
      )
    )
  )

export default {
  getConnectionParametersEpic,
  connectToGameEpic,
  avatarUpdatingTimeoutEpic,
  gameLoadedEpic,
  gameLoadedIntervalEpic,
  codeUpdatingIntervalEpic
}
