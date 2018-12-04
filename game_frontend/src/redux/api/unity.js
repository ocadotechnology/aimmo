import { of } from 'rxjs'
import { map, catchError, mergeMap } from 'rxjs/operators'
import { UnityContent } from 'react-unity-webgl'

const unityContent = new UnityContent(
  '/static/unity/Build/unity.json',
  '/static/unity/Build/UnityLoader.js', {
    adjustOnWindowResize: true
  }
)

const sendExternalEvent = communicator => action$ =>
  action$.pipe(
    mergeMap(action =>
      of(action).pipe(
        communicator,
        map(event => action.payload.successAction),
        catchError(error => of(action.payload.failAction(error)))
      )
    )
  )

const emitToUnity = action$ =>
  action$.pipe(
    map(
      action => {
        unityContent.send('World Controller', action.payload.unityEvent, action.payload.unityData)
      }
    )
  )

export { unityContent }

export default {
  sendExternalEvent,
  emitToUnity
}
