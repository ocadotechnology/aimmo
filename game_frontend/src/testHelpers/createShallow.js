import React from 'react'
import { createShallow } from '@material-ui/core/test-utils'
import theme from '../theme'
import { createMuiTheme } from '@material-ui/core/styles'

const muiTheme = createMuiTheme(theme)

/**
 * Shallow renders the given component with the theme context for material-ui
 * components and styled components.
 * Use this to test components that require the theme context.
 *
 * @example
 * const tree = createShallowWithTheme(component)
 * expect(tree).toMatchSnapshot()
 *
 * @param {React.Component} component The component you want to test
 *
 * @returns {ShallowWrapper} An enzyme ShallowWrapper of the component with the theme context
 */
export default function createShallowWithTheme (component) {
  return createShallow()(React.cloneElement(component, { theme: muiTheme }))
}
