/* eslint-env worker */
import ComputedTurnResult from './computedTurnResult'
// import post from '../redux/api/post';
import { ajax } from 'rxjs/ajax';
import { map } from 'rxjs/operators';

interface TestReport {
  task_id: number
}

export async function checkIfBadgeEarned(
  badges: string,
  result: ComputedTurnResult,
  userCode: string,
  gameState: any,
  currentAvatarID: number
): Promise<string> {
  // const response = post('/', (action) => {
  //   return {
  //     source: { code: userCode },
  //     current_avatar_id: currentAvatarID,
  //     game_state: gameState
  //   };
  // });

  // ajax({
  //   url: 'http://localhost:8080',
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({
  //     source: { code: userCode },
  //     current_avatar_id: currentAvatarID,
  //     game_state: gameState
  //   })
  // })
  //   .pipe(
  //     map((data) => data.response)
  //   )
  //   .subscribe((data) => console.log(data));

  const response = await fetch("http://localhost:8080/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "x-requested-with"
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

  for (var i = 0; i < responseJson.passed.length; i++) {
    const badgeWorksheetPair = `${gameState.worksheetID}:${responseJson.passed[i].task_id}`; // TODO: return in service
    if (!badges.includes(badgeWorksheetPair)) {
      badges += `${badgeWorksheetPair},`
    }
  }

  return badges;
}