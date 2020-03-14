'use strict';
import React from 'react';
import {shallow} from 'enzyme';
import {QuizInit} from '../games/components/QuizInit';
import {Button} from "react-bootstrap";
import {mountComponentWithIntl} from "./utils";


describe('shallow <QuizInit /> components', () => {
  let onLoad = jest.fn();
  let props = {show: true, load: onLoad};

  beforeEach(() => {
    window.__OPTIONS__ = ['name', 'flag', 'coat_of_arms', 'capital'];
  });

  it('render hidden', () => {
    expect(shallow(<QuizInit show={false}/>).html()).toBe('');
  });

  it('render', () => {
    expect(shallow(<QuizInit {...props}/>)).toMatchSnapshot('quizinit');
  });

  it('check props', () => {
    let wrapper = mountComponentWithIntl(<QuizInit {...props}/>);
    expect(wrapper.find(Button).prop('disabled')).toBe(false);
    let quizInit = wrapper.find('QuizInit').instance();
    window.__OPTIONS__.map(key => {
      quizInit.toggle(key);
    });
    wrapper.update();
    expect(wrapper.find(Button).prop('disabled')).toBe(true);
    expect(wrapper.find('i').childAt(0).prop('id')).toMatch("quizInitCheck");
    quizInit.toggle('name');
    wrapper.update();
    wrapper.find(Button).simulate('click');
    expect(onLoad).toHaveBeenCalledWith({name: true, flag: false, coat_of_arms: false, capital: false});
  });
});
