import styled from 'styled-components'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import AceEditor from 'react-ace';

const IDEEditorLayout = styled.div`
  background-color: #2F4F4F
  grid-area: ide-editor
`

export default class IDEEditor extends Component {
  render () {
    return (
      <IDEEditorLayout>
          <AceEditor
              mode="javascript"
              theme="monokai"
              name="blah2"
              onLoad={this.onLoad}
              onChange={this.onChange}
              fontSize={14}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              value={`TODO`}
              setOptions={{
                  enableBasicAutocompletion: true,
                  enableLiveAutocompletion: true,
                  enableSnippets: false,
                  showLineNumbers: true,
                  tabSize: 2,
              }}/>
      </IDEEditorLayout>
    )
  }
}

IDEEditor.propTypes = {
  code: PropTypes.string
}
