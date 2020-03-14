'use strict';
import React from 'react';
import {shallow} from 'enzyme';
import {Congratulation} from '../games/components/Congratulation';


describe('shallow <Congratulation /> components', () => {
  let props = {result: 'result', url: 'url', startTime: new Date('2020-01-01')};
  window.__CONGRATULATION__ = {text: 'Congratulations! Your result is: '};

  it('render', () => {
    expect(shallow(<Congratulation {...props}/>)).toMatchSnapshot();
  });

  it('click close', () => {
    let wrapper = shallow(<Congratulation {...props}/>);
    wrapper.instance().onClose();
    expect(wrapper.html()).toBe('');
  });
});
