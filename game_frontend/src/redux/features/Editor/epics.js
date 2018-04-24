import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, catchError } from 'rxjs/operators'
import { ofType } from 'redux-observable'
import { getCSRFToken, postOperator } from './api'

const getCodeEpic = (action$, store, { getJSON }) =>
  action$.ofType(types.GET_CODE_REQUEST)
    .mergeMap(action =>
      getJSON(`/players/api/code/${store.getState().game.id}/`, {withCredentials: true})
        .map(response => actions.getCodeReceived(response.code))
        .catch(error => Observable.of({
          type: types.GET_CODE_FAILURE,
          payload: error.xhr.response,
          error: true
        }))
    )

const postCodeEpic = (action$, store, { post, getJSON }) => {
  return action$
    .pipe(
      ofType(types.POST_CODE_REQUEST),
      getCSRFToken(getJSON),
      postOperator(
        `/players/api/code/${store.getState().game.id}/`,
        { code: store.getState().editor.code },
        post
      ),
      map(response => actions.postCodeReceived()),
      catchError(error => Observable.of({
        type: types.POST_CODE_FAILURE,
        payload: error.xhr.response,
        error: true
      })
      )
    )
}

export default { getCodeEpic, postCodeEpic }
