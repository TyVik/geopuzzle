'use strict';
import React from "react";
import Tree from "./index";
import CheckBox from "../../components/CheckBox/index";


class Node extends React.Component {
  constructor(props) {
    super(props);
    this.state = {...props}
  }

  toggleCollapse = () => {
    this.setState({...this.state, toggled: !this.state.toggled});
  };

  componentWillReceiveProps(nextProps) {
    let toggled = nextProps.toggled;
    if (toggled === undefined) {
      toggled = this.state.toggled;
    }
    this.setState({...this.state, toggled: toggled});
  }

  renderToggle() {
    let handleClick = this.props.items === undefined ? () => this.props.loadItems(this.props.id) : this.toggleCollapse;
    return <i className={"fas fa-" + (this.state.toggled ? 'minus' : 'plus')} onClick={handleClick} />;
  }

  render() {
    return <li>
      {this.state.showCheckbox &&
        <CheckBox {...this.state} onChange={this.props.onChange} checked={this.props.checked.has(this.state.id)}
                  value={this.props.id} name={this.props.checkboxName} />}
      {this.props.items_exists &&
        this.renderToggle()}
      <span>{this.props.name}</span>
      {this.props.items && this.state.toggled &&
        <Tree items={this.props.items} checked={this.props.checked} checkboxName={this.props.checkboxName}
              onChange={this.props.onChange} loadItems={this.props.loadItems}/>}
    </li>;
  }
}


export default Node;
