/* eslint-env jest */
import React from 'react'
import { IDEMenu } from 'containers/IDEMenu'
import renderer from 'react-test-renderer'
import { shallow } from 'enzyme'
import withTheme from 'testHelpers/withTheme'

describe('<IDEMenu />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(withTheme(<IDEMenu />)).toJSON()
    expect(tree).toMatchSnapshot()
  })

  it('calls the postCode function in props when Post code button is pressed', () => {
    const postCode = jest.fn()
    const props = {
      postCode
    }

    const component = shallow(<IDEMenu {...props} />)

    component.find('#post-code-button').simulate('click')
    expect(postCode.mock.calls.length).toBe(1)
  })
})
