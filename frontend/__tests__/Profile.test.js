'use strict';
import React from "react";
import Profile from "../profile/index";
import {createComponentWithIntl} from "./utils";


describe('shallow <Profile /> components', () => {
  it('render', () => {
    expect(createComponentWithIntl(<Profile/>)).toMatchSnapshot('Profile');
  });
});
