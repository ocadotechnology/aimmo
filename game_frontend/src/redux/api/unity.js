import { UnityEvent } from 'react-unity-webgl'
import { Observable } from 'rxjs'
import { map, catchError } from 'rxjs/operators'

const sendUnityEvent = action$ =>
  action$.mergeMap(action =>
    Observable.of(action).pipe(
      emitToUnity,
      map(event => action.payload.successAction),
      catchError(error => Observable.of(action.payload.failAction))
    )
  )

const emitToUnity = action$ =>
  action$.map(
    action => {
      let unityEvent = new UnityEvent('World Controller', action.payload.unityEvent)

      if (unityEvent.canEmit()) {
        unityEvent.emit(action.payload.unityData)
      } else {
        throw new Error('Cannot emit the function!')
      }
    }
  )

export default {
  sendUnityEvent
}
