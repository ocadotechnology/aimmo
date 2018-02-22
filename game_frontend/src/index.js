import React from 'react'
import {render} from 'react-dom'
import 'rxjs'

import { Provider as ReduxProvider } from 'react-redux'

import GamePage from './containers/GamePage'
import configureStore from './redux/store'

const initialState = {
  movieReducer: {
    movies: []
  }
}
const reduxStore = configureStore(initialState)

const RootJSX = () => (
  <ReduxProvider store={reduxStore}>
    <GamePage />
  </ReduxProvider>
)

const root = document.getElementById('root')
render(<RootJSX />, root)
