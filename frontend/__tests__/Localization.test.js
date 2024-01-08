'use strict';
import React from "react";
import messages from "../locale/messages";
import { IntlProvider } from "react-intl";
import Loading from "../components/Loading";
import { render, screen } from "./utils";


test('check fullness', async () => {
  expect(messages).toHaveProperty('en');
  expect(messages).toHaveProperty('ru');

  expect(Object.keys(messages['en'])).toStrictEqual(Object.keys(messages['ru']));

  Object.keys(messages['en']).forEach(key => {
    expect(messages['en'][key]).not.toBe('');
    expect(messages['ru'][key]).not.toBe('');
    expect(messages['en'][key]).not.toBe(messages['ru'][key]);
  });
});


test('shallow <Loading /> components', async () => {
  const locale = 'en';
  render(<IntlProvider locale={locale} messages={messages[locale]}><Loading hasError={true}/></IntlProvider>);
  expect(screen.getByRole("heading").textContent).toBe("Something went wrong :(");
});
