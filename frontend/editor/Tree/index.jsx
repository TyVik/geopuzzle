'use strict';
import React from "react";
import Node from "./Node";


class Tree extends React.Component {
  constructor(props) {
    super(props);
    this.state = {checked: props.checked, onChange: props.onChange, loadItems: props.loadItems,
        checkboxName: props.checkboxName};
    this.state.showCheckbox = props.showCheckbox === undefined ? true : props.showCheckbox;
  }

  render() {
    return <ul style={{'listStyle': 'none'}} className={this.props.className}>
      {Object.keys(this.props.items).map((x) =>
        <Node key={this.props.items[x].id} {...this.state} {...this.props.items[x]}
              showCheckbox={this.state.showCheckbox}/>)}
    </ul>;
  }
}


export default Tree;
