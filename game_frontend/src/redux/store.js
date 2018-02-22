import { createStore, applyMiddleware } from 'redux'
import { rootEpic, rootReducer } from './features'
import { createEpicMiddleware } from 'redux-observable'

export default function configureStore (initialState) {
  return createStore(
    rootReducer,
    initialState,
    applyMiddleware(
      createEpicMiddleware(rootEpic)
    )
  )
}
