import { ajax } from 'rxjs/observable/dom/ajax'
import { pipe } from 'rxjs/Rx'
import api from '../api'

const getCSRFToken = action$ =>
  action$.mergeMap(action =>
    api.get('csrf_token')
      .map(response => response.csrfToken)
  )

const postOperator = (url, body) => csrfToken$ =>
  csrfToken$.mergeMap(csrfToken =>
    ajax.post(url, body(), {
      withCredentials: true,
      'X-CSRFToken': csrfToken
    })
  )

const post = (url, body) =>
  pipe(
    getCSRFToken,
    postOperator(url, body)
  )

export default post
