import React from "react";
import { connect } from 'react-redux'

import styles from './index.css';


const Loading = ({isLoaded}) => {
    if (isLoaded === true) {
        return null;
    }
    return (
        <div className={styles.loading_wrapper}>
            <h2 className={styles.loading}>
                {isLoaded === null ? 'Loading...' : 'Something wrong'}
            </h2>
        </div>
    );
};


export default connect(state => ({
    isLoaded: state.map.isLoaded}
))(Loading);
