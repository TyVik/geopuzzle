'use strict';
import React from "react";

import './index.css'


const Loading = (props) => {
    return <div className="loading_wrapper">
        <h2 className="loading">
            {props.text}
        </h2>
    </div>;
};


export default Loading;
