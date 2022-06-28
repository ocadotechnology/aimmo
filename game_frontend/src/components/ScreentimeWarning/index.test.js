/* eslint-env jest */
import React from 'react'
import { act } from 'react-dom/test-utils'

import { shallow } from 'enzyme'
import { ajax } from 'rxjs/ajax'

import createMountWithTheme from 'testHelpers/createMount'

import ScreentimeWarning from 'components/ScreentimeWarning'
import { of } from 'rxjs'

jest.mock('rxjs/ajax', () => ({
  ...jest.requireActual('rxjs/ajax'),
  ajax: jest.fn(),
}))

describe('<ScreentimeWarning />', () => {
  it('matches snapshot', () => {
    const tree = shallow(<ScreentimeWarning />)

    expect(tree).toMatchSnapshot()
  })

  it('calls the reset_screentime_warning API when Continue is clicked', () => {
    jest.useFakeTimers()
    const mockAjax = jest.fn(() => of('test'))
    ajax.mockImplementation(mockAjax)

    const component = createMountWithTheme(<ScreentimeWarning />)

    act(() => {
      // Fast-forward and execute pending timers
      jest.runOnlyPendingTimers()
    })

    component.update()

    const button = component.find('button')
    expect(button.text()).toBe('Continue')
    button.simulate('click')
    expect(mockAjax).toHaveBeenCalledWith('/user/reset_screentime_warning/')
  })
})
