import React from "react";
import { connect } from 'react-redux'

import {closeInfobox} from '../../actions'

import './index.css'


const InfoboxAttribute = (props) => {
    return (
        <tr>
            <td scope="row">
                <div>{props.title}</div>
            </td>
            <td>{props.value}</td>
        </tr>
    )
};


class Infobox extends React.Component {
    constructor(props) {
        super(props);
        this.closeSelf = this.closeSelf.bind(this);
    }

    closeSelf() {
        this.props.dispatch(closeInfobox());
    }

    render() {
        if (this.props.show) {
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
                        <tr>
                            <td colSpan="2">
                                <div><img src={this.props.image}/></div>
                            </td>
                        </tr>
                        {this.props.items.map(obj => (
                            <InfoboxAttribute key={obj.title} {...obj} />
                        ))}
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
