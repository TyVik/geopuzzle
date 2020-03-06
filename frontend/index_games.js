'use strict';
import React from "react";
import {render} from "react-dom";
import IndexGames from "./index_games/index";
import {IntlProvider} from "react-intl";
import messages from './locale/messages';


let nodes = document.getElementsByClassName('index_games');

for (var i = 0; i < nodes.length; i++) {
  render(
    <IntlProvider locale={window.__LANGUAGE__} messages={messages[window.__LANGUAGE__]}>
      <IndexGames game={nodes[i].dataset.name} />
    </IntlProvider>,
    nodes[i]);

}
