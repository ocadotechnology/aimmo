import { ajax } from 'rxjs/observable/dom/ajax'
import { pipe } from 'rxjs/Rx'
import api from '../api'

const getCSRFToken = action$ => {
  return action$.mergeMap(action =>
    api.get('csrf_token')
      .map(response => response.csrfToken)
  )
}

const postOperator = (url, body) => csrfToken$ => {
  return csrfToken$.mergeMap(csrfToken => {
    return ajax.post(url, body, {
      withCredentials: true,
      'X-CSRFToken': csrfToken
    })
  })
}

const post = (url, body) => (
  pipe(
    getCSRFToken,
    postOperator(url, body)
  )
)

export default post
