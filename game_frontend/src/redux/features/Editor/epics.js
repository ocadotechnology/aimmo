import actions from './actions'
import types from './types'

const getCodeEpic = (action$, store, { getJSON }) =>
  action$.ofType(types.GET_CODE_REQUEST)
    .mergeMap(action =>
      getJSON(`api/code/${action.payload.gameID}`)
        .map(response => actions.getCodeReceived(response))
    )

export default getCodeEpic
