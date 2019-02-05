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

    const component = createShallowWithTheme(<IDEEditor {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('does not call post code as button is intially disabled', () => {
    const postCode = jest.fn()
    const props = {
      postCode
    }

    const component = createShallowWithTheme(<IDEEditor {...props} />, 'dark')

    component.find('#post-code-button').simulate('click')
    expect(postCode).not.toBeCalled()
  })
})

describe('<IDEEditorLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<IDEEditorLayout />, 'dark')
    expect(tree).toMatchSnapshot()
  })
})
