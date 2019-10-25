/* eslint-env jest */
import React from 'react'
import createShallowWithTheme from 'testHelpers/createShallow'
import FindMeButton, { MarginedLocationIcon } from 'components/FindMeButton'

describe('<FindMeButton />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<FindMeButton />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

describe('<MarginedLocationIcon />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<MarginedLocationIcon />, 'dark')

    expect(component).toMatchSnapshot()
  })
})
