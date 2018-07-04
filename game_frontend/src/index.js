import React from 'react'
import {render} from 'react-dom'
import 'rxjs'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider } from 'styled-components'

import { Provider } from 'react-redux'
import theme from './theme'

import GamePage from './components/GamePage'
import configureStore from './redux/store'

import WebFont from 'webfontloader'

WebFont.load({
  typekit: {
    id: 'mrl4ieu'
  }
})

const initialState = {
  ghibli: {
    movies: []
  },
  editor: {
    code: ''
  },
  game: {
    connectionParameters: {
      id: getGameIDFromURL() || 1,
      game_url_base: '',
      game_url_path: '',
      game_url_port: 0,
      game_ssl_flag: false
    }
  }
}

function getGameIDFromURL () {
  const url = window.location.href
  const gameIDFinder = /\/play\/([0-9]+)/
  return gameIDFinder.exec(url)[1]
}

const reduxStore = configureStore(initialState)
const muiTheme = createMuiTheme(theme)

const RootJSX = () => (
  <ThemeProvider theme={muiTheme}>
    <MuiThemeProvider theme={muiTheme}>
      <Provider store={reduxStore}>
        <GamePage />
      </Provider>
    </MuiThemeProvider>
  </ThemeProvider>
)

const root = document.getElementById('root')
render(<RootJSX />, root)
