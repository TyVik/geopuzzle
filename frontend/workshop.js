'use strict';
import React from "react";
import {render} from "react-dom";
import Workshop from "./workshop/index";
import {IntlProvider} from "react-intl";
import messages from './locale/messages';


let node = document.getElementById('workshop');

render(
  <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
    <Workshop count={parseInt(node.dataset.count, 10)} prop={{
      orderOptions: window.__ORDER__.map(item => { 
        return { value: item[0], label: item[1] }
      })
    }}/>
  </IntlProvider>,
  node);
