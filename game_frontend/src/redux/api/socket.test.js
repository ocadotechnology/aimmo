/* eslint-env jest */
import { of } from 'rxjs'
import actions from '../features/Game/actions'
import { tap } from 'rxjs/operators'
import socket from './socket'
import EventEmitter from 'events'

jest.mock('../features/Game/actions', () => ({
  socketGameStateReceived: jest.fn(),
}))

describe('socket listens correctly', () => {
  it('socket listens for events', (done) => {
    const gameState = JSON.stringify({ hello: 'world' })
    const emitter = new EventEmitter()

    of(emitter)
      .pipe(
        socket.startListeners(),
        tap(() => expect(actions.socketGameStateReceived).toHaveBeenCalledWith(gameState))
      )
      .subscribe(done)

    emitter.emit('game-state', gameState)
  })
})
