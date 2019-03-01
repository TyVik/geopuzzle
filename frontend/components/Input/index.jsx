'use strict';
import {Form, InputGroup} from "react-bootstrap";
import React from "react";


const PasswordInput = ({input, meta, ...params}) => {
  let hasError = meta.error || meta.submitError;
  return <Form.Group>
    <Form.Label>{params.label}</Form.Label>
    <Form.Control type="password" value={input.value} onChange={input.onChange} isInvalid={hasError}/>
    {hasError &&
      <Form.Control.Feedback type="invalid">{meta.error || meta.submitError}</Form.Control.Feedback>}
  </Form.Group>;
};


const UsernameInput = ({input, meta, ...params}) => {
  let hasError = meta.error || meta.submitError;
  return <Form.Group>
    <Form.Label>{params.label}</Form.Label>
    <InputGroup>
      <InputGroup.Prepend>
        <InputGroup.Text>@</InputGroup.Text>
      </InputGroup.Prepend>
      <Form.Control value={input.value} onChange={input.onChange} isInvalid={hasError}/>
      {hasError &&
        <Form.Control.Feedback type="invalid">{meta.error || meta.submitError}</Form.Control.Feedback>}
    </InputGroup>
  </Form.Group>;
};


const EmailInput = ({input, meta, ...params}) => {
  let hasError = meta.error || meta.submitError;
  return <Form.Group>
    <Form.Label>{params.label}</Form.Label>
    <Form.Control type="email" value={input.value} onChange={input.onChange} isInvalid={hasError}/>
    {hasError &&
      <Form.Control.Feedback type="invalid">{meta.error || meta.submitError}</Form.Control.Feedback>}
  </Form.Group>;
};


const SelectInput = ({input, meta, ...params}) => {
  return <Form.Group>
    <Form.Label>{params.label}</Form.Label>
    <Form.Control as="select" value={input.value} onChange={input.onChange}>
      <option value="en">English</option>
      <option value="ru">Russian</option>
    </Form.Control>
  </Form.Group>;
};


const CheckboxInput = ({input, meta, ...params}) => {
  return <Form.Group>
    <Form.Check type="checkbox" label={params.label} value={input.value} onChange={input.onChange}/>
  </Form.Group>;
};


const handle = (target, onChange) => {
  const reader = new FileReader();
  reader.readAsDataURL(target.files[0]);
  reader.onload = () => onChange(reader.result);
  reader.onerror = () => onChange(null);
};

const ImageInput = ({input, meta, ...params}) => {
  return <Form.Group>
    <input type="file" accept="image/*" src={input.value} onChange={e => handle(e.currentTarget, input.onChange)} />
    <img src={input.value} />
  </Form.Group>;
};

export {UsernameInput, EmailInput, SelectInput, CheckboxInput, ImageInput, PasswordInput};
