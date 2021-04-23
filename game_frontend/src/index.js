import 'core-js/stable'
import 'regenerator-runtime/runtime'
import 'threads/register'
import React from 'react'
import { render } from 'react-dom'

import WebFont from 'webfontloader'
import { MuiThemeProvider, StylesProvider } from '@material-ui/core/styles'
import { ThemeProvider as StyledComponentsThemeProvider } from 'styled-components'
import { darkTheme } from 'theme'

import { Provider } from 'react-redux'
import configureStore from './redux/store'
import { enableMapSet } from 'immer'

import ReactGA from 'react-ga'

import GamePage from 'components/GamePage'
import { RunCodeButtonStatus } from 'components/RunCodeButton'

import { hasAnalyticsCookiesConsent } from 'redux/features/Analytics/index'

enableMapSet()

WebFont.load({
  typekit: {
    id: 'mrl4ieu',
  },
  google: {
    families: ['Source Code Pro'],
  },
})

// only triggers GA on production (and with cookie consent)
const isProduction = (location.hostname.search(/codeforlife.education/i) >= 0)

if (hasAnalyticsCookiesConsent()) {
  ReactGA.initialize('UA-49883146-1', {
    debug: false,
    testMode: !isProduction
  })

  if (isProduction) {
    ReactGA.pageview(`/kurono/play/${getGameIDFromURL()}`)
  }
}

const initialState = (window.Cypress && window.initialState) || {
  editor: {
    code: {
      code: '',
    },
    runCodeButton: {
      status: RunCodeButtonStatus.normal,
    },
  },
  game: {
    connectionParameters: {
      game_id: getGameIDFromURL() || 1,
    },
    timeoutStatus: false,
    gameLoaded: false,
    cameraCenteredOnUserAvatar: true,
  },
}

function getGameIDFromURL() {
  const url = window.location.href
  const gameIDFinder = /\/play\/([0-9]+)/
  return gameIDFinder.exec(url)[1]
}

const reduxStore = configureStore(initialState)

const RootJSX = () => (
  <StylesProvider injectFirst>
    <MuiThemeProvider theme={darkTheme}>
      <StyledComponentsThemeProvider theme={darkTheme}>
        <Provider store={reduxStore}>
          <GamePage />
        </Provider>
      </StyledComponentsThemeProvider>
    </MuiThemeProvider>
  </StylesProvider>
)

if (window.Cypress) {
  window.store = reduxStore
}

const root = document.getElementById('root')
render(<RootJSX />, root)
