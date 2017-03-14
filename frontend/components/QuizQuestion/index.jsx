'use strict';
import React from "react";
import { connect } from 'react-redux'

import localization from '../../localization';

import './index.css'


class QuizQuestion extends React.Component {
    render() {
        if (this.props.show) {
            let image = this.props.flag ? this.props.flag : this.props.coat_of_arms;
            return (
                <div className="quiz-question">
                    <table>
                        <tbody>
                        <tr>
                            <th colSpan="2" className="row_name">
                                {this.props.name}
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
