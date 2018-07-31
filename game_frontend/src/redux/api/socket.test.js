/* eslint-env jest */
import { of } from 'rxjs/observable/of'
import actions from '../features/Game/actions'
import { tap } from 'rxjs/operators'
import socket from './socket'
import { Server } from 'mock-socket'

jest.mock('socket.io-client', () => {
  const { SocketIO } = require('mock-socket')
  return SocketIO
})

jest.mock('../features/Game/actions', () => ({
  socketGameStateReceived: jest.fn()
}))

describe('socket listens correctly', () => {
  it('socket listens for events', (done) => {
    const fakeURL = 'ws://localhost:8080'
    const mockServer = new Server(fakeURL)

    const gameState = JSON.stringify({ hello: 'world' })
    const connectionParams = { game_url_base: fakeURL, game_url_path: 'socket.io', avatar_id: 1 }

    mockServer.on('connect', socket => {
      console.log('connected!')
      socket.emit('game-state', gameState)
    })

    of(connectionParams).pipe(
      socket.connectToGame(),
      socket.startListeners(),
      tap(() => expect(actions.socketGameStateReceived).toHaveBeenCalledWith(gameState))
    ).subscribe(done)
  })
})
