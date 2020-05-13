declare var languagePluginLoader: Promise<any>
declare var pyodide: any

export async function initialisePyodide () {
  console.log('HELLO!')
  await languagePluginLoader
  await pyodide.loadPackage(['micropip'])
  await pyodide.runPythonAsync(`
  import micropip

  micropip.install('aimmo-avatar-api')
  `)
  console.log('package installed?')
}
