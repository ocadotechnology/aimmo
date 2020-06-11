import { createMuiTheme } from '@material-ui/core/styles'

const palette = {
  primary: {
    main: '#DF5EE8'
  },
  secondary: {
    main: '#606060'
  }
}

const additionalVariables = {
  typography: {
    code: {
      fontFamily: "'Source Code Pro', monospace",
      fontSize: '1rem'
    }
  }
}

const shape = {
  borderRadius: '24px'
}

const theme = {
  palette,
  additionalVariables,
  shape,
  typography: {
    fontFamily: ['museo-sans', 'Source Code Pro'].join(','),
    display1: {
      fontWeight: 700
    },
    display2: {
      fontWeight: 700
    },
    display3: {
      fontWeight: 900
    },
    display4: {
      fontWeight: 900
    },
    body1: {
      fontWeight: 500
    },
    body2: {
      fontWeight: 500
    },
    button: {
      fontWeight: 500,
      textTransform: 'capitalize'
    },
    caption: {
      fontWeight: 500,
      fontStyle: 'italic'
    }
  }
}

const createTheme = type => {
  const palette = { ...theme.palette, type }
  return createMuiTheme({ ...theme, palette })
}

export const lightTheme = createTheme('light')
export const darkTheme = createTheme('dark')

export default {
  light: lightTheme,
  dark: darkTheme
}
