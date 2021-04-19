declare var pyodide: Pyodide
declare var languagePluginLoader: Promise<void>
declare var OnetrustActiveGroups: string

interface Pyodide {
  loadPackage(packages: string[]): Promise<void>
  runPythonAsync(pythonCode: string): Promise<any>
}
