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
    // get only the exception message line, removing potential traceback
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
    let userPythonCode = userCode.replace(/\s*#.*/gm, "") // Remove all comment lines from the user's code
    if (gameState) {
      computeNextAction(gameState, playerAvatarID).then(result => {
        checkIfBadgeEarned(result, userPythonCode, gameState, playerAvatarID)
        return result
      })
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

//TODO: There is no check at the moment of which worksheet this is for. This will run for all worksheets at the minute.
function checkIfBadgeEarned(result: any, userPythonCode: string, gameState: any, playerAvatarId: number) {
  //TODO: The badge data needs to be stored somewhere else, and the check on whether it has been earned needs to be done from the database.
  let badges = [
    {id: 1, trigger: badge1Trigger(result), earned: false},
    {id: 2, trigger: badge2Trigger(userPythonCode), earned: false},
    {id: 3, trigger: badge3Trigger(result, userPythonCode, gameState, playerAvatarId), earned: false},
  ]

  for (let badge of badges) {
    if (!badge.earned && badge.trigger) {
      badge.earned = true //TODO: Needs to be connected to the DB / User object (so probably needs to be done in the game not the frontend)
      result.badge = badge //TODO: This adds a "badge" property to the turn result, the interface needs to be updated maybe to reflect it
      console.log("You've earned a new badge!") //TODO: This is where the frontend could show the banner and badge image maybe
      break
    }
    else {
      result.badge = null
    }
  }
}

function badge1Trigger(result: any): boolean {
  // Check the code returns a move action other than NORTH
  return result.action.action_type === "move" && JSON.stringify(result.action.options.direction) != JSON.stringify({x: 0, y: 1})
}

function badge2Trigger(userPythonCode: string): boolean {
  // Check code contains keywords
  const substrings = ["import random", "randint(", "direction.NORTH", "direction.EAST", "direction.SOUTH", "direction.WEST", "if ", "elif ", "else:"]
  return substrings.every(substring =>
    userPythonCode.includes(substring)
  )
}

function badge3Trigger(result: any, userPythonCode: string, gameState: any, playerAvatarId: number): boolean {
  // Check code contains keywords
  const substrings = ["world_state.can_move_to(", "print(", "if ", ]
  let codeContainsKeywords = substrings.every((substring) =>
    userPythonCode.includes(substring)
  )

  // Check action is move action
  let isMoveAction = result.action.action_type === "move"

  // Check next cell is available to move onto
  let moveDirection = result.action.options.direction
  let avatarLocation = null

  for (let player of gameState.players) {
    if (player.id == playerAvatarId) {
      avatarLocation = player.location
    }
  }

  let nextCellLocation = {x: avatarLocation.x + moveDirection.x, y: avatarLocation.y + moveDirection.y}
  let isNextCellFree = true
  let isNextCellInMap = nextCellLocation.x <= 15 && nextCellLocation.x >= -15 && nextCellLocation.y <= 15 && nextCellLocation.y >= -15

  if (isNextCellInMap) {
    let obstacles = gameState.obstacles

    for (let obstacle of obstacles) {
      let obstacleLocation = obstacle.location
      if (JSON.stringify(obstacleLocation) == JSON.stringify(nextCellLocation)) {
        isNextCellFree = false
      }
    }
  }
  else {
    isNextCellFree = false
  }

  return codeContainsKeywords && isMoveAction && isNextCellFree
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
