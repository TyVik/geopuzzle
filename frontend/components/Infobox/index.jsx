'use strict';
import React from "react";
import { connect } from 'react-redux'

import {closeInfobox} from '../../actions'
import localization from '../../localization';

import './index.css'


class Infobox extends React.Component {
    constructor(props) {
        super(props);
        this.closeSelf = this.closeSelf.bind(this);
    }

    closeSelf() {
        this.props.dispatch(closeInfobox());
    }

    renderAttribute(name) {
        if (this.props[name]) {
            return (
                <tr>
                    <td>{localization[name]}</td>
                    <td>{this.props[name]}</td>
                </tr>
            );
        } else {
            return null;
        }
    }

    render() {
        if (this.props.show) {
            let image = this.props.flag ? this.props.flag : this.props.coat_of_arms;
            return (
                <div className="infobox">
                    <button type="button" className="close" onClick={this.closeSelf}>
                        <span>&times;</span>
                    </button>
                    <table>
                        <tbody>
                        <tr>
                            <th colSpan="2" className="row_name">
                                {this.props.name} <sup><a href={this.props.wiki} target="_blank">wiki</a></sup>
                            </th>
                        </tr>
                        {image &&
                            <tr>
                                <td colSpan="2">
                                    <img src={image}/>
                                </td>
                            </tr>
                        }
                        {this.props.capital &&
                            <tr>
                                <td>{localization['capital']}</td>
                                <td><a href={this.props.capital.wiki} target="_blank">{this.props.capital.name}</a></td>
                            </tr>
                        }
                        {this.renderAttribute('area')}
                        {this.renderAttribute('population')}
                        {this.renderAttribute('currency')}
                        </tbody>
                    </table>
                </div>
            )
        } else {
            return null;
        }
    }
};

export default connect(state => (state.infobox))(Infobox);
