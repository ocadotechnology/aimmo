/* eslint-env worker */
import { expose } from 'threads/worker'
import ComputedTurnResult from './computedTurnResult'

function getAvatarStateFromGameState(gameState: any, playerAvatarID: number): object {
  return gameState.players.find(player => player.id === playerAvatarID)
}

async function initializePyodide() {
  self.languagePluginUrl = 'https://pyodide-cdn2.iodide.io/v0.15.0/full/'
  importScripts('https://pyodide-cdn2.iodide.io/v0.15.0/full/pyodide.js')
  await languagePluginLoader
  await pyodide.loadPackage(['micropip'])
  await pyodide.runPythonAsync(`
import micropip

micropip.install("${self.location.origin}/static/worker/aimmo_game_worker-0.0.0-py3-none-any.whl")
  `)

  await pyodide.runPythonAsync(`
from simulation import direction
from simulation import location
from simulation.action import MoveAction, PickupAction, WaitAction, MoveTowardsAction
from simulation.world_map import WorldMapCreator
from simulation.avatar_state import create_avatar_state
from io import StringIO
import contextlib


@contextlib.contextmanager
def capture_output(stdout=None, stderr=None):
  """Temporarily switches stdout and stderr to stringIO objects or variable."""
  old_out = sys.stdout
  old_err = sys.stderr

  if stdout is None:
      stdout = StringIO()
  if stderr is None:
      stderr = StringIO()
  sys.stdout = stdout
  sys.stderr = stderr
  yield stdout, stderr

  sys.stdout = old_out
  sys.stderr = old_err
`)
}

async function computeNextAction(gameState, playerAvatarID): Promise<ComputedTurnResult> {
  const avatarState = getAvatarStateFromGameState(gameState, playerAvatarID)
  try {
    return await pyodide.runPythonAsync(`
game_state = ${JSON.stringify(gameState)}
world_map = WorldMapCreator.generate_world_map_from_game_state(game_state)
avatar_state = create_avatar_state(${JSON.stringify(avatarState)})
serialized_action = {"action_type": "wait"}
with capture_output() as output:
    action = next_turn(world_map, avatar_state)
    if action is None:
        raise Exception("Make sure you are returning an action")
    serialized_action = action.serialise()
stdout, stderr = output
logs = stdout.getvalue() + stderr.getvalue()
{"action": serialized_action, "log": logs, "turnCount": game_state["turnCount"] + 1}
    `)
  } catch (error) {
    return Promise.resolve({
      action: { action_type: 'wait' },
      log: simplifyErrorMessageInLog(error.toString()),
      turnCount: gameState.turnCount + 1
    })
  }
}

export function simplifyErrorMessageInLog(log: string): string {
  const regexToFindNextTurnErrors = /.*line (\d+), in next_turn\n((?:.|\n)*)/
  const matches = log.match(regexToFindNextTurnErrors)
  if (matches?.length >= 2) {
    const simpleError = matches[2].split('\n').slice(-2).join('')
    return `Uh oh! Something isn't correct on line ${matches[1]}. Here's the error we got:\n${simpleError}`
  }
  // error not in next_turn function
  return log
    .split('\n')
    .slice(-2)
    .join('\n')
}

export async function updateAvatarCode(
  userCode: string,
  gameState: any,
  playerAvatarID: number = 0
): Promise<ComputedTurnResult> {
  let turnCount = 0
  if (gameState) {
    turnCount = gameState.turnCount + 1
  }

  try {
    await pyodide.runPythonAsync(userCode)
    if (gameState) {
      return computeNextAction(gameState, playerAvatarID)
    }
    return Promise.resolve({
      action: { action_type: 'wait' },
      log: '',
      turnCount: turnCount
    })
  } catch (error) {
    await setAvatarCodeToWaitActionOnError()
    return Promise.resolve({
      action: { action_type: 'wait' },
      log: simplifyErrorMessageInLog(error.toString()),
      turnCount: turnCount
    })
  }
}

async function setAvatarCodeToWaitActionOnError() {
  await pyodide.runPythonAsync(
    `def next_turn(world_map, avatar_state):
    return WaitAction()`
  )
}

const pyodideWorker = {
  initializePyodide,
  computeNextAction,
  updateAvatarCode
}

export type PyodideWorker = typeof pyodideWorker

expose(pyodideWorker)
