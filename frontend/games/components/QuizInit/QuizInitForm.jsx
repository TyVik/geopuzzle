import {Form, FormGroup} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";
import React from "react";


class QuizInitForm extends React.Component {
  renderItem = (item) => {
    return <Form.Check inline
                       label={<Msg id={item}/>}
                       key={item}
                       onClick={() => this.props.toggle(item)}
                       type="checkbox"
                       defaultChecked={this.props.data[item]}/>;
  };

  render() {
    return <FormGroup className="checkbox-group" controlId="quiz">
      {this.props.available.map(this.renderItem)}
    </FormGroup>;
  }
}

export default QuizInitForm;
