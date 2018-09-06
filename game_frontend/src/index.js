import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'

import ThemeProvider from './components/ThemeProvider'
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
  <ThemeProvider variant='light'>
    <Provider store={reduxStore}>
      <GamePage />
    </Provider>
  </ThemeProvider>
)

const root = document.getElementById('root')
render(<RootJSX />, root)
