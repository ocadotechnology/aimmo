import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { actions } from 'features/Editor'

const IDEMenuLayout = styled.nav`
  background-color: pink
  grid-area: ide-menu
`

export class IDEMenu extends Component {
  render () {
    return (
      <IDEMenuLayout>
        <button
          id='post-code-button'
          onClick={this.props.postCode} >Post Code</button>
      </IDEMenuLayout>
    )
  }
}

IDEMenu.propTypes = {
  postCode: PropTypes.func
}

const mapStateToProps = () => ({})

const mapDispatchToProps = {
  postCode: actions.postCodeRequest
}

export default connect(mapStateToProps, mapDispatchToProps)(IDEMenu)
