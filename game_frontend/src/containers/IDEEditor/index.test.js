/* eslint-env jest */
import React from 'react'
import { IDEEditor } from 'containers/IDEEditor'
import { shallow } from 'enzyme/build/index'
import { withTheme } from 'testHelpers/withTheme'

describe('<IDEEditor />', () => {
  it('matches snapshot', () => {
    const props = {
      code: 'class Avatar',
      getCode: jest.fn(),
      postCode: jest.fn()
    }

    const component = shallow(withTheme(<IDEEditor {...props} />))

    expect(component).toMatchSnapshot()
  })
})
