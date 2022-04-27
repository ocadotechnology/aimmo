declare var pyodide: Pyodide
declare var OnetrustActiveGroups: string
declare function loadPyodide(any: any): Promise<any>

interface Pyodide {
  loadPackage(packages: string[]): Promise<void>
  runPythonAsync(pythonCode: string): Promise<any>
}
