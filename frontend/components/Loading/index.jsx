'use strict';
import React from "react";

import './index.css'
import {FormattedMessage as Msg} from "react-intl";


const Loading = (props) => {
  return <div className="loading_wrapper">
    <h2 className="loading">
      <Msg id={props.hasError ? "loadingError": "loading"} />
    </h2>
  </div>;
};


export default Loading;
