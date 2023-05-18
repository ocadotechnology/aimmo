/* eslint-env worker */
import ComputedTurnResult from './computedTurnResult'

interface TestReport {
  task_id: number // eslint-disable-line
}

export async function checkIfBadgeEarned(
  badges: string,
  result: ComputedTurnResult,
  userCode: string,
  gameState: any,
  currentAvatarID: number
): Promise<string> {
  const response = await fetch("https://kurono-badges-dot-decent-digit-629.appspot.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      source: { code: userCode },
      current_avatar_id: currentAvatarID,
      game_state: gameState
    })
  });

  const responseJson: {
    passed: TestReport[]
    failed: TestReport[]
    xfailed: TestReport[]
    skipped: TestReport[]
  } = await response.json();

  for (let i = 0; i < responseJson.passed.length; i++) {
    const badgeWorksheetPair = `${gameState.worksheetID}:${responseJson.passed[i].task_id}`;
    if (!badges.includes(badgeWorksheetPair)) {
      badges += `${badgeWorksheetPair},`
    }
  }

  return badges;
}
