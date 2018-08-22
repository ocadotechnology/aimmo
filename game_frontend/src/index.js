import 'babel-polyfill'
import React from 'react'
import {render} from 'react-dom'
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
  editor: {
    code: ''
  },
  game: {
    connectionParameters: {
      game_id: getGameIDFromURL() || 1
    }
  },
  consoleLog: {
    logs: []
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
