'use strict';
import React from "react";
import Workshop from "../workshop/index";
import { render } from "./utils";


describe('<Workshop />', () => {
  let orderOptions = [
    ["title_asc", "Title \u2193"],
    ["title_desc", "Title \u2191"],
    ["created_asc", "Created \u2193"],
    ["created_desc", "Created \u2191"]
  ];

  test('render', async () => {
    const wrapper = render(<Workshop orderOptions={orderOptions}/>);
  });
});
