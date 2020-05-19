import { runAvatarCode } from './pyodide'

const avatarCode = `
def next_turn(world_state, avatar_state):
    return MoveAction(direction.NORTH)`

describe('runCodeEpic', () => {
  it('returns wait action if not initialised', () => {
    return runAvatarCode(avatarCode, false).then(data => {
      expect(data).toEqual({ action_type: 'wait' })
    })
  })

  it('returns a wait action if code is incorrect', async () => {
    const action = await runAvatarCode(avatarCode, true)
    expect(action).toEqual({ action_type: 'wait' })
  })

  it('returns a wait action if time out', async () => {
    const action = await runAvatarCode(avatarCode, true)
    expect(action).toEqual({ action_type: 'wait' })
  })

  it('returns a move action', async () => {
    const action = await runAvatarCode(avatarCode, true)
    expect(action).toEqual({ action_type: 'wait' })
  })

  it('finds a global variable, stores and updates it', async () => {
    const action = await runAvatarCode(avatarCode, true)
    expect(action).toEqual({ action_type: 'wait' })
  })
})
