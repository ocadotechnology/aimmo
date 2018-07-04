/* eslint-env jest */
import React from 'react'
import Code from 'components/Code'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<Code />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<Code>Code</Code>)
    expect(tree).toMatchSnapshot()
  })
})
