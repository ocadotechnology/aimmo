import { of, Scheduler } from 'rxjs'
import { timeout, catchError } from 'rxjs/operators'

const PYODIDE_WORKER_PROCESSING_TIME = 1000

/**
 * An operator that resets the pyodideWorker if it is taking too long to respond.
 * If there is a timeout, we return a ComputedTurnResult with a wait action and a log message
 * that tells the user about the timeout
 * @param {*} state$ The state observable that's passed to epics
 * @param {*} resetWorker The function that resets the pyodide worker
 */
export const timeoutIfWorkerTakesTooLong = (
  state$,
  resetWorker,
  scheduler
) => computedTurnResult$ =>
  computedTurnResult$.pipe(
    timeout(PYODIDE_WORKER_PROCESSING_TIME, scheduler),
    catchError(() => {
      resetWorker(
        state$.value.editor.code.codeOnServer,
        state$.value.game.connectionParameters.currentAvatarID
      )
      return of({
        action: { action_type: 'wait' },
        log: 'Hmm... your avatar is taking a long time to respond, is there a 🐛 in your code?',
        turnCount: state$.value.game.gameState.turnCount + 1
      })
    })
  )
