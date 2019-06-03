'use strict';
import React from 'react';
import {renderWithIntl, mountWithIntl, loadTranslation} from 'enzyme-react-intl';
import ChangePasswordForm from '../profile/ChangePasswordForm';
import {Button} from "react-bootstrap";

loadTranslation("./frontend/locale/en.json");


describe('shallow <ChangePasswordForm /> components', () => {
  it('render empty', () => {
    expect(renderWithIntl(<ChangePasswordForm/>)).toMatchSnapshot('ChangePasswordForm');
  });

  it('render submit fail', () => {
    let wrapper = mountWithIntl(<ChangePasswordForm/>);
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
