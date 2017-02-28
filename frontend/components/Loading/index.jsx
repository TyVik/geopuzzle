import React from "react";
import { connect } from 'react-redux'


const Loading = ({isLoaded}) => {
    if (isLoaded === true) {
        return null;
    }
    return <h2>{isLoaded === null ? 'Loading...' : 'Something wrong'}</h2>
};


const mapStateToProps = (state, ownProps) => {
  return {
    isLoaded: state.map.isLoaded
  }
};

export default connect(mapStateToProps)(Loading);
