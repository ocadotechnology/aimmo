/* eslint-env jest */
import React from 'react'
import RunCodeButton, {
  MarginedCheckCircle,
  MarginedCircularProgress,
  MarginedPlayIcon,
  RunCodeButtonStatus,
  MarginedBugIcon,
} from 'components/RunCodeButton'
import createShallowWithTheme from 'testHelpers/createShallow'

describe('<RunCodeButton />', () => {
  it('renders with a normal status', () => {
    const props = {
      whenClicked: jest.fn(),
      runCodeButtonStatus: {
        status: RunCodeButtonStatus.normal,
      },
    }

    const component = createShallowWithTheme(<RunCodeButton {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('renders with a updating status', () => {
    const props = {
      whenClicked: jest.fn(),
      runCodeButtonStatus: {
        status: RunCodeButtonStatus.updating,
      },
    }

    const component = createShallowWithTheme(<RunCodeButton {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('renders with a done status', () => {
    const props = {
      whenClicked: jest.fn(),
      runCodeButtonStatus: {
        status: RunCodeButtonStatus.done,
      },
    }

    const component = createShallowWithTheme(<RunCodeButton {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('becomes enabled when code is different from the server', () => {
    const props = {
      whenClicked: jest.fn(),
      runCodeButtonStatus: {
        status: RunCodeButtonStatus.normal,
      },
      isCodeOnServerDifferent: true,
    }

    const component = createShallowWithTheme(<RunCodeButton {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('becomes disabled when code is the same as the server', () => {
    const props = {
      whenClicked: jest.fn(),
      runCodeButtonStatus: {
        status: RunCodeButtonStatus.normal,
      },
      isCodeOnServerDifferent: false,
    }

    const component = createShallowWithTheme(<RunCodeButton {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })

  it('shows an error when a timeout is detected', () => {
    const props = {
      whenClicked: jest.fn(),
      runCodeButtonStatus: {
        status: RunCodeButtonStatus.error,
      },
    }

    const component = createShallowWithTheme(<RunCodeButton {...props} />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

describe('<MarginedPlayIcon />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<MarginedPlayIcon />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

describe('<MarginedCheckCircle />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<MarginedCheckCircle />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

describe('<MarginedCircularProgress />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<MarginedCircularProgress />, 'dark')

    expect(component).toMatchSnapshot()
  })
})

describe('<MarginedBugIcon />', () => {
  it('matches snapshot', () => {
    const component = createShallowWithTheme(<MarginedBugIcon />, 'dark')

    expect(component).toMatchSnapshot()
  })
})
