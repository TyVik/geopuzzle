'use strict';
import React from 'react';
import Infobox from '../games/components/Infobox';
import { render } from "./utils";
import { fireEvent } from "@testing-library/react";


describe('shallow <Infobox /> components', () => {
  let onClose = jest.fn();
  let props = {show: true, name: 'test', wiki: 'wiki', onClose: onClose, flag: 'flag', coat_of_arms: 'coat_of_arms', area: 'area', population: 'population', currency: 'currency', capital: {wiki: 'capital.wiki', name: 'capital.name'}};

  test('render hidden', async () => {
    const wrapper = render(<Infobox show={false}/>);
    expect(wrapper.container.children.length).toBe(0);
  });

  test('render full', async () => {
    const wrapper = render(<Infobox {...props}/>);
    const cells = await wrapper.findAllByRole('cell');
    expect(cells.length).toBe(9);
    // expect(shallow(<Infobox {...props}/>)).toMatchSnapshot('infobox');
    // expect(shallow(<Infobox show={true} coat_of_arms='coat_of_arms'/>)).toMatchSnapshot('infobox-empty');
  });

  test('click close', async () => {
    let wrapper = render(<Infobox {...props}/>);
    fireEvent.click(wrapper.getByRole('button'));
    expect(onClose).toHaveBeenCalled();
  });

  test.skip('click collapse', async () => {
    const wrapper = render(<Infobox {...props}/>);
    fireEvent.click(wrapper.getByRole('button'));

    wrapper.find('.infobox-header i').simulate('click');
    expect(localStorage.getItem('infobox-collapse')).toBe('true');
    expect(wrapper).toMatchSnapshot('infobox-collapse');
    wrapper.find('.infobox-header i').simulate('click');
    expect(localStorage.getItem('infobox-collapse')).toBe('false');
    expect(wrapper).toMatchSnapshot('infobox');
  });
});
