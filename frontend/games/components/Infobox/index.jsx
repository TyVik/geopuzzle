'use strict';
import React from "react";
import {Collapse} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";


class Infobox extends React.Component {
  COLLAPSE_ID = 'infobox-collapse';

  constructor(props) {
    super(props);
    this.state = {collapse: JSON.parse(localStorage.getItem('infobox_collapse')) || false};
  }

  renderAttribute(name) {
    if (this.props[name]) {
      return <tr>
        <td><Msg id={name}/></td>
        <td>{this.props[name]}</td>
      </tr>;
    } else {
      return null;
    }
  }

  toggleCollapse = () => {
    let value = !this.state.collapse;
    localStorage.setItem('infobox_collapse', value);
    this.setState({...this.state, collapse: value});
  };

  render() {
    if (!this.props.show) {
      return null;
    }

    let image = this.props.flag ? this.props.flag : this.props.coat_of_arms;
    return <div className="infobox">
      <div className="infobox-header">
        <button type="button" className="close" onClick={this.props.onClose}>
          <span>&times;</span>
        </button>
        <div className="row_name">
          {this.props.name} <sup><a href={this.props.wiki} target="_blank">wiki</a></sup>
        </div>
        <i
          className={"fas fa-angle-" + (this.state.collapse ? 'up' : 'down')}
          onClick={this.toggleCollapse} aria-controls={this.COLLAPSE_ID} aria-expanded={!this.state.collapse}>
        </i>
      </div>
      <Collapse in={!this.state.collapse}>
        <div id={this.COLLAPSE_ID}>
          <table>
            <tbody>
              {image &&
                <tr>
                  <td colSpan="2">
                    <img src={image}/>
                  </td>
                </tr>}
              {this.props.capital &&
                <tr>
                  <td><Msg id="capital"/></td>
                  <td><a href={this.props.capital.wiki} target="_blank">{this.props.capital.name}</a></td>
                </tr>}
              {this.renderAttribute('area')}
              {this.renderAttribute('population')}
              {this.renderAttribute('currency')}
            </tbody>
          </table>
        </div>
      </Collapse>
    </div>;
  }
}


export default Infobox;
