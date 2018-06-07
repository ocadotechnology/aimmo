import React from 'react'
import {render} from 'react-dom'
import 'rxjs'

import { Provider } from 'react-redux'

import GamePage from './components/GamePage'
import configureStore from './redux/store'

const initialState = {
  ghibli: {
    movies: []
  },
  editor: {
    code: ''
  },
  gameView: {
    connectionParams: {
      game_url_base: '',
      game_url_path: '',
      game_url_port: 0,
      game_ssl_flag: false
    }
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
