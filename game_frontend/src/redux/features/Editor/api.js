const getCSRFToken = getJSON => action$ => {
  return action$.mergeMap(action =>
    getJSON('/players/api/csrf_token', { withCredentials: true })
      .map(response => response.csrfToken)
  )
}

const postOperator = (url, body, post) => csrfToken$ => {
  return csrfToken$.mergeMap(csrfToken => {
    return post(url, body, {
      withCredentials: true,
      'X-CSRFToken': csrfToken
    })
  })
}

export { getCSRFToken, postOperator }
