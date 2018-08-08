const palette = {
  type: 'dark',
  primary: {
    main: '#FFFFFF'
  },
  secondary: {
    main: '#CFCDC5'
  }
}

const additionalVariables = {
  typography: {
    code: {
      fontFamily: '\'Source Code Pro\', monospace',
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
  text: {
    secondary: '#FFFFFF'
  },
  typography: {
    fontFamily: [
      'museo-sans',
      'Source Code Pro'
    ].join(','),
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

export default theme
