import React from 'react';
import {shallow} from 'enzyme';
import QuizInit from '../components/QuizInit';


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
    expect(wrapper.find('Button').props()['disabled']).toBe(true);
    wrapper.instance().toggle('title');
    expect(wrapper.find('Button').props()['disabled']).toBe(false);
    wrapper.find('Button').simulate('click');
    expect(onLoad).toHaveBeenCalledWith({title: true, flag: false, coat_of_arms: false, capital: false});
  });
});
