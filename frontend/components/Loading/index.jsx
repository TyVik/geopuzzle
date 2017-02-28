import React from "react";
import { connect } from 'react-redux'


const Loading = ({isLoaded}) => {
    if (isLoaded === true) {
        return null;
    }
    return <h2>{isLoaded === null ? 'Loading...' : 'Something wrong'}</h2>
};


export default connect(state => ({
    isLoaded: state.map.isLoaded}
))(Loading);
