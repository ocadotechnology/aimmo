export async function initialisePyodide () {
  await languagePluginLoader
  await pyodide.loadPackage(['micropip'])
  await pyodide.runPythonAsync(`
  import micropip

  micropip.install('aimmo-avatar-api')
  `)

  await pyodide.runPythonAsync(`
from simulation import direction
from simulation import location
from simulation.action import MoveAction, PickupAction, WaitAction
`)
}

export async function runNextTurn (userCode, pyodideInitialised) {
  if (!pyodideInitialised) {
    return { action_type: 'wait' }
  }

  try {
    return await pyodide.runPythonAsync('next_turn(None, None).serialise()')
  } catch (error) {
    console.log('python code incorrect')
    console.log(error)
    return { action_type: 'wait' }
  }
}

export async function updateAvatarCode (userCode) {
  await pyodide.runPythonAsync(userCode)
}
