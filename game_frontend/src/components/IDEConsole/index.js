import styled from 'styled-components'
import React, { Component } from 'react'

export const IDEConsoleLayout = styled.div`
  grid-area: ide-console;
  color: ${props => props.theme.palette.text.primary};
  background-color: ${props => props.theme.palette.background.default};
  font-family: ${props => props.theme.additionalVariables.typography.code.fontFamily};
  overflow: auto;
`

export default class IDEConsole extends Component {
  render () {
    return (
      <IDEConsoleLayout>
        <p>{ this.props.logs }</p>
      </IDEConsoleLayout>
    )
  }
}
