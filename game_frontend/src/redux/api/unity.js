import { UnityEvent } from 'react-unity-webgl';
import { Observable } from 'rxjs'
import { map, mergeMap, catchError, tap } from 'rxjs/operators'
import { ofType } from 'redux-observable'
import types from '../features/Game/types'
import actions from '../features/Game/types'

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
        throw 'Cannot emit the function!'
      }
    }
  )

export default {
  sendUnityEvent
}
