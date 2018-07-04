/* eslint-env jest */
import React from 'react'
import { IDEEditor, IDEEditorLayout } from 'containers/IDEEditor'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEEditor />', () => {
  it('matches snapshot', () => {
    const props = {
      code: 'class Avatar',
      getCode: jest.fn(),
      postCode: jest.fn()
    }

    const component = createShallowWithTheme(<IDEEditor {...props} />)

    expect(component).toMatchSnapshot()
  })
})

describe('<IDEEditorLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEEditorLayout />)
    expect(tree).toMatchSnapshot()
  })
})
