let avatarCode = `
def next_turn(world_state, avatar_state):
    return MoveAction(direction.NORTH)`

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
  if (avatarCode.includes('import')) {
    console.log('Import cannot be used')
    return { action_type: 'wait' }
  }

  try {
    return Promise.race([
      new Promise((resolve, reject) =>
        setTimeout(() => {
          console.log('I got timed out')
          resolve({ action_type: 'wait' })
        }, 2000)
      ),
      await runTheCode(avatarCode),
    ])
  } catch (error) {
    console.log('python code incorrect')
    console.log(error)
  }
}

async function runTheCode (userCode) {
  return pyodide.runPythonAsync(`
${userCode}

next_turn(None, None).serialise()
`)
}
