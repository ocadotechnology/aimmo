import io from 'socket.io-client'
import { actions as gameActions } from '../features/Game'
import { actions as consoleLogActions } from '../features/ConsoleLog'
import { map, mergeMap } from 'rxjs/operators'
import { fromEvent, pipe, merge } from 'rxjs'

const connectToGame = () =>
  map(action => {
    const { game_url_base: gameUrlBase, game_url_path: gameUrlPath, avatar_id: avatarId } = action.payload.parameters
    return io(gameUrlBase, {
      path: gameUrlPath,
      query: {
        avatar_id: avatarId
      }
    })
  })

const listenFor = (eventName, socket, action) =>
  fromEvent(socket, eventName).pipe(
    map(event => action(event))
  )

const startListeners = () =>
  pipe(
    mergeMap(socket => merge(
      listenFor('game-state', socket, gameActions.socketGameStateReceived),
      listenFor('log', socket, consoleLogActions.socketConsoleLogReceived),
      listenFor('feedback-avatar-updated', socket, gameActions.socketFeedbackAvatarUpdated)
    ))
  )

export default { connectToGame, startListeners }
