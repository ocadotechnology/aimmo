import React from 'react'
import {render} from 'react-dom'
import 'rxjs'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { ThemeProvider } from 'styled-components'

import { Provider } from 'react-redux'
import theme from './theme'

import GamePage from './components/GamePage'
import configureStore from './redux/store'

const initialState = {
  ghibli: {
    movies: []
  },
  editor: {
    code: ''
  }
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
