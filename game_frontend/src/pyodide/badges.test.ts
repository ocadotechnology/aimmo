/* eslint-env jest */
import { checkIfBadgeEarned } from './badges'
jest.mock('threads/worker')

describe('Badges check', () => {
  it('awards badge 1 if the right conditions are met', () => {
    const badges = ''
    const turnResult = {
      action: {
        action_type: "move",
        options: {
          direction: {x: 0, y: -1}
        }
      },
      log: "",
      turnCount: 1,
    }
    const userCode = ''
    const gameState = {worksheetID: 1}
    const playerAvatarId = 1

    const result = checkIfBadgeEarned(badges, turnResult, userCode, gameState, playerAvatarId)

    const expected = "1:1,"

    expect(result).toBe(expected)
  })

  it('awards badges 1 and 2 if the right conditions are met', () => {
    const badges = ''
    const turnResult = {
      action: {
        action_type: "move",
        options: {
          direction: {x: 0, y: -1}
        }
      },
      log: "",
      turnCount: 1,
    }
    const userCode = `
import random

def next_turn(world_state, avatar_state):
    number = random.randint(1,4)
    if number == 1:
        new_dir = direction.NORTH
    elif number == 2:
        new_dir = direction.EAST
    elif number == 3:
        new_dir = direction.SOUTH
    else:
        new_dir = direction.WEST

    action = MoveAction(new_dir)
    
    return action
`
    const gameState = {worksheetID: 1}
    const playerAvatarId = 1

    const result = checkIfBadgeEarned(badges, turnResult, userCode, gameState, playerAvatarId)

    const expected = "1:1,1:2,"

    expect(result).toBe(expected)
  })

  it('awards badges 1, 2 and 3 if the right conditions are met', () => {
    const badges = ''
    const turnResult = {
      action: {
        action_type: "move",
        options: {
          direction: {x: 0, y: -1}
        }
      },
      log: "",
      turnCount: 1,
    }
    const userCode = `
import random 

def next_turn(world_state, avatar_state):
    number = random.randint(1,4)
    if number == 1:
        new_dir = direction.NORTH
    elif number == 2:
        new_dir = direction.EAST
    elif number == 3:
        new_dir = direction.SOUTH
    else:
        new_dir = direction.WEST
    
    next_location = avatar_state.location + new_dir 
    print("The co-ordinates of the next cell are", next_location)
    if world_state.can_move_to(next_location):
        print("Yes, I can move")
    else:
        print("I can't move there!")
    
    action = MoveAction(new_dir)
    
    return action
`
    const gameState = {
      worksheetID: 1,
      players: [
        {
          id: 1,
          location: {x: 10, y: 10}
        }
      ],
      obstacles: [],
    }
    const playerAvatarId = 1

    const result = checkIfBadgeEarned(badges, turnResult, userCode, gameState, playerAvatarId)

    const expected = "1:1,1:2,1:3,"

    expect(result).toBe(expected)
  })
})