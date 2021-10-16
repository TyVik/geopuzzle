'use strict';
import {configure} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import fetch from 'jest-fetch-mock';
import createGoogleMapsMock from 'jest-google-maps-mock';
import 'jest-localstorage-mock';

configure({adapter: new Adapter()});

global.fetch = fetch;
global.google = {maps: createGoogleMapsMock()};
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

global.REGIONS = [{
  draggable: false, id: 5054,
  infobox: {area: "32,300", capital: {lat: 52, lng: 23, name: "Брест", wiki: "https://ru.wikipedia.org/wiki/Брест"},
    coat_of_arms: "https://upload.wikimedia.org/wikipedia/commons/e/e7/Escut_Oblast_Brest.png",
    flag: "https://upload.wikimedia.org/wikipedia/commons/e/ec/Flag_of_Brest_Voblast%2C_Belarus.svg"},
  loaded: true, marker: {lat: 52, lng: 23}, name: "Брестская область", population: "1386982",
  wiki: "https://ru.wikipedia.org/wiki/Брестская_область", isSolved: true, paths: []
}, {
  draggable: true, id: 5060, infobox: {loaded: false, name: "Витебская область"}, isSolved: false, paths: []
}, {
  draggable: true, id: 5055, infobox: {loaded: false, name: "Гомельская область"}, isSolved: false, paths: []
}];

global.window = window;
global.document = window.document;
global.navigator = {
  userAgent: 'node.js',
};
copyProps(window, global);
