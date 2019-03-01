'use strict';
import React from "react";
import {render} from "react-dom";
import Puzzle from "./games/Puzzle";
import Quiz from "./games/Quiz";
import messages from "./i18n";
import {IntlProvider} from "react-intl";


let puzzle = document.getElementById('puzzle');
if (puzzle !== null) {
    render(
      <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
          <Puzzle />
      </IntlProvider>, puzzle);
}


let quiz = document.getElementById('quiz');
if (quiz !== null) {
    render(
      <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
          <Quiz />
      </IntlProvider>, quiz);
}
