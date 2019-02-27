import React from 'react';
import {shallow} from 'enzyme';
import QuizInit from '../games/components/QuizInit';
import localization from "../localization";
import {Button, Modal} from "react-bootstrap";


describe('shallow <QuizInit /> components', () => {
  let onLoad = jest.fn();
  let props = {show: true, load: onLoad};

  beforeEach(() => {
    window.__OPTIONS__ = ['title', 'flag', 'coat_of_arms', 'capital'];
  });

  it('render hidden', () => {
    expect(shallow(<QuizInit show={false}/>).html()).toBe('');
  });

  it('check props', () => {
    window.__OPTIONS__ = ['title', 'flag', 'coat_of_arms', 'capital'];
    let wrapper = shallow(<QuizInit {...props}/>);
    expect(wrapper).toMatchSnapshot('quizinit');
    expect(wrapper.find(Button).prop('disabled')).toBe(undefined);
    window.__OPTIONS__.map(key => {
      wrapper.instance().toggle(key);
    });
    expect(wrapper.find(Button).prop('disabled')).toBe(true);
    expect(wrapper.find(Modal.Footer).childAt(0).text()).toMatch(localization.quizInitCheck);
    wrapper.instance().toggle('title');
    wrapper.find(Button).simulate('click');
    expect(onLoad).toHaveBeenCalledWith({title: true, flag: false, coat_of_arms: false, capital: false});
  });
});
