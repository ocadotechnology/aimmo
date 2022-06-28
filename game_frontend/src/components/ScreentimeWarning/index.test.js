/* eslint-env jest */
import React from 'react'
import { shallow } from 'enzyme'

import ScreentimeWarning from 'components/ScreentimeWarning'

describe('<ScreentimeWarning />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<ScreentimeWarning />)

    expect(tree).toMatchSnapshot()
  })
})
