module.exports = {
  testURL: 'http://localhost/',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  snapshotSerializers: ['enzyme-to-json/serializer'],
  modulePathIgnorePatterns: ['<rootDir>/dist/', '<rootDir>/cypress/'],
  globals: {
    'babel-jest': {
      useBabelrc: true
    }
  }
}
