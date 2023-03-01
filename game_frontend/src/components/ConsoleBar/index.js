import styled from 'styled-components'
import Toolbar from '@material-ui/core/Toolbar/Toolbar'
import { Typography, IconButton, Button } from '@material-ui/core'
import ConsoleIcon from 'components/icons/Console'
import ClearIcon from 'components/icons/Clear'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

export const StyledConsoleBar = styled(Toolbar)`
  background-color: ${(props) => props.theme.palette.grey.A700};
  display: flex;
  justify-content: space-between;
`

export const StyledConsoleTitle = styled.div`
  display: inline-flex;
`

export const StyledConsoleIcon = styled(ConsoleIcon)`
  padding-right: ${(props) => props.theme.spacing()}px;
`

export default class ConsoleBar extends Component {
  static propTypes = {
    clearConsoleClicked: PropTypes.func,
    handleResetCodeClicked: PropTypes.func,
  }

  render() {
    return (
      <StyledConsoleBar variant="dense">
        <StyledConsoleTitle>
          <StyledConsoleIcon color="disabled" />
          <Typography variant="body1" color="textSecondary">
            Console Log
          </Typography>
        </StyledConsoleTitle>

        <Button variant="outlined" onClick={this.props.handleResetCodeClicked}>
          Reset codeaa
        </Button>

        <Button variant="outlined" onClick={this.props.handlePauseGameClicked}>
          {this.props.gamePaused ? 'Resume' : 'Pause'}
        </Button>

        <IconButton size="small" onClick={this.props.clearConsoleClicked}>
          <ClearIcon />
        </IconButton>
      </StyledConsoleBar>
    )
  }
}
