import React from 'react';
import {shallow} from 'enzyme';
import {Button} from "react-bootstrap";
import ChangePasswordForm from '../profile/ChangePasswordForm';


describe('shallow <ChangePasswordForm /> components', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallow(<ChangePasswordForm/>);
  });

  it('render empty', () => {
    expect(wrapper).toMatchSnapshot('ChangePasswordForm');
  });

  it('render submit fail', () => {
    wrapper.find(Button).simulate('click');
    expect(wrapper).toMatchSnapshot('ChangePasswordForm');
  });

/*  it('check props', () => {
    expect(wrapper).toMatchSnapshot('infobox');
    expect(shallow(<Infobox show={true} coat_of_arms='coat_of_arms'/>)).toMatchSnapshot('infobox-empty');
  });

  it('click close', () => {
    wrapper.find('button.close').simulate('click');
    expect(onClose).toHaveBeenCalled();
  });

  it('click collapse', () => {
    wrapper.find('.header i').simulate('click');
    expect(localStorage.getItem('infobox_collapse')).toBe('true');
    expect(wrapper).toMatchSnapshot('infobox-collapse');
    wrapper.find('.header i').simulate('click');
    expect(localStorage.getItem('infobox_collapse')).toBe('false');
    expect(wrapper).toMatchSnapshot('infobox');
  });*/
});
