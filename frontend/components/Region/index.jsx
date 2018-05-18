'use strict';
/* global google */
import React from "react";
import Polygon from "./Polygon";


class Region extends React.Component {
    onDragEnd = () => {
        this.props.onDragPolygon(this.props.options.id, this.polygon.getBounds(), this.polygon.getPaths());
    };

    onClick = () => {
        if (this.props.onClick !== undefined) {
            this.props.onClick(this.props.options);
        }
    };

    setRef = (node) => {
        this.polygon = node;
    };

    render() {
        return <Polygon {...this.props} ref={this.setRef} onClick={this.onClick} onDragEnd={this.onDragEnd} />;
    }
}


export default Region;
