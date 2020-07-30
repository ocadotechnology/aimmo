/* eslint-env worker */
self.languagePluginUrl = 'https://pyodide-cdn2.iodide.io/v0.15.0/full/'
importScripts('https://pyodide-cdn2.iodide.io/v0.15.0/full/pyodide.js')

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

// eslint-disable-next-line no-unused-vars
var onmessage = function (e) {
  languagePluginLoader.then(() => {
    const data = e.data
    const keys = Object.keys(data)
    for (const key of keys) {
      if (key !== 'python') {
        // Keys other than python must be arguments for the python script.
        // Set them on self, so that `from js import key` works.
        self[key] = data[key]
      }
    }

    self.pyodide
      .runPythonAsync(data.python, () => {})
      .then(results => {
        self.postMessage({ results })
      })
      .catch(err => {
        // if you prefer messages with the error
        self.postMessage({ error: err.message })
        // if you prefer onerror events
        // setTimeout(() => { throw err; });
      })
  })
}
