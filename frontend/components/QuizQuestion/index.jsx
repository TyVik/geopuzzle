'use strict';
import React from "react";
import { connect } from 'react-redux'

import localization from '../../localization';

import './index.css'


class QuizQuestion extends React.Component {
    render() {
        if (this.props.show) {
            return (
                <div className="quiz-question">
                    <table>
                        <tbody>
                        <tr>
                            <th colSpan="2" className="row_name">
                                {this.props.name}
                            </th>
                        </tr>
                        {this.props.image &&
                            <tr>
                                <td colSpan="2">
                                    <img src={this.props.image}/>
                                </td>
                            </tr>
                        }
                        {this.props.capital &&
                            <tr>
                                <td>{localization['capital']}</td>
                                <td>{this.props.capital}</td>
                            </tr>
                        }
                        </tbody>
                    </table>
                </div>
            )
        } else {
            return null;
        }
    }
};

export default connect(state => (state.quiz.question))(QuizQuestion);
