import { createStore, applyMiddleware } from 'redux'
import { rootEpic, rootReducer } from './features'
import { createEpicMiddleware } from 'redux-observable'
import api from './api'
import { composeWithDevTools } from 'redux-devtools-extension/logOnlyInProduction'

export default function configureStore (initialState) {
  return createStore(
    rootReducer,
    initialState,
    composeWithDevTools(applyMiddleware(
      createEpicMiddleware(rootEpic, {
        dependencies: {
          api
        }
      })
    ))
  )
}
