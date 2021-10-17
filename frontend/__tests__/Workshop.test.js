'use strict';
import React from "react";
import Workshop from "../workshop/index";
import {createComponentWithIntl} from "./utils";


describe('shallow <Workshop /> components', () => {
  it('render', () => {
    let order = [
      ["title_asc", "Title \u2193"], ["title_desc", "Title \u2191"],
      ["created_asc", "Created \u2193"], ["created_desc", "Created \u2191"]
    ];
    expect(createComponentWithIntl(<Workshop orderOptions={order}/>)).toMatchSnapshot('Workshop');
  });
});
