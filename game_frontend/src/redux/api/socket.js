import io from 'socket.io-client'
import { actions as gameActions } from '../features/Game'
import { actions as consoleLogActions } from '../features/ConsoleLog'
import { map, mergeMap, tap } from 'rxjs/operators'
import { fromEvent, pipe, merge } from 'rxjs'

var socketIO

const connectToGame = () =>
  map(action => {
    const {
      game_url_base: gameUrlBase,
      game_url_path: gameUrlPath,
      avatar_id: avatarId
    } = action.payload.parameters
    socketIO = io(gameUrlBase, {
      path: gameUrlPath,
      query: {
        avatar_id: avatarId
      }
    })
    return socketIO
  })

const listenFor = (eventName, socket, action) =>
  fromEvent(socket, eventName).pipe(map(event => action(event)))

const emitAction = nextAction => socketIO.emit('action', nextAction)

const emitMove = () =>
  tap(() =>
    socketIO.emit('action', {
      action_type: 'move',
      options: { direction: { x: -1, y: 0 } }
    })
  )

const startListeners = () =>
  pipe(
    mergeMap(socket =>
      merge(
        listenFor('game-state', socket, gameActions.socketGameStateReceived),
        listenFor('log', socket, consoleLogActions.socketConsoleLogReceived)
      )
    )
  )

export default { connectToGame, startListeners, emitMove, emitAction }
