'use strict';
import React from 'react';
import QuizQuestion from "../games/components/QuizQuestion";
import { render } from "./utils";


describe('<QuizQuestion />', () => {
  test('render hidden', async () => {
    const wrapper = render(<QuizQuestion question={null}/>);
    expect(wrapper.container.children.length).toBe(0);
  });
});