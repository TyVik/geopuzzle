'use strict';
import React from "react";
import Node from "./Node";


class Tree extends React.Component {
    constructor(props) {
        super(props);
        this.state = {checked: props.checked, onChange: props.onChange};
    }

    render() {
        return <ul style={{'listStyle': 'none'}}>
            {Object.keys(this.props.items).map((x) =>
                <Node key={this.props.items[x].id} {...this.state} {...this.props.items[x]} />)}
        </ul>;
    }
}


export default Tree;
