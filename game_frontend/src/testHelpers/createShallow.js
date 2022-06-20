import React from 'react'
import { createShallow } from '@material-ui/core/test-utils'
import themeVariants from 'theme'

/**
 * Shallow renders the given component with the theme context for material-ui
 * components and styled components.
 * Use this to test components that require the theme context.
 *
 * @example
 * const tree = createShallowWithTheme(component)
 * expect(tree).toMatchSnapshot()
 *
 * @param {string} themeVariant The variant of the theme (dark or light)
 * @param {React.Component} component The component you want to test
 *
 * @returns {ShallowWrapper} An enzyme ShallowWrapper of the component with the theme context
 */
export default function createShallowWithTheme(component, themeVariant = 'light', dive = false) {
  return createShallow({ dive })(
    React.cloneElement(component, { theme: themeVariants[themeVariant] })
  )
}
