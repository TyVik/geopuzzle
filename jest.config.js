'use strict';


module.exports = {
  automock: false,
  verbose: true,
  testURL: "http://localhost/",
  testMatch: ["**/*.test.js"],
  rootDir: 'frontend',
  snapshotSerializers: ["enzyme-to-json/serializer"],
  setupTestFrameworkScriptFile: "<rootDir>/setupTests.js",
  collectCoverage: true,
  collectCoverageFrom: [
    "**/*.{js,jsx}",
  ],
  moduleNameMapper: {
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$":
      "<rootDir>/frontend/__mocks__/fileMock.js",
    "\\.(css|less)$": "identity-obj-proxy",
  },
};
