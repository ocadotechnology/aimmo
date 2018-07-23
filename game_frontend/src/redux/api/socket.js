import io from 'socket.io-client'
import actions from '../features/Game/actions'
import { map, merge, tap, mapTo, of } from 'rxjs/operators'
import { pipe } from 'rxjs/Rx'
import { fromEvent } from 'rxjs/observable/fromEvent'

let socketConnection = null

const connectToGame = response$ =>
  response$.map(({ game_url_base, game_id }) =>
    io(game_url_base, {
      path: `/game-${game_id}`
    })
  )

const listenFor = (eventName, socket, action) => {
  of({type: 'yo'})
  // return fromEvent(socket, eventName).pipe(
  //   tap(console.log),
  //   mapTo({ type: 'yo' })
  //   // map(event => action(event))
  // )
}

const startListeners = () =>
  pipe(
    tap(console.log),
    // mapTo({ type: 'yo' })
    map(socket =>
      merge(
        listenFor('game-state', socket, actions.socketGameStateReceived)
      )),
    tap(console.log)
  )


export default { connectToGame, startListeners }


