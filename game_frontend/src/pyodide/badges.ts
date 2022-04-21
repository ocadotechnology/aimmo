/* eslint-env worker */
// TODO: There is no check at the moment of which worksheet this is for. This will run for all worksheets at the minute.
import BadgeResult from "./badgeResult";

export async function checkIfBadgeEarned(result: any, userCode: string, gameState: any, playerAvatarId: number): Promise<BadgeResult> {
  // TODO: The badge data needs to be stored somewhere else, and the check on whether it has been earned needs to be done from the database.
  console.log("Starting badge check now")
  const userPythonCode = userCode.replace(/\s*#.*/gm, "") // Remove all comment lines from the user's code
  const badgesPerWorksheet = [
    [
      {id: 1, trigger: badge1Trigger(result), earned: false},
      {id: 2, trigger: badge2Trigger(userPythonCode), earned: false},
      {id: 3, trigger: badge3Trigger(result, userPythonCode, gameState, playerAvatarId), earned: false},
    ],
    [],
    [],
  ]

  const worksheetBadges = badgesPerWorksheet[gameState.worksheetID-1]

  for (const badge of worksheetBadges) {
    if (!badge.earned && badge.trigger) {
      badge.earned = true // TODO: Needs to be connected to the DB / User object (so probably needs to be done in the game not the frontend)
      console.log("You've earned a new badge!") // TODO: This is where the frontend could show the banner and badge image maybe
      return Promise.resolve({badge: `${gameState.worksheetID},${badge.id}`})
    }
  }
  return Promise.resolve({badge: null})
}

function badge1Trigger(result: any): boolean {
  // Check the code returns a move action other than NORTH
  return result.action.action_type === "move" && JSON.stringify(result.action.options.direction) !== JSON.stringify({x: 0, y: 1})
}

function badge2Trigger(userPythonCode: string): boolean {
  // Check code contains keywords
  const substrings = ["import random", "randint(", "direction.NORTH", "direction.EAST", "direction.SOUTH", "direction.WEST", "if ", "elif ", "else:"]
  return substrings.every(substring =>
    userPythonCode.includes(substring)
  )
}

function badge3Trigger(result: any, userPythonCode: string, gameState: any, playerAvatarId: number): boolean {
  // Check code contains keywords
  const substrings = ["world_state.can_move_to(", "print(", "if ", ]
  const codeContainsKeywords = substrings.every((substring) =>
    userPythonCode.includes(substring)
  )

  // Check action is move action
  const isMoveAction = result.action.action_type === "move"

  // Check next cell is available to move onto
  const moveDirection = result.action.options.direction
  let avatarLocation = null

  for (const player of gameState.players) {
    if (player.id === playerAvatarId) {
      avatarLocation = player.location
    }
  }

  const nextCellLocation = {x: avatarLocation.x + moveDirection.x, y: avatarLocation.y + moveDirection.y}
  let isNextCellFree = true
  const isNextCellInMap = nextCellLocation.x <= 15 && nextCellLocation.x >= -15 && nextCellLocation.y <= 15 && nextCellLocation.y >= -15

  if (isNextCellInMap) {
    const obstacles = gameState.obstacles

    for (const obstacle of obstacles) {
      const obstacleLocation = obstacle.location
      if (JSON.stringify(obstacleLocation) === JSON.stringify(nextCellLocation)) {
        isNextCellFree = false
      }
    }
  }
  else {
    isNextCellFree = false
  }

  return codeContainsKeywords && isMoveAction && isNextCellFree
}
