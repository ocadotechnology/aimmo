import types from './types'

const getConnectionParamsRequest = gameID => (
    {
      type: types.GET_CONNECTION_PARAMS_REQUEST,
      payload: {
        gameID
      }
    }
  )
  
  const getConnectionParamsSuccess = connectionParams => (
    {
      type: types.GET_CONNECTION_PARAMS_SUCCESS,
      payload: {
        connectionParams
      }
    }
  )
  
  const emitUnityEvent = (gameObjectName, unityFunctionName, parameter) => (
    {
      type: types.EMIT_UNITY_EVENT,
      payload: {
        gameObjectName,
        unityFunctionName,
        parameter
      }
    }
  )

  export default {
    getConnectionParamsRequest,
    getConnectionParamsSuccess,
    emitUnityEvent
  }