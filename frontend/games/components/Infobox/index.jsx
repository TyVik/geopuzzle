'use strict';
import React from "react";
import {Panel} from "react-bootstrap";
import localization from "../../../localization";
import "./index.css";


class Infobox extends React.Component {
    componentWillMount() {
        this.setState({...this.state,
            collapse: JSON.parse(localStorage.getItem('infobox_collapse')) || false
        });
    }

    renderAttribute(name) {
        if (this.props[name]) {
            return <tr>
                <td>{localization[name]}</td>
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
            <div className="header">
                <button type="button" className="close" onClick={this.props.onClose}>
                    <span>&times;</span>
                </button>
                <div className="row_name">
                    {this.props.name} <sup><a href={this.props.wiki} target="_blank">wiki</a></sup>
                </div>
                <span
                    className={"glyphicon collapse-icon glyphicon-chevron-" + (this.state.collapse ? 'up' : 'down')}
                    onClick={this.toggleCollapse}>
                </span>
            </div>
            <Panel expanded={!this.state.collapse} onToggle={this.toggleCollapse}>
                <Panel.Collapse>
                    <Panel.Body>
                        <table>
                            <tbody>
                                {image &&
                                <tr>
                                    <td colSpan="2">
                                        <img src={image}/>
                                    </td>
                                </tr>
                                }
                                {this.props.capital &&
                                <tr>
                                    <td>{localization.capital}</td>
                                    <td><a href={this.props.capital.wiki} target="_blank">{this.props.capital.name}</a></td>
                                </tr>
                                }
                                {this.renderAttribute('area')}
                                {this.renderAttribute('population')}
                                {this.renderAttribute('currency')}
                            </tbody>
                        </table>
                    </Panel.Body>
                </Panel.Collapse>
            </Panel>
        </div>;
    }
}


export default Infobox;
