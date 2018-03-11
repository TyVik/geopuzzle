import React from "react";
import {render} from "react-dom";
import Tree from "./components/Tree";


class RegionTree extends React.Component {
    constructor(props) {
        super(props);
        this.state = {items: window.__COUNTRIES__, checked: new Set()}
    }

    onChange(event) {
        let checked = this.state.checked;
        if (checked.has(event.target.value)) {
            checked.delete(event.target.value);
        } else {
            checked.add(event.target.value);
        }
        this.setState({...this.state, checked: checked});
    }

    render() {
        return <Tree {...this.state} onChange={this.onChange.bind(this)}/>;
    }
}


render(<RegionTree />, document.getElementById('tree'));
