/* eslint-env jest */
import React from 'react'
import { NavigationBar, NavigationBarLayout } from 'components/NavigationBar'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<NavigationBarLayout />', () => {
  it('renders correctly', () => {
    const tree = createShallowWithTheme(<NavigationBarLayout />)
    expect(tree).toMatchSnapshot()
  })

  it('returns new badge', () => {
    const props = {
      badgesInit: jest.fn()
    }
    const givenProps = {
      gameState: {
        worksheetID: 1
      },
      completedBadges: '1:1,'
    };
    const givenState = {
      completedBadges: [],
      lastBadge: ''
    };
    const expectedResult = {
      completedBadges: ['1:1'],
      lastBadge: '1:1'
    };

    const component = createShallowWithTheme(<NavigationBar {...props} />, 'dark')
    const result = component.instance().constructor.getDerivedStateFromProps(givenProps, givenState);
    expect(result).toEqual(expectedResult);
  })

  it('returns null if no new badges within the same worksheet', () => {
    const props = {
      badgesInit: jest.fn()
    }
    const givenProps = {
      gameState: {
        worksheetID: 1
      },
      completedBadges: '1:1,1:2,2:1'
    };
    const givenState = {
      completedBadges: ['1:1,1:2'],
      lastBadge: ''
    };
    const expectedResult = null;

    const component = createShallowWithTheme(<NavigationBar {...props} />, 'dark')
    const result = component.instance().constructor.getDerivedStateFromProps(givenProps, givenState);
    expect(result).toEqual(expectedResult);
  })
})
