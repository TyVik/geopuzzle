'use strict';
import React from 'react';
import {shallow} from 'enzyme';
import QuizInit from '../games/components/QuizInit';
import {Button, Modal} from "react-bootstrap";


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
    let wrapper = shallow(<QuizInit {...props}/>);
    expect(wrapper.find(Button).prop('disabled')).toBe(false);
    window.__OPTIONS__.map(key => {
      wrapper.instance().toggle(key);
    });
    expect(wrapper.find(Button).prop('disabled')).toBe(true);
    expect(wrapper.find(Modal.Footer).childAt(0).childAt(0).prop('id')).toMatch("quizInitCheck");
    wrapper.instance().toggle('title');
    wrapper.find(Button).simulate('click');
    expect(onLoad).toHaveBeenCalledWith({name: true, flag: false, coat_of_arms: false, capital: false});
  });
});
