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

export { emitUnityEvent }
