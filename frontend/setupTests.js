'use strict';
import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
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
window.__USER__ = {
  "username": "admin", "email": "admin@admin.com", "image": "https://d2nepmml5nn7q0.cloudfront.net/avatars/e_28d3ad97.jpg",
  "language": "en", "is_subscribed": true};
window.__PROVIDERS__ = [
  {"slug": "facebook", "connected": true, "label": "FB", "class": "facebook"},
  {"slug": "vk-oauth2", "connected": true, "label": "VK", "class": "vk"},
  {"slug": "google-oauth2", "connected": false, "label": "Google", "class": "google"}
];
window.__TAGS__ = [
  [1, "Russian regions"], [2, "US states"], [3, "European countries"], [4, "Asian countries"], [5, "African countries"],
  [6, "N. American countries"], [7, "S. American countries"], [8, "Prefectures of Japan"]
];

global.window = window;
global.document = window.document;
global.navigator = {
  userAgent: 'node.js',
};
copyProps(window, global);
