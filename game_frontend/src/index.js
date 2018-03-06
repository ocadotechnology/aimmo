import React from 'react'
import {render} from 'react-dom'
import 'rxjs'

import { Provider } from 'react-redux'

import GamePage from './containers/GamePage'
import configureStore from './redux/store'

const initialState = {
  movieReducer: {
    movies: []
  }
}
const reduxStore = configureStore(initialState)

const RootJSX = () => (
  <Provider store={reduxStore}>
    <GamePage />
  </Provider>
)

const root = document.getElementById('root')
render(<RootJSX />, root)
