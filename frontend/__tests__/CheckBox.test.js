import React from 'react';
import {shallow} from 'enzyme';
import CheckBox from '../components/CheckBox';


describe('shallow <CheckBox /> components', () => {
  let onChange = jest.fn();
  let props = {id: 0, name: 'test', checked: false, onChange: onChange};
  let wrapper;

  beforeEach(() => {
    wrapper = shallow(<CheckBox {...props}/>);
  });

  it('render', () => {
    expect(wrapper).toMatchSnapshot();
  });

  it('check state', () => {
    let attrs = wrapper.props();
    expect(attrs).toHaveProperty('name', 'test');
    expect(attrs).toHaveProperty('checked', false);
    expect(attrs).toHaveProperty('value', 0);
  });

  it('click', () => {
    wrapper.simulate('change');
    expect(onChange).toHaveBeenCalled();
    expect(wrapper.props()).toHaveProperty('checked', false);  // checked should be required by props
  });
});
