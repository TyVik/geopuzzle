'use strict';
import React from 'react';
import ChangePasswordForm from '../profile/ChangePasswordForm';
import {createComponentWithIntl, mountComponentWithIntl} from "./utils";
import {defer} from "lodash";


describe('shallow <ChangePasswordForm /> components', () => {
  beforeEach(() => {
      global.fetch.resetMocks();
  });

  it('render empty', () => {
    expect(createComponentWithIntl(<ChangePasswordForm/>)).toMatchSnapshot('ChangePasswordForm');
  });

  it('submit form error', () => {
    global.fetch.mockReject('');
    let wrapper = mountComponentWithIntl(<ChangePasswordForm/>);

    wrapper.find('form').simulate('submit');
    defer(() => {
      wrapper.update();
      expect(wrapper.find('.spinner-border').length).toBe(0);
      expect(wrapper.find('.unknown-error').length).toBe(1);
    });
  });

  it('submit form empty', () => {
    global.fetch.mockResponse(JSON.stringify({new_password1: ['Required field'], old_password: ['Required field']}));
    let wrapper = mountComponentWithIntl(<ChangePasswordForm/>);

    wrapper.find('form').simulate('submit');
    expect(global.fetch).toHaveBeenCalledWith('blank?section=password',
      expect.objectContaining({ method: 'POST', body: expect.any(FormData) })
    );
    const formData = Array.from(global.fetch.mock.calls[0][1].body.entries())
      .reduce((acc, f) => ({ ...acc, [f[0]]: f[1] }), {});
    expect(formData).toMatchObject({new_password2: 'undefined'});

    wrapper.update();
    expect(wrapper.find('.spinner-border').length).toBe(1);
    defer(() => {
      wrapper.update();
      expect(wrapper.find('.spinner-border').length).toBe(0);
      expect(wrapper.find('.invalid-feedback').length).toBe(2);
    });
  });

  it('submit form success', () => {
    global.fetch.mockResponse('{}');
    let wrapper = mountComponentWithIntl(<ChangePasswordForm/>);

    const form = wrapper.find('ReactFinalForm').instance();
    form.form.change('old_password', 'old_password');
    form.form.change('new_password1', 'new_password');
    wrapper.find('form').simulate('submit');

    expect(global.fetch).toHaveBeenCalledWith('blank?section=password',
      expect.objectContaining({ method: 'POST', body: expect.any(FormData) })
    );
    const formData = Array.from(global.fetch.mock.calls[0][1].body.entries())
      .reduce((acc, f) => ({ ...acc, [f[0]]: f[1] }), {});
    expect(formData).toMatchObject({old_password: 'old_password', new_password1: 'new_password', new_password2: 'new_password'});
    wrapper.update();
    expect(wrapper.find('.spinner-border').length).toBe(1);
    defer(() => {
      wrapper.update();
      expect(wrapper.find('.spinner-border').length).toBe(0);
      expect(wrapper.find('.alert-success').length).toBe(1);
    });
  });
});
