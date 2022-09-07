/* eslint-env jest */
import React from 'react'
import { IDEEditor, IDEEditorLayout } from 'containers/IDEEditor'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<IDEEditor />', () => {
  it("matches snapshot when code isn't loaded", () => {
    const props = {
      code: 'class Avatar',
      getCode: jest.fn(),
      postCode: jest.fn(),
    }

    const component = createShallowWithTheme(<IDEEditor {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })
  it('matches snapshot when code is loaded', () => {
    const props = {
      code: 'class Avatar',
      getCode: jest.fn(),
      postCode: jest.fn(),
      codeOnServer: 'def next_turn(...): pass',
    }

    const component = createShallowWithTheme(<IDEEditor {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('does not call post code as button is initially disabled', () => {
    const postCode = jest.fn()
    const props = {
      postCode,
      getCode: jest.fn(),
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
