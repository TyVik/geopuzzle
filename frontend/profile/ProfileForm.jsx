'use strict';
import React from "react";
import {Button, Form} from "react-bootstrap";
import {CSRFfetch, getFormData} from "../utils";
import {UsernameInput, Input, SelectInput, CheckboxInput, ImageInput} from '../components/Input';
import {Field, Form as FormWrapper} from "react-final-form";
import {FormattedMessage as Msg} from "react-intl";


export default class ProfileForm extends React.Component {
  LANGUAGE_CHOICES = [
    ['en', "english"],
    ['ru', "russian"]
  ];

  onSubmit = async (values) => {
    let options = {method: 'POST', body: getFormData(values)};
    let response = await CSRFfetch(`${window.location.pathname}?section=main`, options);
    return await response.json();
  };

  _render = ({handleSubmit, form, submitting}) => {
    return <Form onSubmit={handleSubmit}>
      <Field name="username" component={UsernameInput} label={<Msg id="username"/>}/>
      <Field name="email" component={Input} label={<Msg id="email"/>} type="email"/>
      <Field name="language" component={SelectInput} label={<Msg id="language"/>} choices={this.LANGUAGE_CHOICES}/>
      <Field name="is_subscribed" component={CheckboxInput} label={<Msg id="subscribe"/>} type="checkbox"/>
      <Field name="image" component={ImageInput}/>
      <Button variant="primary" type="submit" ><Msg id="submit"/></Button>
      {submitting && <div className="spinner-border" role="status" />}
    </Form>;
  };

  render() {
    return <FormWrapper onSubmit={this.onSubmit} validate={this.validate} render={this._render} initialValues={this.props.fields} />;
  }
}
