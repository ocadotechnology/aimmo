import { ajax } from 'rxjs/ajax'
import { pipe } from 'rxjs'
import { mergeMap, map } from 'rxjs/operators'
import Cookies from 'js-cookie'

const getCSRFToken = action$ =>
  action$.pipe(
    map(action => {
      return { csrfToken: Cookies.get('csrftoken'), action }
    })
  )

const postOperator = (url, body) => actionWithCsrfToken$ =>
  actionWithCsrfToken$.pipe(
    mergeMap(({ csrfToken, action }) =>
      ajax.post(url, body(action), {
        withCredentials: true,
        'X-CSRFToken': csrfToken
      })
    )
  )

const post = (url, body) => pipe(getCSRFToken, postOperator(url, body))

export default post
