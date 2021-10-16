'use strict';
import React from 'react';
import {shallow} from 'enzyme';
import QuizQuestion from "../games/components/QuizQuestion";


describe('shallow <QuizQuestion /> components', () => {
  it('render hidden', () => {
    expect(shallow(<QuizQuestion question={null}/>).html()).toBe(null);
  });
});