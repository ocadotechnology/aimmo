import { defer } from 'rxjs'

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
`)
}

async function computeNextAction (gameState, avatarState) {
  try {
    return await pyodide.runPythonAsync(`
game_state = ${JSON.stringify(gameState)}
world_map = WorldMapCreator.generate_world_map_from_game_state(game_state)
avatar_state = AvatarState(**${JSON.stringify(avatarState)})
next_turn(world_map, avatar_state).serialise()
`)
  } catch (error) {
    console.warn('python code incorrect')
    console.warn(error)
    return { action_type: 'wait' }
  }
}

export const computeNextAction$ = (gameState, avatarState) =>
  defer(() => computeNextAction(gameState, avatarState))

export async function updateAvatarCode (userCode) {
  await pyodide.runPythonAsync(userCode)
}
