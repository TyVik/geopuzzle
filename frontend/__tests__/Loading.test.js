import React from 'react';
import {shallow} from 'enzyme';
import Loading from '../components/Loading';


it('shallow <Loading /> components', () => {
  expect(shallow(<Loading text='test'/>)).toMatchSnapshot();
});
