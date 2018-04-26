import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

const IDEEditorLayout = styled.div`
  background-color: #2F4F4F
  grid-area: ide-editor
`

export default class IDEEditor extends Component {
  render () {
    return (
      <IDEEditorLayout>
        <p>{this.props.code}</p>
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  code: PropTypes.string
}
