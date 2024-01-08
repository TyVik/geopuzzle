'use strict';
import React from "react";
import renderer from 'react-test-renderer';
import {IntlProvider} from "react-intl";


export const createComponentWithIntl = (children, props = {locale: 'en'}) => {
  return renderer.create(<IntlProvider {...props}>{children}</IntlProvider>);
};

// export const mountComponentWithIntl = (children, props = {locale: 'en'}) => {
//   return mount(<IntlProvider {...props}>{children}</IntlProvider>);
// };


import {render as rtlRender} from '@testing-library/react'

function render(ui, {locale = 'en', ...renderOptions} = {}) {
  function Wrapper({children}) {
    return <IntlProvider locale={locale} onError={() => {}}>{children}</IntlProvider>
  }
  return rtlRender(ui, {wrapper: Wrapper, ...renderOptions})
}

// re-export everything
export * from '@testing-library/react'

// override render method
export {render}