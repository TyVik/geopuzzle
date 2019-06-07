'use strict';
import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Loading from "../Loading";
import {Col} from "react-bootstrap";


export default class GameScrollList extends React.Component {
  constructor(props) {
    super(props);
    this.state = GameScrollList.getInitialState(props);
  }

  componentDidMount() {
    if (this.state.page === 0) {
      this.fetchPage(1, false).then();
    }
  }

  static getInitialState(props) {
    return {items: [], page: 0, hasMore: true, url: props.url};
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (this.props.url !== prevProps.url) {
      this.setState(GameScrollList.getInitialState(this.props), () => {this.fetchPage(1, false).then()});
    }
  }

  fetchPage = async (page, replace) => {
    let url = new URL(this.props.url);
    url.searchParams.append('page', page);
    try {
      let response = await fetch(url.toString(), {method: 'GET'});
      let data = await response.json();
      let items = replace ? data : this.state.items.concat(data);
      this.setState({...this.state, items: items, page: page, hasMore: data.length === 30});
    } catch {
      this.setState({...this.state, page: page - 1, hasMore: false});
    }
  };

  fetchNextPage = () => {
    this.fetchPage(this.state.page + 1, false).then();
  };

  renderItem = (item) => {
    return <Col md={3} sm={4} xs={6} xl={2} className="my-2 item-container" key={item.url}>
      <a href={item.url}>
        <i className="created_by">by {item.user}</i>
        <img className="img-fluid rounded" src={item.image} alt={item.name}/>
      </a>
      <div className="text-center">
        {item.name}
      </div>
    </Col>;
  };

  render() {
    let items = this.state.items;
    return <InfiniteScroll dataLength={items.length} children={items} next={this.fetchNextPage} className="row"
                           hasMore={this.state.hasMore} loader={<Loading/>}>
      {items.map(this.renderItem)}
    </InfiniteScroll>;
  }
}
