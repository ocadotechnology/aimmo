/* eslint-env jest */
import { simplifyErrorMessageInLog } from './pyodideRunner'

describe('Error formatting', () => {
  it('makes the traceback returned from pyodide more readable', () => {
    const input = `
Error: Traceback (most recent call last):
  File "/lib/python3.7/site-packages/pyodide.py", line 43, in eval_code
    exec(compile(mod, '<exec>', mode='exec'), ns, ns)
  File "<exec>", line 6, in <module>
  File "<exec>", line 3, in next_turn
AttributeError: module 'simulation.direction' has no attribute 'NRTH'`.trim()
    const result = simplifyErrorMessageInLog(input)

    const expected = `
Uh oh! Something isn't correct on line 3. Here's the error we got:
AttributeError: module 'simulation.direction' has no attribute 'NRTH'
`.trim()
    expect(result).toBe(expected)
  })
})
