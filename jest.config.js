'use strict';


module.exports = {
  automock: false,
  verbose: true,
  testURL: "http://localhost/",
  testMatch: ["**/*.test.js"],
  rootDir: 'frontend',
  "setupFiles": [
    "jest-localstorage-mock"
  ],
  snapshotSerializers: ["enzyme-to-json/serializer"],
  setupFilesAfterEnv: ["<rootDir>/setupTests.js"],
  collectCoverage: true,
  collectCoverageFrom: [
    "!<rootDir>/coverage/**",
    "**/*.{js,jsx}",
  ],
  moduleNameMapper: {
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$":
      "<rootDir>/frontend/__mocks__/fileMock.js",
    "\\.(css|less)$": "identity-obj-proxy",
  },
};
