import styled from 'styled-components'
import React, { Component } from 'react'
import AceEditor from 'react-ace'
import 'brace/theme/idle_fingers'

const IDEEditorLayout = styled.div`
  background-color: #2F4F4F
  grid-area: ide-editor
`

export default class IDEEditor extends Component {
  render () {
    return (
      <IDEEditorLayout>
        <AceEditor
          mode='javascript'
          theme='idle_fingers'
          name='blah2'
          onLoad={this.onLoad}
          onChange={this.onChange}
          fontSize={14}
          showPrintMargin
          showGutter
          highlightActiveLine
          value={`TODO`}
          width='100%'
          height='100%'
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: false,
            showLineNumbers: true,
            tabSize: 2
          }} />
      </IDEEditorLayout>
    )
  }
}
