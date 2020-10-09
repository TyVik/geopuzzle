'use strict';
import 'url-search-params-polyfill';
import React from "react";
import {FormattedMessage as Msg} from 'react-intl';
import {CSRFfetch} from "../utils";
import {Button, Col} from "react-bootstrap";

import "./index.css";


class IndexScroll extends React.Component {
  constructor(props) {
    super(props);
    this.state = {items: [], hasMore: true, limitPerLoad: 24};
  }

  componentDidMount() {
    this.loadMore();
  }

  loadMore = async () => {
    let exclude = this.state.items.reduce((result, item) => {result.push(item.id); return result;}, []);
    let url = `/index/scroll/${this.props.game}/?limit=${this.state.limitPerLoad}&ids=${exclude.join(',')}`;
    let response = await CSRFfetch(url, {});
    let data = await response.json();
    this.setState(state =>
      ({...state, items: [...state.items, ...data], hasMore: data.length === state.limitPerLoad}));
  };

  renderItem = (item) => {
    return <Col md={3} sm={4} xs={6} xl={2} className="my-2 item-container" key={item.slug}>
      <a href={`${this.props.game}/${item.slug}`}>
        <img className="img-fluid rounded" src={item.image} alt={item.name}/>
      </a>
      <div className="text-center">
        {item.name}
      </div>
    </Col>;
  };

  render() {
    return <React.Fragment>
      {this.state.items.map(this.renderItem)}
      {this.state.hasMore &&
        <Button variant="primary" onClick={this.loadMore}>
          <Msg id="loadMore"/>
        </Button>}
    </React.Fragment>;
  }
}

export default IndexScroll;
