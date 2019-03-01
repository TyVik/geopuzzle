'use strict';
import React from "react";
import {render} from "react-dom";
import Profile from "./profile/index";
import {IntlProvider} from "react-intl";
import messages from "./i18n";


let node = document.getElementById('profile');

render(
    <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
      <Profile/>
    </IntlProvider>, node);
