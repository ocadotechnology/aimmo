/* eslint-env worker */
import ComputedTurnResult from "./computedTurnResult";

export function checkIfBadgeEarned(badges: string, result: ComputedTurnResult, userCode: string, gameState: any, playerAvatarId: number): string {
  console.log("Starting badge check now")
  console.log(badges)
  console.log(typeof badges)
  const userPythonCode = userCode.replace(/\s*#.*/gm, "") // Remove all comment lines from the user's code
  const badgesPerWorksheet = [
    {id: 1, worksheetID: 1, trigger: badge1Trigger(result)},
    {id: 2, worksheetID: 1, trigger: badge2Trigger(userPythonCode)},
    {id: 3, worksheetID: 1, trigger: badge3Trigger(result, userPythonCode, gameState, playerAvatarId)},
  ]

  for (const badge of badgesPerWorksheet) {
    if (!badges.includes(badge.id.toString()) && badge.worksheetID === gameState.worksheetID && badge.trigger) {
      console.log("You've earned a new badge!") // TODO: This is where the frontend could show the banner and badge image maybe
      badges += `${badge.id},`
    }
  }
  return badges
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

  if (!codeContainsKeywords) return false

  // Check action is move action
  const isMoveAction = result.action.action_type === "move"

  if (!isMoveAction) return false

  // Check next cell is available to move onto
  const moveDirection = result.action.options.direction
  let avatarLocation = null

  for (const player of gameState.players) {
    if (player.id === playerAvatarId) {
      avatarLocation = player.location
    }
  }

  const nextCellLocation = {x: avatarLocation.x + moveDirection.x, y: avatarLocation.y + moveDirection.y}
  const isNextCellInMap = nextCellLocation.x <= 15 && nextCellLocation.x >= -15 && nextCellLocation.y <= 15 && nextCellLocation.y >= -15

  if (isNextCellInMap) {
    const obstacles = gameState.obstacles

    for (const obstacle of obstacles) {
      const obstacleLocation = obstacle.location
      if (JSON.stringify(obstacleLocation) === JSON.stringify(nextCellLocation)) {
        return true
      }
    }
  }
  else {
    return false
  }
}
