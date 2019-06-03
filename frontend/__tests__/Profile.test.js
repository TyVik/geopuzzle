'use strict';
import React from "react";
import {shallow} from "enzyme";
import renderer from 'react-test-renderer';
import {renderWithIntl, loadTranslation} from 'enzyme-react-intl';
import Profile from "../profile/index";


loadTranslation("./frontend/locale/en.json");


describe('shallow <Profile /> components', () => {
  it('render', () => {
    expect(renderWithIntl(<Profile/>)).toMatchSnapshot('Profile');
  });
});
