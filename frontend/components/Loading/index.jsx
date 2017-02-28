import React from "react";
import { connect } from 'react-redux'

import './index.css'


const Loading = ({isLoaded}) => {
    if (isLoaded === true) {
        return null;
    }
    return (
        <div className="loading_wrapper">
            <h2 className="loading">
                {isLoaded === null ? 'Loading...' : 'Something wrong'}
            </h2>
        </div>
    );
};


export default connect(state => ({
    isLoaded: state.map.isLoaded}
))(Loading);
