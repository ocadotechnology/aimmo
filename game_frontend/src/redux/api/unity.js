import { UnityEvent } from "react-unity-webgl";


const emitUnityEvent =  action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent(action.payload.gameObjectName, action.payload.unityFunctionName)

            if(unityEvent.canEmit()) {
                unityEvent.emit(action.payload.parameter)
            }
            else {
                throw "Cannot emit the function: " + action.payload.unityFunctionName + "!"
            }
            
            return unityEvent
        }
    )
}

const emitAUnityEvent = (unityEvent, data) => {
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

            emitAUnityEvent(unityEvent, action.payload.gameURL)
            
            return unityEvent
        }
    )
}

const setGamePath = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetGamePath")

            emitAUnityEvent(unityEvent, action.payload.gamePath)
            
            return unityEvent
        }
    )
}

const setGamePort = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetGamePort")

            emitAUnityEvent(unityEvent, action.payload.gamePort)
            
            return unityEvent
        }
    )
}

const setGameSSL = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "SetSSL")

            emitAUnityEvent(unityEvent, action.payload.gameSSLFlag)
            
            return unityEvent
        }
    )
}

const establishGameConnection = action$ => {
    return action$.map(
        action => {
            let unityEvent = new UnityEvent("World Controller", "EstablishConnection")

            emitAUnityEvent(unityEvent, "OK")
            
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
