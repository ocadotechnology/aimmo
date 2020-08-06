import { defer } from 'rxjs'
import { spawn, Worker, ModuleThread } from 'threads'
import ComputedTurnResult from './computedTurnResult'
import { PyodideWorker } from './webWorker'

let worker: ModuleThread<PyodideWorker>

export async function initializePyodide () {
  worker = await spawn<PyodideWorker>(new Worker('./webWorker.ts'))
  await worker.initializePyodide()
}

export async function updateAvatarCode (
  userCode: string,
  gameState: any,
  playerAvatarID: number = 0
): Promise<ComputedTurnResult> {
  return worker.updateAvatarCode(userCode, gameState, playerAvatarID)
}

export const computeNextAction$ = (gameState: object, avatarState: object) =>
  defer(() => worker.computeNextAction(gameState, avatarState))
