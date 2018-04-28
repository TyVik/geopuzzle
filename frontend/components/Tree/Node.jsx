'use strict';
import React from "react";
import Tree from "./index";
import CheckBox from "../CheckBox";


class Node extends React.Component {
    constructor(props) {
        super(props);
        this.state = {...props}
    }

    toggleCollapse = () => {
        this.setState({...this.state, toggled: !this.state.toggled});
    };

    componentWillReceiveProps(nextProps) {
        let toggled = nextProps.toggled;
        if (toggled === undefined) {
            toggled = this.state.toggled;
        }
        this.setState({...this.state, toggled: toggled});
    }

    renderToggle() {
        if (this.props.items === undefined) {
            return <span className={"glyphicon glyphicon-" + (this.state.toggled ? 'minus' : 'plus')}
                         onClick={() => this.props.loadItems(this.props.id)} />;
        } else {
            return <span className={"glyphicon glyphicon-" + (this.state.toggled ? 'minus' : 'plus')}
                         onClick={this.toggleCollapse} />;
        }
    }

    render() {
        return <li>
            <CheckBox {...this.state} onChange={this.props.onChange} value={this.props.id}
                      checked={this.props.checked.has(this.state.id)} />
            {this.props.items_exists &&
                this.renderToggle()}
            <span>{this.props.name}</span>
            {this.props.items && this.state.toggled &&
                <Tree items={this.props.items} checked={this.props.checked}
                      onChange={this.props.onChange} loadItems={this.props.loadItems}/>}
        </li>;
    }
}


export default Node;
