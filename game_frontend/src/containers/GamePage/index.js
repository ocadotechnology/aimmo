import React, { Component } from 'react'
import styled from 'styled-components'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Editor'
import IDE from 'components/IDE'
import Game from 'components/Game'

const GamePageContainer = styled.div`
  display: grid
  grid-template: 80px 1fr 150px / 1fr 1fr
  grid-template-areas: "ide-menu game-menu"
                       "ide-editor game-view"
                       "ide-console game-view";
  width: 100vw
  height: 100vh
`

export class GamePage extends Component {
  render () {
    return (
      <GamePageContainer>
        <IDE code={this.props.code} getCode={this.props.getCode} />
        <Game />
      </GamePageContainer>
    )
  }
}

GamePage.propTypes = {
  code: PropTypes.string,
  getCode: PropTypes.func
}

const mapStateToProps = state => {
  return {
    code: state.editor.code
  }
}

const mapDispatchToProps = {
  getCode: actions.getCodeRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(GamePage)
