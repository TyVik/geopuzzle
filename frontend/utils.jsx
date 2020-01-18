'use strict';
import 'whatwg-fetch';
import Cookies from 'js-cookie';

import messages from "./locale/messages";


function moveTo(paths, from, to) {
  let newPoints =[];
  let newPaths = [];

  for (let p = 0; p < paths.length; p++) {
    let path = paths[p];
    newPoints.push([]);

    for (let i = 0; i < path.length; i++) {
      newPoints[newPoints.length-1].push({
        heading: google.maps.geometry.spherical.computeHeading(from, path[i]),
        distance: google.maps.geometry.spherical.computeDistanceBetween(from, path[i])
      });
    }
  }

  for (let j = 0, jl = newPoints.length; j < jl; j++) {
    let shapeCoords = [];
    let relativePoint = newPoints[j];
    for (let k = 0, kl = relativePoint.length; k < kl; k++) {
      shapeCoords.push(google.maps.geometry.spherical.computeOffset(to, relativePoint[k].distance, relativePoint[k].heading));
    }
    newPaths.push(shapeCoords);
  }
  return newPaths;
}


function decodePolygon(polygon) {
  return polygon.map(polygon => (google.maps.geometry.encoding.decodePath(polygon)));
}

const prepareInfobox = (json) => {
  if (json.area) {
    json.area = `${Number(json.area).toLocaleString()} ${messages[window.__LANGUAGE__].km2}`;
  }
  if (json.population) {
    json.population = Number(json.population).toLocaleString();
  }
  return json;
};

function shuffle(a) {
  for (let i = a.length; i; i--) {
    let j = Math.floor(Math.random() * i);
    [a[i - 1], a[j]] = [a[j], a[i - 1]];
  }
  return a;
}


const getFormData = (object) => {
  return Object.keys(object).reduce((formData, key) => {
    formData.append(key, object[key]);
    return formData;
  }, new FormData());
};


const CSRFfetch = (url, options) => {
  let headers = options.headers || new Headers();
  headers.append('X-CSRFTOKEN', Cookies.get('csrftoken'));
  return fetch(url, {...options, headers: headers, credentials: 'same-origin'});
};


export {moveTo, decodePolygon, prepareInfobox, shuffle, CSRFfetch, getFormData};
