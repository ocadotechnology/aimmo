import { UnityEvent } from 'react-unity-webgl'
import { of } from 'rxjs'
import { map, catchError, mergeMap } from 'rxjs/operators'

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
        let unityEvent = new UnityEvent('World Controller', action.payload.unityEvent)

        if (unityEvent.canEmit()) {
          unityEvent.emit(action.payload.unityData)
        } else {
          throw new Error('Cannot emit the function!')
        }
      }
    )
  )

export default {
  sendExternalEvent,
  emitToUnity
}
