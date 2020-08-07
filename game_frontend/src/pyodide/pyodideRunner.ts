import { defer, of } from 'rxjs'
import { spawn, Worker, ModuleThread, Thread } from 'threads'
import ComputedTurnResult from './computedTurnResult'
import { PyodideWorker } from './webWorker'
import consoleLogReducer from 'redux/features/ConsoleLog/reducers'

let worker: ModuleThread<PyodideWorker>
let workerReady = false

export async function initializePyodide () {
  await initializePyodideWorker()
  workerReady = true
}

async function initializePyodideWorker () {
  worker = await spawn<PyodideWorker>(new Worker('./webworker.ts'))
  await worker.initializePyodide()
}

export async function updateAvatarCode (
  userCode: string,
  gameState: any,
  playerAvatarID: number = 0
): Promise<ComputedTurnResult> {
  const turnCount = gameState?.turnCount
  return runIfWorkerReady(
    () => worker.updateAvatarCode(userCode, gameState, playerAvatarID),
    turnCount + 1
  )
}

export async function resetWorker (userCode: string, playerAvatarID: number) {
  workerReady = false
  await Thread.terminate(worker)
  await initializePyodideWorker()
  await worker.updateAvatarCode(userCode, null, playerAvatarID)
  workerReady = true
}

async function runIfWorkerReady (
  func: () => Promise<ComputedTurnResult>,
  turnCount: number
): Promise<ComputedTurnResult> {
  if (workerReady) {
    return func()
  } else {
    return Promise.resolve({
      action: { action: { action_type: 'wait' } },
      log: '',
      turnCount: turnCount + 1
    })
  }
}

export const computeNextAction$ = (gameState: any, avatarState: object) =>
  defer(() =>
    runIfWorkerReady(
      () => worker.computeNextAction(gameState, avatarState),
      gameState.turnCount + 1
    )
  )
