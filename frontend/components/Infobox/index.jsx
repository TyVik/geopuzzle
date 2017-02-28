import React from "react";
import { connect } from 'react-redux'

import styles from './index.css';


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


const Infobox = (props) => {
    if ('id' in props) {
        return (
            <div className={styles.container}>
                <button type="button" className={styles.close}>
                    <span>&times;</span>
                </button>
                <table>
                    <tbody>
                        <tr>
                            <th colSpan="2" className={styles.row_name}>
                                {props.name} <sup><a href={props.wiki} target="_blank">wiki</a></sup>
                            </th>
                        </tr>
                        <tr>
                            <td colSpan="2">
                                <div><img src={props.image}/></div>
                            </td>
                        </tr>
                        {props.items.map(obj => (
                            <InfoboxAttribute key={obj.title} {...obj} />
                        ))}
                    </tbody>
                </table>
            </div>
        )
    } else {
        return null;
    }
};

export default connect(state => (state.infobox))(Infobox);
