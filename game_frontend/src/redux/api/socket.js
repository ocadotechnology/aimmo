import io from 'socket.io-client'
import actions from '../features/Game/actions'
import { map, mergeMap } from 'rxjs/operators'
import { merge } from 'rxjs/observable/merge'
import { fromEvent } from 'rxjs/observable/fromEvent'
import { pipe } from 'rxjs/Rx'

const connectToGame = () =>
  map(response => {
    const { game_url_base, game_id } = response
    return io(game_url_base, {
      path: `/game-${game_id}`
    })
  })

const listenFor = (eventName, socket, action) =>
  fromEvent(socket, eventName).pipe(
    map(event => action(event))
  )

const startListeners = () =>
  pipe(
    mergeMap(socket => merge(
      listenFor('game-state', socket, actions.socketGameStateReceived)
    ))
  )

export default { connectToGame, startListeners }
