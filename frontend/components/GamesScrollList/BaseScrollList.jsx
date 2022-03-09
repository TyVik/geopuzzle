'use strict';
import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Loading from "../Loading";


export default class BaseScrollList extends React.Component {
  className = "row";

  constructor(props) {
    super(props);
    this.state = BaseScrollList.getInitialState(props);
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
      this.setState(BaseScrollList.getInitialState(this.props), () => {this.fetchPage(1, false).then()});
    }
  }

  fetchPage = async (page, replace) => {
    let url = new URL(this.props.url);
    url.searchParams.append('page', page);
    try {
      let response = await fetch(url.toString(), {method: 'GET'});
      let data = await response.json();
      let items = replace ? data : this.state.items.concat(data);
      this.setState(state => ({...state, items: items, page: page, hasMore: data.length === 50}));
    } catch {
      this.setState(state => ({...state, page: page - 1, hasMore: false}));
    }
  };

  fetchNextPage = () => {
    this.fetchPage(this.state.page + 1, false).then();
  };

  renderContent() {
    return null;
  }

  render() {
    let items = this.state.items;
    return <InfiniteScroll dataLength={items.length} hasChildren={items.length > 0} next={this.fetchNextPage} className={this.className}
                           hasMore={this.state.hasMore} loader={<Loading/>}>
      {this.renderContent(items)}
    </InfiniteScroll>;
  }
}
