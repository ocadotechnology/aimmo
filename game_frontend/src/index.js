import '@babel/polyfill'
import React from 'react'
import { render } from 'react-dom'

import { MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'
import { lightTheme } from 'theme'
import { Provider } from 'react-redux'

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
    },
    showSnackbarForAvatarUpdated: false
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

const RootJSX = () => (
  <StyledComponentsThemeProvider theme={lightTheme}>
    <MuiThemeProvider theme={lightTheme}>
      <Provider store={reduxStore}>
        <GamePage />
      </Provider>
    </MuiThemeProvider>
  </StyledComponentsThemeProvider>
)

const root = document.getElementById('root')
render(<RootJSX />, root)
