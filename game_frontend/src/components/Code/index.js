import styled from 'styled-components'

const Code = styled.p`
  font-family: ${(props) => props.theme.additionalVariables.typography.code.fontFamily};
  color: ${(props) => props.theme.palette.secondary.main};
`
export default Code
