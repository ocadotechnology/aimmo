import { ajax } from 'rxjs/ajax'
import { pipe } from 'rxjs'
import { mergeMap } from 'rxjs/operators'
import api from '../api'

const getCSRFToken = action$ =>
  action$.pipe(
    mergeMap(action =>
      api.get('csrf_token')
        .map(response => response.csrfToken)
    )
  )

const postOperator = (url, body) => csrfToken$ =>
  csrfToken$.pipe(
    mergeMap(csrfToken =>
      ajax.post(url, body(), {
        withCredentials: true,
        'X-CSRFToken': csrfToken
      })
    )
  )

const post = (url, body) =>
  pipe(
    getCSRFToken,
    postOperator(url, body)
  )

export default post
