/* eslint-env worker */
import ComputedTurnResult from './computedTurnResult'
import fetch from 'node-fetch'

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
  // TODO: fix loading of environment variables. 
  let serviceUrl = process.env.REACT_APP_KURONO_BADGES_URL;
  if (serviceUrl === undefined) {
    serviceUrl = "https://production-kurono-badges-dot-decent-digit-629.appspot.com"
  }

  const response = await fetch(serviceUrl, {
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
