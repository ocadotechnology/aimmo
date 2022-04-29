import { defer } from 'rxjs'
import { spawn, Worker, ModuleThread, Thread } from 'threads'
import ComputedTurnResult from './computedTurnResult'
import { PyodideWorker } from './webWorker'
import BadgeResult from "./badgeResult"

let worker: ModuleThread<PyodideWorker>
let workerReady = false

export async function initializePyodide () {
  await initializePyodideWorker()
  workerReady = true
}

async function initializePyodideWorker () {
  worker = await spawn<PyodideWorker>(new Worker('./webWorker.ts'))
  await worker.initializePyodide()
}

export async function checkIfBadgeEarned (
  result: ComputedTurnResult,
  userCode: string,
  gameState: any,
  playerAvatarId: number
): Promise<BadgeResult> {
  console.log("CHECKING BADGES")
  console.log(result)
  return runBadgeCheck(() => worker.checkIfBadgeEarned('result', userCode, gameState, playerAvatarId))
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
  console.log("RESETTING WORKER")
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

async function runBadgeCheck (
  func: () => Promise<BadgeResult>
): Promise<BadgeResult> {
  console.log("Running badge check")
  if (workerReady) {
    console.log("Worker ready")
    return func()
  } else {
    console.log("Worker not ready")
    return Promise.resolve({
      badge: null
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
