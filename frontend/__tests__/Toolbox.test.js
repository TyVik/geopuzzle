'use strict';

import React from "react";
import {shallow, mount} from "enzyme";
import {mountWithIntl, loadTranslation} from 'enzyme-react-intl';
import Toolbox from "../games/components/Toolbox";

loadTranslation("./frontend/locale/en.json");


describe('shallow <Toolbox /> components', () => {
  let onSetMapType = jest.fn();
  let onOpenInfobox = jest.fn();
  let props = {setMapType: onSetMapType, regions: [], wsState: true, openInfobox: onOpenInfobox};

  it('check props', () => {
    let wrapper = shallow(<Toolbox {...props} regions={global.REGIONS}/>);
    expect(wrapper).toMatchSnapshot('toolbox');
  });

  it('check map type switcher', () => {
    let wrapper = shallow(<Toolbox {...props}/>);
    let switchers = wrapper.find('.map_switcher').getElements();
    expect(switchers.length).toBe(3);
    [google.maps.MapTypeId.TERRAIN, google.maps.MapTypeId.HYBRID, google.maps.MapTypeId.SATELLITE].map((item, index) => {
      switchers[index].props.onClick();
      expect(onSetMapType).toHaveBeenCalledWith(item);
    });
  });

  it('ws disconnect', () => {
    let wrapper = shallow(<Toolbox {...props}/>);
    expect(wrapper.find('#network_connection_label').length).toBe(0);

    wrapper = shallow(<Toolbox {...props} wsState={false}/>);
    expect(wrapper.find('#network_connection_label').length).toBe(1);
  });

  it('click collapse', () => {
    let wrapper = mountWithIntl(<Toolbox {...props} regions={global.REGIONS}/>);
    let header = wrapper.find('.listname-wrapper');
    expect(localStorage.getItem('toolbox_collapse')).toBe(null);
    expect(wrapper.find('#toolbox-collapse').hasClass('show')).toBeTruthy();
    expect(header.find('i').hasClass('fa-angle-down')).toBeTruthy();

    header.simulate('click');
    wrapper.update();
    expect(localStorage.getItem('toolbox_collapse')).toBe('true');
    expect(wrapper.find('#toolbox-collapse').hasClass('show')).toBeFalsy();
    expect(wrapper.find('i').hasClass('fa-angle-up')).toBeTruthy();
  });
});
