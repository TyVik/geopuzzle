'use strict';
import React from 'react';
import {QuizInit} from '../games/components/QuizInit';
import { render } from "./utils";
import { fireEvent } from "@testing-library/react";


describe('<QuizInit />', () => {
  let onLoad = jest.fn();
  let options = ['name', 'flag', 'coat_of_arms', 'capital'];
  let props = {show: true, load: onLoad, options: options};

  test('render hidden', async () => {
    const wrapper = render(<QuizInit show={false} options={[]}/>);
    expect(wrapper.container.children.length).toBe(0);
  });

  test('render', async () => {
    const wrapper = render(<QuizInit {...props}/>);
    const checkers = await wrapper.findAllByRole('checkbox');
    expect(checkers.length).toBe(options.length);
    checkers.forEach(
      (item) => {
        expect(item).toBeChecked();
      }
    );
    expect(wrapper.getByRole('button')).toBeEnabled();
  });

  test('check props', async () => {
    let wrapper = render(<QuizInit {...props}/>);
    const checkers = await wrapper.findAllByRole('checkbox');

    checkers.forEach(
      (item) => {
        fireEvent.click(item);
      }
    );
    expect(wrapper.getByRole('button')).toBeDisabled();

    fireEvent.click(checkers[0]);
    fireEvent.click(wrapper.getByRole('button'));
    expect(onLoad).toHaveBeenCalledWith({name: true, flag: false, coat_of_arms: false, capital: false});
  });
});
