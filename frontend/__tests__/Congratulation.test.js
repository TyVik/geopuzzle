'use strict';
import React from 'react';
import {Congratulation} from '../games/components/Congratulation';
import {mountComponentWithIntl} from "./utils";


describe('shallow <Congratulation /> components', () => {
  let props = {result: 'result', url: 'url', startTime: new Date('2020-01-01'), text: 'congratulations.puzzle'};
  window.__GAME__ = {name: 'Belarus', is_global: false};

  it('render', () => {
    expect(mountComponentWithIntl(<Congratulation {...props}/>)).toMatchSnapshot();
  });

  it('click close', () => {
    let wrapper = mountComponentWithIntl(<Congratulation {...props}/>);
    let instance = wrapper.find('Congratulation').instance()
    instance.onClose();
    expect(instance.state.show).toBe(false);
  });
});
