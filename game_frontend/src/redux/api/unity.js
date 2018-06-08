import { UnityEvent } from "react-unity-webgl";

const emitUnityEvent = (unityEvent, data) => {
    if(unityEvent.canEmit()) {
        unityEvent.emit(data)
    }
    else {
        throw "Cannot emit the function " + unityEvent + "!"
    }
}


const setGameURL = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetGameURL")

            emitUnityEvent(unityEvent, action.payload.gameURL)
            
            return unityEvent
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

export { 
    emitUnityEvent, 
    setGameURL,
    setGamePath,
    setGamePort,
    setGameSSL,
    establishGameConnection
}
