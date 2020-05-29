import { defer } from 'rxjs'

interface ComputedTurnResult {
  action: object
  log: string
  turnCount: number
}

export async function initializePyodide () {
  await languagePluginLoader
  await pyodide.loadPackage(['micropip'])
  await pyodide.runPythonAsync(`
  import micropip

  micropip.install("${window.location.origin}/static/worker/aimmo_avatar_api-0.0.0-py3-none-any.whl")
  `)

  await pyodide.runPythonAsync(`
from simulation import direction
from simulation import location
from simulation.action import MoveAction, PickupAction, WaitAction
from simulation.world_map import WorldMapCreator
from simulation.avatar_state import AvatarState
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

async function computeNextAction (gameState, avatarState): Promise<ComputedTurnResult> {
  try {
    // return Promise.resolve({ action: { action_type: 'wait' }, log: '', turnNumber: 0 })
    return await pyodide.runPythonAsync(`
game_state = ${JSON.stringify(gameState)}
world_map = WorldMapCreator.generate_world_map_from_game_state(game_state)
avatar_state = AvatarState(**${JSON.stringify(avatarState)})
with capture_output() as output:
    action = next_turn(world_map, avatar_state)
    if action is None:
      raise Exception("Make sure you are returning an action")
    action.serialise()
stdout, stderr = output
logs = stdout.getvalue() + stderr.getvalue()
{"action": action, "log": logs, "turnCount": game_state["turnCount"]}
    `)
  } catch (error) {
    return Promise.resolve({
      action: { action_type: 'wait' },
      log: simplifyErrorMessageInLog(error.toString()),
      turnCount: gameState.turnCount + 1
    })
  }
}

export function simplifyErrorMessageInLog (log: string): string {
  const regexToFindNextTurnErrors = /.*line (\d+), in next_turn\n((?:.|\n)*)/
  const matches = log.match(regexToFindNextTurnErrors)
  if (matches?.length >= 2) {
    return `Uh oh! Something isn't correct on line ${matches[1]}. Here's the error we got:\n${matches[2]}`
  }
  return log
    .split('\n')
    .slice(-2)
    .join('\n')
}

export const computeNextAction$ = (gameState: object, avatarState: object) =>
  defer(() => computeNextAction(gameState, avatarState))

export async function updateAvatarCode (
  userCode: string,
  turnCount: number
): Promise<ComputedTurnResult> {
  try {
    return await pyodide.runPythonAsync(userCode)
  } catch (error) {
    return Promise.resolve({
      action: { action_type: 'wait' },
      log: simplifyErrorMessageInLog(error.toString()),
      turnCount: turnCount + 1
    })
  }
  //   const regex = /^(?!\s*$)/gm
  //   const indentedUserCode = userCode.replace(regex, ' '.repeat(4))
  //   const logs = await pyodide.runPythonAsync(`
  // with capture_output() as output:
  // ${indentedUserCode}

  // stdout, stderr = output
  // output_log = stdout.getvalue()
  // error_log = stderr.getvalue()
  // {"output": output_log, "error": error_log}
  //   `)

  //   console.log(logs)
}
