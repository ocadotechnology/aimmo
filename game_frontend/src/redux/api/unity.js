import { UnityEvent } from "react-unity-webgl";
import { Observable } from 'rxjs'
import { map, mergeMap, catchError, tap } from 'rxjs/operators'
import { ofType } from 'redux-observable'
import types from '../features/Game/types'
import actions from '../features/Game/types'

const sendUnityEvent = action$ => {
    return action$.mergeMap(action =>
        Observable.of(action).pipe(
            emitUnityEvent,
            map(event => ({ type: types.SET_GAME_URL_SUCCESS })),
            catchError(error => Observable.of({
                type: types.SET_GAME_URL_FAIL,
                error: true
            })
            )
        )
        )
}


const emitUnityEvent = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", action.payload.unityEvent)

            if(unityEvent.canEmit()) {
                unityEvent.emit(action.payload.unityData)
            }
            else {
                throw "Cannot emit the function!" 
            }
        }
    )
}

const setGamePath = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetGamePath")

            emitUnityEvent(unityEvent, action.payload.gamePath)
            
            return unityEvent
        }
    )
}

const setGamePort = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetGamePort")

            emitUnityEvent(unityEvent, action.payload.gamePort)
            
            return unityEvent
        }
    )
}

const setGameSSL = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetSSL")

            emitUnityEvent(unityEvent, action.payload.gameSSLFlag)
            
            return unityEvent
        }
    )
}

const establishGameConnection = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "EstablishConnection")

            emitUnityEvent(unityEvent, "OK")
            
            return unityEvent
        }
    )
}

export default { 
    emitUnityEvent,
    sendUnityEvent,
    setGamePath,
    setGamePort,
    setGameSSL,
    establishGameConnection
}
