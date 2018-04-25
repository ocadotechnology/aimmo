import { ajax } from 'rxjs/observable/dom/ajax'
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

export default { getCSRFToken, postOperator }
