'use strict';
import React from "react";
import {render} from "react-dom";
import Puzzle from "./games/Puzzle";
import Quiz from "./games/Quiz";
import messages from "./locale/messages";
import {IntlProvider} from "react-intl";

let games = {
  'puzzle': <Puzzle />,
  'quiz': <Quiz />,
};


for (let [game, component] of Object.entries(games)) {
  let node = document.getElementById(game);
  if (node !== null) {
      render(
        <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
          {component}
        </IntlProvider>, node);
  }
}
