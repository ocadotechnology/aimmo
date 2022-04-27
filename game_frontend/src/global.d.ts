declare var OnetrustActiveGroups: string
declare function loadPyodide(): Promise<Pyodide>

interface Pyodide {
  loadPackage(packages: string[]): Promise<void>
  runPythonAsync(pythonCode: string): Promise<any>
}
