'use strict';
import React from "react";
import { createRoot } from "react-dom/client";
import Index from "./index/index";
import messages from "./locale/messages";
import {IntlProvider} from "react-intl";


let root = createRoot(document.getElementById('index'));

root.render(
  <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
    <Index games={window.__GAMES__}/>
  </IntlProvider>
);