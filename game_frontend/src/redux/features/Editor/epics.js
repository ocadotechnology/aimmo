import actions from './actions'
import types from './types'
import { Observable } from 'rxjs'

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

export default getCodeEpic
