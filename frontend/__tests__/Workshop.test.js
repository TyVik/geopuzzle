'use strict';
import React from "react";
import Workshop from "../workshop/index";
import {createComponentWithIntl} from "./utils";


describe('shallow <Workshop /> components', () => {
  it('render', () => {
    expect(createComponentWithIntl(<Workshop/>)).toMatchSnapshot('Workshop');
  });
});
