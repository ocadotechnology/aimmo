import { Button, Toolbar } from '@material-ui/core';
import ClearIcon from 'components/icons/Clear';
import React from 'react';
import styled from 'styled-components'
import PropTypes from 'prop-types'

export const StyledClearConsoleBar = styled(Toolbar)`
  background: #2f3129;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
`

export const StyledConsoleTitle = styled.div`
  display: inline-flex;
`

export const ClearButton = styled(Button)`
  right: 0vw;
`

const ClearConsoleBar = (props) => {
  return (
    <StyledClearConsoleBar variant="dense">
      <StyledConsoleTitle>
        <ClearButton
          variant="outlined"
          onClick={props.clearConsoleClicked}
          startIcon={<ClearIcon />}
        >
          Clear console
        </ClearButton>
      </StyledConsoleTitle>
    </StyledClearConsoleBar>
  )
}

ClearConsoleBar.propTypes = {
  clearConsoleClicked: PropTypes.func,
}

export default ClearConsoleBar;
