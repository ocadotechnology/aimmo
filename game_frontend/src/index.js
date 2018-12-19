import '@babel/polyfill'
import React from 'react'
import { render } from 'react-dom'

import WebFont from 'webfontloader'
import { MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'
import { darkTheme } from 'theme'

import { Provider } from 'react-redux'
import configureStore from './redux/store'

import GamePage from './components/GamePage'
import { RunCodeButtonStatus } from 'components/RunCodeButton'

WebFont.load({
  typekit: {
    id: 'mrl4ieu'
  }
})

const initialState = {
  editor: {
    code: {
      code: ''
    },
    runCodeButton: {
      status: RunCodeButtonStatus.normal
    }
  },
  game: {
    connectionParameters: {
      game_id: getGameIDFromURL() || 1
    },
    gameDataLoaded: false,
    showSnackbarForAvatarUpdated: false,
    timeoutStatus: false
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
  <StyledComponentsThemeProvider theme={darkTheme}>
    <MuiThemeProvider theme={darkTheme}>
      <Provider store={reduxStore}>
        <GamePage />
      </Provider>
    </MuiThemeProvider>
  </StyledComponentsThemeProvider>
)

const root = document.getElementById('root')
render(<RootJSX />, root)
