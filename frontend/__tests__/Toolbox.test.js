'use strict';

import React from "react";
import Toolbox from "../games/components/Toolbox";
import { render, screen, fireEvent } from "./utils";


describe('<Toolbox />', () => {
  let onSetMapType = jest.fn();
  let onOpenInfobox = jest.fn();
  let props = {setMapType: onSetMapType, regions: [], wsState: true, openInfobox: onOpenInfobox};

  test('check items', async () => {
    const wrapper = render(<Toolbox {...props} regions={global.REGIONS}/>);

    const items = await wrapper.findAllByRole('button');
    items.forEach(
      (item) => {
        expect(item).toHaveClass('list-group-item-action');
        if (item.classList.contains('list-group-item-success')) {
          expect(item.textContent).toBe("Брестская область");
        } else {
          expect(item.textContent).toBe("Витебская область");
        }
      }
    );

    expect(wrapper.getByText(/found/)).toHaveTextContent('found: 1/3');
    // screen.debug();
  });

  test('check map type switcher', async () => {
    const wrapper = render(<Toolbox {...props}/>);
    const items = await wrapper.findAllByRole('img');
    expect(items).toHaveLength(3);
    items.forEach(
      (item) => {
        expect(item).toHaveClass('map-switcher');
        fireEvent.click(item);
        const mapType = item.src.split('/').pop().split('.')[0];
        expect(onSetMapType).toHaveBeenCalledWith(mapType);
      }
    );
  });

  test.each([true, false])('ws status %p', async (status) => {
    const count = status ? 0 : 1;
    const wrapper = render(<Toolbox {...props} wsState={status}/>);
    expect(wrapper.queryAllByText('networkError')).toHaveLength(count);
  });

/*
  it('click collapse', () => {
    let wrapper = mountComponentWithIntl(<Toolbox {...props} regions={global.REGIONS}/>);
    let header = wrapper.find('.toolbox-header');
    expect(localStorage.getItem('toolbox-collapse')).toBe(null);
    expect(wrapper.find('#toolbox-collapse').hasClass('show')).toBeTruthy();
    expect(header.find('i').hasClass('fa-angle-down')).toBeTruthy();

    header.simulate('click');
    wrapper.update();
    expect(localStorage.getItem('toolbox-collapse')).toBe('true');
    expect(wrapper.find('#toolbox-collapse').hasClass('show')).toBeFalsy();
    expect(wrapper.find('i').hasClass('fa-angle-up')).toBeTruthy();
  });
*/
});
