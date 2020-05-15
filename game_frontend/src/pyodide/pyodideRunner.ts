let avatarCode = `
turns = 0
def next_turn(world_state, avatar_state):
    global turns
    turns = turns + 1
    print("I've had", turns, "turn(s)")
    return MoveAction(direction.NORTH)`

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

export async function runAvatarCode (userCode, pyodideInitialised) {
  if (!pyodideInitialised) {
    return { action_type: 'wait' }
  }
  let turn_globals = avatarCode.match(globalFinder)
  await initialiseGlobals(turn_globals)

  let globallessCode = avatarCode.replace(globalFinder, '')

  try {
    return Promise.race([
      new Promise((resolve, reject) =>
        setTimeout(() => {
          console.log('I got timed out')
          resolve({ action_type: 'wait' })
        }, 2000)
      ),
      await runTheCode(globallessCode)
    ])
  } catch (error) {
    console.log('python code incorrect')
    console.log(error)
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

async function runTheCode (userCode) {
  return pyodide.runPythonAsync(`
${userCode}

next_turn(None, None).serialise()
`)
}
