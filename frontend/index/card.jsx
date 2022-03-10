'use strict';
import React from "react";
import {Col} from "react-bootstrap";

export default class Card extends React.Component {
  SIZES = {
    lg: {md: 6, sm: 6, col: 12, my: 4, size: '540x540'},
    md: {md: 3, sm: 3, col: 6, my: 4, size: '250x250'},
    sm: {md: 2, sm: 3, col: 6, my: 2, size: '196x196'},
  }

  renderImage = (url, image, name) => {
    let imageUrl = image ? image : `${window.__STATIC_URL__}images/world/default_80.png`
    return <a href={url}>
      <img className="img-fluid rounded" src={imageUrl} alt={name}/>
    </a>;
  };

  render() {
    let size = this.SIZES[this.props.size];
    let className = `col-${size.col} my-${size.my} item-container`;
    return <Col md={size.md} sm={size.sm} className={className} key={`${this.props.item.id}`}>
      {this.renderImage(this.props.item.url, this.props.item.image, this.props.item.name)}
      <div>
        {this.props.item.name}
      </div>
    </Col>;
  }
}
