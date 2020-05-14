import { runAvatarCode } from './pyodide'

let avatarCode = `
def next_turn(world_state, avatar_state):
    return MoveAction(direction.NORTH)`

describe('runCodeEpic', () => {
  it('returns wait action if not initialised', () => {
    return runAvatarCode(avatarCode, false).then(data => {
      expect(data).toEqual({ action_type: 'wait' })
    })
  })

  it('returns a move action', async () => {
    return runAvatarCode(avatarCode, true).then(data => {
      expect(data).toEqual({ action_type: 'wait' })
    })
  })
})
