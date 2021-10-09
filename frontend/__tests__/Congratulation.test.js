'use strict';
import React from 'react';
import {Congratulation} from '../games/components/Congratulation';
import {mountComponentWithIntl} from "./utils";


describe('shallow <Congratulation /> components', () => {
  let props = {text: 'congratulations.puzzle', options: {'score': 60}};
  window.__GAME__ = {name: 'Belarus', is_global: false};

  it('render', () => {
    expect(mountComponentWithIntl(<Congratulation {...props}/>)).toMatchSnapshot();
  });

  it('click close', () => {
    let wrapper = mountComponentWithIntl(<Congratulation {...props}/>);
    let instance = wrapper.find('BaseCongratulation').instance();
    instance.onClose();
    expect(instance.state.show).toBe(false);
  });
});
