import React from 'react';
import {shallow} from 'enzyme';
import Congratulation from '../games/components/Congratulation';


describe('shallow <Congratulation /> components', () => {
  let props = {result: 'result', url: 'url'};
  let wrapper;
  window.__CONGRATULATION__ = {text: 'text'};

  beforeEach(() => {
    wrapper = shallow(<Congratulation {...props}/>);
  });

  it('render', () => {
    expect(wrapper).toMatchSnapshot();
  });

  it('click close', () => {
    wrapper.instance().onClose();
    expect(wrapper.html()).toBe('');
  });
});
