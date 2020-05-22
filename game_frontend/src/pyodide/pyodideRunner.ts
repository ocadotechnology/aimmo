import { defer } from 'rxjs'

export async function initializePyodide () {
  await languagePluginLoader
  await pyodide.loadPackage(['micropip'])
  await pyodide.runPythonAsync(`
  import micropip

  micropip.install("http://localhost:8000/static/worker/aimmo_avatar_api-0.0.0-py3-none-any.whl")
  `)

  await pyodide.runPythonAsync(`
from simulation import direction
from simulation import location
from simulation.action import MoveAction, PickupAction, WaitAction
`)
}

async function computeNextAction () {
  try {
    return await pyodide.runPythonAsync('next_turn(None, None).serialise()')
  } catch (error) {
    console.warn('python code incorrect')
    console.warn(error)
    return { action_type: 'wait' }
  }
}

export const computeNextAction$ = () => defer(computeNextAction)

export async function updateAvatarCode (userCode) {
  await pyodide.runPythonAsync(userCode)
}
