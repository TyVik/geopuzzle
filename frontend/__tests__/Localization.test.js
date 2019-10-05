'use strict';
import React from "react";
import messages from "../messages";


it('check fullness', () => {
  expect(messages).toHaveProperty('en');
  expect(messages).toHaveProperty('ru');

  expect(Object.keys(messages['en'])).toStrictEqual(Object.keys(messages['ru']));

  Object.keys(messages['en']).map(key => {
    expect(messages['en'][key]).not.toBe('');
    expect(messages['ru'][key]).not.toBe('');
    expect(messages['en'][key]).not.toBe(messages['ru'][key]);
  });
});
