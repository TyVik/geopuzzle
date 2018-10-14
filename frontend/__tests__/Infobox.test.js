import React from 'react';
import {shallow} from 'enzyme';
import Infobox from '../games/components/Infobox';


describe('shallow <Infobox /> components', () => {
  let onClose = jest.fn();
  let props = {show: true, name: 'test', wiki: 'wiki', onClose: onClose, flag: 'flag', coat_of_arms: 'coat_of_arms', area: 'area', population: 'population', currency: 'currency', capital: {wiki: 'capital.wiki', name: 'capital.name'}};
  let wrapper;

  beforeEach(() => {
    localStorage.__STORE__ = {};
    wrapper = shallow(<Infobox {...props}/>);
  });

  it('render hidden', () => {
    expect(shallow(<Infobox show={false}/>).html()).toBe(null);
  });

  it('check props', () => {
    expect(wrapper).toMatchSnapshot('infobox');
    expect(shallow(<Infobox show={true} coat_of_arms='coat_of_arms'/>)).toMatchSnapshot('infobox-empty');
  });

  it('click close', () => {
    wrapper.find('button.close').simulate('click');
    expect(onClose).toHaveBeenCalled();
  });

  it('click collapse', () => {
    wrapper.find('.header span.glyphicon').simulate('click');
    expect(localStorage.getItem('infobox_collapse')).toBe('true');
    expect(wrapper).toMatchSnapshot('infobox-collapse');
    wrapper.find('.header span.glyphicon').simulate('click');
    expect(localStorage.getItem('infobox_collapse')).toBe('false');
    expect(wrapper).toMatchSnapshot('infobox');
  });
});
