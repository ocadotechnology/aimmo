/* eslint-env jest */
import { Observable, TestScheduler } from 'rxjs'
import { of } from 'rxjs/observable/of'

import { ActionsObservable } from 'redux-observable'
import io from 'socket.io-client'
import epics from '../features/Game/epics'
// import actions from '../features/Game/actions'
import types from '../features/Game/types'
import { map, mergeMap, tap } from 'rxjs/operators'
import { pipe } from 'rxjs/Rx'
import socket from './socket'
import { SocketIO, Server } from 'mock-socket'

const deepEquals = (actual, expected) =>
  expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('socket listens correctly', () => {
  it('socket listens for events', (done) => {
    const fakeURL = 'ws://localhost:8080'
    const mockServer = new Server(fakeURL)
    window.io = SocketIO

    jest.mock('socket.io-client', () => {
      return jest.fn().mockImplementation((args) => {
        import { SocketIO } from 'mock-socket'
        return SocketIO(args)
      })
    })
    const actions = {
      socketGameStateReceived: jest.fn()
    }
    const connectionParams = { game_url_base: fakeURL, game_url_path: 'socket.io', avatar_id: 1 }
    // SocketIO(connectionParams.game_url_base)
    mockServer.on('connect', socket => {
      console.log('connected!')
      socket.emit('game-state', {})
    })

    of(connectionParams).pipe(
      tap(console.log),
      socket.connectToGame(),
      socket.startListeners(),
      tap(console.log),
      tap(() => expect(actions.socketGameStateReceived).toHaveBeenCalled()),
      tap(done)
    ).subscribe(console.error)

  })
})
