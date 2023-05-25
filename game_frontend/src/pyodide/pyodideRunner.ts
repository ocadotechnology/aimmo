import { defer } from 'rxjs'
import { spawn, Worker, ModuleThread, Thread } from 'threads'
import ComputedTurnResult from './computedTurnResult'
import { PyodideWorker } from './webWorker'

let worker: ModuleThread<PyodideWorker>
let workerReady = false

export async function initializePyodide() {
  await initializePyodideWorker()
  workerReady = true
}

async function initializePyodideWorker() {
  worker = await spawn<PyodideWorker>(new Worker('./webWorker.ts'))
  await worker.initializePyodide()
}

export async function checkIfBadgeEarned(
  badges: string,
  result: ComputedTurnResult,
  userCode: string,
  gameState: any,
  // currentAvatarID: number
): Promise<string> {
  // return await worker.checkIfBadgeEarned(badges, result, userCode, gameState, currentAvatarID)
  return worker.checkIfBadgeEarned(badges, result, userCode, gameState)
}

export async function updateAvatarCode(
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

export async function resetWorker(userCode: string, playerAvatarID: number) {
  workerReady = false
  await Thread.terminate(worker)
  await initializePyodideWorker()
  await worker.updateAvatarCode(userCode, null, playerAvatarID)
  workerReady = true
}

async function runIfWorkerReady(
  func: () => Promise<ComputedTurnResult>,
  turnCount: number
): Promise<ComputedTurnResult> {
  if (workerReady) {
    return func()
  } else {
    return Promise.resolve({
      action: { action: { action_type: 'wait' } },
      log: '',
      turnCount: turnCount + 1,
    })
  }
}

export const computeNextAction$ = (gameState: any, avatarState: object, gamePaused: boolean) =>
  defer(() =>
    runIfWorkerReady(
      () => worker.computeNextAction(gameState, avatarState, gamePaused),
      gameState.turnCount + 1
    )
  )
