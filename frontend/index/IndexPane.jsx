'use strict';
import {Button, Tab} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";
import Card from "./card";
import React from "react";
import {CSRFfetch} from "../utils";

export default class IndexPane extends React.Component {
  constructor(props) {
    super(props);
    this.state = {items: [], hasMore: true, limitPerLoad: 24};
  }

  componentDidMount() {
    this.loadMore();
  }

  loadMore = async () => {
    let exclude = this.state.items.reduce((result, item) => {result.push(item.id); return result;}, []);
    let url = `/index/scroll/${this.props.game.name}/?limit=${this.state.limitPerLoad}&ids=${exclude.join(',')}`;
    let response = await CSRFfetch(url, {});
    let data = await response.json();
    this.setState(state =>
      ({...state, items: [...state.items, ...data], hasMore: data.length === state.limitPerLoad}));
  };

  render() {
    let game = this.props.game;
    return <React.Fragment>
      <div className="media row p-3">
        <video autoPlay loop muted playsInline className="pull-left mr-3 img-fluid">
          <source src={`${window.__STATIC_URL__}images/${game.name}.mp4`} type="video/mp4"/>
        </video>
        <div className="media-body blockquote">
          <p><Msg id={`index.description.${game.name}`}/></p>
        </div>
      </div>
      <div className="row">
        {game.items.world.map(item => <Card size="lg" baseUrl={game.name} item={item} key={item.id}/>)}
      </div>
      <div className="row">
        {game.items.parts.map(item => <Card size="md" baseUrl={game.name} item={item} key={item.id}/>)}
      </div>
      <div className="row">
        {this.state.items.map(item => <Card size="sm" baseUrl={game.name} item={item} key={item.id}/>)}
      </div>
      <div className="row">
        {this.state.hasMore &&
          <Button variant="primary" onClick={this.loadMore}>
            <Msg id="index.loadMore"/>
          </Button>}
      </div>
    </React.Fragment>;
  }
}
