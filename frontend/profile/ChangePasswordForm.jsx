'use strict';
import React from "react";
import {Alert, Button, Form} from "react-bootstrap";
import {CSRFfetch, getFormData} from "../utils";
import {PasswordInput} from '../components/Input';
import {Field, Form as FormWrapper} from "react-final-form";


export default class ChangePasswordForm extends React.Component {
  onSubmit = async (values, form, callback) => {
    let data = getFormData(values);
    data.append('new_password2', values['new_password1']);
    let options = {method: 'POST', body: data};
    let response = await CSRFfetch(`${window.location.pathname}?section=password`, options);
    let result = await response.json();
    if (Object.keys(result).length === 0) {
      form.reset();
    }
    return result;
  };

  _render = ({handleSubmit, form, submitting}) => {
    let state = form.getState();
    return <Form onSubmit={handleSubmit}>
      {state.submitSucceeded && <Alert variant="success">Password has been changed successfully.</Alert>}
      <Field name="old_password" component={PasswordInput} label="Current password"/>
      <Field name="new_password1" component={PasswordInput} label="New password"/>
      <Button variant="primary" type="submit" >Submit</Button>
      {submitting && <div className="spinner-border" role="status" />}
    </Form>;
  };

  render() {
    return <FormWrapper onSubmit={this.onSubmit} render={this._render} />;
  }
}
