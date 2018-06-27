import { UnityEvent } from 'react-unity-webgl'
import { Observable } from 'rxjs'
import { map, catchError } from 'rxjs/operators'

const sendExternalEvent = communicator => action$ =>
  action$.mergeMap(action =>
    Observable.of(action).pipe(
      communicator,
      map(event => action.payload.successAction),
      catchError(error => Observable.of(action.payload.failAction(error)))
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
  sendExternalEvent,
  emitToUnity
}
