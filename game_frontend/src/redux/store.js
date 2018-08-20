import { createStore, applyMiddleware } from 'redux'
import { rootEpic, rootReducer } from './features'
import { createEpicMiddleware } from 'redux-observable'
import api from './api'
import { composeWithDevTools } from 'redux-devtools-extension/logOnlyInProduction'

export default function configureStore (initialState) {
  const epicMiddleware = createEpicMiddleware({
    dependencies: {
      api
    }
  })
  const store = createStore(rootReducer, initialState,
    composeWithDevTools(applyMiddleware(epicMiddleware))
  )
  epicMiddleware.run(rootEpic)
  return store
}
