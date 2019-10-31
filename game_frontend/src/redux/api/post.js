import { ajax } from 'rxjs/ajax'
import { pipe } from 'rxjs'
import { mergeMap, map } from 'rxjs/operators'
import Cookies from 'js-cookie'

const getCSRFToken = action$ =>
  action$.pipe(
    map(action =>
      Cookies.get('csrftoken')
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
