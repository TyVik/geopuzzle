import React from "react";
import {render} from "react-dom";
import Map from './components/Map';
import Tree from "./components/Tree";


class RegionTree extends React.Component {
    mapInit = this.mapInit.bind(this);

    constructor(props) {
        super(props);
        this.state = {items: window.__REGIONS__, checked: new Set(window.__CHECKED__)}
    }

    mapInit() {
        this.props.dispatch({ids: Array.from(this.props.checked), type: PUZZLE_GIVEUP, ws: true});
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
        return <div>
            <Tree {...this.state} onChange={this.onChange.bind(this)} />
            <Map initCallback={this.mapInit} />
        </div>;
    }
}


render(<RegionTree />, document.getElementById('tree'));
