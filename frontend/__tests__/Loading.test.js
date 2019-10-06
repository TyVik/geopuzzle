'use strict';
import React from 'react';
import Loading from '../components/Loading';
import {createComponentWithIntl} from "./utils";



it('shallow <Loading /> components', () => {
  expect(createComponentWithIntl(<Loading text='test'/>)).toMatchSnapshot();
});
