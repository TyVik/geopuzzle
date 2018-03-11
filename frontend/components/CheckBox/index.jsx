'use strict';
import React from 'react';


class CheckBox extends React.Component {
    render() {
        return <input id={this.props.id} value={this.props.id} type="checkbox"
                      onChange={this.props.onChange} checked={this.props.checked} />;
    }
}

export default CheckBox;
