/* eslint-env jest */
import { computeNextAction, simplifyErrorMessageInLog } from './webWorker'
jest.mock('threads/worker')

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

describe('pyodide webWorker', () => {
  it('returns wait action if game is paused', async () => {
    expect.assertions(1);
    const isGamePaused = true
    const playerAvatarID = 1
    const turnCount = 5
    const gameState = {
      "players": [
        {
          "location": {
            "x": -13,
            "y": 13
          },
          "id": 1,
          "orientation": "north"
        },
        {
          "location": {
            "x": 6,
            "y": 10
          },
          "id": 2,
          "orientation": "north"
        }
      ],
      "turnCount": turnCount,
    }

    const expected = {
      action: {
        action_type: "wait",
      },
      log: '',
      turnCount: turnCount + 1,
    }

    return expect(computeNextAction(gameState, playerAvatarID, isGamePaused)).resolves.toEqual(expected);
  })
})
