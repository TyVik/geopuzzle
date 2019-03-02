'use strict';
import React from "react";
import {render} from "react-dom";
import Profile from "./profile/index";
import messages from "./i18n";
import {IntlProvider} from "react-intl";


let node = document.getElementById('profile');

render(
    <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
      <Profile/>
    </IntlProvider>, node);
