module.exports = {
  parser: '@typescript-eslint/parser',
  extends: ['standard', 'standard-react', 'plugin:cypress/recommended', 'prettier'],
  plugins: ['@typescript-eslint'],
  parserOptions: {
    sourceType: 'module',
  },
  env: {
    browser: true,
    'cypress/globals': true,
  },
  globals: {
    loadPyodide: 'readonly',
    OnetrustActiveGroups: 'readonly',
  },
  rules: {
    'react/jsx-handler-names': 'off',
    'react/jsx-pascal-case': [
      'error',
      {
        allowAllCaps: true,
      },
    ],
    '@typescript-eslint/member-delimiter-style': [
      'error',
      {
        multiline: {
          delimiter: 'none',
        },
      },
    ],
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        args: 'none',
      },
    ],
    'no-console': [
      'error',
      {
        allow: ['warn', 'error'],
      },
    ],
  },
}
