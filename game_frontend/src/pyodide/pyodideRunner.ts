let globals = []
let globalFinder = /^(?!def\s|import\s)[\w\d]+\s*=\s*.*/gm

export async function initialisePyodide () {
  await languagePluginLoader
  await pyodide.loadPackage(['micropip'])
  await pyodide.runPythonAsync(`
  import micropip

  micropip.install('aimmo-avatar-api')
  `)

  await pyodide.runPythonAsync(`
from simulation import direction
from simulation.action import MoveAction
`)
}

export async function runNextTurn (userCode, pyodideInitialised) {
  if (!pyodideInitialised) {
    return { action_type: 'wait' }
  }

  try {
    return await pyodide.runPythonAsync(`next_turn(None, None).serialise()`)
  } catch (error) {
    console.log('python code incorrect')
    console.log(error)
    return { action_type: 'wait' }
  }
}

async function initialiseGlobals (turn_globals) {
  for (const turn_global of turn_globals) {
    if (!globals.includes(turn_global)) {
      await pyodide.runPythonAsync(turn_global)
      globals.push(turn_global)
    }
  }
}

export async function updateAvatarCode (userCode) {
  let turn_globals = userCode.match(globalFinder)
  await initialiseGlobals(turn_globals)

  let globallessCode = userCode.replace(globalFinder, '')
  await pyodide.runPythonAsync(globallessCode)

  return globallessCode
}
