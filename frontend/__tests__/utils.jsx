'use strict';
import React from "react";
import renderer from 'react-test-renderer';
import {IntlProvider} from "react-intl";
import {mount} from "enzyme";


export const createComponentWithIntl = (children, props = {locale: 'en'}) => {
  return renderer.create(<IntlProvider {...props}>{children}</IntlProvider>);
};

export const mountComponentWithIntl = (children, props = {locale: 'en'}) => {
  return mount(<IntlProvider {...props}>{children}</IntlProvider>);
};
