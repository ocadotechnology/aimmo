/* eslint-env worker */
import ComputedTurnResult from './computedTurnResult'

export function checkIfBadgeEarned(
  badges: string,
  result: ComputedTurnResult,
  userCode: string,
  gameState: any
): string {
  const userPythonCode = userCode.replace(/\s*#.*/gm, '') // Remove all comment lines from the user's code
  const badgesPerWorksheet = [
    { id: 1, worksheetID: 1, trigger: badge1Trigger(result) },
    { id: 2, worksheetID: 1, trigger: badge2Trigger(result, userPythonCode) },
    {
      id: 3,
      worksheetID: 1,
      trigger: badge3Trigger(result, userPythonCode),
    },
  ]

  for (const badge of badgesPerWorksheet) {
    const badgeWorksheetPair = `${badge.worksheetID}:${badge.id}`
    if (
      !badges.includes(badgeWorksheetPair) &&
      badge.worksheetID === gameState.worksheetID &&
      badge.trigger
    ) {
      // Here is when a new badge is earned
      // TODO on worksheet 2: This might have to order the badges, in case user does not do the worksheet in order
      badges += `${badgeWorksheetPair},`
    }
  }
  return badges
}

function badge1Trigger(result: any): boolean {
  // Check the code returns a move action other than NORTH
  return (
    result.action.action_type === 'move' &&
    JSON.stringify(result.action.options.direction) !== JSON.stringify({ x: 0, y: 1 })
  )
}

function badge2Trigger(result: any, userPythonCode: string): boolean {
  // Check code contains keywords to move in random directions
  const substrings = [
    'import random',
    'randint(',
    'direction.NORTH',
    'direction.EAST',
    'direction.SOUTH',
    'direction.WEST',
    'if ',
    'elif ',
    'else:',
  ]
  // Check the code contains certain keywords about moving in a random direction
  const codeContainsKeywords = substrings.every((substring) => userPythonCode.includes(substring))

  // And check it returns a move action
  return result.action.action_type === 'move' && codeContainsKeywords
}

function badge3Trigger(result: any, userPythonCode: string): boolean {
  // Check the code contains certain keywords about moving to a cell
  const substrings = ['world_state.can_move_to(', 'print(', 'if ']
  const codeContainsKeywords = substrings.every((substring) => userPythonCode.includes(substring))

  // And check it returns a move action
  return result.action.action_type === 'move' && codeContainsKeywords
}
