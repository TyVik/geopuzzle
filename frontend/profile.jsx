'use strict';
import React from "react";
import { createRoot } from "react-dom/client";
import Profile from "./profile/index";
import messages from "./locale/messages";
import {IntlProvider} from "react-intl";


let root = createRoot(document.getElementById('profile'));

root.render(
  <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
    <Profile user={window.__USER__} providers={window.__PROVIDERS__} permissions={window.__USER_PERMISSIONS__}/>
  </IntlProvider>
);