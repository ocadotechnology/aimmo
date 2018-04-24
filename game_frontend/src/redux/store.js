import { createStore, applyMiddleware } from 'redux'
import { rootEpic, rootReducer } from './features'
import { createEpicMiddleware } from 'redux-observable'
import { ajax } from 'rxjs/observable/dom/ajax'
import { composeWithDevTools } from 'redux-devtools-extension'

export default function configureStore (initialState) {
  return createStore(
    rootReducer,
    initialState,
    composeWithDevTools(applyMiddleware(
      createEpicMiddleware(rootEpic, {
        dependencies: {
          getJSON: ajax.getJSON,
          post: ajax.post
        }
      })
    ))
  )
}
