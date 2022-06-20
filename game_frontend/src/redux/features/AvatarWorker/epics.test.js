/* eslint-env jest */

import { TestScheduler } from 'rxjs/testing'
import epics from './epics'
import actions from './actions'
import { of } from 'rxjs'
import { actions as editorActions } from 'features/Editor'
import { actions as gameActions } from 'features/Game'
import { delay } from 'rxjs/operators'

const deepEquals = (actual, expected) => expect(actual).toEqual(expected)

const createTestScheduler = (frameTimeFactor = 10) => {
  TestScheduler.frameTimeFactor = frameTimeFactor
  return new TestScheduler(deepEquals)
}

describe('avatarWorkerEpic', () => {
  it('starts initializing Pyodide when the game is connecting to the server', () => {
    const testScheduler = createTestScheduler()

    const dependencies = {
      pyodideRunner: {
        initializePyodide: () => of(1),
      },
    }

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('--s-', {
        s: gameActions.socketConnectToGameRequest(),
      })

      const state$ = null
      const output$ = epics.initializePyodideEpic(action$, state$, dependencies)

      expectObservable(output$).toBe('--u-', {
        u: actions.pyodideInitialized(),
      })
    })
  })

  it('loads avatar code when we first get it from the server and only when pyodide is initialized', () => {
    const testScheduler = createTestScheduler()

    const dependencies = {
      pyodideRunner: {
        updateAvatarCode: () => of(1),
      },
    }

    const state$ = {
      value: {
        editor: {
          code: {
            codeOnServer: 'some python code',
          },
        },
      },
    }

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const inputActions = {
        p: actions.pyodideInitialized(),
        c: editorActions.getCodeReceived('some python code'),
      }

      const action$1 = hot('--p--c--', inputActions)
      const action$2 = hot('--c--p--', inputActions)

      const output$1 = epics.initialUpdateAvatarCodeEpic(action$1, state$, dependencies)
      const output$2 = epics.initialUpdateAvatarCodeEpic(action$2, state$, dependencies)

      expectObservable(output$1).toBe('-----(u|)', {
        u: actions.avatarCodeUpdated(),
      })

      expectObservable(output$2).toBe('-----(u|)', {
        u: actions.avatarCodeUpdated(),
      })
    })
  })

  it('computes the next action every time we receive the next state of the game', () => {
    const testScheduler = createTestScheduler()

    const dependencies = {
      pyodideRunner: {
        computeNextAction$: () => of({ action_type: 'wait' }),
      },
      api: {
        socket: {
          emitAction: jest.fn(),
        },
      },
    }

    const state$ = {
      value: {
        game: { connectionParameters: { currentAvatarID: 1 } },
        avatarWorker: { pyodideInitialized: true },
      },
    }

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('-p--g--g-g-', {
        g: gameActions.socketGameStateReceived({ players: [{ id: 1 }] }),
        p: actions.pyodideInitialized(),
      })

      const output$ = epics.computeNextActionEpic(action$, state$, dependencies)

      expectObservable(output$).toBe('----a--a-a-', {
        a: actions.avatarsNextActionComputed({ action_type: 'wait' }),
      })
    })
    expect(dependencies.api.socket.emitAction).toBeCalled()
  })

  it('handles a pyodide worker timing out and resets it', () => {
    const testScheduler = createTestScheduler()

    const dependencies = {
      pyodideRunner: {
        computeNextAction$: () => of({ action_type: 'move' }).pipe(delay(2000)),
        resetWorker: jest.fn(),
      },
      api: {
        socket: {
          emitAction: jest.fn(),
        },
      },
    }

    const state$ = {
      value: {
        game: { gameState: { turnCount: 1 }, connectionParameters: { currentAvatarID: 1 } },
        avatarWorker: { pyodideInitialized: true },
        editor: {
          code: {
            codeOnServer: 'some python code',
          },
        },
      },
    }

    testScheduler.run(({ hot, cold, expectObservable }) => {
      const action$ = hot('-p--g----', {
        g: gameActions.socketGameStateReceived({ players: [{ id: 1 }] }),
        p: actions.pyodideInitialized(),
      })

      const output$ = epics.computeNextActionEpic(action$, state$, dependencies)

      expectObservable(output$).toBe('---- 1s a----', {
        a: actions.avatarsNextActionComputed({
          action: { action_type: 'wait' },
          log: "Hmm, we haven't had an action back from your avatar this turn. Is there a 🐞 in your code?",
          turnCount: 2,
        }),
      })
    })
    expect(dependencies.api.socket.emitAction).toBeCalled()
    expect(dependencies.pyodideRunner.resetWorker).toBeCalled()
  })
})
