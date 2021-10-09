'use strict';
import React from 'react';
import {Col} from "react-bootstrap";
import BaseScrollList from "./BaseScrollList";


export default class GameScrollList extends BaseScrollList {
  renderItem = (item) => {
    return <Col md={3} sm={4} xs={6} xl={2} className="my-2 item-container" key={item.url}>
      <a href={item.url}>
        {!this.props.edit && <i className="created_by">by {item.user}</i>}
        <img className="img-fluid rounded" src={item.image} alt={item.name}/>
      </a>
      <div className="text-center">
        {item.name}
        {this.props.edit &&
          <a href={`${item.url}edit/`}>
            &nbsp;
            <i className="fas fa-edit"></i>
          </a>}
      </div>
    </Col>;
  };

  renderContent(items) {
    return items.map(this.renderItem);
  }
}
