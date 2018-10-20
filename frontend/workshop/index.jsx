'use strict';
import React from "react";
import InfiniteScroll from 'react-infinite-scroll-component';
import Loading from "../components/Loading/index";
import localization from "../localization";


class Workshop extends React.Component {
  constructor(props) {
    super(props);
    this.state = {puzzles: [], page: 0};
  }

  componentDidMount() {
    this.fetchPage(1);
  }

  fetchPage(page) {
    fetch(`${location.pathname}items/?page=${page}`, {method: 'GET'})
      .then(response => response.json())
      .then(data => {
        let items = this.state.puzzles.concat(data);
        this.setState({...this.state, puzzles: items, page: page});
      });
  }

  fetchNextPage = () => {
    this.fetchPage(this.state.page + 1);
  };

  render() {
    if (this.state.page === 0) {
      return <Loading text={localization.loading}/>;
    }
    let puzzles = this.state.puzzles;
    return <InfiniteScroll dataLength={puzzles.length} children={puzzles} next={this.fetchNextPage}
                           hasMore={puzzles.length < this.props.count} loader={<Loading text={localization.loading}/>}>
      {puzzles.map(puzzle =>
        <div className="col-md-3 col-sm-4 col-xs-6 item-container" key={puzzle.url}>
          <a href={puzzle.url}>
            <img className="img-responsive img-rounded" src={puzzle.image} alt={puzzle.name}/>
          </a>
          <div className="text-center">{puzzle.name}</div>
        </div>)}
    </InfiniteScroll>;
  }
}

export default Workshop;
