'use strict';
import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-15';
import fetch from 'jest-fetch-mock';
import 'jest-localstorage-mock';

configure({adapter: new Adapter()});

global.fetch = fetch;
jest.mock('js-cookie', ()=> ({get: () => 'csrf'}));

const { JSDOM } = require('jsdom');
const jsdom = new JSDOM('<!doctype html><html><body></body></html>');
const { window } = jsdom;

function copyProps(src, target) {
  const props = Object.getOwnPropertyNames(src)
    .filter(prop => typeof target[prop] === 'undefined')
    .reduce((result, prop) => ({
      ...result,
      [prop]: Object.getOwnPropertyDescriptor(src, prop),
    }), {});
  Object.defineProperties(target, props);
}

window.__STATIC_URL__ = '/static/';
window.__LANGUAGE__ = 'en';
global.window = window;
global.document = window.document;
global.navigator = {
  userAgent: 'node.js',
};
copyProps(window, global);
