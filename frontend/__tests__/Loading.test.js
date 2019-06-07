'use strict';
import React from 'react';
import {renderWithIntl, loadTranslation} from 'enzyme-react-intl';
import Loading from '../components/Loading';

loadTranslation("./frontend/locale/en.json");


it('shallow <Loading /> components', () => {
  expect(renderWithIntl(<Loading text='test'/>)).toMatchSnapshot();
});
