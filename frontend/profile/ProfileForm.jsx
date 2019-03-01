'use strict';
import React from "react";
import {Button, Form} from "react-bootstrap";
import {CSRFfetch, getFormData} from "../utils";
import {UsernameInput, EmailInput, SelectInput, CheckboxInput, ImageInput} from '../components/Input';
import {Field, Form as FormWrapper} from "react-final-form";


export default class ProfileForm extends React.Component {
  onSubmit = async (values, form, callback) => {
    let options = {method: 'POST', body: getFormData(values)};
    let response = await CSRFfetch(`${window.location.pathname}?section=main`, options);
    return await response.json();
  };

  _render = ({handleSubmit, form, submitting, submitError}) => {
    return <Form onSubmit={handleSubmit}>
      <Field name="username" component={UsernameInput} label="Username"/>
      <Field name="email" component={EmailInput} label="Email"/>
      <Field name="language" component={SelectInput} label="Language"/>
      <Field name="is_subscribed" component={CheckboxInput} label="Subscribe" type="checkbox"/>
      <Field name="image" component={ImageInput}/>
      <Button variant="primary" type="submit" >Submit</Button>
      {submitting && <div className="spinner-border" role="status" />}
    </Form>;
  };

  render() {
    return <FormWrapper onSubmit={this.onSubmit} validate={this.validate} render={this._render} initialValues={this.props.fields} />;
  }
}
