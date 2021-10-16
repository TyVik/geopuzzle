'use strict';
import React from "react";
import {render} from "react-dom";
import Index from "./index/index";
import messages from "./locale/messages";
import {IntlProvider} from "react-intl";


let node = document.getElementById('index');

render(
    <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
      <Index games={window.__GAMES__}/>
    </IntlProvider>, node);