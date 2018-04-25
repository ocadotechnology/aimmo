import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'
import { map, catchError } from 'rxjs/operators'
import { ofType } from 'redux-observable'

const getCodeEpic = (action$, store, { api }) =>
  action$.ofType(types.GET_CODE_REQUEST)
    .mergeMap(action =>
      api.get(`code/${store.getState().game.id}/`)
        .map(response => actions.getCodeReceived(response.code))
        .catch(error => Observable.of({
          type: types.GET_CODE_FAILURE,
          payload: error.xhr.response,
          error: true
        }))
    )

const postCodeEpic = (action$, store, { api }) => {
  return action$
    .pipe(
      ofType(types.POST_CODE_REQUEST),
      api.post(
        `/players/api/code/${store.getState().game.id}/`,
        { code: store.getState().editor.code }
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
