// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  modulePathIgnorePatterns: ['Api/dist/'], // ignore the dist folder from tests
};

