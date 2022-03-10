'use strict';
import React from "react";
import {Form, InputGroup} from "react-bootstrap";


const Input = ({input, meta, ...params}) => {
  let hasError = meta.error || meta.submitError;
  return <Form.Group className="form-group">
    <Form.Label>{params.label}</Form.Label>
    <Form.Control type={params.type} value={input.value} onChange={input.onChange} isInvalid={hasError}/>
    {hasError &&
      <Form.Control.Feedback type="invalid">{meta.error || meta.submitError}</Form.Control.Feedback>}
  </Form.Group>;
};


const PasswordInput = ({input, meta, ...params}) => {
  params = {...params, type: "password"}
  return Input({input, meta, ...params});
}

const UsernameInput = ({input, meta, ...params}) => {
  let hasError = meta.error || meta.submitError;
  return <Form.Group className="form-group">
    <Form.Label>{params.label}</Form.Label>
    <InputGroup>
      <InputGroup.Text>@</InputGroup.Text>
      <Form.Control value={input.value} onChange={input.onChange} isInvalid={hasError}/>
      {hasError &&
        <Form.Control.Feedback type="invalid">{meta.error || meta.submitError}</Form.Control.Feedback>}
    </InputGroup>
  </Form.Group>;
};


const SelectInput = ({input, meta, ...params}) => {
  return <Form.Group className="form-group">
    <Form.Label>{params.label}</Form.Label>
    <Form.Select value={input.value} onChange={input.onChange}>
      <option value="en">English</option>
      <option value="ru">Russian</option>
    </Form.Select>
  </Form.Group>;
};


const CheckboxInput = ({input, meta, ...params}) => {
  return <Form.Group className="form-group">
    <Form.Check type="checkbox" label={params.label} checked={input.checked} onChange={input.onChange}/>
  </Form.Group>;
};


const handle = (target, onChange) => {
  const reader = new FileReader();
  reader.readAsDataURL(target.files[0]);
  reader.onload = () => onChange(reader.result);
  reader.onerror = () => onChange(null);
};

const ImageInput = ({input, meta, ...params}) => {
  return <Form.Group className="form-group">
    <input type="file" accept="image/*" src={input.value} onChange={e => handle(e.currentTarget, input.onChange)} />
    <img src={input.value} className="w-25 d-block"/>
  </Form.Group>;
};

export {UsernameInput, Input, SelectInput, CheckboxInput, ImageInput, PasswordInput};
