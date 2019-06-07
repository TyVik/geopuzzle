'use strict';
import React from "react";
import {renderWithIntl, loadTranslation} from 'enzyme-react-intl';
import Workshop from "../workshop/index";


loadTranslation("./frontend/locale/en.json");


describe('shallow <Workshop /> components', () => {
  it('render', () => {
    expect(renderWithIntl(<Workshop/>)).toMatchSnapshot('Workshop');
  });
});
