'use strict';
import 'whatwg-fetch';
import Cookies from 'js-cookie';


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


export {CSRFfetch, getFormData};
